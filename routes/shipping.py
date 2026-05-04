"""
Shipping Routes
Handles shipping quotes, shipment creation, and tracking operations.
Now using Terminal Africa API for multi-carrier shipping.
"""

from flask import Blueprint, request, jsonify
from db import get_db_connection
from middleware.auth_middleware import token_required, admin_required
from services.terminal_service import get_terminal_client, TerminalAPIError
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
# TERMINAL AFRICA - CARRIERS
# ──────────────────────────────────────────────

@shipping_bp.route("/api/shipping/carriers", methods=["GET"])
@token_required
def get_carriers(current_user):
    """
    Get available carriers from Terminal Africa.
    
    Query Parameters:
        - active: Filter by active status (true/false)
        - domestic: Filter domestic carriers (true/false)
        - regional: Filter regional carriers (true/false)
        - international: Filter international carriers (true/false)
    
    Returns:
        List of available carriers with their details
    """
    try:
        # Get filter parameters
        active = request.args.get("active")
        domestic = request.args.get("domestic")
        regional = request.args.get("regional")
        international = request.args.get("international")
        
        # Convert string to boolean
        def str_to_bool(val):
            if val is None:
                return None
            return val.lower() in ['true', '1', 'yes']
        
        active = str_to_bool(active)
        domestic = str_to_bool(domestic)
        regional = str_to_bool(regional)
        international = str_to_bool(international)
        
        # Get carriers from Terminal Africa
        client = get_terminal_client()
        
        try:
            response = client.get_carriers(
                active=active,
                domestic=domestic,
                regional=regional,
                international=international
            )
            
            # Handle nested response structure
            if 'data' in response:
                carriers_data = response['data']
                
                # Check if carriers is nested further
                if isinstance(carriers_data, dict) and 'carriers' in carriers_data:
                    carriers = carriers_data['carriers']
                else:
                    carriers = carriers_data if isinstance(carriers_data, list) else []
            else:
                carriers = response if isinstance(response, list) else []
            
            # Count active carriers
            active_count = sum(1 for c in carriers if isinstance(c, dict) and c.get('active', False))
            
            return jsonify({
                "status": "success",
                "message": "Carriers retrieved successfully",
                "data": {
                    "carriers": carriers,
                    "count": len(carriers),
                    "active_count": active_count
                }
            }), 200
            
        except TerminalAPIError as e:
            return jsonify({
                "status": "error",
                "message": f"Terminal API error: {e.message}",
                "error_code": e.status_code
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


# ──────────────────────────────────────────────
# TERMINAL AFRICA - PACKAGING
# ──────────────────────────────────────────────

@shipping_bp.route("/api/shipping/packaging", methods=["GET"])
@token_required
def get_packaging(current_user):
    """
    Get available packaging options from Terminal Africa.
    
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 20, max: 100)
    
    Returns:
        List of packaging options with dimensions and weights
    """
    try:
        page = max(int(request.args.get("page", 1)), 1)
        per_page = min(max(int(request.args.get("per_page", 20)), 1), 100)
        
        # Get packaging from Terminal Africa
        client = get_terminal_client()
        
        try:
            response = client.get_packaging(page=page, per_page=per_page)
            
            # Handle nested response structure
            if 'data' in response:
                packaging_data = response['data']
                
                # Check if packaging is nested further
                if isinstance(packaging_data, dict) and 'packaging' in packaging_data:
                    packaging = packaging_data['packaging']
                    pagination = packaging_data.get('pagination', {})
                else:
                    packaging = packaging_data if isinstance(packaging_data, list) else []
                    pagination = response.get('pagination', {})
            else:
                packaging = response if isinstance(response, list) else []
                pagination = {}
            
            return jsonify({
                "status": "success",
                "message": "Packaging options retrieved successfully",
                "data": {
                    "packaging": packaging,
                    "count": len(packaging),
                    "pagination": pagination
                }
            }), 200
            
        except TerminalAPIError as e:
            return jsonify({
                "status": "error",
                "message": f"Terminal API error: {e.message}",
                "error_code": e.status_code
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@shipping_bp.route("/api/shipping/packaging", methods=["POST"])
@token_required
def create_packaging(current_user):
    """
    Create a new packaging option in Terminal Africa.
    
    Expected JSON body:
    {
        "name": "Small Box",
        "type": "box",  // box, envelope, or soft-packaging
        "length": 20,
        "width": 15,
        "height": 10,
        "weight": 0.5,
        "size_unit": "cm",  // cm or in
        "weight_unit": "kg"  // kg or lb
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["name", "type", "length", "width", "height", "weight"]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"'{field}' is required"
                }), 400
        
        # Validate type
        valid_types = ["box", "envelope", "soft-packaging"]
        if data["type"] not in valid_types:
            return jsonify({
                "status": "error",
                "message": f"'type' must be one of: {', '.join(valid_types)}"
            }), 400
        
        # Create packaging
        client = get_terminal_client()
        
        try:
            response = client.create_packaging(
                name=data["name"],
                type=data["type"],
                length=float(data["length"]),
                width=float(data["width"]),
                height=float(data["height"]),
                weight=float(data["weight"]),
                size_unit=data.get("size_unit", "cm"),
                weight_unit=data.get("weight_unit", "kg")
            )
            
            # Handle nested response
            packaging = response.get('data', response)
            
            return jsonify({
                "status": "success",
                "message": "Packaging created successfully",
                "data": {"packaging": packaging}
            }), 201
            
        except TerminalAPIError as e:
            return jsonify({
                "status": "error",
                "message": f"Terminal API error: {e.message}",
                "error_code": e.status_code
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


# ──────────────────────────────────────────────
# TERMINAL AFRICA - RATES
# ──────────────────────────────────────────────

@shipping_bp.route("/api/shipping/rates", methods=["POST"])
@token_required
def get_shipping_rates(current_user):
    """
    Get shipping rates from multiple Terminal Africa carriers.
    
    Expected JSON body:
    {
        "origin_address_id": 123,  // Local address ID
        "destination_address_id": 456,  // Local address ID
        "items": [
            {
                "name": "Product Name",
                "quantity": 2,
                "value": 15000,
                "weight": 2.5,
                "description": "Product description"
            }
        ],
        "packaging_id": "PKG-123",  // Terminal packaging ID (optional)
        "currency": "NGN"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if "origin_address_id" not in data:
            return jsonify({
                "status": "error",
                "message": "'origin_address_id' is required"
            }), 400
        
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
        
        origin_address_id = data["origin_address_id"]
        destination_address_id = data["destination_address_id"]
        items = data["items"]
        packaging_id = data.get("packaging_id")
        currency = data.get("currency", "NGN")
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Fetch origin address
                cursor.execute(
                    """
                    SELECT * FROM shipping_addresses
                    WHERE id = %s AND user_id = %s
                    """,
                    (origin_address_id, current_user["id"])
                )
                origin_address = cursor.fetchone()
                
                if not origin_address:
                    return jsonify({
                        "status": "error",
                        "message": "Origin address not found"
                    }), 404
                
                # Fetch destination address
                cursor.execute(
                    """
                    SELECT * FROM shipping_addresses
                    WHERE id = %s AND user_id = %s
                    """,
                    (destination_address_id, current_user["id"])
                )
                destination_address = cursor.fetchone()
                
                if not destination_address:
                    return jsonify({
                        "status": "error",
                        "message": "Destination address not found"
                    }), 404
                
                # Check if addresses are synced to Terminal
                origin_terminal_id = origin_address.get("terminal_address_id")
                dest_terminal_id = destination_address.get("terminal_address_id")
                
                if not origin_terminal_id or not dest_terminal_id:
                    return jsonify({
                        "status": "error",
                        "message": "Both addresses must be synced to Terminal Africa first",
                        "details": {
                            "origin_synced": origin_terminal_id is not None,
                            "destination_synced": dest_terminal_id is not None
                        }
                    }), 400
                
                # Calculate total weight and prepare items
                total_weight = 0
                terminal_items = []
                
                for item in items:
                    weight = float(item.get("weight", 0.5))
                    quantity = int(item.get("quantity", 1))
                    value = float(item.get("value", 0))
                    
                    total_weight += weight * quantity
                    
                    terminal_items.append({
                        "name": item.get("name", "Item"),
                        "quantity": quantity,
                        "value": value,
                        "currency": currency,  # Add currency to each item
                        "weight": weight,
                        "description": item.get("description", item.get("name", "Item"))
                    })
                
                # Get or create packaging
                client = get_terminal_client()
                
                if not packaging_id:
                    # Use default packaging or create one based on weight
                    # For now, get first available packaging
                    packaging_response = client.get_packaging(page=1, per_page=1)
                    
                    if 'data' in packaging_response:
                        pkg_data = packaging_response['data']
                        if isinstance(pkg_data, dict) and 'packaging' in pkg_data:
                            packaging_list = pkg_data['packaging']
                        else:
                            packaging_list = pkg_data if isinstance(pkg_data, list) else []
                    else:
                        packaging_list = packaging_response if isinstance(packaging_response, list) else []
                    
                    if packaging_list and len(packaging_list) > 0:
                        packaging_id = packaging_list[0].get('packaging_id') or packaging_list[0].get('id')
                    else:
                        return jsonify({
                            "status": "error",
                            "message": "No packaging options available. Please create a packaging first."
                        }), 400
                
                # Create parcel
                try:
                    parcel_response = client.create_parcel(
                        packaging_id=packaging_id,
                        items=terminal_items,
                        description=f"Shipment with {len(terminal_items)} items",
                        weight=total_weight,
                        weight_unit="kg"
                    )
                    
                    parcel_data = parcel_response.get('data', parcel_response)
                    parcel_id = parcel_data.get('parcel_id') or parcel_data.get('id')
                    
                    if not parcel_id:
                        return jsonify({
                            "status": "error",
                            "message": "Failed to create parcel"
                        }), 500
                    
                    # Get rates
                    rates_response = client.get_rates(
                        origin_address_id=origin_terminal_id,
                        destination_address_id=dest_terminal_id,
                        parcel_id=parcel_id,
                        currency=currency
                    )
                    
                    # Handle nested response
                    if 'data' in rates_response:
                        rates_data = rates_response['data']
                        # data is directly a list of rates
                        rates = rates_data if isinstance(rates_data, list) else []
                    else:
                        rates = rates_response if isinstance(rates_response, list) else []
                    
                    return jsonify({
                        "status": "success",
                        "message": "Shipping rates retrieved successfully",
                        "data": {
                            "rates": rates,
                            "count": len(rates),
                            "parcel_id": parcel_id,
                            "summary": {
                                "total_weight": total_weight,
                                "total_items": len(terminal_items),
                                "origin": f"{origin_address['city']}, {origin_address['state']}",
                                "destination": f"{destination_address['city']}, {destination_address['state']}",
                                "currency": currency
                            }
                        }
                    }), 200
                    
                except TerminalAPIError as e:
                    return jsonify({
                        "status": "error",
                        "message": f"Terminal API error: {e.message}",
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
# SHIPPING QUOTES (Legacy Sendbox)
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


# ──────────────────────────────────────────────
# TERMINAL AFRICA - SHIPMENTS (PHASE 5)
# ──────────────────────────────────────────────

@shipping_bp.route("/api/shipping/shipments", methods=["POST"])
@token_required
def create_shipment(current_user):
    """
    Create a shipment from a selected rate.
    
    Expected JSON body:
    {
        "rate_id": "RT-ABC123",  // Terminal rate ID from rates endpoint
        "origin_address_id": 15,  // Local address ID
        "destination_address_id": 14,  // Local address ID
        "parcel_id": "PC-XYZ789",  // Terminal parcel ID from rates endpoint
        "metadata": {  // Optional
            "order_id": 123,
            "customer_notes": "Handle with care"
        }
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ["rate_id", "origin_address_id", "destination_address_id", "parcel_id"]
        for field in required:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"'{field}' is required"
                }), 400
        
        rate_id = data["rate_id"]
        origin_address_id = data["origin_address_id"]
        destination_address_id = data["destination_address_id"]
        parcel_id = data["parcel_id"]
        metadata = data.get("metadata", {})
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Verify addresses belong to user and are synced
                cursor.execute(
                    """
                    SELECT terminal_address_id FROM shipping_addresses
                    WHERE id = %s AND user_id = %s
                    """,
                    (origin_address_id, current_user["id"])
                )
                origin = cursor.fetchone()
                
                cursor.execute(
                    """
                    SELECT terminal_address_id FROM shipping_addresses
                    WHERE id = %s AND user_id = %s
                    """,
                    (destination_address_id, current_user["id"])
                )
                destination = cursor.fetchone()
                
                if not origin or not destination:
                    return jsonify({
                        "status": "error",
                        "message": "One or both addresses not found"
                    }), 404
                
                if not origin["terminal_address_id"] or not destination["terminal_address_id"]:
                    return jsonify({
                        "status": "error",
                        "message": "Both addresses must be synced to Terminal Africa"
                    }), 400
                
                # Create shipment via Terminal
                client = get_terminal_client()
                
                try:
                    shipment_response = client.create_shipment(
                        rate_id=rate_id,
                        origin_address_id=origin["terminal_address_id"],
                        destination_address_id=destination["terminal_address_id"],
                        parcel_id=parcel_id,
                        metadata=metadata
                    )
                    
                    # Extract shipment data
                    shipment_data = shipment_response.get('data', shipment_response)
                    
                    return jsonify({
                        "status": "success",
                        "message": "Shipment created successfully",
                        "data": {
                            "shipment": shipment_data
                        }
                    }), 201
                    
                except TerminalAPIError as e:
                    return jsonify({
                        "status": "error",
                        "message": f"Terminal API error: {e.message}",
                        "error_code": e.status_code
                    }), 500
                    
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@shipping_bp.route("/api/shipping/shipments", methods=["GET"])
@token_required
def get_shipments(current_user):
    """
    Get all shipments for the current user.
    
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 20, max: 100)
        - status: Filter by status (optional)
    """
    try:
        page = max(int(request.args.get("page", 1)), 1)
        per_page = min(max(int(request.args.get("per_page", 20)), 1), 100)
        status = request.args.get("status")
        
        client = get_terminal_client()
        
        try:
            response = client.get_shipments(page=page, per_page=per_page, status=status)
            
            # Handle nested response
            if 'data' in response:
                shipments_data = response['data']
                if isinstance(shipments_data, dict) and 'shipments' in shipments_data:
                    shipments = shipments_data['shipments']
                    pagination = shipments_data.get('pagination', {})
                else:
                    shipments = shipments_data if isinstance(shipments_data, list) else []
                    pagination = response.get('pagination', {})
            else:
                shipments = response if isinstance(response, list) else []
                pagination = {}
            
            return jsonify({
                "status": "success",
                "message": "Shipments retrieved successfully",
                "data": {
                    "shipments": shipments,
                    "count": len(shipments),
                    "pagination": pagination
                }
            }), 200
            
        except TerminalAPIError as e:
            return jsonify({
                "status": "error",
                "message": f"Terminal API error: {e.message}",
                "error_code": e.status_code
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@shipping_bp.route("/api/shipping/shipments/<string:shipment_id>", methods=["GET"])
@token_required
def get_shipment_details(current_user, shipment_id):
    """
    Get details of a specific shipment.
    
    Path Parameters:
        - shipment_id: Terminal shipment ID
    """
    try:
        client = get_terminal_client()
        
        try:
            response = client.get_shipment(shipment_id)
            
            # Handle nested response
            shipment = response.get('data', response)
            
            return jsonify({
                "status": "success",
                "message": "Shipment details retrieved successfully",
                "data": {
                    "shipment": shipment
                }
            }), 200
            
        except TerminalAPIError as e:
            if e.status_code == 404:
                return jsonify({
                    "status": "error",
                    "message": "Shipment not found"
                }), 404
            return jsonify({
                "status": "error",
                "message": f"Terminal API error: {e.message}",
                "error_code": e.status_code
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@shipping_bp.route("/api/shipping/shipments/<string:shipment_id>/cancel", methods=["POST"])
@token_required
def cancel_shipment(current_user, shipment_id):
    """
    Cancel a shipment.
    
    Path Parameters:
        - shipment_id: Terminal shipment ID
    """
    try:
        client = get_terminal_client()
        
        try:
            response = client.cancel_shipment(shipment_id)
            
            return jsonify({
                "status": "success",
                "message": "Shipment cancelled successfully",
                "data": response.get('data', response)
            }), 200
            
        except TerminalAPIError as e:
            if e.status_code == 404:
                return jsonify({
                    "status": "error",
                    "message": "Shipment not found"
                }), 404
            return jsonify({
                "status": "error",
                "message": f"Terminal API error: {e.message}",
                "error_code": e.status_code
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


# ──────────────────────────────────────────────
# TERMINAL AFRICA - TRACKING (PHASE 6)
# ──────────────────────────────────────────────

@shipping_bp.route("/api/shipping/track/<string:shipment_id>", methods=["GET"])
def track_shipment_by_id(shipment_id):
    """
    Track a shipment by Terminal shipment ID (public endpoint).
    
    Path Parameters:
        - shipment_id: Terminal shipment ID
    """
    try:
        client = get_terminal_client()
        
        try:
            response = client.track_shipment(shipment_id)
            
            # Handle nested response
            tracking_data = response.get('data', response)
            
            return jsonify({
                "status": "success",
                "message": "Tracking information retrieved successfully",
                "data": {
                    "tracking": tracking_data
                }
            }), 200
            
        except TerminalAPIError as e:
            if e.status_code == 404:
                return jsonify({
                    "status": "error",
                    "message": "Shipment not found"
                }), 404
            return jsonify({
                "status": "error",
                "message": f"Terminal API error: {e.message}",
                "error_code": e.status_code
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@shipping_bp.route("/api/shipping/track/number/<string:tracking_number>", methods=["GET"])
def track_by_tracking_number(tracking_number):
    """
    Track a shipment by carrier tracking number (public endpoint).
    
    Path Parameters:
        - tracking_number: Carrier tracking number
    """
    try:
        client = get_terminal_client()
        
        try:
            response = client.track_by_tracking_number(tracking_number)
            
            # Handle nested response
            tracking_data = response.get('data', response)
            
            return jsonify({
                "status": "success",
                "message": "Tracking information retrieved successfully",
                "data": {
                    "tracking": tracking_data
                }
            }), 200
            
        except TerminalAPIError as e:
            if e.status_code == 404:
                return jsonify({
                    "status": "error",
                    "message": "Tracking number not found"
                }), 404
            return jsonify({
                "status": "error",
                "message": f"Terminal API error: {e.message}",
                "error_code": e.status_code
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500
