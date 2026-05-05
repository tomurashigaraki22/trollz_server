# Admin Panel Integration Guide

This document describes the complete admin route surface for the Trollz server and how to integrate it into an admin web interface.

## Overview

The admin section is powered by protected REST endpoints under `/api/admin/*`.
All admin routes require a valid admin JWT token in the `Authorization` header.

- Endpoint prefix: `/api/admin`
- Authentication header:
  ```http
  Authorization: Bearer ADMIN_TOKEN
  ```

> If your admin UI is separate from the main storefront, keep admin credentials and tokens isolated from customer authentication.

---

## Admin authentication

### Admin login

- `POST /api/admin/login`
- Request body:
  ```json
  {
    "username": "admin",
    "password": "secret"
  }
  ```
- Response contains:
  - `data.token`
  - `data.admin` object

Use this token for all subsequent admin route calls.

---

## Product management

Admin product routes are in `routes/products.py`.

| Method | Route | Description |
|---|---|---|
| `POST` | `/api/admin/products` | Create a new product |
| `PUT` | `/api/admin/products/<product_id>` | Update an existing product |
| `DELETE` | `/api/admin/products/<product_id>` | Delete a product |

### Recommended UI pages

- Product list
- Create product form
- Edit product form
- Product details page

### Example: Create product

