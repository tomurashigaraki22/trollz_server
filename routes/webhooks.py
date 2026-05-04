"""
Webhook Routes
Handles incoming webhooks from Sendbox for shipment tracking updates.
"""

from flask import Blueprint, request, jsonify
from db import get_db_connection
from services.shipment_manager import map_sendbox_status_to_internal
from datetime import datetime
import logging
import json

webhooks_bp = Blueprint("webhooks", __name__)
logger = logging.getLogger(__name__)


@webhooks_bp.route("/api/webhooks/sendbox", methods=["POST"])
def sendbox_webhook():
    """
    Handle incoming webhooks from Sendbox.
    
    Sendbox sends webhooks for tracking updates with payload like:
    {
        "event": "shipment.status_updated",
        "tracking_code": "SB123456789",
        "shipment_id": 12345,
        "status": "in_transit",
        "timestamp": "2026-04-20T10:30:00Z",
        "data": { ... }
    }
    """
    try:
        # Get webhook payload
        payload = request.get_json()
        
        if not payload:
            logger.warning("Received empty webhook payload")
            return jsonify({"status": "error", "message": "Empty payload"}), 400
        
        logger.info(f"Received Sendbox webhook: {payload.get('event', 'unknown')}")
        
        # Extract key fields
        event_type = payload.get("event", "unknown")
        tracking_code = payload.get("tracking_code") or payload.get("tracking")
        shipment_id = payload.get("shipment_id") or payload.get("id")
        sendbox_status = payload.get("status")
        
        if not tracking_code:
            logger.warning("Webhook missing tracking_code")
            return jsonify({"status": "error", "message": "Missing tracking_code"}), 400
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Find order by tracking code
                cursor.execute(
                    "SELECT id, order_status, delivery_status FROM orders WHERE sendbox_tracking_code = %s",
                    (tracking_code,)
                )
                order = cursor.fetchone()
                
                if not order:
                    logger.warning(f"Order not found for tracking code: {tracking_code}")
                    # Log webhook event even if order not found
                    cursor.execute(
                        """
                        INSERT INTO webhook_events
                            (event_type, sendbox_tracking_code, payload, processed, error_message)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            event_type,
                            tracking_code,
                            json.dumps(payload),
                            False,
                            "Order not found"
                        )
                    )
                    conn.commit()
                    
                    return jsonify({
                        "status": "error",
                        "message": "Order not found for tracking code"
                    }), 404
                
                order_id = order["id"]
                
                # Map Sendbox status to internal statuses
                if sendbox_status:
                    order_status, delivery_status = map_sendbox_status_to_internal(sendbox_status)
                else:
                    # Keep existing statuses if no status in webhook
                    order_status = order["order_status"]
                    delivery_status = order["delivery_status"]
                
                # Update order with webhook data
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
                        sendbox_status or order.get("sendbox_status"),
                        order_status,
                        delivery_status,
                        json.dumps(payload),
                        order_id
                    )
                )
                
                # Log webhook event
                cursor.execute(
                    """
                    INSERT INTO webhook_events
                        (event_type, order_id, sendbox_tracking_code, payload, processed, processed_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        event_type,
                        order_id,
                        tracking_code,
                        json.dumps(payload),
                        True,
                        datetime.now()
                    )
                )
                
                conn.commit()
                
                logger.info(f"Webhook processed successfully for order {order_id}: {sendbox_status}")
                
                # TODO: Send customer notification (email/SMS) about status update
                
                return jsonify({
                    "status": "success",
                    "message": "Webhook processed successfully",
                    "data": {
                        "order_id": order_id,
                        "tracking_code": tracking_code,
                        "status": sendbox_status,
                        "order_status": order_status,
                        "delivery_status": delivery_status
                    }
                }), 200
                
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        
        # Try to log the failed webhook
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO webhook_events
                        (event_type, payload, processed, error_message)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        "error",
                        json.dumps(request.get_json() or {}),
                        False,
                        str(e)
                    )
                )
                conn.commit()
            conn.close()
        except:
            pass
        
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@webhooks_bp.route("/api/webhooks/test", methods=["POST"])
def test_webhook():
    """Test endpoint to verify webhook configuration."""
    payload = request.get_json()
    logger.info(f"Test webhook received: {payload}")
    
    return jsonify({
        "status": "success",
        "message": "Test webhook received",
        "received_data": payload
    }), 200



# ──────────────────────────────────────────────
# TERMINAL AFRICA WEBHOOKS (PHASE 6)
# ──────────────────────────────────────────────

