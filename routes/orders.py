from flask import Blueprint, request, jsonify
from db import get_db_connection
from middleware.auth_middleware import token_required, admin_required
from datetime import datetime
import random

orders_bp = Blueprint("orders", __name__)


# ──────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────

def _generate_tracking_number():
    """Generate a unique tracking number."""
    timestamp = int(datetime.now().timestamp() * 1000)
    random_suffix = random.randint(100, 999)
    return f"TS{timestamp}{random_suffix}"


def _serialize_order(row):
    """Convert DB row to a JSON-safe order dict."""
    if row is None:
        return None
    order = dict(row)
    # Convert datetime fields to string
    for key in ("created_at", "updated_at"):
        if order.get(key):
            order[key] = order[key].strftime("%Y-%m-%d %H:%M:%S")
    # Convert Decimal fields to float
    if order.get("total_amount") is not None:
        order["total_amount"] = float(order["total_amount"])
    # Convert tinyint booleans
    if order.get("stock_restored") is not None:
        order["stock_restored"] = bool(order["stock_restored"])
    return order


def _serialize_order_item(row):
    """Convert DB row to a JSON-safe order item dict."""
    if row is None:
        return None
    item = dict(row)
    # Convert Decimal fields to float
    for key in ("price", "subtotal"):
        if item.get(key) is not None:
            item[key] = float(item[key])
    return item


# ──────────────────────────────────────────────
# CHECKOUT & ORDER CREATION
# ──────────────────────────────────────────────