```js
const response = await fetch('/api/admin/products', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${adminToken}`,
  },
  body: JSON.stringify({
    item: 'New Product',
    description: 'Product description',
    price: 12000,
    qty: 10,
    category: 'Electronics',
    weight: 1.2
  }),
});
```

---

## Category management

Admin category routes are in `routes/categories.py`.

| Method | Route | Description |
|---|---|---|
| `POST` | `/api/admin/categories` | Create a category |
| `PUT` | `/api/admin/categories/<category_id>` | Update category name |
| `DELETE` | `/api/admin/categories/<category_id>` | Delete category if unused |

### Recommended UI pages

- Category list
- Create category form
- Edit category form

---

## Order management

Order admin routes are in `routes/orders.py`.

| Method | Route | Description |
|---|---|---|
| `GET` | `/api/admin/orders` | List orders with pagination and filters |
| `GET` | `/api/admin/orders/<order_id>` | View order details |
| `PUT` | `/api/admin/orders/<order_id>` | Update order status/payment/delivery |
| `DELETE` | `/api/admin/orders/<order_id>` | Delete an order |
| `POST` | `/api/admin/orders/<order_id>/create-shipment` | Create shipment manually (legacy route) |
| `GET` | `/api/admin/orders/<order_id>/sendbox-details` | Get shipment details (legacy route) |
| `POST` | `/api/admin/orders/<order_id>/refresh-tracking` | Refresh tracking (legacy route) |

### Filters supported on order list

- `order_status`
- `payment_status`
- `delivery_status`
- `page`
- `limit`

### Recommended UI pages

- Order list with filters
- Order detail page
- Order actions panel (update statuses, delete order)
- Shipment creation / tracking actions

### Example: Update order status

```js
await fetch(`/api/admin/orders/${orderId}`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${adminToken}`,
  },
  body: JSON.stringify({
    order_status: 'shipped',
    delivery_status: 'in_transit',
  }),
});
```

---

## Shipping management (Terminal Africa)

Primary shipping support is now based on Terminal Africa. The backend still contains legacy Sendbox endpoints for backward compatibility, but admin UI integration should use Terminal Africa routing and monitoring wherever possible.

### Terminal Africa shipping admin routes

| Method | Route | Description |
|---|---|---|
| `POST` | `/api/admin/shipping/sync-tracking` | Sync shipment tracking for multiple orders |
| `GET` | `/api/admin/terminal/carriers` | List Terminal Africa carriers |
| `POST` | `/api/admin/terminal/carriers/<carrier_id>/enable` | Enable a carrier |
| `POST` | `/api/admin/terminal/carriers/<carrier_id>/disable` | Disable a carrier |
| `GET` | `/api/admin/terminal/packaging` | List Terminal packaging options |
| `POST` | `/api/admin/terminal/packaging` | Create a packaging option |
| `DELETE` | `/api/admin/terminal/packaging/<packaging_id>` | Delete a packaging option |
| `GET` | `/api/admin/terminal/shipments` | List Terminal-managed shipments |
| `GET` | `/api/admin/terminal/reports/shipping` | Terminal shipping performance report |
| `GET` | `/api/admin/webhooks/events` | List webhook events |
| `GET` | `/api/admin/webhooks/stats` | Get webhook processing metrics |
| `GET` | `/api/admin/webhooks/events/<event_id>` | Get details for a webhook event |
| `POST` | `/api/admin/webhooks/retry/<event_id>` | Retry a webhook event |

### Recommended UI pages

- Shipping dashboard
- Terminal Africa carrier and packaging settings
- Shipment list and details
- Webhook monitoring and retry panel
- Order shipment health

---

## Monitoring and dashboard ideas

For a complete admin section, build these screens:

1. **Admin dashboard / home**
   - Total orders
   - Pending shipments
   - Terminal Africa carrier status
   - Recent webhook events
   - Orders waiting shipment creation
2. **Product dashboard**
   - Product count
   - Low stock alerts
   - Active flash sales
3. **Order dashboard**
   - Orders by status
   - Payment collection issues
   - Delivery performance
4. **Shipping dashboard**
   - Shipments by carrier
   - Sync health
   - Webhook errors / retries
5. **Terminal settings**
   - Carriers enabled
   - Packaging options
   - Shipment reconciliation

---

## Integration guidance

### 1. Admin login flow

- Add an admin login page that calls `POST /api/admin/login`.
- Store the returned token securely in memory, HTTP-only cookie, or encrypted storage.
- Apply the token to every `/api/admin/*` request.

### 2. Build the layout

Use a separate admin layout with:

- Sidebar navigation
- Header with admin name and logout
- Breadcrumbs for section navigation
- Permission guard to redirect unauthorized users

### 3. Use the endpoints in UI components

- `GET /api/admin/orders` for the order table
- `GET /api/admin/orders/<order_id>` for the order detail panel
- `GET /api/admin/terminal/carriers` for carrier configuration
- `GET /api/admin/terminal/packaging` for packaging settings
- `GET /api/admin/terminal/shipments` for shipment list

### 4. Use query params for list pages

- `page` and `limit` for pagination
- `order_status`, `payment_status`, `delivery_status` for orders

### 5. Build action buttons

- `Create shipment` → `POST /api/admin/orders/<order_id>/create-shipment` (legacy)
- `Cancel shipment` → `POST /api/admin/orders/<order_id>/cancel-shipment` (legacy)
- `Refresh tracking` → `POST /api/admin/orders/<order_id>/refresh-tracking` (legacy)
- `Retry webhook` → `POST /api/admin/webhooks/retry/<event_id>`

### 6. Error handling

Always handle these response cases:

- `401 Unauthorized` / invalid token
- `403 Forbidden` when admin token is missing or invalid
- `400 Bad Request` for invalid request payloads
- `404 Not Found` for missing resources
- `500 Internal Server Error` for server issues

---

## Frontend integration example (React / fetch)

```js
const adminFetch = async (url, options = {}) => {
  const token = localStorage.getItem('adminToken');
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
      ...options.headers,
    },
  });

  if (response.status === 401) {
    // redirect to admin login
  }

  return response.json();
};

const fetchOrders = async (page = 1, status = '') => {
  const url = new URL('/api/admin/orders', window.location.origin);
  url.searchParams.set('page', page);
  if (status) url.searchParams.set('order_status', status);
  return adminFetch(url);
};
```

---

## Admin page structure recommendation

- `/admin/login`
- `/admin/dashboard`
- `/admin/products`
- `/admin/products/new`
- `/admin/products/:id/edit`
- `/admin/categories`
- `/admin/orders`
- `/admin/orders/:id`
- `/admin/shipments`
- `/admin/shipping/reports`
- `/admin/webhooks`
- `/admin/settings`

---

## Notes and references

- Public product endpoints can still be used for store preview or product search:
  - `GET /api/products`
  - `GET /api/products/<product_id>`
  - `GET /api/categories`
- Admin routes use `admin_required` in `middleware/auth_middleware.py`.
- Existing admin route implementation files:
  - `routes/auth.py`
  - `routes/products.py`
  - `routes/categories.py`
  - `routes/orders.py`
  - `routes/shipping.py`
  - `routes/admin_shipping.py`

If you want, I can also add a short `admin-panel.md` section to your frontend README describing layout and route usage specifically for React or Vue.