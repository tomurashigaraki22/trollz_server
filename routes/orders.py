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
        "address": "Full delivery address",
        "payment_method": "flutterwave|paystack|cash_on_delivery",
        "transaction_id": "optional_payment_transaction_id",
        "items": [
            {
                "product_id": 123,
                "quantity": 2,
                "size": "XL"
            }
        ]
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ["address", "payment_method", "items"]
        for field in required:
            if field not in data or not data[field]:
                return jsonify({"status": "error", "message": f"'{field}' is required"}), 400
        
        if not isinstance(data["items"], list) or len(data["items"]) == 0:
            return jsonify({"status": "error", "message": "At least one item is required"}), 400
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Calculate total and validate products
                total_amount = 0
                order_items = []
                
                for item in data["items"]:
                    if "product_id" not in item or "quantity" not in item:
                        return jsonify({"status": "error", "message": "Each item must have product_id and quantity"}), 400
                    
                    product_id = int(item["product_id"])
                    quantity = int(item["quantity"])
                    size = item.get("size", "")
                    
                    # Fetch product details
                    cursor.execute(
                        "SELECT id, item, price, discount, qty FROM product WHERE id = %s",
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
                    
                    order_items.append({
                        "product_id": product_id,
                        "product_name": product["item"],
                        "price": price,
                        "quantity": quantity,
                        "size": size,
                        "subtotal": subtotal
                    })
                
                # Generate tracking number
                tracking = _generate_tracking_number()
                
                # Determine payment status
                payment_status = "paid" if data.get("transaction_id") else "Pending"
                
                # Create order
                cursor.execute(
                    """
                    INSERT INTO orders
                        (user_id, tracking, total_amount, payment_method, transaction_id,
                         payment_status, order_status, delivery_status, address)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                        data["address"]
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
                
                # Fetch created order
                cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
                order = cursor.fetchone()
                
                return jsonify({
                    "status": "success",
                    "message": "Order created successfully",
                    "data": {
                        "order": _serialize_order(order),
                        "tracking_number": tracking
                    }
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
    """Track an order by tracking number (public endpoint)."""
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
                
                return jsonify({
                    "status": "success",
                    "data": {"order": order_data}
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
    """Confirm order payment (update transaction_id and payment_status)."""
    try:
        data = request.get_json()
        
        if "transaction_id" not in data:
            return jsonify({"status": "error", "message": "transaction_id is required"}), 400
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Check order exists and belongs to user
                cursor.execute(
                    "SELECT id FROM orders WHERE id = %s AND user_id = %s",
                    (order_id, current_user["id"])
                )
                if not cursor.fetchone():
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
                
                # Fetch updated order
                cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
                order = cursor.fetchone()
                
                return jsonify({
                    "status": "success",
                    "message": "Order payment confirmed",
                    "data": {"order": _serialize_order(order)}
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500
