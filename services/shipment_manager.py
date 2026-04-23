"""
Shipment Manager Service
Handles Sendbox shipment creation and management for orders.
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from services.sendbox_service import get_sendbox_client, SendboxAPIError
from services.address_validator import format_address_for_sendbox, calculate_service_type
from config import Config
import json

logger = logging.getLogger(__name__)


class ShipmentCreationError(Exception):
    """Custom exception for shipment creation errors."""
    pass


def create_shipment_for_order(
    order_id: int,
    order_items: List[Dict],
    destination_address: Dict,
    total_weight: float,
    total_value: float,
    service_code: str = "standard",
    pickup_date: str = None
) -> Tuple[bool, Optional[Dict], Optional[str]]:
    """
    Create a Sendbox shipment for an order.
    
    Args:
        order_id: Order ID
        order_items: List of order items with product details
        destination_address: Destination shipping address
        total_weight: Total weight in KG
        total_value: Total order value
        service_code: Service code (standard, premium, expedient)
        pickup_date: Pickup date (defaults to next business day)
        
    Returns:
        Tuple of (success, shipment_data, error_message)
    """
    try:
        # Get warehouse address (origin)
        origin_address = Config.get_warehouse_address()
        
        # Format destination address for Sendbox
        dest_address = format_address_for_sendbox(
            first_name=destination_address["first_name"],
            last_name=destination_address["last_name"],
            phone=destination_address["phone"],
            street=destination_address["street"],
            city=destination_address["city"],
            state=destination_address["state"],
            country=destination_address["country"],
            email=destination_address.get("email"),
            street_line_2=destination_address.get("street_line_2"),
            post_code=destination_address.get("post_code"),
            lng=float(destination_address["lng"]) if destination_address.get("lng") else None,
            lat=float(destination_address["lat"]) if destination_address.get("lat") else None
        )
        
        # Determine service type
        service_type = calculate_service_type(
            origin_address["country"],
            dest_address["country"]
        )
        
        # Prepare items for Sendbox
        sendbox_items = []
        for item in order_items:
            sendbox_items.append({
                "name": item["product_name"],
                "quantity": item["quantity"],
                "value": float(item["price"]),
                "weight": float(item.get("weight", 0.5)),
                "description": item.get("description", item["product_name"]),
                "item_type": item.get("item_type", "general"),
                "hts_code": item.get("hts_code", "")
            })
        
        # Set pickup date (next business day if not provided)
        if not pickup_date:
            tomorrow = datetime.now() + timedelta(days=1)
            # Skip weekends
            while tomorrow.weekday() >= 5:  # 5=Saturday, 6=Sunday
                tomorrow += timedelta(days=1)
            pickup_date = tomorrow.strftime("%Y-%m-%d")
        
        # Generate callback URL for webhooks
        # TODO: Update with actual domain in production
        callback_url = f"{Config.get_sendbox_base_url()}/api/webhooks/sendbox"
        
        # Create shipment via Sendbox API
        client = get_sendbox_client()
        
        logger.info(f"Creating Sendbox shipment for order {order_id}")
        
        shipment_response = client.create_shipment(
            origin=origin_address,
            destination=dest_address,
            weight=total_weight,
            items=sendbox_items,
            service_code=service_code,
            service_type=service_type,
            pickup_date=pickup_date,
            total_value=total_value,
            currency="NGN",
            callback_url=callback_url
        )
        
        logger.info(f"Sendbox shipment created successfully for order {order_id}")
        
        return True, shipment_response, None
        
    except SendboxAPIError as e:
        error_msg = f"Sendbox API error: {e.message}"
        logger.error(f"Failed to create shipment for order {order_id}: {error_msg}")
        return False, None, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"Failed to create shipment for order {order_id}: {error_msg}")
        return False, None, error_msg


def extract_shipment_details(shipment_response: Dict) -> Dict:
    """
    Extract relevant shipment details from Sendbox response.
    
    Args:
        shipment_response: Sendbox API response
        
    Returns:
        Dictionary with extracted details
    """
    return {
        "sendbox_shipment_id": shipment_response.get("id"),
        "sendbox_tracking_code": shipment_response.get("tracking_code") or shipment_response.get("tracking"),
        "sendbox_status": shipment_response.get("status", "pending"),
        "sendbox_carrier": shipment_response.get("carrier", "Sendbox"),
        "estimated_delivery_date": shipment_response.get("estimated_delivery_date"),
        "sendbox_webhook_data": json.dumps(shipment_response)
    }


def retry_shipment_creation(
    order_id: int,
    max_retries: int = 3,
    delay_seconds: int = 5
) -> Tuple[bool, Optional[Dict], Optional[str]]:
    """
    Retry shipment creation with exponential backoff.
    
    Args:
        order_id: Order ID
        max_retries: Maximum number of retry attempts
        delay_seconds: Initial delay between retries
        
    Returns:
        Tuple of (success, shipment_data, error_message)
    """
    import time
    
    for attempt in range(max_retries):
        logger.info(f"Shipment creation attempt {attempt + 1}/{max_retries} for order {order_id}")
        
        # TODO: Fetch order details and call create_shipment_for_order
        # This is a placeholder for the retry logic
        
        if attempt < max_retries - 1:
            wait_time = delay_seconds * (2 ** attempt)  # Exponential backoff
            logger.info(f"Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
    
    return False, None, "Max retries exceeded"


def map_sendbox_status_to_internal(sendbox_status: str) -> Tuple[str, str]:
    """
    Map Sendbox status to internal order and delivery statuses.
    
    Args:
        sendbox_status: Sendbox shipment status
        
    Returns:
        Tuple of (order_status, delivery_status)
    """
    status_map = {
        "drafted": ("processing", "Pending"),
        "pending": ("processing", "Pending"),
        "pickup_started": ("processing", "Pending"),
        "pickup_completed": ("shipped", "in_transit"),
        "in_transit": ("shipped", "in_transit"),
        "in_delivery": ("shipped", "in_transit"),
        "delivered": ("delivered", "delivered"),
        "cancelled": ("cancelled", "Pending"),
        "failed": ("processing", "Pending")
    }
    
    return status_map.get(sendbox_status.lower(), ("processing", "Pending"))


def calculate_order_weight(order_items: List[Dict], cursor) -> float:
    """
    Calculate total weight for order items.
    
    Args:
        order_items: List of order items
        cursor: Database cursor
        
    Returns:
        Total weight in KG
    """
    total_weight = 0.0
    
    for item in order_items:
        # Fetch product weight if not in item
        if "weight" not in item or item["weight"] is None:
            cursor.execute(
                "SELECT weight FROM product WHERE id = %s",
                (item["product_id"],)
            )
            product = cursor.fetchone()
            weight = float(product["weight"]) if product and product.get("weight") else 0.5
        else:
            weight = float(item["weight"])
        
        total_weight += weight * item["quantity"]
    
    return total_weight
