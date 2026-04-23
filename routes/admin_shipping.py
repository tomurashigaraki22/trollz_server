"""
Admin Shipping Routes
Advanced admin features for Sendbox shipment management, reports, and account monitoring.
"""

from flask import Blueprint, request, jsonify
from db import get_db_connection
from middleware.auth_middleware import admin_required
from services.sendbox_service import get_sendbox_client, SendboxAPIError
from datetime import datetime, timedelta
import logging

admin_shipping_bp = Blueprint("admin_shipping", __name__)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# SHIPMENT CANCELLATION
# ──────────────────────────────────────────────

@admin_shipping_bp.route("/api/admin/orders/<int:order_id>/cancel-shipment", methods=["POST"])
@admin_required
def cancel_shipment(current_admin, order_id):
    """
    Cancel Sendbox shipment and optionally restore stock (admin only).
    
    Request body (optional):
    {
        "restore_stock": true,
        "reason": "Customer requested cancellation"
    }
    """
    try:
        data = request.get_json() or {}
        restore_stock = data.get("restore_stock", False)
        reason = data.get("reason", "Admin cancelled shipment")
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Fetch order
                cursor.execute(
                    """
                    SELECT id, sendbox_shipment_id, sendbox_tracking_code, 
                           order_status, stock_restored
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
                
                # Check if already cancelled
                if order["order_status"] == "cancelled":
                    return jsonify({
                        "status": "error",
                        "message": "Order is already cancelled"
                    }), 400
                
                # Cancel shipment in Sendbox (if API supports it)
                # Note: Sendbox may not have a cancel endpoint, so we'll just update locally
                # TODO: Implement actual Sendbox cancellation if API supports it
                
                # Update order status
                cursor.execute(
                    """
                    UPDATE orders
                    SET order_status = 'cancelled',
                        sendbox_status = 'cancelled'
                    WHERE id = %s
                    """,
                    (order_id,)
                )
                
                # Restore stock if requested
                restored_items = []
                if restore_stock and not order.get("stock_restored"):
                    cursor.execute(
                        "SELECT product_id, quantity FROM order_items WHERE order_id = %s",
                        (order_id,)
                    )
                    items = cursor.fetchall()
                    
                    for item in items:
                        cursor.execute(
                            "UPDATE product SET qty = qty + %s WHERE id = %s",
                            (item["quantity"], item["product_id"])
                        )
                        restored_items.append({
                            "product_id": item["product_id"],
                            "quantity": item["quantity"]
                        })
                    
                    # Mark stock as restored
                    cursor.execute(
                        "UPDATE orders SET stock_restored = TRUE WHERE id = %s",
                        (order_id,)
                    )
                
                conn.commit()
                
                logger.info(f"Shipment cancelled for order {order_id} by admin {current_admin['id']}")
                
                return jsonify({
                    "status": "success",
                    "message": "Shipment cancelled successfully",
                    "data": {
                        "order_id": order_id,
                        "sendbox_shipment_id": order["sendbox_shipment_id"],
                        "stock_restored": restore_stock,
                        "restored_items": restored_items,
                        "reason": reason
                    }
                }), 200
                
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error cancelling shipment: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


# ──────────────────────────────────────────────
# BULK SHIPMENT CREATION
# ──────────────────────────────────────────────

@admin_shipping_bp.route("/api/admin/orders/bulk-create-shipments", methods=["POST"])
@admin_required
def bulk_create_shipments(current_admin):
    """
    Create Sendbox shipments for multiple orders (admin only).
    
    Request body:
    {
        "order_ids": [1, 2, 3, 4, 5],
        "service_code": "standard"
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
        service_code = data.get("service_code", "standard")
        
        results = {
            "success": [],
            "failed": [],
            "total": len(order_ids)
        }
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                for order_id in order_ids:
                    try:
                        # Fetch order
                        cursor.execute(
                            "SELECT * FROM orders WHERE id = %s",
                            (order_id,)
                        )
                        order = cursor.fetchone()
                        
                        if not order:
                            results["failed"].append({
                                "order_id": order_id,
                                "error": "Order not found"
                            })
                            continue
                        
                        # Check if shipment already exists
                        if order.get("sendbox_shipment_id"):
                            results["failed"].append({
                                "order_id": order_id,
                                "error": "Shipment already exists"
                            })
                            continue
                        
                        # Check if address exists
                        if not order.get("address_id"):
                            results["failed"].append({
                                "order_id": order_id,
                                "error": "No shipping address"
                            })
                            continue
                        
                        # Fetch shipping address
                        cursor.execute(
                            "SELECT * FROM shipping_addresses WHERE id = %s",
                            (order["address_id"],)
                        )
                        shipping_address = cursor.fetchone()
                        
                        if not shipping_address:
                            results["failed"].append({
                                "order_id": order_id,
                                "error": "Shipping address not found"
                            })
                            continue
                        
                        # Fetch order items
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
                        
                        # Calculate weight
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
                            service_code=service_code
                        )
                        
                        if success and shipment_data:
                            # Update order
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
                            
                            results["success"].append({
                                "order_id": order_id,
                                "tracking_code": shipment_details["sendbox_tracking_code"]
                            })
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
                
                logger.info(f"Bulk shipment creation: {len(results['success'])} succeeded, {len(results['failed'])} failed")
                
                return jsonify({
                    "status": "success",
                    "message": f"Created {len(results['success'])} of {results['total']} shipments",
                    "data": results
                }), 200
                
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error in bulk shipment creation: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


# ──────────────────────────────────────────────
# SHIPPING REPORTS
# ──────────────────────────────────────────────

@admin_shipping_bp.route("/api/admin/reports/shipping", methods=["GET"])
@admin_required
def get_shipping_reports(current_admin):
    """
    Generate shipping analytics and reports (admin only).
    
    Query parameters:
    - start_date: YYYY-MM-DD (default: 30 days ago)
    - end_date: YYYY-MM-DD (default: today)
    - report_type: summary|detailed (default: summary)
    """
    try:
        # Parse date range
        end_date = request.args.get("end_date", datetime.now().strftime("%Y-%m-%d"))
        start_date = request.args.get("start_date", (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        report_type = request.args.get("report_type", "summary")
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Total shipping costs
                cursor.execute(
                    """
                    SELECT 
                        COUNT(*) as total_shipments,
                        SUM(shipping_cost) as total_shipping_cost,
                        AVG(shipping_cost) as avg_shipping_cost,
                        MIN(shipping_cost) as min_shipping_cost,
                        MAX(shipping_cost) as max_shipping_cost
                    FROM orders
                    WHERE created_at BETWEEN %s AND %s
                    AND sendbox_shipment_id IS NOT NULL
                    """,
                    (start_date, end_date)
                )
                shipping_summary = cursor.fetchone()
                
                # Carrier breakdown
                cursor.execute(
                    """
                    SELECT 
                        sendbox_carrier,
                        COUNT(*) as shipment_count,
                        SUM(shipping_cost) as total_cost,
                        AVG(shipping_cost) as avg_cost
                    FROM orders
                    WHERE created_at BETWEEN %s AND %s
                    AND sendbox_carrier IS NOT NULL
                    GROUP BY sendbox_carrier
                    ORDER BY shipment_count DESC
                    """,
                    (start_date, end_date)
                )
                carrier_breakdown = cursor.fetchall()
                
                # Status breakdown
                cursor.execute(
                    """
                    SELECT 
                        sendbox_status,
                        COUNT(*) as count
                    FROM orders
                    WHERE created_at BETWEEN %s AND %s
                    AND sendbox_status IS NOT NULL
                    GROUP BY sendbox_status
                    ORDER BY count DESC
                    """,
                    (start_date, end_date)
                )
                status_breakdown = cursor.fetchall()
                
                # Delivery success rate
                cursor.execute(
                    """
                    SELECT 
                        COUNT(CASE WHEN sendbox_status = 'delivered' THEN 1 END) as delivered,
                        COUNT(CASE WHEN sendbox_status = 'failed' THEN 1 END) as failed,
                        COUNT(CASE WHEN sendbox_status = 'cancelled' THEN 1 END) as cancelled,
                        COUNT(*) as total
                    FROM orders
                    WHERE created_at BETWEEN %s AND %s
                    AND sendbox_shipment_id IS NOT NULL
                    """,
                    (start_date, end_date)
                )
                delivery_stats = cursor.fetchone()
                
                # Average delivery time (for delivered orders)
                cursor.execute(
                    """
                    SELECT 
                        AVG(DATEDIFF(updated_at, created_at)) as avg_delivery_days
                    FROM orders
                    WHERE created_at BETWEEN %s AND %s
                    AND sendbox_status = 'delivered'
                    """,
                    (start_date, end_date)
                )
                delivery_time = cursor.fetchone()
                
                # Shipping cost vs order value ratio
                cursor.execute(
                    """
                    SELECT 
                        AVG((shipping_cost / total_amount) * 100) as avg_shipping_percentage
                    FROM orders
                    WHERE created_at BETWEEN %s AND %s
                    AND sendbox_shipment_id IS NOT NULL
                    AND total_amount > 0
                    """,
                    (start_date, end_date)
                )
                cost_ratio = cursor.fetchone()
                
                # Build report
                report = {
                    "period": {
                        "start_date": start_date,
                        "end_date": end_date
                    },
                    "summary": {
                        "total_shipments": shipping_summary["total_shipments"] or 0,
                        "total_shipping_cost": float(shipping_summary["total_shipping_cost"] or 0),
                        "avg_shipping_cost": float(shipping_summary["avg_shipping_cost"] or 0),
                        "min_shipping_cost": float(shipping_summary["min_shipping_cost"] or 0),
                        "max_shipping_cost": float(shipping_summary["max_shipping_cost"] or 0),
                        "avg_delivery_days": float(delivery_time["avg_delivery_days"] or 0),
                        "avg_shipping_percentage": float(cost_ratio["avg_shipping_percentage"] or 0)
                    },
                    "carriers": [
                        {
                            "carrier": c["sendbox_carrier"],
                            "shipment_count": c["shipment_count"],
                            "total_cost": float(c["total_cost"]),
                            "avg_cost": float(c["avg_cost"])
                        }
                        for c in carrier_breakdown
                    ],
                    "status_breakdown": [
                        {
                            "status": s["sendbox_status"],
                            "count": s["count"]
                        }
                        for s in status_breakdown
                    ],
                    "delivery_performance": {
                        "delivered": delivery_stats["delivered"] or 0,
                        "failed": delivery_stats["failed"] or 0,
                        "cancelled": delivery_stats["cancelled"] or 0,
                        "total": delivery_stats["total"] or 0,
                        "success_rate": (delivery_stats["delivered"] / delivery_stats["total"] * 100) if delivery_stats["total"] > 0 else 0
                    }
                }
                
                # Add detailed data if requested
                if report_type == "detailed":
                    cursor.execute(
                        """
                        SELECT 
                            id, tracking, sendbox_tracking_code, sendbox_carrier,
                            shipping_cost, sendbox_status, created_at, updated_at
                        FROM orders
                        WHERE created_at BETWEEN %s AND %s
                        AND sendbox_shipment_id IS NOT NULL
                        ORDER BY created_at DESC
                        """,
                        (start_date, end_date)
                    )
                    shipments = cursor.fetchall()
                    
                    report["shipments"] = [
                        {
                            "order_id": s["id"],
                            "tracking": s["tracking"],
                            "sendbox_tracking_code": s["sendbox_tracking_code"],
                            "carrier": s["sendbox_carrier"],
                            "shipping_cost": float(s["shipping_cost"]),
                            "status": s["sendbox_status"],
                            "created_at": s["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
                            "updated_at": s["updated_at"].strftime("%Y-%m-%d %H:%M:%S") if s["updated_at"] else None
                        }
                        for s in shipments
                    ]
                
                return jsonify({
                    "status": "success",
                    "data": report
                }), 200
                
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error generating shipping report: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


# ──────────────────────────────────────────────
# SENDBOX ACCOUNT MANAGEMENT
# ──────────────────────────────────────────────

@admin_shipping_bp.route("/api/admin/sendbox/account", methods=["GET"])
@admin_required
def get_sendbox_account(current_admin):
    """Get Sendbox account information and balance (admin only)."""
    try:
        client = get_sendbox_client()
        
        try:
            account_info = client.get_account_balance()
            
            return jsonify({
                "status": "success",
                "data": {
                    "account": account_info,
                    "environment": client.environment,
                    "base_url": client.base_url
                }
            }), 200
            
        except SendboxAPIError as e:
            return jsonify({
                "status": "error",
                "message": f"Sendbox API error: {e.message}",
                "error_code": e.status_code
            }), 500
            
    except Exception as e:
        logger.error(f"Error fetching Sendbox account: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@admin_shipping_bp.route("/api/admin/sendbox/fund-account", methods=["POST"])
@admin_required
def fund_staging_account(current_admin):
    """
    Fund Sendbox staging account (staging environment only).
    
    Request body:
    {
        "amount": 10000
    }
    """
    try:
        data = request.get_json()
        
        if "amount" not in data:
            return jsonify({
                "status": "error",
                "message": "'amount' is required"
            }), 400
        
        amount = float(data["amount"])
        
        if amount <= 0:
            return jsonify({
                "status": "error",
                "message": "Amount must be greater than 0"
            }), 400
        
        client = get_sendbox_client()
        
        # Check if staging environment
        if client.environment != "staging":
            return jsonify({
                "status": "error",
                "message": "Fund account is only available in staging environment"
            }), 403
        
        try:
            result = client.add_money_staging(amount)
            
            logger.info(f"Staging account funded with {amount} by admin {current_admin['id']}")
            
            return jsonify({
                "status": "success",
                "message": f"Successfully added {amount} to staging account",
                "data": result
            }), 200
            
        except SendboxAPIError as e:
            return jsonify({
                "status": "error",
                "message": f"Sendbox API error: {e.message}",
                "error_code": e.status_code
            }), 500
            
    except Exception as e:
        logger.error(f"Error funding staging account: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@admin_shipping_bp.route("/api/admin/sendbox/shipments", methods=["GET"])
@admin_required
def get_all_sendbox_shipments(current_admin):
    """Get all shipments from Sendbox (admin only)."""
    try:
        client = get_sendbox_client()
        
        try:
            shipments = client.get_shipments()
            
            return jsonify({
                "status": "success",
                "data": {
                    "shipments": shipments,
                    "count": len(shipments) if isinstance(shipments, list) else 0
                }
            }), 200
            
        except SendboxAPIError as e:
            return jsonify({
                "status": "error",
                "message": f"Sendbox API error: {e.message}",
                "error_code": e.status_code
            }), 500
            
    except Exception as e:
        logger.error(f"Error fetching Sendbox shipments: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500



# ──────────────────────────────────────────────
# WEBHOOK MANAGEMENT
# ──────────────────────────────────────────────

@admin_shipping_bp.route("/api/admin/webhooks/events", methods=["GET"])
@admin_required
def get_webhook_events(current_admin):
    """
    Get webhook events for admin dashboard (admin only).
    
    Query parameters:
    - page: Page number (default: 1)
    - limit: Items per page (default: 20, max: 100)
    - processed: Filter by processed status (true/false)
    - order_id: Filter by order ID
    - tracking_code: Filter by tracking code
    """
    try:
        page = max(int(request.args.get("page", 1)), 1)
        limit = min(max(int(request.args.get("limit", 20)), 1), 100)
        offset = (page - 1) * limit
        
        # Build filters
        filters = []
        params = []
        
        processed = request.args.get("processed")
        if processed is not None:
            filters.append("processed = %s")
            params.append(processed.lower() == "true")
        
        order_id = request.args.get("order_id")
        if order_id:
            filters.append("order_id = %s")
            params.append(int(order_id))
        
        tracking_code = request.args.get("tracking_code")
        if tracking_code:
            filters.append("sendbox_tracking_code = %s")
            params.append(tracking_code)
        
        where_clause = ""
        if filters:
            where_clause = "WHERE " + " AND ".join(filters)
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Get total count
                cursor.execute(
                    f"SELECT COUNT(*) as total FROM webhook_events {where_clause}",
                    params
                )
                total = cursor.fetchone()["total"]
                
                # Fetch webhook events
                cursor.execute(
                    f"""
                    SELECT 
                        id, event_type, order_id, sendbox_tracking_code,
                        processed, processed_at, error_message, created_at,
                        payload
                    FROM webhook_events
                    {where_clause}
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    params + [limit, offset]
                )
                events = cursor.fetchall()
                
                # Format events
                formatted_events = []
                for event in events:
                    event_dict = dict(event)
                    
                    # Parse JSON payload
                    if event_dict.get("payload"):
                        try:
                            event_dict["payload"] = json.loads(event_dict["payload"])
                        except:
                            pass
                    
                    # Format timestamps
                    if event_dict.get("created_at"):
                        event_dict["created_at"] = event_dict["created_at"].strftime("%Y-%m-%d %H:%M:%S")
                    if event_dict.get("processed_at"):
                        event_dict["processed_at"] = event_dict["processed_at"].strftime("%Y-%m-%d %H:%M:%S")
                    
                    formatted_events.append(event_dict)
                
                total_pages = (total + limit - 1) // limit
                
                return jsonify({
                    "status": "success",
                    "data": {
                        "events": formatted_events,
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
        logger.error(f"Error fetching webhook events: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@admin_shipping_bp.route("/api/admin/webhooks/stats", methods=["GET"])
@admin_required
def get_webhook_stats(current_admin):
    """
    Get webhook statistics for admin dashboard (admin only).
    
    Returns:
    - Total webhooks received
    - Processed vs failed
    - Recent webhook activity
    - Event type breakdown
    """
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Total webhooks
                cursor.execute("SELECT COUNT(*) as total FROM webhook_events")
                total = cursor.fetchone()["total"]
                
                # Processed vs failed
                cursor.execute("""
                    SELECT 
                        COUNT(CASE WHEN processed = TRUE THEN 1 END) as processed,
                        COUNT(CASE WHEN processed = FALSE THEN 1 END) as failed
                    FROM webhook_events
                """)
                status_counts = cursor.fetchone()
                
                # Event type breakdown
                cursor.execute("""
                    SELECT event_type, COUNT(*) as count
                    FROM webhook_events
                    GROUP BY event_type
                    ORDER BY count DESC
                """)
                event_types = cursor.fetchall()
                
                # Recent activity (last 24 hours)
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM webhook_events
                    WHERE created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
                """)
                recent_24h = cursor.fetchone()["count"]
                
                # Recent activity (last 7 days)
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM webhook_events
                    WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
                """)
                recent_7d = cursor.fetchone()["count"]
                
                # Failed webhooks (last 24 hours)
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM webhook_events
                    WHERE processed = FALSE
                    AND created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
                """)
                failed_24h = cursor.fetchone()["count"]
                
                # Latest webhooks
                cursor.execute("""
                    SELECT 
                        id, event_type, order_id, sendbox_tracking_code,
                        processed, created_at
                    FROM webhook_events
                    ORDER BY created_at DESC
                    LIMIT 10
                """)
                latest = cursor.fetchall()
                
                # Format latest webhooks
                formatted_latest = []
                for webhook in latest:
                    webhook_dict = dict(webhook)
                    if webhook_dict.get("created_at"):
                        webhook_dict["created_at"] = webhook_dict["created_at"].strftime("%Y-%m-%d %H:%M:%S")
                    formatted_latest.append(webhook_dict)
                
                return jsonify({
                    "status": "success",
                    "data": {
                        "summary": {
                            "total_webhooks": total,
                            "processed": status_counts["processed"],
                            "failed": status_counts["failed"],
                            "success_rate": (status_counts["processed"] / total * 100) if total > 0 else 0
                        },
                        "recent_activity": {
                            "last_24_hours": recent_24h,
                            "last_7_days": recent_7d,
                            "failed_24_hours": failed_24h
                        },
                        "event_types": [
                            {
                                "event_type": et["event_type"],
                                "count": et["count"]
                            }
                            for et in event_types
                        ],
                        "latest_webhooks": formatted_latest
                    }
                }), 200
                
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error fetching webhook stats: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@admin_shipping_bp.route("/api/admin/webhooks/events/<int:event_id>", methods=["GET"])
@admin_required
def get_webhook_event_details(current_admin, event_id):
    """
    Get detailed information about a specific webhook event (admin only).
    
    Args:
        event_id: Webhook event ID
    """
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        we.*,
                        o.tracking as order_tracking,
                        o.order_status,
                        o.delivery_status
                    FROM webhook_events we
                    LEFT JOIN orders o ON we.order_id = o.id
                    WHERE we.id = %s
                """, (event_id,))
                
                event = cursor.fetchone()
                
                if not event:
                    return jsonify({
                        "status": "error",
                        "message": "Webhook event not found"
                    }), 404
                
                event_dict = dict(event)
                
                # Parse JSON payload
                if event_dict.get("payload"):
                    try:
                        event_dict["payload"] = json.loads(event_dict["payload"])
                    except:
                        pass
                
                # Format timestamps
                if event_dict.get("created_at"):
                    event_dict["created_at"] = event_dict["created_at"].strftime("%Y-%m-%d %H:%M:%S")
                if event_dict.get("processed_at"):
                    event_dict["processed_at"] = event_dict["processed_at"].strftime("%Y-%m-%d %H:%M:%S")
                
                return jsonify({
                    "status": "success",
                    "data": {
                        "event": event_dict
                    }
                }), 200
                
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error fetching webhook event details: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@admin_shipping_bp.route("/api/admin/webhooks/retry/<int:event_id>", methods=["POST"])
@admin_required
def retry_webhook_event(current_admin, event_id):
    """
    Retry processing a failed webhook event (admin only).
    
    Args:
        event_id: Webhook event ID
    """
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Get webhook event
                cursor.execute("""
                    SELECT * FROM webhook_events WHERE id = %s
                """, (event_id,))
                
                event = cursor.fetchone()
                
                if not event:
                    return jsonify({
                        "status": "error",
                        "message": "Webhook event not found"
                    }), 404
                
                # Parse payload
                try:
                    payload = json.loads(event["payload"])
                except:
                    return jsonify({
                        "status": "error",
                        "message": "Invalid webhook payload"
                    }), 400
                
                # Extract tracking code
                tracking_code = payload.get("tracking_code") or payload.get("tracking")
                sendbox_status = payload.get("status")
                
                if not tracking_code:
                    return jsonify({
                        "status": "error",
                        "message": "Missing tracking code in payload"
                    }), 400
                
                # Find order
                cursor.execute("""
                    SELECT id, order_status, delivery_status 
                    FROM orders 
                    WHERE sendbox_tracking_code = %s
                """, (tracking_code,))
                
                order = cursor.fetchone()
                
                if not order:
                    return jsonify({
                        "status": "error",
                        "message": "Order not found for tracking code"
                    }), 404
                
                # Map status
                if sendbox_status:
                    order_status, delivery_status = map_sendbox_status_to_internal(sendbox_status)
                else:
                    order_status = order["order_status"]
                    delivery_status = order["delivery_status"]
                
                # Update order
                cursor.execute("""
                    UPDATE orders
                    SET sendbox_status = %s,
                        order_status = %s,
                        delivery_status = %s,
                        sendbox_webhook_data = %s
                    WHERE id = %s
                """, (
                    sendbox_status,
                    order_status,
                    delivery_status,
                    event["payload"],
                    order["id"]
                ))
                
                # Update webhook event
                cursor.execute("""
                    UPDATE webhook_events
                    SET processed = TRUE,
                        processed_at = %s,
                        error_message = NULL,
                        order_id = %s
                    WHERE id = %s
                """, (datetime.now(), order["id"], event_id))
                
                conn.commit()
                
                logger.info(f"Webhook event {event_id} retried successfully for order {order['id']}")
                
                return jsonify({
                    "status": "success",
                    "message": "Webhook event processed successfully",
                    "data": {
                        "event_id": event_id,
                        "order_id": order["id"],
                        "order_status": order_status,
                        "delivery_status": delivery_status
                    }
                }), 200
                
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error retrying webhook event: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500
