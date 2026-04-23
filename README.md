# Trollz Store API Documentation

## Overview
The Trollz Store API is a Flask-based e-commerce backend that provides authentication, product management, and category management functionality. The API supports both regular users and admin users with different access levels.

**Base URL**: `http://0.0.0.0:4500`

## Database Setup

### Database Information
- **Database Name**: `trollzstorecom_tr0llz_db`
- **Host**: `57.131.33.181`
- **Port**: `3306`
- **Current Data**: 714 products, 17 categories, 3 orders, 9 cart items

### Initial Setup

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Import Database** (if needed):
```bash
python import_sql.py
```

This will import all data from `trollzstorecom_tr0llz_db.sql` including:
- All product tables with full product catalog
- Category hierarchy
- Order history
- Cart items
- User data structures

3. **Start the Server**:
```bash
python app.py
```

The database will be automatically initialized on first run if tables don't exist.

## Authentication

### JWT Token Usage
All protected routes require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Token Types
- **User Token**: For regular user operations (profile, etc.)
- **Admin Token**: For administrative operations (product/category management)

---

## API Endpoints

### 🔐 Authentication Routes

#### User Registration
```http
POST /api/auth/register
```
**Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "phone": "1234567890"
}
```
**Response:** Returns JWT token and user data

#### User Login
```http
POST /api/auth/login
```
**Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```
**Response:** Returns JWT token and user data

#### Get User Profile
```http
GET /api/auth/profile
```
**Headers:** `Authorization: Bearer <user_token>`
**Response:** Returns current user profile data

#### Update User Profile
```http
PUT /api/auth/profile
```
**Headers:** `Authorization: Bearer <user_token>`
**Body:**
```json
{
  "name": "Updated Name",
  "phone": "9876543210"
}
```

#### Change Password
```http
POST /api/auth/change-password
```
**Headers:** `Authorization: Bearer <user_token>`
**Body:**
```json
{
  "current_password": "oldpassword",
  "new_password": "newpassword123"
}
```

#### Admin Login
```http
POST /api/admin/login
```
**Body:**
```json
{
  "username": "admin",
  "password": "adminpassword"
}
```
**Response:** Returns admin JWT token

---

### 📦 Product Routes

#### Get Products (Public)
```http
GET /api/products
```
**Query Parameters:**
- `page` (int): Page number (default: 1)
- `limit` (int): Items per page (default: 20, max: 100)
- `sort` (string): Sort field - `price`, `date`, `item`, `id`, `discount` (default: `date`)
- `order` (string): Sort order - `asc` or `desc` (default: `desc`)
- `category` (string): Filter by category name
- `supplier` (string): Filter by supplier
- `min_price` (int): Minimum price filter
- `max_price` (int): Maximum price filter

**Example:**
```http
GET /api/products?page=1&limit=10&sort=price&order=asc&category=Electronics&min_price=100&max_price=500
```

#### Search Products
```http
GET /api/products/search?q=<search_term>
```
**Query Parameters:**
- `q` (string): Search query (required)
- `page` (int): Page number (default: 1)
- `limit` (int): Items per page (default: 20)

#### Get Flash Sale Products
```http
GET /api/products/flash-sales
```
**Query Parameters:** `page`, `limit`

#### Get New Arrivals
```http
GET /api/products/new-arrivals
```
**Query Parameters:** `page`, `limit`

#### Get Products by Category
```http
GET /api/products/category/<category_name>
```
**Query Parameters:** `page`, `limit`, `sort`, `order`

#### Get Single Product
```http
GET /api/products/<product_id>
```

#### Create Product (Admin Only)
```http
POST /api/admin/products
```
**Headers:** `Authorization: Bearer <admin_token>`
**Body:**
```json
{
  "item": "Product Name",
  "category": "Electronics",
  "price": 299,
  "discount": 10,
  "description": "Product description",
  "supplier": "Supplier Name",
  "new": "Yes",
  "img": "image_url.jpg",
  "qty": 50,
  "shipped_from_abroad": 0,
  "is_flash_sale": 1,
  "flash_sale_price": 249.99,
  "flash_sale_start": "2026-03-15 10:00:00",
  "flash_sale_end": "2026-03-20 23:59:59",
  "old_price": 349.99
}
```

#### Update Product (Admin Only)
```http
PUT /api/admin/products/<product_id>
```
**Headers:** `Authorization: Bearer <admin_token>`
**Body:** Any subset of the product fields to update

#### Delete Product (Admin Only)
```http
DELETE /api/admin/products/<product_id>
```
**Headers:** `Authorization: Bearer <admin_token>`

---

### 🏷️ Category Routes

#### Get All Categories
```http
GET /api/categories
```
**Query Parameters:**
- `include_count` (boolean): Include product count for each category (default: false)

#### Get Single Category
```http
GET /api/categories/<category_id>
```
**Response:** Includes product count for the category

#### Create Category (Admin Only)
```http
POST /api/admin/categories
```
**Headers:** `Authorization: Bearer <admin_token>`
**Body:**
```json
{
  "category": "New Category Name"
}
```

