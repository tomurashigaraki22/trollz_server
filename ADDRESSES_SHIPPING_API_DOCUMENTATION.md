# Addresses & Shipping API Documentation

**Base URL:** `http://localhost:4500`

## Table of Contents
1. [Address Management](#address-management)
2. [Shipping Quotes](#shipping-quotes)
3. [Product Weight](#product-weight)
4. [Error Codes](#error-codes)

---

## Address Management

### Create Shipping Address

**Endpoint:** `POST /api/addresses`

**Authentication:** Required (User token)

**Description:** Creates a new shipping address for the authenticated user.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "08001234567",
  "email": "john@example.com",
  "street": "123 Main Street",
  "street_line_2": "Apt 4B",
  "city": "Lagos",
  "state": "Lagos",
  "country": "NG",
  "post_code": "100001",
  "lng": 3.37,
  "lat": 6.56,
  "is_default": false
}
```

**Required Fields:**
- `first_name` (string)
- `last_name` (string)
- `phone` (string) - Will be formatted automatically
- `street` (string)
- `city` (string)
- `state` (string)

**Optional Fields:**
- `email` (string)
- `street_line_2` (string)
- `country` (string) - Default: "NG"
- `post_code` (string)
- `lng` (decimal) - Longitude
- `lat` (decimal) - Latitude
- `is_default` (boolean) - Default: false

**Success Response (201 Created):**
```json
{
  "status": "success",
  "message": "Address created successfully",
  "data": {
    "address": {
      "id": 1,
      "user_id": 79,
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
      "lng": 3.37,
      "lat": 6.56,
      "is_default": false,
      "created_at": "2026-04-20 14:30:00",
      "updated_at": "2026-04-20 14:30:00"
    }
  }
}
```

---

### List User Addresses

**Endpoint:** `GET /api/addresses`

**Authentication:** Required (User token)

**Description:** Retrieves all shipping addresses for the authenticated user.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "addresses": [
      {
        "id": 1,
        "user_id": 79,
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+234 800 123 4567",
        "street": "123 Main Street",
        "city": "Lagos",
        "state": "Lagos",
        "country": "NG",
        "is_default": true,
        "created_at": "2026-04-20 14:30:00"
      }
    ],
    "count": 1
  }
}
```

---

### Get Specific Address

**Endpoint:** `GET /api/addresses/<address_id>`

**Authentication:** Required (User token)

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "address": {
      "id": 1,
      "user_id": 79,
      "first_name": "John",
      "last_name": "Doe",
      "phone": "+234 800 123 4567",
      "street": "123 Main Street",
      "city": "Lagos",
      "state": "Lagos",
      "country": "NG",
      "is_default": true
    }
  }
}
```

---

### Update Address

**Endpoint:** `PUT /api/addresses/<address_id>`

**Authentication:** Required (User token)

**Description:** Updates an existing shipping address. Only provided fields will be updated.

**Request Body (partial update):**
```json
{
  "phone": "08009876543",
  "street": "456 New Street"
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Address updated successfully",
  "data": {
    "address": {
      "id": 1,
      "phone": "+234 800 987 6543",
      "street": "456 New Street",
      ...
    }
  }
}
```

---

### Delete Address

**Endpoint:** `DELETE /api/addresses/<address_id>`

**Authentication:** Required (User token)

**Description:** Deletes a shipping address. If the deleted address was default, another address will be set as default automatically.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Address deleted successfully"
}
```

---

### Set Default Address

**Endpoint:** `POST /api/addresses/<address_id>/set-default`

**Authentication:** Required (User token)

**Description:** Sets the specified address as the default shipping address.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Default address updated successfully",
  "data": {
    "address": {
      "id": 1,
      "is_default": true,
      ...
    }
  }
}
```

---

### Get Default Address

**Endpoint:** `GET /api/addresses/default`

**Authentication:** Required (User token)

**Description:** Retrieves the user's default shipping address.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "address": {
      "id": 1,
      "is_default": true,
      ...
    }
  }
}
```

