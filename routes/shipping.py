"""
Shipping Routes
Handles shipping quotes, shipment creation, and tracking operations.
"""

from flask import Blueprint, request, jsonify
from db import get_db_connection
from middleware.auth_middleware import token_required, admin_required
from services.sendbox_service import get_sendbox_client, SendboxAPIError
from services.address_validator import format_address_for_sendbox, calculate_service_type
from config import Config
from datetime import datetime, timedelta
import json

shipping_bp = Blueprint("shipping", __name__)


def _serialize_quote(row):
    """Convert DB row to JSON-safe quote dict."""
    if row is None:
        return None
    quote = dict(row)
    # Convert datetime to string
    if quote.get("created_at"):
        quote["created_at"] = quote["created_at"].strftime("%Y-%m-%d %H:%M:%S")
    if quote.get("expires_at"):
        quote["expires_at"] = quote["expires_at"].strftime("%Y-%m-%d %H:%M:%S")
    # Convert decimal to float
    if quote.get("weight") is not None:
        quote["weight"] = float(quote["weight"])
    if quote.get("quoted_price") is not None:
        quote["quoted_price"] = float(quote["quoted_price"])
    # Parse JSON data
    if quote.get("quote_data") and isinstance(quote["quote_data"], str):
        try:
            quote["quote_data"] = json.loads(quote["quote_data"])
        except:
            pass
    return quote


# ──────────────────────────────────────────────
# SHIPPING QUOTES
# ──────────────────────────────────────────────

