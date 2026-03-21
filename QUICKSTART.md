# Trollz Store API - Quick Start Guide

## ✅ Database Migration Complete!

Your Trollz Store API has been successfully migrated to use the `trollzstorecom_tr0llz_db` database structure.

### What Changed

1. **Database Name**: Changed from `trollz_db` to `trollzstorecom_tr0llz_db`
2. **Data Imported**: 714 products, 17 categories, 3 orders, 9 cart items
3. **Schema Updated**: All routes now use the complete database structure from the SQL file

### Current Database Status

```
✓ Database: trollzstorecom_tr0llz_db
✓ Products: 714 items
✓ Categories: 17 categories
✓ Orders: 3 orders
✓ Cart Items: 9 items
```

## 🚀 Running the Application

### Start the Server

```bash
python app.py
```

The server will start on `http://0.0.0.0:4500`

### Test the API

1. **Health Check**:
```bash
curl http://localhost:4500/
```

2. **Get Products**:
```bash
curl http://localhost:4500/api/products?limit=5
```

3. **Get Categories**:
```bash
curl http://localhost:4500/api/categories
```

4. **Search Products**:
```bash
curl http://localhost:4500/api/products/search?q=phone
```

## 📊 Sample API Responses

### Products Endpoint
```json
{
  "status": "success",
  "data": {
    "products": [
      {
        "id": 1280,
        "item": "Lovely Triben Ladies Handbag- Black",
        "category": "Fashion",
        "price": 14500,
        "discount": 10,
        "description": "...",
        "supplier": "Trollz Store",
        "img": "[\"https://...\"]",
        "qty": 100,
        "date": "2025-06-26 01:30:27"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 5,
      "total": 714,
      "total_pages": 143
    }
  }
}
```

### Categories Endpoint
```json
{
  "status": "success",
  "data": {
    "categories": [
      {
        "id": 1,
        "category": "Computing"
      },
      {
        "id": 3,
        "category": "Health & Beauty"
      },
      {
        "id": 4,
        "category": "Phones & Tablets"
      }
    ],
    "total": 17
  }
}
```

## 🔧 Troubleshooting

### If Products Show Empty

Run the import script to reload data:
```bash
python import_sql.py
```

### Check Database Connection

```bash
python -c "from db import get_db_connection; conn = get_db_connection(); print('✓ Connected'); conn.close()"
```

### Verify Data

Create a test script:
```python
from db import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) as count FROM product')
print(f"Products: {cursor.fetchone()['count']}")
conn.close()
```

## 📁 Project Structure

```
trollz_server/
├── app.py                          # Main Flask application
├── config.py                       # Configuration (updated with new DB name)
├── db.py                          # Database connection & initialization
├── import_sql.py                  # SQL import utility
├── trollzstorecom_tr0llz_db.sql  # Complete database dump
├── requirements.txt               # Python dependencies
├── routes/
│   ├── auth.py                   # Authentication endpoints
│   ├── products.py               # Product management endpoints
│   └── categories.py             # Category management endpoints
└── middleware/
    └── auth_middleware.py        # JWT authentication middleware
```

## 🎯 Next Steps

1. **Test all endpoints** using the examples in README.md
2. **Set up authentication** by creating admin and user accounts
3. **Customize products** using the admin endpoints
4. **Integrate with frontend** using the documented API endpoints

## 📚 Full Documentation

See [README.md](README.md) for complete API documentation including:
- All available endpoints
- Request/response formats
- Authentication details
- Error handling
- Admin operations

## ✨ Features Available

- ✅ Product catalog with 714 items
- ✅ Category management (17 categories)
- ✅ Product search and filtering
- ✅ Flash sales support
- ✅ Shopping cart functionality
- ✅ Order management
- ✅ User authentication
- ✅ Admin panel endpoints
- ✅ Pagination and sorting
- ✅ Size and color variants

---

**Need Help?** Check the README.md or review the route files in the `routes/` directory for detailed implementation examples.