---

## Shipping Quotes

### Get Shipping Quotes

**Endpoint:** `POST /api/shipping/quotes`

**Authentication:** Required (User token)

**Description:** Retrieves shipping quotes from Sendbox for the specified items and destination.

**Request Body:**
```json
{
  "destination_address_id": 1,
  "items": [
    {
      "product_id": 55,
      "quantity": 2
    },
    {
      "product_id": 72,
      "quantity": 1,
      "name": "Custom Item",
      "value": 15000,
      "weight": 2.5
    }
  ],
  "service_code": "standard",
  "pickup_date": "2026-04-25"
}
```

**Request Fields:**
- `destination_address_id` (integer, required) - ID of saved shipping address
- `items` (array, required) - Array of items to ship
  - `product_id` (integer) - Product ID (will fetch details automatically)
  - `quantity` (integer, required) - Quantity to ship
  - `name` (string, optional) - Item name (if not using product_id)
  - `value` (float, optional) - Item value (if not using product_id)
  - `weight` (float, optional) - Item weight in KG (if not using product_id)
  - `description` (string, optional) - Item description
  - `item_type` (string, optional) - Item type
  - `hts_code` (string, optional) - Harmonized Tariff Schedule code
- `service_code` (string, optional) - "standard", "premium", or "expedient" (default: "standard")
- `pickup_date` (string, optional) - Pickup date in YYYY-MM-DD format (default: tomorrow)

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Shipping quotes retrieved successfully",
  "data": {
    "quote_id": 456,
    "quotes": {
      "amount": 5000,
      "carrier": "DHL",
      "delivery_time": "2-3 days",
      "service_code": "standard"
    },
    "summary": {
      "total_weight": 5.0,
      "total_value": 100000,
      "service_type": "local",
      "service_code": "standard",
      "origin": "Ikeja, Lagos",
      "destination": "Maitama, Abuja",
      "expires_at": "2026-04-21 14:30:00"
    }
  }
}
```

---

### Get Specific Quote

**Endpoint:** `GET /api/shipping/quotes/<quote_id>`

**Authentication:** Required (User token)

**Description:** Retrieves a previously saved shipping quote.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "quote": {
      "id": 456,
      "user_id": 79,
      "origin_state": "Lagos",
      "destination_state": "Abuja",
      "weight": 5.0,
      "service_type": "local",
      "service_code": "standard",
      "carrier": "DHL",
      "quoted_price": 5000,
      "currency": "NGN",
      "quote_data": {...},
      "created_at": "2026-04-20 14:30:00",
      "expires_at": "2026-04-21 14:30:00"
    }
  }
}
```

**Error Response (410 Gone) - Quote Expired:**
```json
{
  "status": "error",
  "message": "Quote has expired. Please request a new quote."
}
```

---

### Get Quote History

**Endpoint:** `GET /api/shipping/quotes/history`

**Authentication:** Required (User token)

**Description:** Retrieves the user's shipping quote history with pagination.

**Query Parameters:**
- `page` (integer, optional) - Page number (default: 1)
- `limit` (integer, optional) - Items per page (default: 20, max: 100)

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "quotes": [
      {
        "id": 456,
        "origin_state": "Lagos",
        "destination_state": "Abuja",
        "weight": 5.0,
        "quoted_price": 5000,
        "created_at": "2026-04-20 14:30:00"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 15,
      "total_pages": 1
    }
  }
}
```

---

### Calculate Landed Cost

**Endpoint:** `POST /api/shipping/landed-cost`

**Authentication:** Required (User token)

**Description:** Calculates the total landed cost for international shipments, including duties, taxes, and fees.

**Request Body:** Same as shipping quotes

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Landed cost calculated successfully",
  "data": {
    "landed_cost": {
      "customs_option": "sender",
      "estimate": {
        "code": "duties_and_taxes",
        "name": "Duties and taxes",
        "value": 18.93,
        "breakdown": [
          {
            "code": "duties",
            "name": "Duties",
            "value": 0.0
          },
          {
            "code": "taxes",
            "name": "Taxes",
            "value": 12.22
          },
          {
            "code": "fees",
            "name": "Fees",
            "value": 6.71
          }
        ],
        "exchange_rate": 1669.025
      }
    },
    "summary": {
      "total_weight": 5.0,
      "total_value": 100000,
      "origin": "Ikeja, Lagos",
      "destination": "London, GB"
    }
  }
}
```