#### Update Category (Admin Only)
```http
PUT /api/admin/categories/<category_id>
```
**Headers:** `Authorization: Bearer <admin_token>`
**Body:**
```json
{
  "category": "Updated Category Name"
}
```
**Note:** This also updates all product references to maintain consistency

#### Delete Category (Admin Only)
```http
DELETE /api/admin/categories/<category_id>
```
**Headers:** `Authorization: Bearer <admin_token>`
**Note:** Fails if products still reference this category

---

## Response Format

All API responses follow this standard format:

### Success Response
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": {
    // Response data here
  }
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description"
}
```

### Paginated Response
```json
{
  "status": "success",
  "data": {
    "products": [...],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "total_pages": 8
    }
  }
}
```

---

## Product Data Structure

```json
{
  "id": 1,
  "item": "Product Name",
  "category": "Electronics",
  "price": 299,
  "discount": 10,
  "description": "Product description",
  "supplier": "Supplier Name",
  "new": "Yes",
  "img": "image_url.jpg",
  "qty": 50,
  "date": "2026-03-15 10:30:00",
  "shipped_from_abroad": false,
  "is_flash_sale": true,
  "flash_sale_price": 249.99,
  "flash_sale_start": "2026-03-15 10:00:00",
  "flash_sale_end": "2026-03-20 23:59:59",
  "old_price": 349.99
}
```

---

## Error Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (missing/invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `409` - Conflict (duplicate data)
- `500` - Internal Server Error

---

## Configuration

The API uses the following configuration:
- **Host**: `0.0.0.0`
- **Port**: `4500`
- **JWT Expiration**: 72 hours
- **Database**: `trollzstorecom_tr0llz_db` on `57.131.33.181:3306`

Environment variables can override these defaults via `.env` file:
```env
# Database Configuration
DB_HOST=57.131.33.181
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=your_password
DB_NAME=trollzstorecom_tr0llz_db

# JWT Configuration
JWT_SECRET=your_secret_key
JWT_EXPIRATION_HOURS=72

# Flask Configuration
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=4500

# Sendbox API Configuration (for shipping integration)
SENDBOX_API_KEY=your_sendbox_api_key
SENDBOX_ENV=staging  # or 'live' for production

# Warehouse Address Configuration
WAREHOUSE_FIRST_NAME=Trollz Store
WAREHOUSE_LAST_NAME=Warehouse
WAREHOUSE_STREET=10 Warehouse Street
WAREHOUSE_CITY=Ikeja
WAREHOUSE_STATE=Lagos
WAREHOUSE_COUNTRY=NG
WAREHOUSE_POST_CODE=100001
WAREHOUSE_PHONE=+234 800 000 0000
WAREHOUSE_EMAIL=warehouse@trollzstore.com
```

See `.env.example` for a complete template.

---

## Database Schema

The database includes the following main tables:

### Products Table
- Full product catalog with 714 items
- Fields: id, item, category, subcategory, price, discount, description, supplier, img, qty, date
- Flash sale support with time-based pricing
- Size and color options for fashion items
- Stock tracking and view counts

### Categories Table
- 17 product categories
- Hierarchical structure with parent-child relationships
- Custom icons and background colors
- Fields: id, category, parent_id, bg_color, icon, created_at

### Orders Table
- Order tracking with unique tracking numbers
- Payment integration (Flutterwave)
- Delivery status tracking
- Fields: id, user_id, tracking, total_amount, payment_method, transaction_id, payment_status, order_status, delivery_status

### Cart Table
- User shopping carts
- Size and color selection
- Quantity management

### Users Table
- User authentication and profiles
- Password reset functionality
- Address management

---

## Sendbox Shipping Integration

The Trollz Store API includes integration with Sendbox for automated shipping and logistics.

### Features
- Real-time shipping quotes
- Automatic shipment creation
- Live tracking updates
- International shipping with landed cost calculation
- Webhook support for status updates

### Setup

1. **Register for Sendbox API:**
   - Staging: https://developers.staging.sendbox.co/
   - Production: https://developers.sendbox.co/

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your SENDBOX_API_KEY
   ```

3. **Run database migrations:**
   ```bash
   python run_migrations.py run
   ```

4. **Verify setup:**
   ```bash
   python test_sendbox_setup.py
   ```

### Documentation
- **Integration Guide:** `SENDBOX_INTEGRATION_PHASES.md`
- **Phase 1 Setup:** `PHASE1_SETUP_GUIDE.md`
- **API Reference:** `SENDBOX_D.md`
- **Migrations:** `migrations/README.md`

### Current Status
- ✓ Phase 1: Foundation Setup (Complete)
- ⧗ Phase 2: Shipping Quotes (Pending)
- ⧗ Phase 3: Shipment Creation (Pending)
- ⧗ Phase 4: Tracking Integration (Pending)

---

## Health Check

```http
GET /
```
Returns API status and version information.