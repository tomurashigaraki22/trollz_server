"""
Address Management Routes
Handles CRUD operations for user shipping addresses with Terminal Africa integration.
"""

from flask import Blueprint, request, jsonify
from db import get_db_connection
from middleware.auth_middleware import token_required
from services.address_validator import validate_address, format_phone_number, get_state_code
from services.terminal_address_manager import get_address_manager
from services.terminal_service import TerminalAPIError
import logging

addresses_bp = Blueprint("addresses", __name__)
logger = logging.getLogger(__name__)


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
    Create a new shipping address for the current user and sync to Terminal Africa.
    
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
            "email": data.get("email", "").strip() or current_user.get("email", ""),
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
                
                # Sync to Terminal Africa
                terminal_address_id = None
                terminal_sync_error = None
                
                try:
                    address_mgr = get_address_manager()
                    result = address_mgr.create_and_sync_address(
                        user_id=current_user["id"],
                        first_name=address_data["first_name"],
                        last_name=address_data["last_name"],
                        phone=address_data["phone"],
                        email=address_data["email"],
                        line1=address_data["street"],
                        line2=address_data["street_line_2"],
                        city=address_data["city"],
                        state=address_data["state"],
                        country=address_data["country"],
                        zip_code=address_data["post_code"],
                        is_residential=True
                    )
                    terminal_address_id = result.get("terminal_address_id")
                    
                    # Store terminal_address_id in shipping_addresses table
                    if terminal_address_id:
                        cursor.execute(
                            "UPDATE shipping_addresses SET terminal_address_id = %s WHERE id = %s",
                            (terminal_address_id, address_id)
                        )
                        logger.info(f"Address synced to Terminal: {terminal_address_id}")
                except TerminalAPIError as e:
                    terminal_sync_error = str(e)
                    logger.warning(f"Failed to sync address to Terminal: {e.message}")
                except Exception as e:
                    terminal_sync_error = str(e)
                    logger.warning(f"Failed to sync address to Terminal: {str(e)}")
                
                # Fetch created address
                cursor.execute(
                    "SELECT * FROM shipping_addresses WHERE id = %s",
                    (address_id,)
                )
                address = cursor.fetchone()
                
                conn.commit()
                
                response_data = {
                    "address": _serialize_address(address),
                    "terminal_synced": terminal_address_id is not None,
                }
                
                if terminal_address_id:
                    response_data["terminal_address_id"] = terminal_address_id
                
                if terminal_sync_error:
                    response_data["terminal_sync_warning"] = terminal_sync_error
                
                return jsonify({
                    "status": "success",
                    "message": "Address created successfully",
                    "data": response_data
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
    """Get all shipping addresses for the current user with Terminal sync status."""
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
                
                # Serialize addresses and add Terminal sync status
                serialized_addresses = []
                for addr in addresses:
                    serialized = _serialize_address(addr)
                    
                    # Check if address is synced to Terminal (has terminal_address_id)
                    terminal_address_id = addr.get('terminal_address_id')
                    serialized['terminal_synced'] = terminal_address_id is not None
                    if terminal_address_id:
                        serialized['terminal_address_id'] = terminal_address_id
                    
                    serialized_addresses.append(serialized)
                
                # Count synced addresses
                terminal_count = sum(1 for addr in addresses if addr.get('terminal_address_id'))
                
                return jsonify({
                    "status": "success",
                    "data": {
                        "addresses": serialized_addresses,
                        "count": len(addresses),
                        "terminal_count": terminal_count
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


@addresses_bp.route("/api/addresses/validate", methods=["POST"])
def validate_address_endpoint():
    """
    Validate an address without saving it.
    
    Expected JSON body:
    {
        "address": "123 Main Street",
        "city": "Lagos",
        "state": "Lagos",
        "country": "NG"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        # Validate required fields
        required = ["address", "city", "state"]
        for field in required:
            if field not in data or not data[field]:
                return jsonify({
                    "status": "error",
                    "message": f"'{field}' is required"
                }), 400
        
        # Prepare address data for validation
        address_data = {
            "street": data["address"].strip(),
            "city": data["city"].strip(),
            "state": data["state"].strip(),
            "country": data.get("country", "NG").upper().strip(),
            "post_code": data.get("postal_code") or data.get("post_code"),
            "first_name": "Test",
            "last_name": "User",
            "phone": "+2348000000000"
        }
        
        # Validate address
        is_valid, error = validate_address(address_data)
        
        if is_valid:
            return jsonify({
                "status": "success",
                "data": {
                    "valid": True,
                    "message": "Address is valid",
                    "address": {
                        "street": address_data["street"],
                        "city": address_data["city"],
                        "state": address_data["state"],
                        "country": address_data["country"]
                    }
                }
            }), 200
        else:
            return jsonify({
                "status": "success",
                "data": {
                    "valid": False,
                    "message": error,
                    "errors": [error]
                }
            }), 200
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@addresses_bp.route("/api/addresses/terminal", methods=["GET"])
@token_required
def get_terminal_addresses(current_user):
    """Get all Terminal Africa addresses for the current user."""
    try:
        address_mgr = get_address_manager()
        terminal_addresses = address_mgr.get_user_addresses(current_user["id"])
        
        return jsonify({
            "status": "success",
            "data": {
                "addresses": terminal_addresses,
                "count": len(terminal_addresses)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500


@addresses_bp.route("/api/addresses/<int:address_id>/sync-terminal", methods=["POST"])
@token_required
def sync_address_to_terminal(current_user, address_id):
    """Sync an existing address to Terminal Africa."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Get the address
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
                
                # Sync to Terminal
                try:
                    address_mgr = get_address_manager()
                    result = address_mgr.create_and_sync_address(
                        user_id=current_user["id"],
                        first_name=address["first_name"],
                        last_name=address["last_name"],
                        phone=address["phone"],
                        email=address["email"] or current_user.get("email", ""),
                        line1=address["street"],
                        line2=address["street_line_2"],
                        city=address["city"],
                        state=address["state"],
                        country=address["country"],
                        zip_code=address["post_code"],
                        is_residential=True
                    )
                    
                    terminal_address_id = result.get("terminal_address_id")
                    
                    # Store terminal_address_id in shipping_addresses table
                    if terminal_address_id:
                        cursor.execute(
                            "UPDATE shipping_addresses SET terminal_address_id = %s WHERE id = %s",
                            (terminal_address_id, address_id)
                        )
                        conn.commit()
                    
                    return jsonify({
                        "status": "success",
                        "message": "Address synced to Terminal Africa successfully",
                        "data": {
                            "terminal_address_id": terminal_address_id,
                            "local_address_id": result.get("local_address_id")
                        }
                    }), 200
                    
                except TerminalAPIError as e:
                    return jsonify({
                        "status": "error",
                        "message": f"Terminal API error: {e.message}"
                    }), 400
                    
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500