**Error Response (400 Bad Request) - Not International:**
```json
{
  "status": "error",
  "message": "Landed cost calculation is only for international shipments"
}
```

---

## Product Weight

### Create Product with Weight

**Endpoint:** `POST /api/admin/products`

**Authentication:** Required (Admin token)

**Request Body:**
```json
{
  "item": "Laptop",
  "category": "Electronics",
  "price": 500000,
  "discount": 10,
  "supplier": "Tech Supplier",
  "img": "laptop.jpg",
  "qty": 50,
  "weight": 2.5,
  "description": "High-performance laptop"
}
```

**New Field:**
- `weight` (float, optional) - Product weight in KG (default: 0.5)

**Success Response (201 Created):**
```json
{
  "status": "success",
  "message": "Product created successfully",
  "data": {
    "product": {
      "id": 100,
      "item": "Laptop",
      "weight": 2.5,
      ...
    }
  }
}
```

---

### Update Product Weight

**Endpoint:** `PUT /api/admin/products/<product_id>`

**Authentication:** Required (Admin token)

**Request Body (partial update):**
```json
{
  "weight": 3.0
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Product updated successfully",
  "data": {
    "product": {
      "id": 100,
      "weight": 3.0,
      ...
    }
  }
}
```

---

### Get Product (includes weight)

**Endpoint:** `GET /api/products/<product_id>`

**Authentication:** Not required

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "product": {
      "id": 100,
      "item": "Laptop",
      "price": 500000,
      "weight": 2.5,
      ...
    }
  }
}
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created successfully |
| 400 | Bad request - Invalid input or validation error |
| 401 | Unauthorized - Invalid or missing token |
| 404 | Not found - Resource doesn't exist |
| 410 | Gone - Resource expired (e.g., quote) |
| 500 | Internal server error - Sendbox API error or server issue |

### Common Error Responses

**Missing Required Field:**
```json
{
  "status": "error",
  "message": "'first_name' is required"
}
```

**Invalid Address:**
```json
{
  "status": "error",
  "message": "Invalid address: Phone number must start with country code (e.g., +234)"
}
```

**Address Not Found:**
```json
{
  "status": "error",
  "message": "Address not found"
}
```

**Product Not Found:**
```json
{
  "status": "error",
  "message": "Product 999 not found"
}
```

**Sendbox API Error:**
```json
{
  "status": "error",
  "message": "Sendbox API error: Authentication failed",
  "error_code": 401
}
```

**Invalid Weight:**
```json
{
  "status": "error",
  "message": "Weight must be greater than 0"
}
```

---

## Workflow Examples

### Complete Shipping Quote Flow

1. **Create or select shipping address:**
   ```
   POST /api/addresses
   ```

2. **Get shipping quotes:**
   ```
   POST /api/shipping/quotes
   {
     "destination_address_id": 1,
     "items": [{"product_id": 55, "quantity": 2}]
   }
   ```

3. **Save quote_id for checkout:**
   ```
   Response: { "quote_id": 456, ... }
   ```

4. **Use quote in checkout (Phase 3)**

### Address Management Flow

1. **Create multiple addresses:**
   ```
   POST /api/addresses (home)
   POST /api/addresses (office)
   ```

2. **List all addresses:**
   ```
   GET /api/addresses
   ```

3. **Set preferred as default:**
   ```
   POST /api/addresses/2/set-default
   ```

4. **Use default in checkout:**
   ```
   GET /api/addresses/default
   ```