@shipping_bp.route("/api/shipping/quotes", methods=["POST"])
@token_required
def get_shipping_quotes(current_user):
    """
    Get shipping quotes from Sendbox.
    
    Expected JSON body:
    {
        "destination_address_id": 123,
        "items": [
            {
                "product_id": 55,
                "quantity": 2,
                "name": "Product Name",
                "value": 15000,
                "weight": 2.5
            }
        ],
        "service_code": "standard",
        "pickup_date": "2026-04-25"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if "destination_address_id" not in data:
            return jsonify({
                "status": "error",
                "message": "'destination_address_id' is required"
            }), 400
        
        if "items" not in data or not isinstance(data["items"], list) or len(data["items"]) == 0:
            return jsonify({
                "status": "error",
                "message": "'items' is required and must be a non-empty array"
            }), 400
        
        destination_address_id = data["destination_address_id"]
        items = data["items"]
        service_code = data.get("service_code", "standard")
        pickup_date = data.get("pickup_date")
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Fetch destination address
                cursor.execute(
                    """
                    SELECT * FROM shipping_addresses
                    WHERE id = %s AND user_id = %s
                    """,
                    (destination_address_id, current_user["id"])
                )
                dest_address = cursor.fetchone()
                
                if not dest_address:
                    return jsonify({
                        "status": "error",
                        "message": "Destination address not found"
                    }), 404
                
                # Calculate total weight and value
                total_weight = 0
                total_value = 0
                sendbox_items = []
                
                for item in items:
                    # Validate item fields
                    if "product_id" not in item or "quantity" not in item:
                        return jsonify({
                            "status": "error",
                            "message": "Each item must have 'product_id' and 'quantity'"
                        }), 400
                    
                    product_id = item["product_id"]
                    quantity = item["quantity"]
                    
                    # Fetch product details if not provided
                    if "weight" not in item or "value" not in item or "name" not in item:
                        cursor.execute(
                            "SELECT item, price, discount, weight FROM product WHERE id = %s",
                            (product_id,)
                        )
                        product = cursor.fetchone()
                        
                        if not product:
                            return jsonify({
                                "status": "error",
                                "message": f"Product {product_id} not found"
                            }), 404
                        
                        # Calculate price with discount
                        price = product["price"]
                        if product["discount"] > 0:
                            price = price * (1 - product["discount"] / 100)
                        
                        item_weight = float(product.get("weight", 0.5))
                        item_value = float(price)
                        item_name = product["item"]
                    else:
                        item_weight = float(item["weight"])
                        item_value = float(item["value"])
                        item_name = item["name"]
                    
                    # Calculate totals
                    item_total_weight = item_weight * quantity
                    item_total_value = item_value * quantity
                    
                    total_weight += item_total_weight
                    total_value += item_total_value
                    
                    # Prepare Sendbox item format
                    sendbox_items.append({
                        "name": item_name,
                        "quantity": quantity,
                        "value": item_value,
                        "weight": item_weight,
                        "description": item.get("description", item_name),
                        "item_type": item.get("item_type", "general"),
                        "hts_code": item.get("hts_code", "")
                    })
                
                # Get warehouse address (origin)
                origin_address = Config.get_warehouse_address()
                
                # Format destination address for Sendbox
                destination_address = format_address_for_sendbox(
                    first_name=dest_address["first_name"],
                    last_name=dest_address["last_name"],
                    phone=dest_address["phone"],
                    street=dest_address["street"],
                    city=dest_address["city"],
                    state=dest_address["state"],
                    country=dest_address["country"],
                    email=dest_address.get("email"),
                    street_line_2=dest_address.get("street_line_2"),
                    post_code=dest_address.get("post_code"),
                    lng=float(dest_address["lng"]) if dest_address.get("lng") else None,
                    lat=float(dest_address["lat"]) if dest_address.get("lat") else None
                )
                
                # Determine service type
                service_type = calculate_service_type(
                    origin_address["country"],
                    destination_address["country"]
                )
                
                # Get shipping quotes from Sendbox
                client = get_sendbox_client()
                
                try:
                    quotes_response = client.get_shipping_quotes(
                        origin=origin_address,
                        destination=destination_address,
                        weight=total_weight,
                        items=sendbox_items,
                        service_code=service_code,
                        service_type=service_type,
                        pickup_date=pickup_date,
                        total_value=total_value,
                        currency="NGN"
                    )
                    
                    # Save quote to database
                    expires_at = datetime.now() + timedelta(hours=24)
                    
                    cursor.execute(
                        """
                        INSERT INTO shipping_quotes
                            (user_id, origin_state, origin_city, destination_state, destination_city,
                             weight, service_type, service_code, carrier, quoted_price, currency,
                             quote_data, expires_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            current_user["id"],
                            origin_address["state"],
                            origin_address["city"],
                            destination_address["state"],
                            destination_address["city"],
                            total_weight,
                            service_type,
                            service_code,
                            quotes_response.get("carrier", "Sendbox"),
                            quotes_response.get("amount", 0),
                            "NGN",
                            json.dumps(quotes_response),
                            expires_at
                        )
                    )
                    quote_id = cursor.lastrowid
                    conn.commit()
                    
                    return jsonify({
                        "status": "success",
                        "message": "Shipping quotes retrieved successfully",
                        "data": {
                            "quote_id": quote_id,
                            "quotes": quotes_response,
                            "summary": {
                                "total_weight": total_weight,
                                "total_value": total_value,
                                "service_type": service_type,
                                "service_code": service_code,
                                "origin": f"{origin_address['city']}, {origin_address['state']}",
                                "destination": f"{destination_address['city']}, {destination_address['state']}",
                                "expires_at": expires_at.strftime("%Y-%m-%d %H:%M:%S")
                            }
                        }
                    }), 200
                    
                except SendboxAPIError as e:
                    return jsonify({
                        "status": "error",
                        "message": f"Sendbox API error: {e.message}",
                        "error_code": e.status_code
                    }), 500
                    
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@shipping_bp.route("/api/shipping/quotes/<int:quote_id>", methods=["GET"])
@token_required
def get_quote(current_user, quote_id):
    """Get a specific shipping quote by ID."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM shipping_quotes
                    WHERE id = %s AND user_id = %s
                    """,
                    (quote_id, current_user["id"])
                )
                quote = cursor.fetchone()
                
                if not quote:
                    return jsonify({
                        "status": "error",
                        "message": "Quote not found"
                    }), 404
                
                # Check if quote has expired
                if quote["expires_at"] and quote["expires_at"] < datetime.now():
                    return jsonify({
                        "status": "error",
                        "message": "Quote has expired. Please request a new quote."
                    }), 410
                
                return jsonify({
                    "status": "success",
                    "data": {"quote": _serialize_quote(quote)}
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@shipping_bp.route("/api/shipping/quotes/history", methods=["GET"])
@token_required
def get_quote_history(current_user):
    """Get shipping quote history for the current user."""
    try:
        page = max(int(request.args.get("page", 1)), 1)
        limit = min(max(int(request.args.get("limit", 20)), 1), 100)
        offset = (page - 1) * limit
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Get total count
                cursor.execute(
                    "SELECT COUNT(*) as total FROM shipping_quotes WHERE user_id = %s",
                    (current_user["id"],)
                )
                total = cursor.fetchone()["total"]
                
                # Fetch quotes
                cursor.execute(
                    """
                    SELECT * FROM shipping_quotes
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    (current_user["id"], limit, offset)
                )
                quotes = cursor.fetchall()
                
                total_pages = (total + limit - 1) // limit
                
                return jsonify({
                    "status": "success",
                    "data": {
                        "quotes": [_serialize_quote(q) for q in quotes],
                        "pagination": {
                            "page": page,
                            "limit": limit,
                            "total": total,
                            "total_pages": total_pages
                        }
                    }
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


# ──────────────────────────────────────────────
# LANDED COST CALCULATION
# ──────────────────────────────────────────────

@shipping_bp.route("/api/shipping/landed-cost", methods=["POST"])
@token_required
def calculate_landed_cost(current_user):
    """
    Calculate landed cost for international shipments.
    
    Expected JSON body: Same as shipping quotes
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if "destination_address_id" not in data:
            return jsonify({
                "status": "error",
                "message": "'destination_address_id' is required"
            }), 400
        
        if "items" not in data or not isinstance(data["items"], list):
            return jsonify({
                "status": "error",
                "message": "'items' is required and must be an array"
            }), 400
        
        destination_address_id = data["destination_address_id"]
        items = data["items"]
        service_code = data.get("service_code", "standard")
        pickup_date = data.get("pickup_date")
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Fetch destination address
                cursor.execute(
                    """
                    SELECT * FROM shipping_addresses
                    WHERE id = %s AND user_id = %s
                    """,
                    (destination_address_id, current_user["id"])
                )
                dest_address = cursor.fetchone()
                
                if not dest_address:
                    return jsonify({
                        "status": "error",
                        "message": "Destination address not found"
                    }), 404
                
                # Check if international
                if dest_address["country"] == "NG":
                    return jsonify({
                        "status": "error",
                        "message": "Landed cost calculation is only for international shipments"
                    }), 400
                
                # Calculate totals and prepare items (similar to quotes)
                total_weight = 0
                total_value = 0
                sendbox_items = []
                
                for item in items:
                    product_id = item.get("product_id")
                    quantity = item["quantity"]
                    
                    if product_id:
                        cursor.execute(
                            "SELECT item, price, discount, weight FROM product WHERE id = %s",
                            (product_id,)
                        )
                        product = cursor.fetchone()
                        
                        if product:
                            price = product["price"]
                            if product["discount"] > 0:
                                price = price * (1 - product["discount"] / 100)
                            
                            item_weight = float(product.get("weight", 0.5))
                            item_value = float(price)
                            item_name = product["item"]
                        else:
                            continue
                    else:
                        item_weight = float(item.get("weight", 0.5))
                        item_value = float(item.get("value", 0))
                        item_name = item.get("name", "Item")
                    
                    total_weight += item_weight * quantity
                    total_value += item_value * quantity
                    
                    sendbox_items.append({
                        "name": item_name,
                        "quantity": quantity,
                        "value": item_value,
                        "weight": item_weight,
                        "hts_code": item.get("hts_code", ""),
                        "item_type": item.get("item_type", "general")
                    })
                
                # Get addresses
                origin_address = Config.get_warehouse_address()
                destination_address = format_address_for_sendbox(
                    first_name=dest_address["first_name"],
                    last_name=dest_address["last_name"],
                    phone=dest_address["phone"],
                    street=dest_address["street"],
                    city=dest_address["city"],
                    state=dest_address["state"],
                    country=dest_address["country"],
                    email=dest_address.get("email"),
                    street_line_2=dest_address.get("street_line_2"),
                    post_code=dest_address.get("post_code")
                )
                
                # Calculate landed cost
                client = get_sendbox_client()
                
                try:
                    landed_cost = client.calculate_landed_cost(
                        origin=origin_address,
                        destination=destination_address,
                        weight=total_weight,
                        items=sendbox_items,
                        service_code=service_code,
                        pickup_date=pickup_date,
                        total_value=total_value,
                        currency="NGN"
                    )
                    
                    return jsonify({
                        "status": "success",
                        "message": "Landed cost calculated successfully",
                        "data": {
                            "landed_cost": landed_cost,
                            "summary": {
                                "total_weight": total_weight,
                                "total_value": total_value,
                                "origin": f"{origin_address['city']}, {origin_address['state']}",
                                "destination": f"{destination_address['city']}, {destination_address['state']}, {destination_address['country']}"
                            }
                        }
                    }), 200
                    
                except SendboxAPIError as e:
                    return jsonify({
                        "status": "error",
                        "message": f"Sendbox API error: {e.message}",
                        "error_code": e.status_code
                    }), 500
                    
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500



# ──────────────────────────────────────────────
# TRACKING
# ──────────────────────────────────────────────

@shipping_bp.route("/api/shipping/track/<string:tracking_code>", methods=["GET"])
def track_shipment(tracking_code):
    """
    Track a shipment by Sendbox tracking code (public endpoint).
    
    Args:
        tracking_code: Sendbox tracking code
        
    Returns:
        Tracking information with timeline and current status
    """
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Find order by Sendbox tracking code
                cursor.execute(
                    "SELECT * FROM orders WHERE sendbox_tracking_code = %s",
                    (tracking_code,)
                )
                order = cursor.fetchone()
                
                if not order:
                    return jsonify({
                        "status": "error",
                        "message": "Shipment not found for tracking code"
                    }), 404
                
                # Sync tracking from Sendbox
                from services.tracking_sync import sync_tracking_from_sendbox, get_tracking_summary
                
                success, tracking_data, error_msg = sync_tracking_from_sendbox(
                    tracking_code,
                    cursor
                )
                
                if not success:
                    # Return cached data if sync fails
                    import json
                    tracking_data = None
                    if order.get("sendbox_webhook_data"):
                        try:
                            tracking_data = json.loads(order["sendbox_webhook_data"])
                        except:
                            pass
                
                # Commit any updates from sync
                conn.commit()
                
                # Refresh order data
                cursor.execute(
                    "SELECT * FROM orders WHERE sendbox_tracking_code = %s",
                    (tracking_code,)
                )
                order = cursor.fetchone()
                
                # Get tracking summary
                tracking_summary = get_tracking_summary(order, tracking_data)
                
                return jsonify({
                    "status": "success",
                    "message": "Tracking information retrieved successfully",
                    "data": {
                        "tracking": tracking_summary,
                        "order_id": order["id"],
                        "order_tracking": order["tracking"]
                    }
                }), 200
                
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@shipping_bp.route("/api/admin/shipping/sync-tracking", methods=["POST"])
@admin_required
def bulk_sync_tracking(current_admin):
    """
    Bulk sync tracking for multiple orders (admin only).
    
    Expected JSON body:
    {
        "order_ids": [1, 2, 3, 4, 5]
    }
    """
    try:
        data = request.get_json()
        
        if "order_ids" not in data or not isinstance(data["order_ids"], list):
            return jsonify({
                "status": "error",
                "message": "'order_ids' is required and must be an array"
            }), 400
        
        order_ids = data["order_ids"]
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                from services.tracking_sync import bulk_sync_tracking
                
                results = bulk_sync_tracking(order_ids, cursor)
                conn.commit()
                
                return jsonify({
                    "status": "success",
                    "message": f"Synced {len(results['success'])} of {results['total']} orders",
                    "data": results
                }), 200
                
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500
