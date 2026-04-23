# Mobile App Integration Guide - Sendbox Shipping

## Overview
This guide provides complete documentation for integrating the Trollz Store Sendbox shipping features into your mobile application. It covers all API endpoints, request/response formats, workflows, and best practices.

**API Base URL:** `https://api.trollzstore.com` (replace with your actual domain)

**API Version:** 1.0

**Last Updated:** April 20, 2026

---

## Table of Contents
1. [Authentication](#authentication)
2. [Shipping Address Management](#shipping-address-management)
3. [Shipping Quotes](#shipping-quotes)
4. [Checkout with Shipping](#checkout-with-shipping)
5. [Order Tracking](#order-tracking)
6. [Complete User Flows](#complete-user-flows)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)

---

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header.

```http
Authorization: Bearer YOUR_USER_TOKEN
```

### Login to Get Token

**Endpoint:** `POST /api/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "userpassword"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 5,
      "email": "user@example.com",
      "name": "John Doe"
    }
  }
}
```

---

## Shipping Address Management

### 1. Create Shipping Address

**Endpoint:** `POST /api/addresses`

**Authentication:** Required

**Description:** Save a new shipping address for the user.

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
  "is_default": false
}
```

**Required Fields:**
- `first_name` (string)
- `last_name` (string)
- `phone` (string)
- `street` (string)
- `city` (string)
- `state` (string)

**Optional Fields:**
- `email` (string)
- `street_line_2` (string)
- `country` (string, default: "NG")
- `post_code` (string)
- `lng` (decimal) - Longitude
- `lat` (decimal) - Latitude
- `is_default` (boolean, default: false)

**Success Response (201 Created):**
```json
{
  "status": "success",
  "message": "Address created successfully",
  "data": {
    "address": {
      "id": 1,
      "user_id": 5,
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
      "is_default": false,
      "created_at": "2026-04-20 10:00:00"
    }
  }
}
```

---

### 2. List User Addresses

**Endpoint:** `GET /api/addresses`

**Authentication:** Required

**Description:** Get all shipping addresses for the authenticated user.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "addresses": [
      {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+234 800 123 4567",
        "street": "123 Main Street",
        "city": "Lagos",
        "state": "Lagos",
        "country": "NG",
        "is_default": true
      },
      {
        "id": 2,
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+234 800 123 4567",
        "street": "456 Work Avenue",
        "city": "Abuja",
        "state": "FCT",
        "country": "NG",
        "is_default": false
      }
    ]
  }
}
```

---

### 3. Get Single Address

**Endpoint:** `GET /api/addresses/<address_id>`

**Authentication:** Required

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "address": {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "phone": "+234 800 123 4567",
      "email": "john@example.com",
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

### 4. Update Address

**Endpoint:** `PUT /api/addresses/<address_id>`

**Authentication:** Required

**Request Body:** (all fields optional)
```json
{
  "first_name": "John",
  "phone": "08009876543",
  "is_default": true
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
      "first_name": "John",
      "phone": "+234 800 987 6543",
      "is_default": true
    }
  }
}
```

---

### 5. Delete Address

**Endpoint:** `DELETE /api/addresses/<address_id>`

**Authentication:** Required

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Address deleted successfully"
}
```

---

### 6. Set Default Address

**Endpoint:** `POST /api/addresses/<address_id>/set-default`

**Authentication:** Required

**Description:** Set an address as the default shipping address.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Default address updated successfully",
  "data": {
    "address": {
      "id": 1,
      "is_default": true
    }
  }
}
```

---

### 7. Get Default Address

**Endpoint:** `GET /api/addresses/default`

**Authentication:** Required

**Description:** Get the user's default shipping address.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "address": {
      "id": 1,
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

## Shipping Quotes

### Get Shipping Quotes

**Endpoint:** `POST /api/shipping/quotes`

**Authentication:** Required

**Description:** Get shipping quotes from Sendbox for a list of items to a destination address.

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
      "product_id": 60,
      "quantity": 1
    }
  ],
  "service_code": "standard"
}
```

**Fields:**
- `destination_address_id` (integer, required) - ID of shipping address
- `items` (array, required) - List of items to ship
  - `product_id` (integer, required)
  - `quantity` (integer, required)
- `service_code` (string, optional) - "standard", "premium", or "expedient" (default: "standard")
- `pickup_date` (string, optional) - ISO date format "YYYY-MM-DD"

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Shipping quotes retrieved successfully",
  "data": {
    "quote_id": 123,
    "quotes": {
      "amount": 5000,
      "currency": "NGN",
      "carrier": "DHL",
      "service_code": "standard",
      "estimated_delivery_days": 3
    },
    "summary": {
      "total_weight": 3.5,
      "total_value": 75000,
      "service_type": "local",
      "service_code": "standard",
      "origin": "Lagos, Lagos",
      "destination": "Abuja, FCT",
      "expires_at": "2026-04-21 10:00:00"
    }
  }
}
```

**Important Notes:**
- Quotes expire after 24 hours
- Save the `quote_id` to use during checkout
- The `amount` is the shipping cost in the specified currency

---

### Calculate Landed Cost (International)

**Endpoint:** `POST /api/shipping/landed-cost`

**Authentication:** Required

**Description:** Calculate total landed cost including duties and taxes for international shipments.

**Request Body:** (same as shipping quotes)
```json
{
  "destination_address_id": 1,
  "items": [
    {
      "product_id": 55,
      "quantity": 1
    }
  ]
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Landed cost calculated successfully",
  "data": {
    "landed_cost": {
      "shipping_cost": 15000,
      "duties": 5000,
      "taxes": 3000,
      "total_landed_cost": 23000,
      "currency": "NGN"
    },
    "summary": {
      "total_weight": 2.5,
      "total_value": 50000,
      "origin": "Lagos, Lagos, NG",
      "destination": "New York, NY, US"
    }
  }
}
```

---

## Checkout with Shipping

### Create Order with Shipping

**Endpoint:** `POST /api/checkout`

**Authentication:** Required

**Description:** Create a new order with shipping information.

**Request Body:**
```json
{
  "address_id": 1,
  "payment_method": "flutterwave",
  "transaction_id": "FLW123456789",
  "items": [
    {
      "product_id": 55,
      "quantity": 2,
      "size": "XL"
    }
  ],
  "selected_shipping": {
    "quote_id": 123,
    "carrier": "DHL",
    "service_code": "standard",
    "shipping_cost": 5000
  }
}
```

**Required Fields:**
- `address_id` (integer) - Shipping address ID
- `payment_method` (string) - "flutterwave", "paystack", or "cash_on_delivery"
- `items` (array) - List of items to order
  - `product_id` (integer, required)
  - `quantity` (integer, required)
  - `size` (string, optional)

**Optional Fields:**
- `transaction_id` (string) - Payment transaction ID (required if paid)
- `selected_shipping` (object) - Shipping selection
  - `quote_id` (integer, optional) - Quote ID from shipping quotes
  - `carrier` (string, optional)
  - `service_code` (string, optional)
  - `shipping_cost` (number, required)

**Success Response (201 Created):**
```json
{
  "status": "success",
  "message": "Order created successfully",
  "data": {
    "order": {
      "id": 123,
      "tracking": "TS1713600000123",
      "user_id": 5,
      "total_amount": 105000,
      "payment_method": "flutterwave",
      "payment_status": "paid",
      "order_status": "processing",
      "delivery_status": "Pending",
      "address": "123 Main Street, Lagos, Lagos, NG",
      "shipping_cost": 5000,
      "created_at": "2026-04-20 10:00:00",
      "items": [
        {
          "product_id": 55,
          "product_name": "Midea Refrigerator",
          "price": 50000,
          "quantity": 2,
          "size": "XL",
          "subtotal": 100000
        }
      ]
    },
    "tracking_number": "TS1713600000123",
    "shipping": {
      "cost": 5000,
      "service_code": "standard",
      "shipment_created": true
    }
  }
}
```

**If Shipment Creation Fails:**
```json
{
  "status": "success",
  "message": "Order created successfully",
  "data": {
    "order": {...},
    "shipping": {
      "cost": 5000,
      "service_code": "standard",
      "shipment_created": false,
      "error": "Sendbox API error: ...",
      "note": "Shipment will be created automatically or can be created manually by admin"
    }
  }
}
```

**Important Notes:**
- Order is created even if shipment creation fails
- If `transaction_id` is provided, order is marked as paid and shipment is created automatically
- Save the `tracking` number to track the order later

---

## Order Tracking

### 1. Track Order by Tracking Number

**Endpoint:** `GET /api/orders/track/<tracking_number>`

**Authentication:** None (Public endpoint)

**Description:** Track an order using the internal tracking number.

**Example:** `GET /api/orders/track/TS1713600000123`

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "order": {
      "id": 123,
      "tracking": "TS1713600000123",
      "total_amount": 105000,
      "payment_status": "paid",
      "order_status": "shipped",
      "delivery_status": "in_transit",
      "address": "123 Main Street, Lagos, Lagos, NG",
      "shipping_cost": 5000,
      "created_at": "2026-04-20 10:00:00",
      "items": [...]
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
    }
  }
}
```

---

### 2. Track by Sendbox Tracking Code

**Endpoint:** `GET /api/shipping/track/<tracking_code>`

**Authentication:** None (Public endpoint)

**Description:** Track a shipment using the Sendbox tracking code.

**Example:** `GET /api/shipping/track/SB123456789`

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
      "tracking_timeline": [...]
    },
    "order_id": 123,
    "order_tracking": "TS1713600000123"
  }
}
```