---

## Notes

- All monetary values are in Nigerian Naira (NGN)
- Timestamps are in format: `YYYY-MM-DD HH:MM:SS`
- Phone numbers are automatically formatted with country code
- Quotes expire after 24 hours
- Weight is measured in kilograms (KG)
- Addresses are user-specific (users can only access their own)
- Default address is automatically managed

---

## Support

For issues or questions, refer to:
- Main API documentation: `README.md`
- Orders API: `ORDERS_API_DOCUMENTATION.md`
- Sendbox API reference: `SENDBOX_D.md`
- Integration guide: `SENDBOX_INTEGRATION_PHASES.md`

---

**Last Updated:** April 20, 2026  
**Phase:** 2 - Shipping Quotes Integration  
**Status:** Complete


---

## Tracking & Webhooks

### Track Order by Internal Tracking Number

**Endpoint:** `GET /api/orders/track/<tracking_number>`

**Authentication:** None (Public endpoint)

**Description:** Track an order using the internal tracking number. Returns order details with enhanced Sendbox tracking information if available.

**Example Request:**
```bash
GET /api/orders/track/TS1713600000123
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "order": {
      "id": 1,
      "tracking": "TS1713600000123",
      "user_id": 5,
      "total_amount": 55000,
      "payment_method": "flutterwave",
      "payment_status": "paid",
      "order_status": "shipped",
      "delivery_status": "in_transit",
      "address": "123 Main Street, Lagos, Lagos, NG",
      "shipping_cost": 5000,
      "created_at": "2026-04-20 10:00:00",
      "items": [
        {
          "id": 1,
          "product_id": 55,
          "product_name": "Midea Refrigerator",
          "price": 50000,
          "quantity": 1,
          "size": "",
          "subtotal": 50000
        }
      ]
    },
    "tracking": {
      "order_tracking": "TS1713600000123",
      "sendbox_tracking_code": "SB123456789",
      "carrier": "DHL",
      "current_status": "in_transit",
      "order_status": "shipped",
      "delivery_status": "in_transit",
      "estimated_delivery_date": "2026-04-25",
      "tracking_timeline": [
        {
          "status": "pickup_completed",
          "description": "Package has been picked up",
          "location": "Lagos, Nigeria",
          "timestamp": "2026-04-20T10:30:00Z"
        },
        {
          "status": "in_transit",
          "description": "Package is in transit to destination",
          "location": "Abuja, Nigeria",
          "timestamp": "2026-04-21T14:20:00Z"
        }
      ],
      "last_updated": "2026-04-21T14:20:00Z",
      "current_location": "Abuja, Nigeria"
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

### Track Shipment by Sendbox Tracking Code

**Endpoint:** `GET /api/shipping/track/<tracking_code>`

**Authentication:** None (Public endpoint)

**Description:** Track a shipment using the Sendbox tracking code. Syncs latest tracking information from Sendbox API.

**Example Request:**
```bash
GET /api/shipping/track/SB123456789
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Tracking information retrieved successfully",
  "data": {
    "tracking": {
      "order_tracking": "TS1713600000123",
      "sendbox_tracking_code": "SB123456789",
      "carrier": "DHL",
      "current_status": "in_transit",
      "order_status": "shipped",
      "delivery_status": "in_transit",
      "estimated_delivery_date": "2026-04-25",
      "tracking_timeline": [
        {
          "status": "pickup_completed",
          "description": "Package has been picked up",
          "location": "Lagos, Nigeria",
          "timestamp": "2026-04-20T10:30:00Z",
          "date": "2026-04-20"
        },
        {
          "status": "in_transit",
          "description": "Package is in transit to destination",
          "location": "Abuja, Nigeria",
          "timestamp": "2026-04-21T14:20:00Z",
          "date": "2026-04-21"
        }
      ],
      "last_updated": "2026-04-21T14:20:00Z",
      "current_location": "Abuja, Nigeria"
    },
    "order_id": 1,
    "order_tracking": "TS1713600000123"
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Shipment not found for tracking code"
}
```

---

### Sendbox Webhook Handler

**Endpoint:** `POST /api/webhooks/sendbox`

**Authentication:** None (Public endpoint - called by Sendbox)

**Description:** Receives real-time tracking updates from Sendbox. Automatically updates order status when shipment status changes.

**Webhook Payload Example:**
```json
{
  "event": "shipment.status_updated",
  "tracking_code": "SB123456789",
  "shipment_id": 12345,
  "status": "in_transit",
  "timestamp": "2026-04-21T14:20:00Z",
  "data": {
    "carrier": "DHL",
    "current_location": "Abuja, Nigeria",
    "estimated_delivery": "2026-04-25"
  }
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Webhook processed successfully",
  "data": {
    "order_id": 1,
    "tracking_code": "SB123456789",
    "status": "in_transit",
    "order_status": "shipped",
    "delivery_status": "in_transit"
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Order not found for tracking code"
}
```

**Notes:**
- This endpoint is called automatically by Sendbox
- All webhook events are logged to the `webhook_events` table
- Order status is updated automatically based on Sendbox status
- Failed webhooks are logged with error messages for debugging

---

### Test Webhook Endpoint

**Endpoint:** `POST /api/webhooks/test`

**Authentication:** None

**Description:** Test endpoint to verify webhook configuration and reception.

**Request Body:**
```json
{
  "test": "data",
  "any": "payload"
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Test webhook received",
  "received_data": {
    "test": "data",
    "any": "payload"
  }
}
```

---

### Bulk Sync Tracking (Admin)

**Endpoint:** `POST /api/admin/shipping/sync-tracking`

**Authentication:** Required (Admin token)

**Description:** Bulk synchronize tracking information for multiple orders from Sendbox.

**Request Body:**
```json
{
  "order_ids": [1, 2, 3, 4, 5]
}
```

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

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "'order_ids' is required and must be an array"
}
```

---

## Status Mapping Reference

### Sendbox Status to Internal Status Mapping

| Sendbox Status | Internal Order Status | Internal Delivery Status | Description |
|----------------|----------------------|-------------------------|-------------|
| drafted | processing | Pending | Shipment created and awaiting processing |
| pending | processing | Pending | Shipment is pending pickup |
| pickup_started | processing | Pending | Courier is on the way to pick up |
| pickup_completed | shipped | in_transit | Package has been picked up |
| in_transit | shipped | in_transit | Package is in transit to destination |
| in_delivery | shipped | in_transit | Package is out for delivery |
| delivered | delivered | delivered | Package has been delivered |
| cancelled | cancelled | Pending | Shipment has been cancelled |
| failed | processing | Pending | Delivery attempt failed |

---

## Tracking Timeline Events

### Event Structure
```json
{
  "status": "string",
  "description": "string",
  "location": "string (optional)",
  "timestamp": "ISO 8601 datetime",
  "date": "YYYY-MM-DD (optional)"
}
```

### Status Descriptions

| Status | Description |
|--------|-------------|
| drafted | Shipment created and awaiting processing |
| pending | Shipment is pending pickup |
| pickup_started | Courier is on the way to pick up your package |
| pickup_completed | Package has been picked up |
| in_transit | Package is in transit to destination |
| in_delivery | Package is out for delivery |
| delivered | Package has been delivered |
| cancelled | Shipment has been cancelled |
| failed | Delivery attempt failed |

---

## Webhook Configuration

### Setting Up Webhooks

1. **Staging Environment:**
   - Log in to https://developers.staging.sendbox.co/
   - Navigate to Webhooks settings
   - Add webhook URL: `https://yourdomain.com/api/webhooks/sendbox`
   - Select events: Shipment status updates
   - Save configuration

2. **Production Environment:**
   - Log in to https://live.sendbox.co/
   - Add production webhook URL
   - Test webhook delivery

### Webhook Events

Sendbox sends webhooks for the following events:
- `shipment.created` - When shipment is created
- `shipment.status_updated` - When shipment status changes
- `shipment.delivered` - When shipment is delivered
- `shipment.cancelled` - When shipment is cancelled

### Webhook Security

- All webhooks are logged to `webhook_events` table
- Failed webhooks are marked with `processed = FALSE`
- Error messages stored for debugging
- TODO: Implement webhook signature verification (if Sendbox provides)

---

## Database Tables

### webhook_events

Stores all incoming webhook events:

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| event_type | VARCHAR(100) | Type of webhook event |
| order_id | INT | Associated order ID (nullable) |
| sendbox_tracking_code | VARCHAR(100) | Tracking code |
| payload | JSON | Full webhook payload |
| processed | BOOLEAN | Whether webhook was processed |
| processed_at | TIMESTAMP | When webhook was processed |
| error_message | TEXT | Error if processing failed |
| created_at | TIMESTAMP | When webhook was received |

**Query Examples:**
```sql
-- View recent webhooks
SELECT * FROM webhook_events 
ORDER BY created_at DESC 
LIMIT 10;

-- View failed webhooks
SELECT * FROM webhook_events 
WHERE processed = FALSE;

-- View webhooks for specific order
SELECT * FROM webhook_events 
WHERE order_id = 1;
```

---

## Integration Examples

### Complete Tracking Flow

1. **Customer Places Order:**
```bash
POST /api/checkout
{
  "address_id": 1,
  "payment_method": "flutterwave",
  "transaction_id": "FLW123456",
  "items": [...],
  "selected_shipping": {
    "quote_id": 1,
    "carrier": "DHL",
    "service_code": "standard",
    "shipping_cost": 5000
  }
}
```

2. **Shipment Created Automatically:**
- Order is paid → Sendbox shipment created
- Order updated with `sendbox_tracking_code`
- Callback URL registered: `/api/webhooks/sendbox`

3. **Sendbox Sends Webhook:**
```json
POST /api/webhooks/sendbox
{
  "event": "shipment.status_updated",
  "tracking_code": "SB123456789",
  "status": "in_transit"
}
```

4. **Order Status Updated Automatically:**
- Webhook received and processed
- Order status: `processing` → `shipped`
- Delivery status: `Pending` → `in_transit`

5. **Customer Tracks Order:**
```bash
GET /api/orders/track/TS1713600000123
# or
GET /api/shipping/track/SB123456789
```

6. **Customer Sees Updated Status:**
- Tracking timeline with all events
- Current location and carrier
- Estimated delivery date

---

## Troubleshooting

### Webhooks Not Received

**Check webhook URL is accessible:**
```bash
curl -X POST https://yourdomain.com/api/webhooks/test \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

**Verify Sendbox configuration:**
- Check webhook URL in Sendbox portal
- Ensure URL is publicly accessible
- Verify events are selected

**Review webhook logs:**
```sql
SELECT * FROM webhook_events 
WHERE processed = FALSE 
ORDER BY created_at DESC;
```

### Tracking Not Updating

**Check Sendbox API connectivity:**
```bash
curl http://localhost:5000/api/shipping/track/SB123456789
```

**Force refresh tracking (Admin):**
```bash
curl -X POST http://localhost:5000/api/admin/orders/1/refresh-tracking \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

**Check order has tracking code:**
```sql
SELECT id, tracking, sendbox_tracking_code, sendbox_status 
FROM orders 
WHERE id = 1;
```

---

## Related Documentation

- **Phase 4 Completion Summary:** `PHASE4_COMPLETION_SUMMARY.md`
- **Phase 4 Ready Guide:** `PHASE4_READY.md`
- **Integration Plan:** `SENDBOX_INTEGRATION_PHASES.md`
- **Sendbox API Reference:** `SENDBOX_D.md`

---

**Last Updated:** April 20, 2026
**Phase:** 4 - Tracking Integration Complete
