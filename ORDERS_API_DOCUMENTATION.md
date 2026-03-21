# Trollz Store - Orders & Checkout API Documentation

**Base URL:** `http://10.195.223.20:4500`

## Table of Contents
1. [Authentication](#authentication)
2. [Checkout & Order Creation](#checkout--order-creation)
3. [Order Retrieval](#order-retrieval)
4. [Order Tracking](#order-tracking)
5. [Order Confirmation](#order-confirmation)
6. [Admin Order Management](#admin-order-management)
7. [Response Formats](#response-formats)
8. [Error Codes](#error-codes)

---

## Authentication

Most endpoints require authentication via JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

Admin endpoints require an admin-level JWT token.

---

## Checkout & Order Creation

### Create Order from Checkout

**Endpoint:** `POST /api/checkout`

**Authentication:** Required (User token)

**Description:** Creates a new order from the provided items, validates stock availability, calculates totals with discounts, generates tracking number, and reduces product quantities.

**Request Body:**
```json
{
  "address": "123 Main Street, Lagos, Nigeria",
  "payment_method": "flutterwave",
  "transaction_id": "FLW-12345678",
  "items": [
    {
      "product_id": 55,
      "quantity": 2,
      "size": "XL"
    },
    {
      "product_id": 72,
      "quantity": 1,
      "size": ""
    }
  ]
}
```

**Request Fields:**
- `address` (string, required) - Full delivery address
- `payment_method` (string, required) - Payment method: `flutterwave`, `paystack`, or `cash_on_delivery`
- `transaction_id` (string, optional) - Payment transaction ID from payment gateway. If provided, payment_status is set to "paid", otherwise "Pending"
- `items` (array, required) - Array of order items
  - `product_id` (integer, required) - Product ID
  - `quantity` (integer, required) - Quantity to order
  - `size` (string, optional) - Product size if applicable

**Success Response (201 Created):**
```json
{
  "status": "success",
  "message": "Order created successfully",
  "data": {
    "order": {
      "id": 50,
      "user_id": 79,
      "tracking": "TS1772812345678123",
      "total_amount": 64560.0,
      "payment_method": "flutterwave",
      "transaction_id": "FLW-12345678",
      "payment_status": "paid",
      "order_status": "processing",
      "delivery_status": "Pending",
      "created_at": "2026-03-21 14:30:00",
      "address": "123 Main Street, Lagos, Nigeria",
      "updated_at": "2026-03-21 14:30:00",
      "stock_restored": false
    },
    "tracking_number": "TS1772812345678123"
  }
}
```

**Error Responses:**

400 Bad Request - Missing required fields:
```json
{
  "status": "error",
  "message": "'address' is required"
}
```

400 Bad Request - Invalid items:
```json
{
  "status": "error",
  "message": "At least one item is required"
}
```

404 Not Found - Product not found:
```json
{
  "status": "error",
  "message": "Product 999 not found"
}
```

400 Bad Request - Insufficient stock:
```json
{
  "status": "error",
  "message": "Insufficient stock for Product Name. Available: 5"
}
```

**Notes:**
- Automatically calculates prices with discounts applied
- Reduces product quantities in stock
- Clears user's cart after successful order creation
- Generates unique tracking number in format: `TS{timestamp}{random}`

---

## Order Retrieval

### Get User Orders

**Endpoint:** `GET /api/orders`

**Authentication:** Required (User token)

**Description:** Retrieves all orders for the authenticated user with pagination.

**Query Parameters:**
- `page` (integer, optional) - Page number, default: 1
- `limit` (integer, optional) - Items per page, default: 20, max: 100

**Example Request:**
```
GET http://10.195.223.20:4500/api/orders?page=1&limit=10
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "orders": [
      {
        "id": 50,
        "user_id": 79,
        "tracking": "TS1772812345678123",
        "total_amount": 64560.0,
        "payment_method": "flutterwave",
        "transaction_id": "FLW-12345678",
        "payment_status": "paid",
        "order_status": "processing",
        "delivery_status": "Pending",
        "created_at": "2026-03-21 14:30:00",
        "address": "123 Main Street, Lagos, Nigeria",
        "updated_at": "2026-03-21 14:30:00",
        "stock_restored": false,
        "items": [
          {
            "id": 77,
            "order_id": 50,
            "product_id": 55,
            "product_name": "Midea 173 Litres Double Door Refrigerator",
            "price": 251527.0,
            "quantity": 2,
            "size": "XL",
            "subtotal": 503054.0
          }
        ]
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 15,
      "total_pages": 2
    }
  }
}
```

---

### Get Order Details

**Endpoint:** `GET /api/orders/<order_id>`

**Authentication:** Required (User token)

**Description:** Retrieves details of a specific order including all items.

**Example Request:**
```
GET http://10.195.223.20:4500/api/orders/50
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "order": {
      "id": 50,
      "user_id": 79,
      "tracking": "TS1772812345678123",
      "total_amount": 64560.0,
      "payment_method": "flutterwave",
      "transaction_id": "FLW-12345678",
      "payment_status": "paid",
      "order_status": "processing",
      "delivery_status": "Pending",
      "created_at": "2026-03-21 14:30:00",
      "address": "123 Main Street, Lagos, Nigeria",
      "updated_at": "2026-03-21 14:30:00",
      "stock_restored": false,
      "items": [
        {
          "id": 77,
          "order_id": 50,
          "product_id": 55,
          "product_name": "Midea 173 Litres Double Door Refrigerator",
          "price": 251527.0,
          "quantity": 2,
          "size": "XL",
          "subtotal": 503054.0
        }
      ]
    }
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Order not found"
}
```

---

## Order Tracking

### Track Order by Tracking Number

**Endpoint:** `GET /api/orders/track/<tracking_number>`

**Authentication:** Not required (Public endpoint)

**Description:** Allows anyone to track an order using the tracking number. Useful for customers to check order status without logging in.

**Example Request:**
```
GET http://10.195.223.20:4500/api/orders/track/TS1772812345678123
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "order": {
      "id": 50,
      "user_id": 79,
      "tracking": "TS1772812345678123",
      "total_amount": 64560.0,
      "payment_method": "flutterwave",
      "transaction_id": "FLW-12345678",
      "payment_status": "paid",
      "order_status": "processing",
      "delivery_status": "Pending",
      "created_at": "2026-03-21 14:30:00",
      "address": "123 Main Street, Lagos, Nigeria",
      "updated_at": "2026-03-21 14:30:00",
      "stock_restored": false,
      "items": [
        {
          "id": 77,
          "order_id": 50,
          "product_id": 55,
          "product_name": "Midea 173 Litres Double Door Refrigerator",
          "price": 251527.0,
          "quantity": 2,
          "size": "XL",
          "subtotal": 503054.0
        }
      ]
    }
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Order not found"
}
```

---

## Order Confirmation

### Confirm Order Payment

**Endpoint:** `POST /api/orders/<order_id>/confirm`

**Authentication:** Required (User token)

**Description:** Updates an order with payment transaction ID and marks payment as confirmed. Useful when payment is completed after order creation.

**Request Body:**
```json
{
  "transaction_id": "FLW-98765432"
}
```

**Example Request:**
```
POST http://10.195.223.20:4500/api/orders/50/confirm
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Order payment confirmed",
  "data": {
    "order": {
      "id": 50,
      "user_id": 79,
      "tracking": "TS1772812345678123",
      "total_amount": 64560.0,
      "payment_method": "flutterwave",
      "transaction_id": "FLW-98765432",
      "payment_status": "paid",
      "order_status": "processing",
      "delivery_status": "Pending",
      "created_at": "2026-03-21 14:30:00",
      "address": "123 Main Street, Lagos, Nigeria",
      "updated_at": "2026-03-21 14:35:00",
      "stock_restored": false
    }
  }
}
```

**Error Responses:**

400 Bad Request:
```json
{
  "status": "error",
  "message": "transaction_id is required"
}
```

404 Not Found:
```json
{
  "status": "error",
  "message": "Order not found"
}
```

---

## Admin Order Management

### Get All Orders (Admin)

**Endpoint:** `GET /api/admin/orders`

**Authentication:** Required (Admin token)

**Description:** Retrieves all orders in the system with optional filters and pagination.

**Query Parameters:**
- `page` (integer, optional) - Page number, default: 1
- `limit` (integer, optional) - Items per page, default: 20, max: 100
- `order_status` (string, optional) - Filter by order status: `processing`, `shipped`, `delivered`, `cancelled`
- `payment_status` (string, optional) - Filter by payment status: `Pending`, `paid`, `failed`, `refunded`
- `delivery_status` (string, optional) - Filter by delivery status: `Pending`, `in_transit`, `delivered`

**Example Request:**
```
GET http://10.195.223.20:4500/api/admin/orders?page=1&limit=20&order_status=processing&payment_status=paid
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "orders": [
      {
        "id": 50,
        "user_id": 79,
        "tracking": "TS1772812345678123",
        "total_amount": 64560.0,
        "payment_method": "flutterwave",
        "transaction_id": "FLW-12345678",
        "payment_status": "paid",
        "order_status": "processing",
        "delivery_status": "Pending",
        "created_at": "2026-03-21 14:30:00",
        "address": "123 Main Street, Lagos, Nigeria",
        "updated_at": "2026-03-21 14:30:00",
        "stock_restored": false
      }
    ],
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

### Update Order Status (Admin)

**Endpoint:** `PUT /api/admin/orders/<order_id>`

**Authentication:** Required (Admin token)

**Description:** Updates the status of an order. Can update order status, payment status, and/or delivery status.

**Request Body:**
```json
{
  "order_status": "shipped",
  "payment_status": "paid",
  "delivery_status": "in_transit"
}
```

**Request Fields (all optional, but at least one required):**
- `order_status` (string) - Order status: `processing`, `shipped`, `delivered`, `cancelled`
- `payment_status` (string) - Payment status: `Pending`, `paid`, `failed`, `refunded`
- `delivery_status` (string) - Delivery status: `Pending`, `in_transit`, `delivered`

**Example Request:**
```
PUT http://10.195.223.20:4500/api/admin/orders/50
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Order updated successfully",
  "data": {
    "order": {
      "id": 50,
      "user_id": 79,
      "tracking": "TS1772812345678123",
      "total_amount": 64560.0,
      "payment_method": "flutterwave",
      "transaction_id": "FLW-12345678",
      "payment_status": "paid",
      "order_status": "shipped",
      "delivery_status": "in_transit",
      "created_at": "2026-03-21 14:30:00",
      "address": "123 Main Street, Lagos, Nigeria",
      "updated_at": "2026-03-21 15:00:00",
      "stock_restored": false
    }
  }
}
```

**Error Responses:**

400 Bad Request:
```json
{
  "status": "error",
  "message": "No valid fields to update"
}
```

404 Not Found:
```json
{
  "status": "error",
  "message": "Order not found"
}
```

---

### Delete Order (Admin)

**Endpoint:** `DELETE /api/admin/orders/<order_id>`

**Authentication:** Required (Admin token)

**Description:** Deletes an order and all associated order items.

**Example Request:**
```
DELETE http://10.195.223.20:4500/api/admin/orders/50
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Order TS1772812345678123 deleted successfully"
}
```

**Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Order not found"
}
```

---

## Response Formats

### Order Object Structure

```json
{
  "id": 50,
  "user_id": 79,
  "tracking": "TS1772812345678123",
  "total_amount": 64560.0,
  "payment_method": "flutterwave",
  "transaction_id": "FLW-12345678",
  "payment_status": "paid",
  "order_status": "processing",
  "delivery_status": "Pending",
  "created_at": "2026-03-21 14:30:00",
  "address": "123 Main Street, Lagos, Nigeria",
  "updated_at": "2026-03-21 14:30:00",
  "stock_restored": false,
  "items": [...]
}
```

**Field Descriptions:**
- `id` - Unique order identifier
- `user_id` - ID of the user who placed the order
- `tracking` - Unique tracking number (format: TS{timestamp}{random})
- `total_amount` - Total order amount in NGN
- `payment_method` - Payment method used: `flutterwave`, `paystack`, `cash_on_delivery`
- `transaction_id` - Payment gateway transaction ID
- `payment_status` - Payment status: `Pending`, `paid`, `failed`, `refunded`
- `order_status` - Order processing status: `processing`, `shipped`, `delivered`, `cancelled`
- `delivery_status` - Delivery status: `Pending`, `in_transit`, `delivered`
- `created_at` - Order creation timestamp
- `address` - Delivery address
- `updated_at` - Last update timestamp
- `stock_restored` - Whether stock was restored (for cancelled orders)
- `items` - Array of order items (when included)

### Order Item Object Structure

```json
{
  "id": 77,
  "order_id": 50,
  "product_id": 55,
  "product_name": "Midea 173 Litres Double Door Refrigerator",
  "price": 251527.0,
  "quantity": 2,
  "size": "XL",
  "subtotal": 503054.0
}
```

**Field Descriptions:**
- `id` - Unique order item identifier
- `order_id` - Associated order ID
- `product_id` - Product ID
- `product_name` - Product name at time of order
- `price` - Unit price (with discount applied)
- `quantity` - Quantity ordered
- `size` - Product size (if applicable)
- `subtotal` - Line total (price × quantity)

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created successfully |
| 400 | Bad request - Invalid input or missing required fields |
| 401 | Unauthorized - Invalid or missing authentication token |
| 403 | Forbidden - Insufficient permissions (admin required) |
| 404 | Not found - Resource doesn't exist |
| 500 | Internal server error |

### Common Error Response Format

```json
{
  "status": "error",
  "message": "Descriptive error message"
}
```

---

## Workflow Examples

### Complete Checkout Flow

1. **User adds items to cart** (via cart endpoints)
2. **User initiates checkout:**
   ```
   POST /api/checkout
   {
     "address": "123 Main St",
     "payment_method": "flutterwave",
     "items": [{"product_id": 55, "quantity": 2}]
   }
   ```
3. **System returns order with tracking number**
4. **User completes payment on payment gateway**
5. **User confirms payment:**
   ```
   POST /api/orders/50/confirm
   {
     "transaction_id": "FLW-12345678"
   }
   ```
6. **User tracks order:**
   ```
   GET /api/orders/track/TS1772812345678123
   ```

### Admin Order Management Flow

1. **Admin views all pending orders:**
   ```
   GET /api/admin/orders?order_status=processing&payment_status=paid
   ```
2. **Admin updates order to shipped:**
   ```
   PUT /api/admin/orders/50
   {
     "order_status": "shipped",
     "delivery_status": "in_transit"
   }
   ```
3. **Admin marks as delivered:**
   ```
   PUT /api/admin/orders/50
   {
     "order_status": "delivered",
     "delivery_status": "delivered"
   }
   ```

---

## Notes

- All monetary values are in Nigerian Naira (NGN)
- Timestamps are in format: `YYYY-MM-DD HH:MM:SS`
- Tracking numbers are unique and generated automatically
- Product quantities are automatically reduced when orders are created
- User's cart is cleared after successful order creation
- Discounts are automatically applied from product discount field
- Orders can only be accessed by the user who created them (except admin)
- Tracking endpoint is public and doesn't require authentication

---

## Support

For issues or questions, contact the development team or refer to the main API documentation.
