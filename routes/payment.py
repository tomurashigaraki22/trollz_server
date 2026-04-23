"""
Payment Routes
Handles payment-related endpoints including Flutterwave configuration.
"""

from flask import Blueprint, jsonify
from config import Config

payment_bp = Blueprint("payment", __name__, url_prefix="/api/payment")


@payment_bp.route("/config", methods=["GET"])
def get_payment_config():
    """
    Get payment configuration (public keys only).
    
    Returns:
        JSON response with Flutterwave public key
    """
    try:
        # Only return public key, never secret keys
        config = {
            "flutterwave": {
                "public_key": Config.FLUTTERWAVE_PUBLIC_KEY,
                "enabled": bool(Config.FLUTTERWAVE_PUBLIC_KEY)
            }
        }
        
        return jsonify({
            "status": "success",
            "data": config
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to get payment config: {str(e)}"
        }), 500


@payment_bp.route("/flutterwave/public-key", methods=["GET"])
def get_flutterwave_public_key():
    """
    Get Flutterwave public key.
    
    Returns:
        JSON response with public key
    """
    try:
        if not Config.FLUTTERWAVE_PUBLIC_KEY:
            return jsonify({
                "status": "error",
                "message": "Flutterwave public key not configured"
            }), 404
        
        return jsonify({
            "status": "success",
            "data": {
                "public_key": Config.FLUTTERWAVE_PUBLIC_KEY
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to get public key: {str(e)}"
        }), 500