@webhooks_bp.route("/api/webhooks/terminal", methods=["POST"])
def terminal_webhook():
    """
    Handle incoming webhooks from Terminal Africa.
    
    Terminal sends webhooks for tracking updates with payload like:
    {
        "event": "shipment.tracking.updated",
        "shipment_id": "SH-ABC123",
        "tracking_number": "TN123456789",
        "status": "in_transit",
        "timestamp": "2026-05-04T10:30:00Z",
        "data": { ... }
    }
    """
    try:
        # Get webhook payload
        payload = request.get_json()
        
        if not payload:
            logger.warning("Received empty Terminal webhook payload")
            return jsonify({"status": "error", "message": "Empty payload"}), 400
        
        logger.info(f"Received Terminal webhook: {payload.get('event', 'unknown')}")
        
        # Extract key fields
        event_type = payload.get("event", "unknown")
        shipment_id = payload.get("shipment_id") or payload.get("id")
        tracking_number = payload.get("tracking_number")
        status = payload.get("status")
        
        if not shipment_id:
            logger.warning("Terminal webhook missing shipment_id")
            return jsonify({"status": "error", "message": "Missing shipment_id"}), 400
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Find order by Terminal shipment ID
                cursor.execute(
                    "SELECT id, order_status, delivery_status FROM orders WHERE terminal_shipment_id = %s",
                    (shipment_id,)
                )
                order = cursor.fetchone()
                
                if not order:
                    logger.warning(f"Order not found for Terminal shipment ID: {shipment_id}")
                    # Log webhook event even if order not found
                    cursor.execute(
                        """
                        INSERT INTO webhook_events
                            (event_type, payload, processed, error_message)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            event_type,
                            json.dumps(payload),
                            False,
                            "Order not found"
                        )
                    )
                    conn.commit()
                    
                    return jsonify({
                        "status": "error",
                        "message": "Order not found for shipment ID"
                    }), 404
                
                order_id = order["id"]
                
                # Map Terminal status to internal statuses
                if status:
                    order_status, delivery_status = map_terminal_status_to_internal(status)
                else:
                    # Keep existing statuses if no status in webhook
                    order_status = order["order_status"]
                    delivery_status = order["delivery_status"]
                
                # Update order with webhook data
                cursor.execute(
                    """
                    UPDATE orders
                    SET terminal_status = %s,
                        order_status = %s,
                        delivery_status = %s,
                        terminal_webhook_data = %s
                    WHERE id = %s
                    """,
                    (
                        status,
                        order_status,
                        delivery_status,
                        json.dumps(payload),
                        order_id
                    )
                )
                
                # Log webhook event
                cursor.execute(
                    """
                    INSERT INTO webhook_events
                        (event_type, order_id, payload, processed, processed_at)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        event_type,
                        order_id,
                        json.dumps(payload),
                        True,
                        datetime.now()
                    )
                )
                
                conn.commit()
                
                logger.info(f"Terminal webhook processed successfully for order {order_id}: {status}")
                
                # TODO: Send customer notification (email/SMS) about status update
                
                return jsonify({
                    "status": "success",
                    "message": "Webhook processed successfully",
                    "data": {
                        "order_id": order_id,
                        "shipment_id": shipment_id,
                        "status": status,
                        "order_status": order_status,
                        "delivery_status": delivery_status
                    }
                }), 200
                
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Error processing Terminal webhook: {str(e)}")
        
        # Try to log the failed webhook
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO webhook_events
                        (event_type, payload, processed, error_message)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        "error",
                        json.dumps(request.get_json() or {}),
                        False,
                        str(e)
                    )
                )
                conn.commit()
            conn.close()
        except:
            pass
        
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


def map_terminal_status_to_internal(terminal_status: str) -> tuple:
    """
    Map Terminal Africa status to internal order and delivery statuses.
    
    Args:
        terminal_status: Terminal shipment status
        
    Returns:
        Tuple of (order_status, delivery_status)
    """
    status_map = {
        "pending": ("processing", "Pending"),
        "confirmed": ("processing", "Pending"),
        "in-transit": ("shipped", "in_transit"),
        "in_transit": ("shipped", "in_transit"),
        "out-for-delivery": ("shipped", "in_transit"),
        "delivered": ("delivered", "delivered"),
        "cancelled": ("cancelled", "Pending"),
        "failed": ("processing", "Pending"),
        "returned": ("cancelled", "Pending")
    }
    
    return status_map.get(terminal_status.lower(), ("processing", "Pending"))
