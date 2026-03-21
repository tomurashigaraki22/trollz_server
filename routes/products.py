from flask import Blueprint, request, jsonify
from db import get_db_connection
from middleware.auth_middleware import admin_required

products_bp = Blueprint("products", __name__)


# ──────────────────────────────────────────────
# HELPER: serialize a product row
# ──────────────────────────────────────────────

def _serialize_product(row):
    """Convert DB row to a JSON-safe product dict."""
    if row is None:
        return None
    product = dict(row)
    # Convert datetime fields to string
    for key in ("date", "flash_sale_start", "flash_sale_end"):
        if product.get(key):
            product[key] = product[key].strftime("%Y-%m-%d %H:%M:%S")
    # Convert Decimal fields to float
    for key in ("flash_sale_price", "old_price"):
        if product.get(key) is not None:
            product[key] = float(product[key])
    # Convert tinyint booleans
    for key in ("shipped_from_abroad", "is_flash_sale"):
        if product.get(key) is not None:
            product[key] = bool(product[key])
    return product


# ──────────────────────────────────────────────
# PUBLIC PRODUCT ROUTES
# ──────────────────────────────────────────────


@products_bp.route("/api/products", methods=["GET"])
def get_products():
    """
    List products with pagination, sorting, and optional filters.

    Query params:
        page      (int)  – page number, default 1
        limit     (int)  – items per page, default 20 (max 100)
        sort      (str)  – field to sort by (price, date, item), default 'date'
        order     (str)  – asc / desc, default 'desc'
        category  (str)  – filter by category name
        supplier  (str)  – filter by supplier
        min_price (int)  – minimum price
        max_price (int)  – maximum price
    """
    try:
        # Pagination
        page = max(int(request.args.get("page", 1)), 1)
        limit = min(max(int(request.args.get("limit", 20)), 1), 100)
        offset = (page - 1) * limit

        # Sorting
        allowed_sort = {"price", "date", "item", "id", "discount"}
        sort = request.args.get("sort", "date")
        if sort not in allowed_sort:
            sort = "date"
        order = request.args.get("order", "desc").upper()
        if order not in ("ASC", "DESC"):
            order = "DESC"

        # Filters
        filters = []
        params = []

        category = request.args.get("category", "").strip()
        if category:
            filters.append("p.category = %s")
            params.append(category)

        supplier = request.args.get("supplier", "").strip()
        if supplier:
            filters.append("p.supplier = %s")
            params.append(supplier)

        min_price = request.args.get("min_price")
        if min_price is not None and min_price != "":
            filters.append("p.price >= %s")
            params.append(int(min_price))

        max_price = request.args.get("max_price")
        if max_price is not None and max_price != "":
            filters.append("p.price <= %s")
            params.append(int(max_price))

        where_clause = ""
        if filters:
            where_clause = "WHERE " + " AND ".join(filters)

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Total count
                cursor.execute(
                    f"SELECT COUNT(*) as total FROM product p {where_clause}",
                    params,
                )
                total = cursor.fetchone()["total"]

                # Fetch products
                cursor.execute(
                    f"""
                    SELECT p.* FROM product p
                    {where_clause}
                    ORDER BY p.`{sort}` {order}
                    LIMIT %s OFFSET %s
                    """,
                    params + [limit, offset],
                )
                rows = cursor.fetchall()

            products = [_serialize_product(r) for r in rows]
            total_pages = (total + limit - 1) // limit  # ceil division

            return jsonify({
                "status": "success",
                "data": {
                    "products": products,
                    "pagination": {
                        "page": page,
                        "limit": limit,
                        "total": total,
                        "total_pages": total_pages,
                    },
                },
            }), 200
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@products_bp.route("/api/products/search", methods=["GET"])
def search_products():
    """
    Search products by name/item or description.

    Query params:
        q     (str) – search query  (required)
        page  (int) – default 1
        limit (int) – default 20
    """
    try:
        q = request.args.get("q", "").strip()
        if not q:
            return jsonify({"status": "error", "message": "Search query 'q' is required"}), 400

        page = max(int(request.args.get("page", 1)), 1)
        limit = min(max(int(request.args.get("limit", 20)), 1), 100)
        offset = (page - 1) * limit

        like = f"%{q}%"

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) as total FROM product WHERE item LIKE %s OR description LIKE %s",
                    (like, like),
                )
                total = cursor.fetchone()["total"]

                cursor.execute(
                    """
                    SELECT * FROM product
                    WHERE item LIKE %s OR description LIKE %s
                    ORDER BY `date` DESC
                    LIMIT %s OFFSET %s
                    """,
                    (like, like, limit, offset),
                )
                rows = cursor.fetchall()

            products = [_serialize_product(r) for r in rows]
            total_pages = (total + limit - 1) // limit

            return jsonify({
                "status": "success",
                "data": {
                    "products": products,
                    "pagination": {
                        "page": page,
                        "limit": limit,
                        "total": total,
                        "total_pages": total_pages,
                    },
                },
            }), 200
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@products_bp.route("/api/products/flash-sales", methods=["GET"])
def get_flash_sales():
    """Get products currently on flash sale."""
    try:
        page = max(int(request.args.get("page", 1)), 1)
        limit = min(max(int(request.args.get("limit", 20)), 1), 100)
        offset = (page - 1) * limit

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) as total FROM product WHERE is_flash_sale = 1"
                )
                total = cursor.fetchone()["total"]

                cursor.execute(
                    """
                    SELECT * FROM product
                    WHERE is_flash_sale = 1
                    ORDER BY flash_sale_end DESC
                    LIMIT %s OFFSET %s
                    """,
                    (limit, offset),
                )
                rows = cursor.fetchall()

            products = [_serialize_product(r) for r in rows]
            total_pages = (total + limit - 1) // limit

            return jsonify({
                "status": "success",
                "data": {
                    "products": products,
                    "pagination": {
                        "page": page,
                        "limit": limit,
                        "total": total,
                        "total_pages": total_pages,
                    },
                },
            }), 200
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@products_bp.route("/api/products/new-arrivals", methods=["GET"])
def get_new_arrivals():
    """Get products marked as new arrivals."""
    try:
        page = max(int(request.args.get("page", 1)), 1)
        limit = min(max(int(request.args.get("limit", 20)), 1), 100)
        offset = (page - 1) * limit

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) as total FROM product WHERE `new` = 'Yes'"
                )
                total = cursor.fetchone()["total"]

                cursor.execute(
                    """
                    SELECT * FROM product
                    WHERE `new` = 'Yes'
                    ORDER BY `date` DESC
                    LIMIT %s OFFSET %s
                    """,
                    (limit, offset),
                )
                rows = cursor.fetchall()

            products = [_serialize_product(r) for r in rows]
            total_pages = (total + limit - 1) // limit

            return jsonify({
                "status": "success",
                "data": {
                    "products": products,
                    "pagination": {
                        "page": page,
                        "limit": limit,
                        "total": total,
                        "total_pages": total_pages,
                    },
                },
            }), 200
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@products_bp.route("/api/products/category/<string:category>", methods=["GET"])
def get_products_by_category(category):
    """Get products filtered by category name."""
    try:
        page = max(int(request.args.get("page", 1)), 1)
        limit = min(max(int(request.args.get("limit", 20)), 1), 100)
        offset = (page - 1) * limit

        sort = request.args.get("sort", "date")
        if sort not in ("price", "date", "item", "id", "discount"):
            sort = "date"
        order = request.args.get("order", "desc").upper()
        if order not in ("ASC", "DESC"):
            order = "DESC"

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) as total FROM product WHERE category = %s",
                    (category,),
                )
                total = cursor.fetchone()["total"]

                cursor.execute(
                    f"""
                    SELECT * FROM product
                    WHERE category = %s
                    ORDER BY `{sort}` {order}
                    LIMIT %s OFFSET %s
                    """,
                    (category, limit, offset),
                )
                rows = cursor.fetchall()

            products = [_serialize_product(r) for r in rows]
            total_pages = (total + limit - 1) // limit

            return jsonify({
                "status": "success",
                "data": {
                    "category": category,
                    "products": products,
                    "pagination": {
                        "page": page,
                        "limit": limit,
                        "total": total,
                        "total_pages": total_pages,
                    },
                },
            }), 200
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@products_bp.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Get a single product by ID."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM product WHERE id = %s", (product_id,))
                row = cursor.fetchone()

            if not row:
                return jsonify({"status": "error", "message": "Product not found"}), 404

            return jsonify({
                "status": "success",
                "data": {"product": _serialize_product(row)},
            }), 200
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