---

### 3. Get User Orders

**Endpoint:** `GET /api/orders`

**Authentication:** Required

**Query Parameters:**
- `page` (integer, optional) - Page number (default: 1)
- `limit` (integer, optional) - Items per page (default: 20, max: 100)

**Example:** `GET /api/orders?page=1&limit=20`

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "orders": [
      {
        "id": 123,
        "tracking": "TS1713600000123",
        "total_amount": 105000,
        "order_status": "shipped",
        "delivery_status": "in_transit",
        "created_at": "2026-04-20 10:00:00",
        "items": [...]
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 50,
      "total_pages": 3
    }
  }
}
```

---

### 4. Get Single Order

**Endpoint:** `GET /api/orders/<order_id>`

**Authentication:** Required

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "order": {
      "id": 123,
      "tracking": "TS1713600000123",
      "total_amount": 105000,
      "payment_status": "paid",
      "order_status": "shipped",
      "delivery_status": "in_transit",
      "sendbox_tracking_code": "SB123456789",
      "sendbox_carrier": "DHL",
      "estimated_delivery_date": "2026-04-25",
      "items": [...]
    }
  }
}
```

---

## Complete User Flows

### Flow 1: Complete Checkout with Shipping

```
1. User adds items to cart
2. User proceeds to checkout
3. App fetches user's saved addresses
   GET /api/addresses
4. User selects or creates shipping address
   POST /api/addresses (if new)
5. App requests shipping quotes
   POST /api/shipping/quotes
   {
     "destination_address_id": 1,
     "items": [cart items]
   }
6. App displays shipping options to user
7. User selects shipping option
8. User completes payment (Flutterwave/Paystack)
9. App creates order with shipping
   POST /api/checkout
   {
     "address_id": 1,
     "transaction_id": "payment_id",
     "items": [cart items],
     "selected_shipping": {
       "quote_id": 123,
       "shipping_cost": 5000
     }
   }
10. App receives order confirmation with tracking number
11. App displays order confirmation to user
```

