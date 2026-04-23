"""
Address Management Routes
Handles CRUD operations for user shipping addresses.
"""

from flask import Blueprint, request, jsonify
from db import get_db_connection
from middleware.auth_middleware import token_required
from services.address_validator import validate_address, format_phone_number, get_state_code

addresses_bp = Blueprint("addresses", __name__)


def _serialize_address(row):
    """Convert DB row to JSON-safe address dict."""
    if row is None:
        return None
    address = dict(row)
    # Convert datetime fields to string
    for key in ("created_at", "updated_at"):
        if address.get(key):
            address[key] = address[key].strftime("%Y-%m-%d %H:%M:%S")
    # Convert boolean
    if address.get("is_default") is not None:
        address["is_default"] = bool(address["is_default"])
    # Convert decimal to float
    if address.get("lng") is not None:
        address["lng"] = float(address["lng"]) if address["lng"] else None
    if address.get("lat") is not None:
        address["lat"] = float(address["lat"]) if address["lat"] else None
    return address


# ──────────────────────────────────────────────
# ADDRESS CRUD OPERATIONS
# ──────────────────────────────────────────────

@addresses_bp.route("/api/addresses", methods=["POST"])
@token_required
def create_address(current_user):
    """
    Create a new shipping address for the current user.
    
    Expected JSON body:
    {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+234 800 123 4567",
        "email": "john@example.com",
        "street": "123 Main Street",
        "street_line_2": "Apt 4B",
        "city": "Lagos",
        "state": "Lagos",
        "country": "NG",
        "post_code": "100001",
        "is_default": false
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ["first_name", "last_name", "phone", "street", "city", "state"]
        for field in required:
            if field not in data or not data[field]:
                return jsonify({
                    "status": "error",
                    "message": f"'{field}' is required"
                }), 400
        
        # Format phone number
        phone = format_phone_number(data["phone"])
        
        # Prepare address data
        address_data = {
            "first_name": data["first_name"].strip(),
            "last_name": data["last_name"].strip(),
            "phone": phone,
            "email": data.get("email", "").strip() or None,
            "street": data["street"].strip(),
            "street_line_2": data.get("street_line_2", "").strip() or None,
            "city": data["city"].strip(),
            "state": data["state"].strip(),
            "country": data.get("country", "NG").upper().strip(),
            "post_code": data.get("post_code", "").strip() or None,
            "lng": data.get("lng"),
            "lat": data.get("lat"),
            "name": None
        }
        
        # Validate address
        is_valid, error = validate_address(address_data)
        if not is_valid:
            return jsonify({
                "status": "error",
                "message": f"Invalid address: {error}"
            }), 400
        
        is_default = data.get("is_default", False)
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # If this is set as default, unset other defaults
                if is_default:
                    cursor.execute(
                        "UPDATE shipping_addresses SET is_default = FALSE WHERE user_id = %s",
                        (current_user["id"],)
                    )
                
                # Insert new address
                cursor.execute(
                    """
                    INSERT INTO shipping_addresses
                        (user_id, first_name, last_name, phone, email, street, street_line_2,
                         city, state, country, post_code, lng, lat, is_default)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        current_user["id"],
                        address_data["first_name"],
                        address_data["last_name"],
                        address_data["phone"],
                        address_data["email"],
                        address_data["street"],
                        address_data["street_line_2"],
                        address_data["city"],
                        address_data["state"],
                        address_data["country"],
                        address_data["post_code"],
                        address_data["lng"],
                        address_data["lat"],
                        is_default
                    )
                )
                address_id = cursor.lastrowid
                
                # Fetch created address
                cursor.execute(
                    "SELECT * FROM shipping_addresses WHERE id = %s",
                    (address_id,)
                )
                address = cursor.fetchone()
                
                conn.commit()
                
                return jsonify({
                    "status": "success",
                    "message": "Address created successfully",
                    "data": {"address": _serialize_address(address)}
                }), 201
                
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@addresses_bp.route("/api/addresses", methods=["GET"])
@token_required
def get_addresses(current_user):
    """Get all shipping addresses for the current user."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM shipping_addresses
                    WHERE user_id = %s
                    ORDER BY is_default DESC, created_at DESC
                    """,
                    (current_user["id"],)
                )
                addresses = cursor.fetchall()
                
                return jsonify({
                    "status": "success",
                    "data": {
                        "addresses": [_serialize_address(addr) for addr in addresses],
                        "count": len(addresses)
                    }
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@addresses_bp.route("/api/addresses/<int:address_id>", methods=["GET"])
@token_required
def get_address(current_user, address_id):
    """Get a specific shipping address."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM shipping_addresses
                    WHERE id = %s AND user_id = %s
                    """,
                    (address_id, current_user["id"])
                )
                address = cursor.fetchone()
                
                if not address:
                    return jsonify({
                        "status": "error",
                        "message": "Address not found"
                    }), 404
                
                return jsonify({
                    "status": "success",
                    "data": {"address": _serialize_address(address)}
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@addresses_bp.route("/api/addresses/<int:address_id>", methods=["PUT"])
@token_required
def update_address(current_user, address_id):
    """Update a shipping address."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Check address exists and belongs to user
                cursor.execute(
                    "SELECT id FROM shipping_addresses WHERE id = %s AND user_id = %s",
                    (address_id, current_user["id"])
                )
                if not cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "message": "Address not found"
                    }), 404
                
                # Build update query
                updatable = [
                    "first_name", "last_name", "phone", "email", "street",
                    "street_line_2", "city", "state", "country", "post_code",
                    "lng", "lat"
                ]
                set_parts = []
                values = []
                
                for field in updatable:
                    if field in data:
                        value = data[field]
                        # Format phone if provided
                        if field == "phone" and value:
                            value = format_phone_number(value)
                        # Strip strings
                        if isinstance(value, str):
                            value = value.strip() or None
                        set_parts.append(f"{field} = %s")
                        values.append(value)
                
                if not set_parts:
                    return jsonify({
                        "status": "error",
                        "message": "No valid fields to update"
                    }), 400
                
                values.append(address_id)
                cursor.execute(
                    f"UPDATE shipping_addresses SET {', '.join(set_parts)} WHERE id = %s",
                    values
                )
                
                # Fetch updated address
                cursor.execute(
                    "SELECT * FROM shipping_addresses WHERE id = %s",
                    (address_id,)
                )
                address = cursor.fetchone()
                
                # Validate updated address
                address_dict = _serialize_address(address)
                is_valid, error = validate_address(address_dict)
                if not is_valid:
                    conn.rollback()
                    return jsonify({
                        "status": "error",
                        "message": f"Invalid address after update: {error}"
                    }), 400
                
                conn.commit()
                
                return jsonify({
                    "status": "success",
                    "message": "Address updated successfully",
                    "data": {"address": address_dict}
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@addresses_bp.route("/api/addresses/<int:address_id>", methods=["DELETE"])
@token_required
def delete_address(current_user, address_id):
    """Delete a shipping address."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Check address exists and belongs to user
                cursor.execute(
                    "SELECT id, is_default FROM shipping_addresses WHERE id = %s AND user_id = %s",
                    (address_id, current_user["id"])
                )
                address = cursor.fetchone()
                
                if not address:
                    return jsonify({
                        "status": "error",
                        "message": "Address not found"
                    }), 404
                
                # Delete address
                cursor.execute(
                    "DELETE FROM shipping_addresses WHERE id = %s",
                    (address_id,)
                )
                
                # If deleted address was default, set another as default
                if address["is_default"]:
                    cursor.execute(
                        """
                        UPDATE shipping_addresses
                        SET is_default = TRUE
                        WHERE user_id = %s
                        ORDER BY created_at DESC
                        LIMIT 1
                        """,
                        (current_user["id"],)
                    )
                
                conn.commit()
                
                return jsonify({
                    "status": "success",
                    "message": "Address deleted successfully"
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@addresses_bp.route("/api/addresses/<int:address_id>/set-default", methods=["POST"])
@token_required
def set_default_address(current_user, address_id):
    """Set an address as the default shipping address."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Check address exists and belongs to user
                cursor.execute(
                    "SELECT id FROM shipping_addresses WHERE id = %s AND user_id = %s",
                    (address_id, current_user["id"])
                )
                if not cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "message": "Address not found"
                    }), 404
                
                # Unset all defaults for this user
                cursor.execute(
                    "UPDATE shipping_addresses SET is_default = FALSE WHERE user_id = %s",
                    (current_user["id"],)
                )
                
                # Set this address as default
                cursor.execute(
                    "UPDATE shipping_addresses SET is_default = TRUE WHERE id = %s",
                    (address_id,)
                )
                
                # Fetch updated address
                cursor.execute(
                    "SELECT * FROM shipping_addresses WHERE id = %s",
                    (address_id,)
                )
                address = cursor.fetchone()
                
                conn.commit()
                
                return jsonify({
                    "status": "success",
                    "message": "Default address updated successfully",
                    "data": {"address": _serialize_address(address)}
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@addresses_bp.route("/api/addresses/default", methods=["GET"])
@token_required
def get_default_address(current_user):
    """Get the default shipping address for the current user."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM shipping_addresses
                    WHERE user_id = %s AND is_default = TRUE
                    LIMIT 1
                    """,
                    (current_user["id"],)
                )
                address = cursor.fetchone()
                
                if not address:
                    return jsonify({
                        "status": "error",
                        "message": "No default address found"
                    }), 404
                
                return jsonify({
                    "status": "success",
                    "data": {"address": _serialize_address(address)}
                }), 200
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500
