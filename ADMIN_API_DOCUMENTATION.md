# Admin API Documentation - Sendbox Integration

**Base URL:** `http://localhost:4500`

**Authentication:** All endpoints require admin authentication token in the Authorization header.

```
Authorization: Bearer YOUR_ADMIN_TOKEN
```

---

## Table of Contents
1. [Shipment Management](#shipment-management)
2. [Bulk Operations](#bulk-operations)
3. [Shipping Reports](#shipping-reports)
4. [Account Management](#account-management)
5. [Tracking Management](#tracking-management)
6. [Order Management](#order-management)

---

## Shipment Management

### Create Shipment Manually

**Endpoint:** `POST /api/admin/orders/<order_id>/create-shipment`

**Authentication:** Required (Admin token)

**Description:** Manually create a Sendbox shipment for an order that doesn't have one.

**URL Parameters:**
- `order_id` (integer) - The order ID

**Success Response (201 Created):**
```json
{
  "status": "success",
  "message": "Shipment created successfully",
  "data": {
    "order": {
      "id": 123,
      "tracking": "TS1713600000123",
      "sendbox_tracking_code": "SB123456789",
      "sendbox_carrier": "DHL",
      "order_status": "processing"
    },
    "shipment": {
      "sendbox_shipment_id": "12345",
      "sendbox_tracking_code": "SB123456789",
      "carrier": "DHL",
      "status": "pending"
    }
  }
}
```

**Error Responses:**
- `404 Not Found` - Order not found
- `400 Bad Request` - Shipment already exists
- `400 Bad Request` - No shipping address
- `500 Internal Server Error` - Shipment creation failed

---

### Cancel Shipment

**Endpoint:** `POST /api/admin/orders/<order_id>/cancel-shipment`

**Authentication:** Required (Admin token)

**Description:** Cancel a Sendbox shipment and optionally restore stock.

**URL Parameters:**
- `order_id` (integer) - The order ID

**Request Body:**
```json
{
  "restore_stock": true,
  "reason": "Customer requested cancellation"
}
```

**Fields:**
- `restore_stock` (boolean, optional) - Whether to restore product stock (default: false)
- `reason` (string, optional) - Reason for cancellation (default: "Admin cancelled shipment")

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Shipment cancelled successfully",
  "data": {
    "order_id": 123,
    "sendbox_shipment_id": "12345",
    "stock_restored": true,
    "restored_items": [
      {
        "product_id": 55,
        "quantity": 1
      }
    ],
    "reason": "Customer requested cancellation"
  }
}
```

**Error Responses:**
- `404 Not Found` - Order not found or no shipment
- `400 Bad Request` - Order already cancelled

---

### Get Sendbox Details

**Endpoint:** `GET /api/admin/orders/<order_id>/sendbox-details`

**Authentication:** Required (Admin token)

**Description:** View full Sendbox shipment data for an order.

**URL Parameters:**
- `order_id` (integer) - The order ID

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "sendbox_shipment_id": "12345",
    "sendbox_tracking_code": "SB123456789",
    "sendbox_status": "in_transit",
    "sendbox_carrier": "DHL",
    "estimated_delivery_date": "2026-04-25",
    "webhook_data": {
      "event": "shipment.status_updated",
      "tracking_code": "SB123456789",
      "status": "in_transit",
      "data": {...}
    }
  }
}
```

**Error Responses:**
- `404 Not Found` - Order not found or no shipment

---

### Refresh Tracking

**Endpoint:** `POST /api/admin/orders/<order_id>/refresh-tracking`

**Authentication:** Required (Admin token)

**Description:** Force refresh tracking information from Sendbox API.

**URL Parameters:**
- `order_id` (integer) - The order ID

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Tracking information refreshed successfully",
  "data": {
    "sendbox_status": "in_transit",
    "order_status": "shipped",
    "delivery_status": "in_transit",
    "tracking_data": {
      "status": "in_transit",
      "tracking_history": [...]
    }
  }
}
```

**Error Responses:**
- `404 Not Found` - Order not found or no tracking code
- `500 Internal Server Error` - Sendbox API error

---

## Bulk Operations

### Bulk Create Shipments

**Endpoint:** `POST /api/admin/orders/bulk-create-shipments`

**Authentication:** Required (Admin token)

**Description:** Create Sendbox shipments for multiple orders at once.

**Request Body:**
```json
{
  "order_ids": [1, 2, 3, 4, 5],
  "service_code": "standard"
}
```

**Fields:**
- `order_ids` (array of integers, required) - List of order IDs
- `service_code` (string, optional) - Service code for shipments (default: "standard")

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Created 4 of 5 shipments",
  "data": {
    "success": [
      {
        "order_id": 1,
        "tracking_code": "SB123456"
      },
      {
        "order_id": 2,
        "tracking_code": "SB123457"
      },
      {
        "order_id": 3,
        "tracking_code": "SB123458"
      },
      {
        "order_id": 4,
        "tracking_code": "SB123459"
      }
    ],
    "failed": [
      {
        "order_id": 5,
        "error": "No shipping address"
      }
    ],
    "total": 5
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid request body

---

### Bulk Sync Tracking

**Endpoint:** `POST /api/admin/shipping/sync-tracking`

**Authentication:** Required (Admin token)

**Description:** Sync tracking information for multiple orders from Sendbox.

**Request Body:**
```json
{
  "order_ids": [1, 2, 3, 4, 5]
}
```

**Fields:**
- `order_ids` (array of integers, required) - List of order IDs

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Synced 4 of 5 orders",
  "data": {
    "success": [1, 2, 3, 4],
    "failed": [
      {
        "order_id": 5,
        "error": "No tracking code found"
      }
    ],
    "total": 5
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid request body

---

## Shipping Reports

### Generate Shipping Report

**Endpoint:** `GET /api/admin/reports/shipping`

**Authentication:** Required (Admin token)

**Description:** Generate comprehensive shipping analytics and reports.

**Query Parameters:**
- `start_date` (string, optional) - Start date in YYYY-MM-DD format (default: 30 days ago)
- `end_date` (string, optional) - End date in YYYY-MM-DD format (default: today)
- `report_type` (string, optional) - 'summary' or 'detailed' (default: 'summary')

**Example Request:**
```bash
GET /api/admin/reports/shipping?start_date=2026-03-01&end_date=2026-04-20&report_type=summary
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "period": {
      "start_date": "2026-03-01",
      "end_date": "2026-04-20"
    },
    "summary": {
      "total_shipments": 150,
      "total_shipping_cost": 750000.00,
      "avg_shipping_cost": 5000.00,
      "min_shipping_cost": 2500.00,
      "max_shipping_cost": 15000.00,
      "avg_delivery_days": 3.5,
      "avg_shipping_percentage": 8.5
    },
    "carriers": [
      {
        "carrier": "DHL",
        "shipment_count": 80,
        "total_cost": 400000.00,
        "avg_cost": 5000.00
      },
      {
        "carrier": "FedEx",
        "shipment_count": 50,
        "total_cost": 275000.00,
        "avg_cost": 5500.00
      }
    ],
    "status_breakdown": [
      {
        "status": "delivered",
        "count": 120
      },
      {
        "status": "in_transit",
        "count": 25
      },
      {
        "status": "pending",
        "count": 5
      }
    ],
    "delivery_performance": {
      "delivered": 120,
      "failed": 3,
      "cancelled": 2,
      "total": 150,
      "success_rate": 80.0
    }
  }
}
```

**Detailed Report (report_type=detailed):**
Includes all summary data plus:
```json
{
  "shipments": [
    {
      "order_id": 1,
      "tracking": "TS1713600000123",
      "sendbox_tracking_code": "SB123456789",
      "carrier": "DHL",
      "shipping_cost": 5000.00,
      "status": "delivered",
      "created_at": "2026-04-01 10:00:00",
      "updated_at": "2026-04-04 15:30:00"
    }
  ]
}
```

---

## Account Management

### Get Sendbox Account Info

**Endpoint:** `GET /api/admin/sendbox/account`

**Authentication:** Required (Admin token)

**Description:** View Sendbox account information and balance.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "account": {
      "balance": 50000,
      "currency": "NGN",
      "account_name": "Trollz Store",
      "account_email": "admin@trollzstore.com"
    },
    "environment": "staging",
    "base_url": "https://sandbox.staging.sendbox.co"
  }
}
```

**Error Responses:**
- `500 Internal Server Error` - Sendbox API error

---

### Fund Staging Account

**Endpoint:** `POST /api/admin/sendbox/fund-account`

**Authentication:** Required (Admin token)

**Description:** Add funds to Sendbox staging account (staging environment only).

**Request Body:**
```json
{
  "amount": 10000
}
```

**Fields:**
- `amount` (number, required) - Amount to add (must be > 0)

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Successfully added 10000 to staging account",
  "data": {
    "new_balance": 60000,
    "amount_added": 10000
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid amount
- `403 Forbidden` - Not in staging environment
- `500 Internal Server Error` - Sendbox API error

---

### List All Sendbox Shipments

**Endpoint:** `GET /api/admin/sendbox/shipments`

**Authentication:** Required (Admin token)

**Description:** Get all shipments from Sendbox API.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "shipments": [
      {
        "id": 12345,
        "tracking_code": "SB123456789",
        "status": "in_transit",
        "carrier": "DHL",
        "created_at": "2026-04-20T10:00:00Z"
      }
    ],
    "count": 150
  }
}
```

**Error Responses:**
- `500 Internal Server Error` - Sendbox API error

---

## Tracking Management

### Bulk Sync Tracking

See [Bulk Operations](#bulk-operations) section above.

---

## Order Management

### Get All Orders (Admin)

**Endpoint:** `GET /api/admin/orders`

**Authentication:** Required (Admin token)

**Description:** Get all orders with pagination and filters.

**Query Parameters:**
- `page` (integer, optional) - Page number (default: 1)
- `limit` (integer, optional) - Items per page (default: 20, max: 100)
- `order_status` (string, optional) - Filter by order status
- `payment_status` (string, optional) - Filter by payment status
- `delivery_status` (string, optional) - Filter by delivery status

**Example Request:**
```bash
GET /api/admin/orders?page=1&limit=20&order_status=shipped
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "orders": [
      {
        "id": 1,
        "tracking": "TS1713600000123",
        "user_id": 5,
        "total_amount": 55000.00,
        "order_status": "shipped",
        "delivery_status": "in_transit",
        "sendbox_tracking_code": "SB123456789",
        "created_at": "2026-04-20 10:00:00"
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

### Update Order Status

**Endpoint:** `PUT /api/admin/orders/<order_id>`

**Authentication:** Required (Admin token)

**Description:** Update order status fields.

**URL Parameters:**
- `order_id` (integer) - The order ID

**Request Body:**
```json
{
  "order_status": "shipped",
  "payment_status": "paid",
  "delivery_status": "in_transit"
}
```

**Fields (all optional):**
- `order_status` (string) - Order status
- `payment_status` (string) - Payment status
- `delivery_status` (string) - Delivery status

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Order updated successfully",
  "data": {
    "order": {
      "id": 123,
      "order_status": "shipped",
      "payment_status": "paid",
      "delivery_status": "in_transit"
    }
  }
}
```

**Error Responses:**
- `404 Not Found` - Order not found
- `400 Bad Request` - No valid fields to update

---

### Delete Order

**Endpoint:** `DELETE /api/admin/orders/<order_id>`

**Authentication:** Required (Admin token)

**Description:** Delete an order and its items.

**URL Parameters:**
- `order_id` (integer) - The order ID

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Order TS1713600000123 deleted successfully"
}
```

**Error Responses:**
- `404 Not Found` - Order not found

---

## Error Codes

### Standard Error Response Format:
```json
{
  "status": "error",
  "message": "Error description"
}
```

### HTTP Status Codes:
- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Operation not allowed
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Common Error Messages:

**Authentication Errors:**
- "No token provided"
- "Invalid token"
- "Admin access required"

**Validation Errors:**
- "Order not found"
- "Shipment already exists"
- "No shipping address"
- "Invalid amount"
- "'order_ids' is required and must be an array"

**Business Logic Errors:**
- "Order is already cancelled"
- "No Sendbox shipment found for this order"
- "Fund account is only available in staging environment"

**API Errors:**
- "Sendbox API error: [details]"
- "Failed to create shipment: [details]"

---

## Rate Limiting

Currently no rate limiting is implemented. Consider implementing rate limiting for production:
- Recommended: 100 requests per minute per admin user
- Bulk operations: 10 requests per minute
- Report generation: 20 requests per minute

---

## Best Practices

### Authentication:
- Always include admin token in Authorization header
- Rotate tokens regularly
- Keep tokens secure
- Don't share tokens

### Bulk Operations:
- Start with small batches (5-10 items)
- Review failures before retrying
- Run during off-peak hours
- Monitor API response times

### Report Generation:
- Use summary reports for quick checks
- Use detailed reports for deep analysis
- Cache report results when possible
- Schedule regular report generation

### Error Handling:
- Always check response status
- Handle errors gracefully
- Log errors for debugging
- Retry failed operations with backoff

---

## Changelog

### Version 1.0 (April 20, 2026)
- Initial admin API release
- Shipment management endpoints
- Bulk operations
- Shipping reports
- Account management
- Tracking management

---

## Support

For API support:
- Review this documentation
- Check error messages in responses
- Review application logs
- Test in staging environment first

---

**Last Updated:** April 20, 2026
**API Version:** 1.0
**Phase:** 5 - Admin Features Complete
