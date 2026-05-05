# Admin API Documentation - Terminal Africa Shipping

**Base URL:** `http://localhost:4500`

**Authentication:** All admin endpoints require an admin JWT token in the `Authorization` header.

```
Authorization: Bearer YOUR_ADMIN_TOKEN
```

---

## Table of Contents
1. [Admin Authentication](#admin-authentication)
2. [Dashboard Statistics](#dashboard-statistics)
3. [Order Management](#order-management)
4. [Product Management](#product-management)
5. [Category Management](#category-management)
6. [Terminal Africa Shipping](#terminal-africa-shipping)
7. [Webhook & Monitoring](#webhook--monitoring)

---

## Dashboard Statistics

### Get Admin Statistics

**Endpoint:** `GET /api/admin/statistics`

**Description:** Retrieve dashboard statistics including number of users, orders, products, revenue, and status breakdowns.

**Success Response:**
```json
{
  "status": "success",
  "data": {
    "summary": {
      "total_users": 150,
      "total_orders": 320,
      "total_products": 85,
      "total_revenue": 450000.00
    },
    "order_status_breakdown": [
      {"status": "pending", "count": 45},
      {"status": "processing", "count": 120},
      {"status": "shipped", "count": 80},
      {"status": "delivered", "count": 75}
    ],
    "payment_status_breakdown": [
      {"status": "paid", "count": 250},
      {"status": "Pending", "count": 70}
    ],
    "last_7_days": {
      "orders_count": 45,
      "revenue": 67500.00
    }
  }
}
```

---

## Admin Authentication

### Admin Login

**Endpoint:** `POST /api/admin/login`

**Description:** Authenticate administrators and return a JWT token for `/api/admin/*` routes.

**Request Body:**
```json
{
  "email": "admin@example.com",
  "password": "password123"
}
```

**Success Response:**
```json
{
  "status": "success",
  "access_token": "eyJhbGci...",
  "admin": {
    "id": 1,
    "email": "admin@example.com"
  }
}
```

---

## Order Management

### List Orders

**Endpoint:** `GET /api/admin/orders`

**Description:** Retrieve orders with filters, pagination, and status search.

**Query Parameters:**
- `page` - page number
- `limit` - page size
- `order_status` - filter by order status
- `payment_status` - filter by payment status
- `delivery_status` - filter by delivery status

---

### Get Order Details

**Endpoint:** `GET /api/admin/orders/<order_id>`

**Description:** Get details for a single order.

---

### Update Order

**Endpoint:** `PUT /api/admin/orders/<order_id>`

**Description:** Update order fields such as `order_status`, `payment_status`, and `delivery_status`.

**Request Body Example:**
```json
{
  "order_status": "shipped",
  "payment_status": "paid",
  "delivery_status": "in_transit"
}
```

---

### Delete Order

**Endpoint:** `DELETE /api/admin/orders/<order_id>`

**Description:** Delete an order record.

---

## Product Management

### Create Product

**Endpoint:** `POST /api/admin/products`

**Description:** Create a new product in the catalog.

---

### Update Product

**Endpoint:** `PUT /api/admin/products/<product_id>`

**Description:** Update an existing product.

---

### Delete Product

**Endpoint:** `DELETE /api/admin/products/<product_id>`

**Description:** Remove a product from the catalog.

---

## Category Management

### Create Category

**Endpoint:** `POST /api/admin/categories`

**Description:** Create a new product category.

---

### Update Category

**Endpoint:** `PUT /api/admin/categories/<category_id>`

**Description:** Update an existing category.

---

### Delete Category

**Endpoint:** `DELETE /api/admin/categories/<category_id>`

**Description:** Delete a category.

---

## Terminal Africa Shipping

### Carrier Management

**Endpoint:** `GET /api/admin/terminal/carriers`

**Description:** List active Terminal Africa carriers.

**Endpoint:** `POST /api/admin/terminal/carriers/<carrier_id>/enable`

**Description:** Enable a carrier for shipping.

**Endpoint:** `POST /api/admin/terminal/carriers/<carrier_id>/disable`

**Description:** Disable a carrier.

---

### Packaging Management

**Endpoint:** `GET /api/admin/terminal/packaging`

**Description:** List configured Terminal packaging options.

**Endpoint:** `POST /api/admin/terminal/packaging`

**Description:** Create a new packaging option.

**Endpoint:** `DELETE /api/admin/terminal/packaging/<packaging_id>`

**Description:** Delete a packaging option.

---

### Shipment Monitoring

**Endpoint:** `GET /api/admin/terminal/shipments`

**Description:** List shipments managed through Terminal Africa.

**Endpoint:** `GET /api/admin/terminal/reports/shipping`

**Description:** Get shipping performance metrics and summary data.

---

## Webhook & Monitoring

### List Webhook Events

**Endpoint:** `GET /api/admin/webhooks/events`

**Description:** Browse webhook event records and filtering data.

### Webhook Stats

**Endpoint:** `GET /api/admin/webhooks/stats`

**Description:** Get webhook processing metrics.

### Webhook Event Details

**Endpoint:** `GET /api/admin/webhooks/events/<event_id>`

**Description:** Inspect a single webhook event.

### Retry Webhook Event

**Endpoint:** `POST /api/admin/webhooks/retry/<event_id>`

**Description:** Retry processing of a webhook event.

---

## Legacy Sendbox Routes

These backend routes still exist for backward compatibility, but new admin UI flows should prefer Terminal Africa shipping endpoints.

- `POST /api/admin/orders/<order_id>/create-shipment` - legacy manual shipment creation route
- `GET /api/admin/orders/<order_id>/sendbox-details` - legacy shipment details
- `POST /api/admin/orders/<order_id>/refresh-tracking` - legacy tracking refresh
- `POST /api/admin/orders/bulk-create-shipments` - legacy bulk shipment creation
- `GET /api/admin/sendbox/account` - legacy account information
- `POST /api/admin/sendbox/fund-account` - legacy staging account top-up
- `GET /api/admin/sendbox/shipments` - legacy shipment list

---

## Notes

- `order_status` is now set to `pending` for unpaid orders and only moves to `processing` once payment is confirmed.
- Active shipping support is **Terminal Africa** (Sendbox is no longer used).
- For UI integration, use Terminal Africa admin shipping routes.
