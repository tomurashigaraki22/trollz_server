"""
Tracking Synchronization Service
Handles syncing tracking information between Sendbox and internal orders.
"""

import logging
from typing import Dict, Optional, Tuple
from datetime import datetime
from services.sendbox_service import get_sendbox_client, SendboxAPIError
from services.shipment_manager import map_sendbox_status_to_internal
import json

logger = logging.getLogger(__name__)


def sync_tracking_from_sendbox(tracking_code: str, cursor) -> Tuple[bool, Optional[Dict], Optional[str]]:
    """
    Sync tracking information from Sendbox for a given tracking code.
    
    Args:
        tracking_code: Sendbox tracking code
        cursor: Database cursor
        
    Returns:
        Tuple of (success, tracking_data, error_message)
    """
    try:
        # Get tracking from Sendbox
        client = get_sendbox_client()
        tracking_data = client.track_shipment(tracking_code)
        
        # Extract status
        sendbox_status = tracking_data.get("status", "pending")
        
        # Map to internal statuses
        order_status, delivery_status = map_sendbox_status_to_internal(sendbox_status)
        
        # Find order by tracking code
        cursor.execute(
            "SELECT id FROM orders WHERE sendbox_tracking_code = %s",
            (tracking_code,)
        )
        order = cursor.fetchone()
        
        if not order:
            return False, None, "Order not found for tracking code"
        
        # Update order with latest tracking info
        cursor.execute(
            """
            UPDATE orders
            SET sendbox_status = %s,
                order_status = %s,
                delivery_status = %s,
                sendbox_webhook_data = %s
            WHERE id = %s
            """,
            (
                sendbox_status,
                order_status,
                delivery_status,
                json.dumps(tracking_data),
                order["id"]
            )
        )
        
        logger.info(f"Tracking synced for order {order['id']}: {sendbox_status}")
        
        return True, tracking_data, None
        
    except SendboxAPIError as e:
        error_msg = f"Sendbox API error: {e.message}"
        logger.error(f"Failed to sync tracking for {tracking_code}: {error_msg}")
        return False, None, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"Failed to sync tracking for {tracking_code}: {error_msg}")
        return False, None, error_msg


def format_tracking_timeline(tracking_data: Dict) -> list:
    """
    Format tracking data into a timeline of events.
    
    Args:
        tracking_data: Raw tracking data from Sendbox
        
    Returns:
        List of tracking events
    """
    timeline = []
    
    # Extract tracking history if available
    history = tracking_data.get("tracking_history", [])
    
    if history:
        for event in history:
            timeline.append({
                "status": event.get("status"),
                "description": event.get("description"),
                "location": event.get("location"),
                "timestamp": event.get("timestamp"),
                "date": event.get("date")
            })
    else:
        # Create basic timeline from current status
        current_status = tracking_data.get("status", "pending")
        timeline.append({
            "status": current_status,
            "description": get_status_description(current_status),
            "timestamp": tracking_data.get("updated_at") or datetime.now().isoformat()
        })
    
    return timeline


def get_status_description(status: str) -> str:
    """
    Get human-readable description for a status.
    
    Args:
        status: Sendbox status code
        
    Returns:
        Human-readable description
    """
    descriptions = {
        "drafted": "Shipment created and awaiting processing",
        "pending": "Shipment is pending pickup",
        "pickup_started": "Courier is on the way to pick up your package",
        "pickup_completed": "Package has been picked up",
        "in_transit": "Package is in transit to destination",
        "in_delivery": "Package is out for delivery",
        "delivered": "Package has been delivered",
        "cancelled": "Shipment has been cancelled",
        "failed": "Delivery attempt failed"
    }
    
    return descriptions.get(status.lower(), "Status update")


def get_tracking_summary(order: Dict, tracking_data: Optional[Dict] = None) -> Dict:
    """
    Get a summary of tracking information for an order.
    
    Args:
        order: Order dictionary
        tracking_data: Optional tracking data from Sendbox
        
    Returns:
        Tracking summary dictionary
    """
    summary = {
        "order_tracking": order.get("tracking"),
        "sendbox_tracking_code": order.get("sendbox_tracking_code"),
        "carrier": order.get("sendbox_carrier"),
        "current_status": order.get("sendbox_status"),
        "order_status": order.get("order_status"),
        "delivery_status": order.get("delivery_status"),
        "estimated_delivery_date": order.get("estimated_delivery_date").strftime("%Y-%m-%d") if order.get("estimated_delivery_date") else None
    }
    
    if tracking_data:
        summary["tracking_timeline"] = format_tracking_timeline(tracking_data)
        summary["last_updated"] = tracking_data.get("updated_at")
        summary["current_location"] = tracking_data.get("current_location")
    
    return summary


def bulk_sync_tracking(order_ids: list, cursor) -> Dict:
    """
    Sync tracking for multiple orders.
    
    Args:
        order_ids: List of order IDs
        cursor: Database cursor
        
    Returns:
        Dictionary with sync results
    """
    results = {
        "success": [],
        "failed": [],
        "total": len(order_ids)
    }
    
    for order_id in order_ids:
        try:
            # Get order tracking code
            cursor.execute(
                "SELECT sendbox_tracking_code FROM orders WHERE id = %s",
                (order_id,)
            )
            order = cursor.fetchone()
            
            if not order or not order.get("sendbox_tracking_code"):
                results["failed"].append({
                    "order_id": order_id,
                    "error": "No tracking code found"
                })
                continue
            
            # Sync tracking
            success, tracking_data, error_msg = sync_tracking_from_sendbox(
                order["sendbox_tracking_code"],
                cursor
            )
            
            if success:
                results["success"].append(order_id)
            else:
                results["failed"].append({
                    "order_id": order_id,
                    "error": error_msg
                })
                
        except Exception as e:
            results["failed"].append({
                "order_id": order_id,
                "error": str(e)
            })
    
    return results
