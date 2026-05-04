from functools import wraps
from flask import request, jsonify
import jwt
from config import Config


def token_required(f):
    """Decorator to protect routes that require user authentication."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from Authorization header
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"status": "error", "message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
            
            # Handle both user and admin tokens
            user_type = data.get("type", "user")
            
            if user_type == "admin":
                # Admin tokens have username, not email
                current_user = {
                    "id": data["user_id"],
                    "username": data.get("username", ""),
                    "email": data.get("email", ""),  # May not exist for admin
                    "type": "admin",
                    "role": data.get("role", "admin"),
                }
            else:
                # User tokens have email
                current_user = {
                    "id": data["user_id"],
                    "email": data.get("email", ""),
                    "username": data.get("username", ""),  # May not exist for user
                    "type": data.get("type", "user"),
                }
        except jwt.ExpiredSignatureError:
            return (
                jsonify({"status": "error", "message": "Token has expired"}),
                401,
            )
        except jwt.InvalidTokenError:
            return (
                jsonify({"status": "error", "message": "Token is invalid"}),
                401,
            )

        return f(current_user, *args, **kwargs)

    return decorated


def admin_required(f):
    """Decorator to protect routes that require admin authentication."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"status": "error", "message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
            if data.get("type") != "admin":
                return (
                    jsonify(
                        {"status": "error", "message": "Admin access required"}
                    ),
                    403,
                )
            current_admin = {
                "id": data["user_id"],
                "username": data.get("username", ""),
                "role": data.get("role", "admin"),
                "type": "admin",
            }
        except jwt.ExpiredSignatureError:
            return (
                jsonify({"status": "error", "message": "Token has expired"}),
                401,
            )
        except jwt.InvalidTokenError:
            return (
                jsonify({"status": "error", "message": "Token is invalid"}),
                401,
            )

        return f(current_admin, *args, **kwargs)

    return decorated