---

### Flow 2: Track Order

```
1. User opens "My Orders" screen
2. App fetches user's orders
   GET /api/orders
3. App displays list of orders
4. User taps on an order
5. App fetches order details
   GET /api/orders/<order_id>
6. App displays order details with tracking info
7. User taps "Track Shipment"
8. App fetches tracking details
   GET /api/orders/track/<tracking_number>
9. App displays tracking timeline with:
   - Current status
   - Tracking events
   - Estimated delivery date
   - Current location
   - Carrier information
```

---

### Flow 3: Manage Shipping Addresses

```
1. User opens "Shipping Addresses" screen
2. App fetches saved addresses
   GET /api/addresses
3. App displays list of addresses
4. User can:
   a. Add new address
      POST /api/addresses
   b. Edit existing address
      PUT /api/addresses/<id>
   c. Delete address
      DELETE /api/addresses/<id>
   d. Set default address
      POST /api/addresses/<id>/set-default
```

---

## Error Handling

### Standard Error Response Format

```json
{
  "status": "error",
  "message": "Error description"
}
```

### HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Operation not allowed
- `404 Not Found` - Resource not found
- `410 Gone` - Resource expired (e.g., quote expired)
- `500 Internal Server Error` - Server error

### Common Error Messages

**Authentication Errors:**
```json
{
  "status": "error",
  "message": "No token provided"
}
```

**Validation Errors:**
```json
{
  "status": "error",
  "message": "'address_id' is required"
}
```

**Resource Not Found:**
```json
{
  "status": "error",
  "message": "Address not found"
}
```

**Quote Expired:**
```json
{
  "status": "error",
  "message": "Shipping quote has expired. Please request a new quote."
}
```

**Insufficient Stock:**
```json
{
  "status": "error",
  "message": "Insufficient stock for Midea Refrigerator. Available: 5"
}
```

### Error Handling in Mobile App

```javascript
// Example error handling
try {
  const response = await fetch('/api/shipping/quotes', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
  });
  
  const data = await response.json();
  
  if (response.ok && data.status === 'success') {
    // Handle success
    return data.data;
  } else {
    // Handle error
    throw new Error(data.message || 'Request failed');
  }
} catch (error) {
  // Handle network or other errors
  console.error('Error:', error.message);
  // Show error to user
  showErrorMessage(error.message);
}
```

---

## Best Practices

### 1. Caching

**Cache User Addresses:**
- Cache addresses locally after fetching
- Refresh when user adds/updates/deletes
- Use cached data for offline viewing

**Cache Shipping Quotes:**
- Cache quotes for 24 hours (expiration time)
- Clear cache when quote expires
- Request new quote if expired

**Cache Order Data:**
- Cache order list locally
- Refresh on pull-to-refresh
- Cache individual order details