@orders_bp.route("/api/checkout", methods=["POST"])
@token_required
def create_checkout(current_user):
    """
    Create a new order from checkout.
    
    Expected JSON body:
    {
        "address_id": 123,  # Shipping address ID (preferred)
        "address": "Full delivery address",  # Fallback if address_id not provided
        "payment_method": "flutterwave|paystack|cash_on_delivery",
        "transaction_id": "optional_payment_transaction_id",
        "items": [
            {
                "product_id": 123,
                "quantity": 2,
                "size": "XL"
            }
        ],
        "selected_shipping": {  # Optional shipping selection
            "quote_id": 456,
            "carrier": "DHL",
            "service_code": "standard",
            "shipping_cost": 5000
        }
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ["payment_method", "items"]
        for field in required:
            if field not in data or not data[field]:
                return jsonify({"status": "error", "message": f"'{field}' is required"}), 400
        
        # Require either address_id or address
        if "address_id" not in data and "address" not in data:
            return jsonify({"status": "error", "message": "Either 'address_id' or 'address' is required"}), 400
        
        if not isinstance(data["items"], list) or len(data["items"]) == 0:
            return jsonify({"status": "error", "message": "At least one item is required"}), 400
        
        # Extract shipping information
        selected_shipping = data.get("selected_shipping", {})
        shipping_cost = float(selected_shipping.get("shipping_cost", 0)) if selected_shipping else 0
        quote_id = selected_shipping.get("quote_id")
        service_code = selected_shipping.get("service_code", "standard")
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Fetch shipping address if address_id provided
                shipping_address = None
                address_id = data.get("address_id")
                
                if address_id:
                    cursor.execute(
                        """
                        SELECT * FROM shipping_addresses
                        WHERE id = %s AND user_id = %s
                        """,
                        (address_id, current_user["id"])
                    )
                    shipping_address = cursor.fetchone()
                    
                    if not shipping_address:
                        return jsonify({"status": "error", "message": "Shipping address not found"}), 404
                    
                    # Format full address string for orders table
                    address_string = f"{shipping_address['street']}, {shipping_address['city']}, {shipping_address['state']}, {shipping_address['country']}"
                    if shipping_address.get('street_line_2'):
                        address_string = f"{shipping_address['street']}, {shipping_address['street_line_2']}, {shipping_address['city']}, {shipping_address['state']}, {shipping_address['country']}"
                else:
                    address_string = data["address"]
                
                # Validate shipping quote if provided
                if quote_id:
                    cursor.execute(
                        """
                        SELECT * FROM shipping_quotes
                        WHERE id = %s AND user_id = %s
                        """,
                        (quote_id, current_user["id"])
                    )
                    quote = cursor.fetchone()
                    
                    if not quote:
                        return jsonify({"status": "error", "message": "Shipping quote not found"}), 404
                    
                    # Check if quote has expired
                    if quote["expires_at"] and quote["expires_at"] < datetime.now():
                        return jsonify({"status": "error", "message": "Shipping quote has expired. Please request a new quote."}), 410
                    
                    # Use quote's shipping cost if not provided
                    if shipping_cost == 0:
                        shipping_cost = float(quote["quoted_price"])
                
                # Calculate total and validate products
                total_amount = 0
                order_items = []
                total_weight = 0
                
                for item in data["items"]:
                    if "product_id" not in item or "quantity" not in item:
                        return jsonify({"status": "error", "message": "Each item must have product_id and quantity"}), 400
                    
                    product_id = int(item["product_id"])
                    quantity = int(item["quantity"])
                    size = item.get("size", "")
                    
                    # Fetch product details including weight
                    cursor.execute(
                        "SELECT id, item, price, discount, qty, weight FROM product WHERE id = %s",
                        (product_id,)
                    )
                    product = cursor.fetchone()
                    
                    if not product:
                        return jsonify({"status": "error", "message": f"Product {product_id} not found"}), 404
                    
                    # Check stock availability
                    if product["qty"] < quantity:
                        return jsonify({
                            "status": "error",
                            "message": f"Insufficient stock for {product['item']}. Available: {product['qty']}"
                        }), 400
                    
                    # Calculate price with discount
                    price = product["price"]
                    if product["discount"] > 0:
                        price = price * (1 - product["discount"] / 100)
                    
                    subtotal = price * quantity
                    total_amount += subtotal
                    
                    # Calculate weight
                    item_weight = float(product.get("weight", 0.5))
                    total_weight += item_weight * quantity
                    
                    order_items.append({
                        "product_id": product_id,
                        "product_name": product["item"],
                        "price": price,
                        "quantity": quantity,
                        "size": size,
                        "subtotal": subtotal,
                        "weight": item_weight
                    })
                
                # Add shipping cost to total
                total_amount += shipping_cost
                
                # Generate tracking number
                tracking = _generate_tracking_number()
                
                # Determine payment status
                payment_status = "paid" if data.get("transaction_id") else "Pending"
                
                # Create order with shipping information
                cursor.execute(
                    """
                    INSERT INTO orders
                        (user_id, tracking, total_amount, payment_method, transaction_id,
                         payment_status, order_status, delivery_status, address, address_id, shipping_cost)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        current_user["id"],
                        tracking,
                        total_amount,
                        data["payment_method"],
                        data.get("transaction_id"),
                        payment_status,
                        "processing",
                        "Pending",
                        address_string,
                        address_id,
                        shipping_cost
                    )
                )
                order_id = cursor.lastrowid
                
                # Insert order items and update product quantities
                for item in order_items:
                    cursor.execute(
                        """
                        INSERT INTO order_items
                            (order_id, product_id, product_name, price, quantity, size, subtotal)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            order_id,
                            item["product_id"],
                            item["product_name"],
                            item["price"],
                            item["quantity"],
                            item["size"],
                            item["subtotal"]
                        )
                    )
                    
                    # Reduce product quantity
                    cursor.execute(
                        "UPDATE product SET qty = qty - %s WHERE id = %s",
                        (item["quantity"], item["product_id"])
                    )
                
                # Clear user's cart (optional)
                cursor.execute("DELETE FROM cart WHERE userid = %s", (current_user["id"],))
                
                conn.commit()
                
                # If payment is confirmed, create Sendbox shipment
                shipment_created = False
                shipment_error = None
                
                if payment_status == "paid" and shipping_address:
                    from services.shipment_manager import create_shipment_for_order, extract_shipment_details
                    
                    success, shipment_data, error_msg = create_shipment_for_order(
                        order_id=order_id,
                        order_items=order_items,
                        destination_address=shipping_address,
                        total_weight=total_weight,
                        total_value=total_amount - shipping_cost,  # Exclude shipping from item value
                        service_code=service_code
                    )
                    
                    if success and shipment_data:
                        # Extract shipment details
                        shipment_details = extract_shipment_details(shipment_data)
                        
                        # Update order with Sendbox information
                        cursor.execute(
                            """
                            UPDATE orders
                            SET sendbox_shipment_id = %s,
                                sendbox_tracking_code = %s,
                                sendbox_status = %s,
                                sendbox_carrier = %s,
                                estimated_delivery_date = %s,
                                sendbox_webhook_data = %s
                            WHERE id = %s
                            """,
                            (
                                shipment_details["sendbox_shipment_id"],
                                shipment_details["sendbox_tracking_code"],
                                shipment_details["sendbox_status"],
                                shipment_details["sendbox_carrier"],
                                shipment_details["estimated_delivery_date"],
                                shipment_details["sendbox_webhook_data"],
                                order_id
                            )
                        )
                        conn.commit()
                        shipment_created = True
                    else:
                        shipment_error = error_msg
                        # Log error but don't fail the order
                        import logging
                        logging.error(f"Failed to create shipment for order {order_id}: {error_msg}")
                
                # Fetch created order
                cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
                order = cursor.fetchone()
                
                response_data = {
                    "order": _serialize_order(order),
                    "tracking_number": tracking,
                    "shipping": {
                        "cost": shipping_cost,
                        "service_code": service_code,
                        "shipment_created": shipment_created
                    }
                }
                
                if shipment_error:
                    response_data["shipping"]["error"] = shipment_error
                    response_data["shipping"]["note"] = "Shipment will be created automatically or can be created manually by admin"
                
                return jsonify({
                    "status": "success",
                    "message": "Order created successfully",
                    "data": response_data
                }), 201
                
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


# ──────────────────────────────────────────────
# ORDER RETRIEVAL
# ──────────────────────────────────────────────

@orders_bp.route("/api/orders", methods=["GET"])
@token_required
def get_user_orders(current_user):
    """Get all orders for the current user with pagination."""
    try:
        page = max(int(request.args.get("page", 1)), 1)
        limit = min(max(int(request.args.get("limit", 20)), 1), 100)
        offset = (page - 1) * limit
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Get total count
                cursor.execute(
                    "SELECT COUNT(*) as total FROM orders WHERE user_id = %s",
                    (current_user["id"],)
                )
                total = cursor.fetchone()["total"]
                
                # Fetch orders
                cursor.execute(
                    """
                    SELECT * FROM orders
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    (current_user["id"], limit, offset)
                )
                orders = cursor.fetchall()
                
                # Fetch items for each order
                result = []
                for order in orders:
                    cursor.execute(
                        "SELECT * FROM order_items WHERE order_id = %s",
                        (order["id"],)
                    )
                    items = cursor.fetchall()
                    
                    order_data = _serialize_order(order)
                    order_data["items"] = [_serialize_order_item(item) for item in items]
                    result.append(order_data)
                
                total_pages = (total + limit - 1) // limit
                
                return jsonify({
                    "status": "success",
                    "data": {
                        "orders": result,
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
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@orders_bp.route("/api/orders/<int:order_id>", methods=["GET"])
@token_required
def get_order_details(current_user, order_id):
    """Get details of a specific order."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Fetch order
                cursor.execute(
                    "SELECT * FROM orders WHERE id = %s AND user_id = %s",
                    (order_id, current_user["id"])
                )
                order = cursor.fetchone()
                
                if not order:
                    return jsonify({"status": "error", "message": "Order not found"}), 404
                
                # Fetch order items
                cursor.execute(
                    "SELECT * FROM order_items WHERE order_id = %s",
                    (order_id,)
                )
                items = cursor.fetchall()
                
                order_data = _serialize_order(order)
                order_data["items"] = [_serialize_order_item(item) for item in items]
                
                return jsonify({
                    "status": "success",
                    "data": {"order": order_data}
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


# ──────────────────────────────────────────────
# ORDER TRACKING
# ──────────────────────────────────────────────

@orders_bp.route("/api/orders/track/<string:tracking_number>", methods=["GET"])
def track_order(tracking_number):
    """
    Track an order by tracking number (public endpoint).
    Enhanced with Sendbox tracking information.
    """
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM orders WHERE tracking = %s",
                    (tracking_number,)
                )
                order = cursor.fetchone()
                
                if not order:
                    return jsonify({"status": "error", "message": "Order not found"}), 404
                
                # Fetch order items
                cursor.execute(
                    "SELECT * FROM order_items WHERE order_id = %s",
                    (order["id"],)
                )
                items = cursor.fetchall()
                
                order_data = _serialize_order(order)
                order_data["items"] = [_serialize_order_item(item) for item in items]
                
                # Add Sendbox tracking information if available
                tracking_info = None
                if order.get("sendbox_tracking_code"):
                    from services.tracking_sync import get_tracking_summary
                    
                    # Get tracking data from Sendbox if needed
                    tracking_data = None
                    if order.get("sendbox_webhook_data"):
                        import json
                        try:
                            tracking_data = json.loads(order["sendbox_webhook_data"])
                        except:
                            pass
                    
                    # Get tracking summary
                    tracking_info = get_tracking_summary(order, tracking_data)
                
                response_data = {
                    "order": order_data
                }
                
                if tracking_info:
                    response_data["tracking"] = tracking_info
                
                return jsonify({
                    "status": "success",
                    "data": response_data
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


# ──────────────────────────────────────────────
# ADMIN ORDER MANAGEMENT
# ──────────────────────────────────────────────

@orders_bp.route("/api/admin/orders", methods=["GET"])
@admin_required
def get_all_orders(current_admin):
    """Get all orders (admin only) with pagination and filters."""
    try:
        page = max(int(request.args.get("page", 1)), 1)
        limit = min(max(int(request.args.get("limit", 20)), 1), 100)
        offset = (page - 1) * limit
        
        # Filters
        filters = []
        params = []
        
        order_status = request.args.get("order_status")
        if order_status:
            filters.append("order_status = %s")
            params.append(order_status)
        
        payment_status = request.args.get("payment_status")
        if payment_status:
            filters.append("payment_status = %s")
            params.append(payment_status)
        
        delivery_status = request.args.get("delivery_status")
        if delivery_status:
            filters.append("delivery_status = %s")
            params.append(delivery_status)
        
        where_clause = ""
        if filters:
            where_clause = "WHERE " + " AND ".join(filters)
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Get total count
                cursor.execute(
                    f"SELECT COUNT(*) as total FROM orders {where_clause}",
                    params
                )
                total = cursor.fetchone()["total"]
                
                # Fetch orders
                cursor.execute(
                    f"""
                    SELECT * FROM orders
                    {where_clause}
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    params + [limit, offset]
                )
                orders = cursor.fetchall()
                
                result = [_serialize_order(order) for order in orders]
                total_pages = (total + limit - 1) // limit
                
                return jsonify({
                    "status": "success",
                    "data": {
                        "orders": result,
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
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@orders_bp.route("/api/admin/orders/<int:order_id>", methods=["PUT"])
@admin_required
def update_order_status(current_admin, order_id):
    """
    Update order status (admin only).
    
    Expected JSON body:
    {
        "order_status": "processing|shipped|delivered|cancelled",
        "payment_status": "Pending|paid|failed|refunded",
        "delivery_status": "Pending|in_transit|delivered"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Check order exists
                cursor.execute("SELECT id FROM orders WHERE id = %s", (order_id,))
                if not cursor.fetchone():
                    return jsonify({"status": "error", "message": "Order not found"}), 404
                
                # Build update query
                updatable = ["order_status", "payment_status", "delivery_status"]
                set_parts = []
                values = []
                
                for field in updatable:
                    if field in data:
                        set_parts.append(f"{field} = %s")
                        values.append(data[field])
                
                if not set_parts:
                    return jsonify({"status": "error", "message": "No valid fields to update"}), 400
                
                values.append(order_id)
                cursor.execute(
                    f"UPDATE orders SET {', '.join(set_parts)} WHERE id = %s",
                    values
                )
                conn.commit()
                
                # Fetch updated order
                cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
                order = cursor.fetchone()
                
                return jsonify({
                    "status": "success",
                    "message": "Order updated successfully",
                    "data": {"order": _serialize_order(order)}
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@orders_bp.route("/api/admin/orders/<int:order_id>", methods=["DELETE"])
@admin_required
def delete_order(current_admin, order_id):
    """Delete an order (admin only)."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, tracking FROM orders WHERE id = %s", (order_id,))
                order = cursor.fetchone()
                
                if not order:
                    return jsonify({"status": "error", "message": "Order not found"}), 404
                
                # Delete order items first
                cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
                
                # Delete order
                cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
                conn.commit()
                
                return jsonify({
                    "status": "success",
                    "message": f"Order {order['tracking']} deleted successfully"
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


# ──────────────────────────────────────────────
# ORDER CONFIRMATION
# ──────────────────────────────────────────────

@orders_bp.route("/api/orders/<int:order_id>/confirm", methods=["POST"])
@token_required
def confirm_order(current_user, order_id):
    """Confirm order payment (update transaction_id and payment_status) and create shipment."""
    try:
        data = request.get_json()
        
        if "transaction_id" not in data:
            return jsonify({"status": "error", "message": "transaction_id is required"}), 400
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Check order exists and belongs to user
                cursor.execute(
                    """
                    SELECT o.*, o.address_id
                    FROM orders o
                    WHERE o.id = %s AND o.user_id = %s
                    """,
                    (order_id, current_user["id"])
                )
                order = cursor.fetchone()
                
                if not order:
                    return jsonify({"status": "error", "message": "Order not found"}), 404
                
                # Update payment info
                cursor.execute(
                    """
                    UPDATE orders
                    SET transaction_id = %s, payment_status = 'paid'
                    WHERE id = %s
                    """,
                    (data["transaction_id"], order_id)
                )
                conn.commit()
                
                # Create Sendbox shipment if address_id exists and shipment not already created
                shipment_created = False
                shipment_error = None
                
                if order.get("address_id") and not order.get("sendbox_shipment_id"):
                    # Fetch shipping address
                    cursor.execute(
                        "SELECT * FROM shipping_addresses WHERE id = %s",
                        (order["address_id"],)
                    )
                    shipping_address = cursor.fetchone()
                    
                    if shipping_address:
                        # Fetch order items with product details
                        cursor.execute(
                            """
                            SELECT oi.*, p.weight
                            FROM order_items oi
                            LEFT JOIN product p ON oi.product_id = p.id
                            WHERE oi.order_id = %s
                            """,
                            (order_id,)
                        )
                        order_items = cursor.fetchall()
                        
                        # Calculate total weight
                        total_weight = 0
                        items_with_weight = []
                        for item in order_items:
                            item_dict = dict(item)
                            weight = float(item.get("weight", 0.5))
                            total_weight += weight * item["quantity"]
                            item_dict["weight"] = weight
                            items_with_weight.append(item_dict)
                        
                        # Create shipment
                        from services.shipment_manager import create_shipment_for_order, extract_shipment_details
                        
                        success, shipment_data, error_msg = create_shipment_for_order(
                            order_id=order_id,
                            order_items=items_with_weight,
                            destination_address=shipping_address,
                            total_weight=total_weight,
                            total_value=float(order["total_amount"]) - float(order.get("shipping_cost", 0)),
                            service_code="standard"
                        )
                        
                        if success and shipment_data:
                            # Extract and update shipment details
                            shipment_details = extract_shipment_details(shipment_data)
                            
                            cursor.execute(
                                """
                                UPDATE orders
                                SET sendbox_shipment_id = %s,
                                    sendbox_tracking_code = %s,
                                    sendbox_status = %s,
                                    sendbox_carrier = %s,
                                    estimated_delivery_date = %s,
                                    sendbox_webhook_data = %s
                                WHERE id = %s
                                """,
                                (
                                    shipment_details["sendbox_shipment_id"],
                                    shipment_details["sendbox_tracking_code"],
                                    shipment_details["sendbox_status"],
                                    shipment_details["sendbox_carrier"],
                                    shipment_details["estimated_delivery_date"],
                                    shipment_details["sendbox_webhook_data"],
                                    order_id
                                )
                            )
                            conn.commit()
                            shipment_created = True
                        else:
                            shipment_error = error_msg
                
                # Fetch updated order
                cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
                order = cursor.fetchone()
                
                response_data = {
                    "order": _serialize_order(order)
                }
                
                if shipment_created:
                    response_data["shipment"] = {
                        "created": True,
                        "tracking_code": order.get("sendbox_tracking_code"),
                        "carrier": order.get("sendbox_carrier")
                    }
                elif shipment_error:
                    response_data["shipment"] = {
                        "created": False,
                        "error": shipment_error,
                        "note": "Shipment can be created manually by admin"
                    }
                
                return jsonify({
                    "status": "success",
                    "message": "Order payment confirmed",
                    "data": response_data
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


# ──────────────────────────────────────────────
# ADMIN SHIPMENT MANAGEMENT
# ──────────────────────────────────────────────

@orders_bp.route("/api/admin/orders/<int:order_id>/create-shipment", methods=["POST"])
@admin_required
def admin_create_shipment(current_admin, order_id):
    """Manually create Sendbox shipment for an order (admin only)."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Fetch order with address
                cursor.execute(
                    """
                    SELECT o.*, o.address_id
                    FROM orders o
                    WHERE o.id = %s
                    """,
                    (order_id,)
                )
                order = cursor.fetchone()
                
                if not order:
                    return jsonify({"status": "error", "message": "Order not found"}), 404
                
                # Check if shipment already exists
                if order.get("sendbox_shipment_id"):
                    return jsonify({
                        "status": "error",
                        "message": "Shipment already exists for this order",
                        "data": {
                            "sendbox_shipment_id": order["sendbox_shipment_id"],
                            "sendbox_tracking_code": order["sendbox_tracking_code"]
                        }
                    }), 400
                
                # Check if address_id exists
                if not order.get("address_id"):
                    return jsonify({
                        "status": "error",
                        "message": "Order does not have a structured shipping address. Cannot create shipment."
                    }), 400
                
                # Fetch shipping address
                cursor.execute(
                    "SELECT * FROM shipping_addresses WHERE id = %s",
                    (order["address_id"],)
                )
                shipping_address = cursor.fetchone()
                
                if not shipping_address:
                    return jsonify({"status": "error", "message": "Shipping address not found"}), 404
                
                # Fetch order items with product details
                cursor.execute(
                    """
                    SELECT oi.*, p.weight
                    FROM order_items oi
                    LEFT JOIN product p ON oi.product_id = p.id
                    WHERE oi.order_id = %s
                    """,
                    (order_id,)
                )
                order_items = cursor.fetchall()
                
                # Calculate total weight
                total_weight = 0
                items_with_weight = []
                for item in order_items:
                    item_dict = dict(item)
                    weight = float(item.get("weight", 0.5))
                    total_weight += weight * item["quantity"]
                    item_dict["weight"] = weight
                    items_with_weight.append(item_dict)
                
                # Create shipment
                from services.shipment_manager import create_shipment_for_order, extract_shipment_details
                
                success, shipment_data, error_msg = create_shipment_for_order(
                    order_id=order_id,
                    order_items=items_with_weight,
                    destination_address=shipping_address,
                    total_weight=total_weight,
                    total_value=float(order["total_amount"]) - float(order.get("shipping_cost", 0)),
                    service_code="standard"
                )
                
                if not success:
                    return jsonify({
                        "status": "error",
                        "message": f"Failed to create shipment: {error_msg}"
                    }), 500
                
                # Extract and update shipment details
                shipment_details = extract_shipment_details(shipment_data)
                
                cursor.execute(
                    """
                    UPDATE orders
                    SET sendbox_shipment_id = %s,
                        sendbox_tracking_code = %s,
                        sendbox_status = %s,
                        sendbox_carrier = %s,
                        estimated_delivery_date = %s,
                        sendbox_webhook_data = %s
                    WHERE id = %s
                    """,
                    (
                        shipment_details["sendbox_shipment_id"],
                        shipment_details["sendbox_tracking_code"],
                        shipment_details["sendbox_status"],
                        shipment_details["sendbox_carrier"],
                        shipment_details["estimated_delivery_date"],
                        shipment_details["sendbox_webhook_data"],
                        order_id
                    )
                )
                conn.commit()
                
                # Fetch updated order
                cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
                order = cursor.fetchone()
                
                return jsonify({
                    "status": "success",
                    "message": "Shipment created successfully",
                    "data": {
                        "order": _serialize_order(order),
                        "shipment": {
                            "sendbox_shipment_id": shipment_details["sendbox_shipment_id"],
                            "sendbox_tracking_code": shipment_details["sendbox_tracking_code"],
                            "carrier": shipment_details["sendbox_carrier"],
                            "status": shipment_details["sendbox_status"]
                        }
                    }
                }), 201
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@orders_bp.route("/api/admin/orders/<int:order_id>/sendbox-details", methods=["GET"])
@admin_required
def get_sendbox_details(current_admin, order_id):
    """Get full Sendbox shipment details for an order (admin only)."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT sendbox_shipment_id, sendbox_tracking_code, sendbox_status,
                           sendbox_carrier, estimated_delivery_date, sendbox_webhook_data
                    FROM orders
                    WHERE id = %s
                    """,
                    (order_id,)
                )
                order = cursor.fetchone()
                
                if not order:
                    return jsonify({"status": "error", "message": "Order not found"}), 404
                
                if not order.get("sendbox_shipment_id"):
                    return jsonify({
                        "status": "error",
                        "message": "No Sendbox shipment found for this order"
                    }), 404
                
                # Parse webhook data
                webhook_data = None
                if order.get("sendbox_webhook_data"):
                    import json
                    try:
                        webhook_data = json.loads(order["sendbox_webhook_data"])
                    except:
                        webhook_data = order["sendbox_webhook_data"]
                
                return jsonify({
                    "status": "success",
                    "data": {
                        "sendbox_shipment_id": order["sendbox_shipment_id"],
                        "sendbox_tracking_code": order["sendbox_tracking_code"],
                        "sendbox_status": order["sendbox_status"],
                        "sendbox_carrier": order["sendbox_carrier"],
                        "estimated_delivery_date": order["estimated_delivery_date"].strftime("%Y-%m-%d") if order.get("estimated_delivery_date") else None,
                        "webhook_data": webhook_data
                    }
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@orders_bp.route("/api/admin/orders/<int:order_id>/refresh-tracking", methods=["POST"])
@admin_required
def refresh_tracking(current_admin, order_id):
    """Force refresh tracking information from Sendbox (admin only)."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT sendbox_tracking_code FROM orders WHERE id = %s",
                    (order_id,)
                )
                order = cursor.fetchone()
                
                if not order:
                    return jsonify({"status": "error", "message": "Order not found"}), 404
                
                if not order.get("sendbox_tracking_code"):
                    return jsonify({
                        "status": "error",
                        "message": "No Sendbox tracking code found for this order"
                    }), 404
                
                # Get tracking from Sendbox
                from services.sendbox_service import get_sendbox_client, SendboxAPIError
                
                client = get_sendbox_client()
                
                try:
                    tracking_data = client.track_shipment(order["sendbox_tracking_code"])
                    
                    # Update order with latest tracking info
                    from services.shipment_manager import map_sendbox_status_to_internal
                    import json
                    
                    sendbox_status = tracking_data.get("status", "pending")
                    order_status, delivery_status = map_sendbox_status_to_internal(sendbox_status)
                    
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
                            order_id
                        )
                    )
                    conn.commit()
                    
                    return jsonify({
                        "status": "success",
                        "message": "Tracking information refreshed successfully",
                        "data": {
                            "sendbox_status": sendbox_status,
                            "order_status": order_status,
                            "delivery_status": delivery_status,
                            "tracking_data": tracking_data
                        }
                    }), 200
                    
                except SendboxAPIError as e:
                    return jsonify({
                        "status": "error",
                        "message": f"Sendbox API error: {e.message}"
                    }), 500
                    
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500
