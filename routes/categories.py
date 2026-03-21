from flask import Blueprint, request, jsonify
from db import get_db_connection
from middleware.auth_middleware import admin_required

categories_bp = Blueprint("categories", __name__)


# ──────────────────────────────────────────────
# PUBLIC CATEGORY ROUTES
# ──────────────────────────────────────────────


@categories_bp.route("/api/categories", methods=["GET"])
def get_categories():
    """List all categories with optional product count."""
    try:
        include_count = request.args.get("include_count", "false").lower() == "true"

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                if include_count:
                    cursor.execute("""
                        SELECT c.id, c.category, COUNT(p.id) AS product_count
                        FROM category c
                        LEFT JOIN product p ON p.category = c.category
                        GROUP BY c.id, c.category
                        ORDER BY c.category ASC
                    """)
                else:
                    cursor.execute(
                        "SELECT id, category FROM category ORDER BY category ASC"
                    )
                categories = cursor.fetchall()

            return jsonify({
                "status": "success",
                "data": {"categories": categories, "total": len(categories)},
            }), 200
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@categories_bp.route("/api/categories/<int:category_id>", methods=["GET"])
def get_category(category_id):
    """Get a single category by ID, optionally with product count."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT c.id, c.category, COUNT(p.id) AS product_count
                    FROM category c
                    LEFT JOIN product p ON p.category = c.category
                    WHERE c.id = %s
                    GROUP BY c.id, c.category
                    """,
                    (category_id,),
                )
                category = cursor.fetchone()

            if not category:
                return jsonify({"status": "error", "message": "Category not found"}), 404

            return jsonify({
                "status": "success",
                "data": {"category": category},
            }), 200
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


# ──────────────────────────────────────────────
# ADMIN CATEGORY ROUTES
# ──────────────────────────────────────────────


@categories_bp.route("/api/admin/categories", methods=["POST"])
@admin_required
def create_category(current_admin):
    """Create a new category (admin only)."""
    try:
        data = request.get_json()
        name = data.get("category", "").strip()

        if not name:
            return jsonify({"status": "error", "message": "'category' name is required"}), 400

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Check for duplicate
                cursor.execute(
                    "SELECT id FROM category WHERE category = %s", (name,)
                )
                if cursor.fetchone():
                    return jsonify({"status": "error", "message": "Category already exists"}), 409

                cursor.execute(
                    "INSERT INTO category (category) VALUES (%s)", (name,)
                )
                new_id = cursor.lastrowid

            return jsonify({
                "status": "success",
                "message": "Category created successfully",
                "data": {"category": {"id": new_id, "category": name}},
            }), 201
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@categories_bp.route("/api/admin/categories/<int:category_id>", methods=["PUT"])
@admin_required
def update_category(current_admin, category_id):
    """Update a category name (admin only). Also updates product references."""
    try:
        data = request.get_json()
        new_name = data.get("category", "").strip()

        if not new_name:
            return jsonify({"status": "error", "message": "'category' name is required"}), 400

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Get current category
                cursor.execute(
                    "SELECT id, category FROM category WHERE id = %s", (category_id,)
                )
                existing = cursor.fetchone()
                if not existing:
                    return jsonify({"status": "error", "message": "Category not found"}), 404

                old_name = existing["category"]

                # Check duplicate name
                cursor.execute(
                    "SELECT id FROM category WHERE category = %s AND id != %s",
                    (new_name, category_id),
                )
                if cursor.fetchone():
                    return jsonify({"status": "error", "message": "Category name already in use"}), 409

                # Update category table
                cursor.execute(
                    "UPDATE category SET category = %s WHERE id = %s",
                    (new_name, category_id),
                )

                # Update product references so they stay in sync
                cursor.execute(
                    "UPDATE product SET category = %s WHERE category = %s",
                    (new_name, old_name),
                )
                products_updated = cursor.rowcount

            return jsonify({
                "status": "success",
                "message": f"Category updated. {products_updated} product(s) re-linked.",
                "data": {"category": {"id": category_id, "category": new_name}},
            }), 200
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@categories_bp.route("/api/admin/categories/<int:category_id>", methods=["DELETE"])
@admin_required
def delete_category(current_admin, category_id):
    """Delete a category (admin only). Fails if products still reference it."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, category FROM category WHERE id = %s", (category_id,)
                )
                existing = cursor.fetchone()
                if not existing:
                    return jsonify({"status": "error", "message": "Category not found"}), 404

                # Check for products using this category
                cursor.execute(
                    "SELECT COUNT(*) as count FROM product WHERE category = %s",
                    (existing["category"],),
                )
                count = cursor.fetchone()["count"]
                if count > 0:
                    return jsonify({
                        "status": "error",
                        "message": f"Cannot delete: {count} product(s) still use this category. Reassign them first.",
                    }), 409

                cursor.execute(
                    "DELETE FROM category WHERE id = %s", (category_id,)
                )

            return jsonify({
                "status": "success",
                "message": f"Category '{existing['category']}' deleted successfully",
            }), 200
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500