### 2. Loading States

**Show Loading Indicators:**
- When fetching addresses
- When requesting shipping quotes
- When creating order
- When fetching tracking info

**Provide Feedback:**
- "Calculating shipping costs..."
- "Creating your order..."
- "Fetching tracking information..."

### 3. Error Handling

**User-Friendly Messages:**
- Convert technical errors to user-friendly messages
- Provide actionable solutions
- Allow retry for failed operations

**Offline Handling:**
- Detect network errors
- Show offline message
- Queue operations for retry when online

### 4. Performance

**Optimize API Calls:**
- Batch requests when possible
- Use pagination for lists
- Implement pull-to-refresh
- Cache responses appropriately

**Reduce Data Transfer:**
- Only request needed fields
- Use pagination
- Compress images

### 5. Security

**Protect Tokens:**
- Store tokens securely (Keychain/Keystore)
- Never log tokens
- Refresh tokens before expiry
- Clear tokens on logout

**Validate Input:**
- Validate all user input before sending
- Sanitize data
- Handle special characters

### 6. User Experience

**Address Management:**
- Allow quick address selection
- Show default address first
- Enable address search/autocomplete
- Validate addresses before submission

**Shipping Selection:**
- Display shipping options clearly
- Show estimated delivery dates
- Highlight recommended option
- Show cost breakdown

**Order Tracking:**
- Show visual timeline
- Update automatically
- Push notifications for status changes
- Allow sharing tracking info

---

## Status Reference

### Order Statuses

| Status | Description | User Display |
|--------|-------------|--------------|
| processing | Order is being processed | "Processing" |
| shipped | Order has been shipped | "Shipped" |
| delivered | Order has been delivered | "Delivered" |
| cancelled | Order has been cancelled | "Cancelled" |

### Delivery Statuses

| Status | Description | User Display |
|--------|-------------|--------------|
| Pending | Awaiting shipment | "Pending Shipment" |
| in_transit | Package in transit | "In Transit" |
| delivered | Package delivered | "Delivered" |

### Sendbox Statuses

| Status | Description | User Display |
|--------|-------------|--------------|
| drafted | Shipment created | "Shipment Created" |
| pending | Awaiting pickup | "Awaiting Pickup" |
| pickup_started | Courier on the way | "Pickup in Progress" |
| pickup_completed | Package picked up | "Picked Up" |
| in_transit | In transit | "In Transit" |
| in_delivery | Out for delivery | "Out for Delivery" |
| delivered | Delivered | "Delivered" |
| cancelled | Cancelled | "Cancelled" |
| failed | Delivery failed | "Delivery Failed" |

---

## Testing

### Test Credentials

**Staging Environment:**
- Base URL: `https://staging-api.trollzstore.com`
- Test User: `test@example.com` / `testpassword`
- Test Admin: `admin@example.com` / `adminpassword`

### Test Data

**Test Products:**
- Product ID: 1 (Test Product, ₦10,000, 0.5kg)
- Product ID: 55 (Midea Refrigerator, ₦50,000, 2.5kg)

**Test Addresses:**
- Lagos: "123 Test Street, Lagos, Lagos, NG"
- Abuja: "456 Test Avenue, Abuja, FCT, NG"

### Test Scenarios

1. **Create Address and Get Quotes:**
   - Create shipping address
   - Request shipping quotes
   - Verify quote response

2. **Complete Checkout:**
   - Add items to cart
   - Get shipping quotes
   - Create order with shipping
   - Verify order created

3. **Track Order:**
   - Get order tracking number
   - Track order
   - Verify tracking info

---

## Support

### API Issues

For API-related issues:
1. Check error message in response
2. Verify request format matches documentation
3. Check authentication token is valid
4. Review API logs (if available)

### Integration Support

For integration help:
- Review this documentation
- Check example requests/responses
- Test in staging environment first
- Contact backend team for API issues

---

## Changelog

### Version 1.0 (April 20, 2026)
- Initial release
- Complete Sendbox integration
- Address management
- Shipping quotes
- Order tracking
- Admin features

---

## Appendix

### Example Mobile App Screens

**1. Shipping Address Screen:**
- List of saved addresses
- Add new address button
- Edit/Delete options
- Set default option

**2. Shipping Options Screen:**
- List of shipping quotes
- Carrier logos
- Estimated delivery dates
- Shipping costs
- Recommended option highlighted

**3. Order Tracking Screen:**
- Order summary
- Tracking timeline (vertical)
- Current status highlighted
- Estimated delivery date
- Carrier information
- Share tracking button

**4. Order Details Screen:**
- Order number
- Order date
- Items list
- Shipping address
- Shipping cost
- Total amount
- Payment status
- Track shipment button

---

**Document Version:** 1.0
**Last Updated:** April 20, 2026
**For:** Mobile App Development Team
**API Version:** 1.0
