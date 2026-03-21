from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import datetime
from config import Config
from db import get_db_connection
from middleware.auth_middleware import token_required, admin_required

auth_bp = Blueprint("auth", __name__)


# ──────────────────────────────────────────────
# USER AUTHENTICATION
# ──────────────────────────────────────────────


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    """Register a new user."""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["name", "email", "password"]
        for field in required_fields:
            if not data.get(field):
                return (
                    jsonify(
                        {"status": "error", "message": f"{field} is required"}
                    ),
                    400,
                )

        name = data["name"].strip()
        email = data["email"].strip().lower()
        password = data["password"]
        phone = data.get("phone", "").strip()

        # Validate email format (basic)
        if "@" not in email or "." not in email:
            return (
                jsonify({"status": "error", "message": "Invalid email format"}),
                400,
            )

        # Validate password length
        if len(password) < 6:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Password must be at least 6 characters",
                    }
                ),
                400,
            )

        # Hash password
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Check if email already exists
                cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                if cursor.fetchone():
                    return (
                        jsonify(
                            {
                                "status": "error",
                                "message": "Email already registered",
                            }
                        ),
                        409,
                    )

                # Insert new user
                cursor.execute(
                    """
                    INSERT INTO users (name, email, password, phone, role, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (name, email, hashed_password, phone or None, "Customer", 0),
                )
                user_id = cursor.lastrowid

            # Generate JWT token
            token = jwt.encode(
                {
                    "user_id": user_id,
                    "email": email,
                    "type": "user",
                    "exp": datetime.datetime.utcnow()
                    + datetime.timedelta(hours=Config.JWT_EXPIRATION_HOURS),
                },
                Config.JWT_SECRET,
                algorithm="HS256",
            )

            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "User registered successfully",
                        "data": {
                            "token": token,
                            "user": {
                                "id": user_id,
                                "name": name,
                                "email": email,
                                "phone": phone or None,
                            },
                        },
                    }
                ),
                201,
            )
        finally:
            conn.close()

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"Server error: {str(e)}"}),
            500,
        )


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """Login an existing user."""
    try:
        data = request.get_json()

        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        if not email or not password:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Email and password are required",
                    }
                ),
                400,
            )

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, email, password, phone FROM users WHERE email = %s",
                    (email,),
                )
                user = cursor.fetchone()

                if not user:
                    return (
                        jsonify(
                            {
                                "status": "error",
                                "message": "Invalid email or password",
                            }
                        ),
                        401,
                    )

                # Verify password
                if not bcrypt.checkpw(
                    password.encode("utf-8"), user["password"].encode("utf-8")
                ):
                    return (
                        jsonify(
                            {
                                "status": "error",
                                "message": "Invalid email or password",
                            }
                        ),
                        401,
                    )

                # Generate JWT token
                token = jwt.encode(
                    {
                        "user_id": user["id"],
                        "email": user["email"],
                        "type": "user",
                        "exp": datetime.datetime.utcnow()
                        + datetime.timedelta(hours=Config.JWT_EXPIRATION_HOURS),
                    },
                    Config.JWT_SECRET,
                    algorithm="HS256",
                )

                return (
                    jsonify(
                        {
                            "status": "success",
                            "message": "Login successful",
                            "data": {
                                "token": token,
                                "user": {
                                    "id": user["id"],
                                    "name": user["name"],
                                    "email": user["email"],
                                    "phone": user["phone"],
                                },
                            },
                        }
                    ),
                    200,
                )
        finally:
            conn.close()

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"Server error: {str(e)}"}),
            500,
        )


@auth_bp.route("/api/auth/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    """Get current user profile."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, email, phone, address FROM users WHERE id = %s",
                    (current_user["id"],),
                )
                user = cursor.fetchone()

                if not user:
                    return (
                        jsonify(
                            {"status": "error", "message": "User not found"}
                        ),
                        404,
                    )

                return (
                    jsonify({"status": "success", "data": {"user": user}}),
                    200,
                )
        finally:
            conn.close()

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"Server error: {str(e)}"}),
            500,
        )