# ──────────────────────────────────────────────
# ADMIN PRODUCT ROUTES
# ──────────────────────────────────────────────


@products_bp.route("/api/admin/products", methods=["POST"])
@admin_required
def create_product(current_admin):
    """Create a new product (admin only)."""
    try:
        data = request.get_json()

        required = ["item", "category", "price", "discount", "supplier", "img", "qty"]
        for field in required:
            if field not in data or data[field] is None:
                return jsonify({"status": "error", "message": f"'{field}' is required"}), 400

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO product
                        (item, category, price, discount, description, supplier,
                         `new`, img, qty, shipped_from_abroad,
                         is_flash_sale, flash_sale_price, flash_sale_start, flash_sale_end, old_price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        data["item"],
                        data["category"],
                        int(data["price"]),
                        int(data["discount"]),
                        data.get("description", ""),
                        data["supplier"],
                        data.get("new", "Yes"),
                        data["img"],
                        int(data["qty"]),
                        int(data.get("shipped_from_abroad", 0)),
                        int(data.get("is_flash_sale", 0)),
                        data.get("flash_sale_price"),
                        data.get("flash_sale_start"),
                        data.get("flash_sale_end"),
                        data.get("old_price"),
                    ),
                )
                new_id = cursor.lastrowid

                cursor.execute("SELECT * FROM product WHERE id = %s", (new_id,))
                product = cursor.fetchone()

            return jsonify({
                "status": "success",
                "message": "Product created successfully",
                "data": {"product": _serialize_product(product)},
            }), 201
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@products_bp.route("/api/admin/products/<int:product_id>", methods=["PUT"])
@admin_required
def update_product(current_admin, product_id):
    """Update an existing product (admin only)."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Check product exists
                cursor.execute("SELECT id FROM product WHERE id = %s", (product_id,))
                if not cursor.fetchone():
                    return jsonify({"status": "error", "message": "Product not found"}), 404

                # Build dynamic UPDATE query from provided fields
                updatable = {
                    "item": str,
                    "category": str,
                    "price": int,
                    "discount": int,
                    "description": str,
                    "supplier": str,
                    "new": str,
                    "img": str,
                    "qty": int,
                    "shipped_from_abroad": int,
                    "is_flash_sale": int,
                    "flash_sale_price": lambda v: float(v) if v is not None else None,
                    "flash_sale_start": str,
                    "flash_sale_end": str,
                    "old_price": lambda v: float(v) if v is not None else None,
                }

                set_parts = []
                values = []
                for field, cast_fn in updatable.items():
                    if field in data:
                        col = f"`{field}`" if field in ("new",) else field
                        set_parts.append(f"{col} = %s")
                        val = data[field]
                        if val is not None and callable(cast_fn):
                            val = cast_fn(val)
                        values.append(val)

                if not set_parts:
                    return jsonify({"status": "error", "message": "No valid fields to update"}), 400

                values.append(product_id)
                cursor.execute(
                    f"UPDATE product SET {', '.join(set_parts)} WHERE id = %s",
                    values,
                )

                cursor.execute("SELECT * FROM product WHERE id = %s", (product_id,))
                product = cursor.fetchone()

            return jsonify({
                "status": "success",
                "message": "Product updated successfully",
                "data": {"product": _serialize_product(product)},
            }), 200
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@products_bp.route("/api/admin/products/<int:product_id>", methods=["DELETE"])
@admin_required
def delete_product(current_admin, product_id):
    """Delete a product (admin only)."""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, item FROM product WHERE id = %s", (product_id,))
                product = cursor.fetchone()
                if not product:
                    return jsonify({"status": "error", "message": "Product not found"}), 404

                # Remove related cart entries
                cursor.execute("DELETE FROM cart WHERE pid = %s", (product_id,))
                # Remove related media
                cursor.execute("DELETE FROM media WHERE pid = %s", (product_id,))
                # Delete product
                cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))

            return jsonify({
                "status": "success",
                "message": f"Product '{product['item']}' deleted successfully",
            }), 200
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500