@auth_bp.route("/api/auth/profile", methods=["PUT"])
@token_required
def update_profile(current_user):
    """Update current user profile."""
    try:
        data = request.get_json()

        name = data.get("name", "").strip()
        phone = data.get("phone", "").strip()
        address = data.get("address", "").strip()

        if not name:
            return (
                jsonify({"status": "error", "message": "Name is required"}),
                400,
            )

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users SET name = %s, phone = %s, address = %s
                    WHERE id = %s
                    """,
                    (name, phone or None, address or None, current_user["id"]),
                )

                # Fetch updated user
                cursor.execute(
                    "SELECT id, name, email, phone, address FROM users WHERE id = %s",
                    (current_user["id"],),
                )
                user = cursor.fetchone()

                return (
                    jsonify(
                        {
                            "status": "success",
                            "message": "Profile updated successfully",
                            "data": {"user": user},
                        }
                    ),
                    200,
                )
        finally:
            conn.close()

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"Server error: {str(e)}"}),
            500,
        )


@auth_bp.route("/api/auth/change-password", methods=["POST"])
@token_required
def change_password(current_user):
    """Change user password."""
    try:
        data = request.get_json()

        current_password = data.get("current_password", "")
        new_password = data.get("new_password", "")

        if not current_password or not new_password:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Current password and new password are required",
                    }
                ),
                400,
            )

        if len(new_password) < 6:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "New password must be at least 6 characters",
                    }
                ),
                400,
            )

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Get current password hash
                cursor.execute(
                    "SELECT password FROM users WHERE id = %s",
                    (current_user["id"],),
                )
                user = cursor.fetchone()

                if not user:
                    return (
                        jsonify(
                            {"status": "error", "message": "User not found"}
                        ),
                        404,
                    )

                # Verify current password
                if not bcrypt.checkpw(
                    current_password.encode("utf-8"),
                    user["password"].encode("utf-8"),
                ):
                    return (
                        jsonify(
                            {
                                "status": "error",
                                "message": "Current password is incorrect",
                            }
                        ),
                        401,
                    )

                # Hash new password and update
                new_hashed = bcrypt.hashpw(
                    new_password.encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8")

                cursor.execute(
                    "UPDATE users SET password = %s WHERE id = %s",
                    (new_hashed, current_user["id"]),
                )

                return (
                    jsonify(
                        {
                            "status": "success",
                            "message": "Password changed successfully",
                        }
                    ),
                    200,
                )
        finally:
            conn.close()

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"Server error: {str(e)}"}),
            500,
        )


# ──────────────────────────────────────────────
# ADMIN AUTHENTICATION
# ──────────────────────────────────────────────


@auth_bp.route("/api/admin/login", methods=["POST"])
def admin_login():
    """Login as admin."""
    try:
        data = request.get_json()

        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Username and password are required",
                    }
                ),
                400,
            )

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, password, role FROM `admin` WHERE username = %s",
                    (username,),
                )
                admin = cursor.fetchone()

                if not admin:
                    return (
                        jsonify(
                            {
                                "status": "error",
                                "message": "Invalid username or password",
                            }
                        ),
                        401,
                    )

                # Verify password
                if not bcrypt.checkpw(
                    password.encode("utf-8"), admin["password"].encode("utf-8")
                ):
                    return (
                        jsonify(
                            {
                                "status": "error",
                                "message": "Invalid username or password",
                            }
                        ),
                        401,
                    )

                # Generate JWT token
                token = jwt.encode(
                    {
                        "user_id": admin["id"],
                        "username": admin["username"],
                        "role": admin["role"],
                        "type": "admin",
                        "exp": datetime.datetime.utcnow()
                        + datetime.timedelta(hours=Config.JWT_EXPIRATION_HOURS),
                    },
                    Config.JWT_SECRET,
                    algorithm="HS256",
                )

                return (
                    jsonify(
                        {
                            "status": "success",
                            "message": "Admin login successful",
                            "data": {
                                "token": token,
                                "admin": {
                                    "id": admin["id"],
                                    "username": admin["username"],
                                    "role": admin["role"],
                                },
                            },
                        }
                    ),
                    200,
                )
        finally:
            conn.close()

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"Server error: {str(e)}"}),
            500,
        )
