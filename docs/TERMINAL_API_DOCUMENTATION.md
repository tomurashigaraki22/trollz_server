# Terminal Africa API Documentation

Complete API reference for Terminal Africa integration with Postman examples.

---

## Base Configuration

### Base URL
```
https://api.terminal.africa/v1
```

### Authentication
All requests require Bearer token authentication using your secret key:

**Test Environment:**
```
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

**Live Environment:**
```
Authorization: Bearer sk_live_jiep2FyoHX3tImNV4eVkdVl1SXIHrFWM
```

### Headers
```
Content-Type: application/json
Authorization: Bearer {SECRET_KEY}
```

---

## 1. User & Account Management

### 1.1 Get User Profile

**Endpoint:** `GET /users/profile`

**Description:** Get your user profile and account information.

**Postman Example:**
```http
GET https://api.terminal.africa/v1/users/profile
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": "user_xxx",
    "name": "Trollz Store",
    "email": "warehouse@trollzstore.com",
    "phone": "+234 800 000 0000",
    "created_at": "2026-01-01T00:00:00Z"
  }
}
```

### 1.2 Get Wallet Balance

**Endpoint:** `GET /wallets/balance`

**Description:** Get your wallet balance.

**Postman Example:**
```http
GET https://api.terminal.africa/v1/wallets/balance
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

**Response:**
```json
{
  "success": true,
  "data": {
    "balance": 50000.00,
    "currency": "NGN",
    "available_balance": 45000.00,
    "pending_balance": 5000.00
  }
}
```

---

## 2. Address Management

### 2.1 Create Address

**Endpoint:** `POST /addresses`

**Description:** Create a new address in Terminal Africa.

**Postman Example:**
```http
POST https://api.terminal.africa/v1/addresses
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+2348012345678",
  "email": "john@example.com",
  "line1": "123 Main Street",
  "line2": "Apartment 4B",
  "city": "Lagos",
  "state": "Lagos",
  "country": "NG",
  "zip": "100001",
  "is_residential": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "address_id": "addr_xxx123",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+2348012345678",
    "email": "john@example.com",
    "line1": "123 Main Street",
    "line2": "Apartment 4B",
    "city": "Lagos",
    "state": "Lagos",
    "country": "NG",
    "zip": "100001",
    "is_residential": true,
    "created_at": "2026-05-04T10:00:00Z"
  }
}
```

### 2.2 List Addresses

**Endpoint:** `GET /addresses`

**Description:** Get all addresses with pagination.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `perPage` (optional): Items per page (default: 20)

**Postman Example:**
```http
GET https://api.terminal.africa/v1/addresses?page=1&perPage=20
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "address_id": "addr_xxx123",
      "first_name": "John",
      "last_name": "Doe",
      "city": "Lagos",
      "state": "Lagos",
      "country": "NG"
    }
  ],
  "pagination": {
    "page": 1,
    "perPage": 20,
    "total": 5,
    "totalPages": 1
  }
}
```

### 2.3 Get Address

**Endpoint:** `GET /addresses/{address_id}`

**Description:** Get a specific address by ID.

**Postman Example:**
```http
GET https://api.terminal.africa/v1/addresses/addr_xxx123
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

### 2.4 Update Address

**Endpoint:** `PATCH /addresses/{address_id}`

**Description:** Update an existing address.

**Postman Example:**
```http
PATCH https://api.terminal.africa/v1/addresses/addr_xxx123
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
Content-Type: application/json

{
  "phone": "+2348087654321",
  "line2": "Suite 5C"
}
```

### 2.5 Delete Address

**Endpoint:** `DELETE /addresses/{address_id}`

**Description:** Delete an address.

**Postman Example:**
```http
DELETE https://api.terminal.africa/v1/addresses/addr_xxx123
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

---

## 3. Packaging Management

### 3.1 Create Packaging

**Endpoint:** `POST /packaging`

**Description:** Create a new packaging option.

**Postman Example:**
```http
POST https://api.terminal.africa/v1/packaging
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
Content-Type: application/json

{
  "name": "Medium Box",
  "type": "box",
  "length": 30,
  "width": 25,
  "height": 20,
  "weight": 1.0,
  "size_unit": "cm",
  "weight_unit": "kg"
}
```

**Packaging Types:**
- `box` - Standard box
- `envelope` - Envelope/flat package
- `soft-packaging` - Soft/flexible packaging

**Response:**
```json
{
  "success": true,
  "data": {
    "packaging_id": "pkg_xxx123",
    "name": "Medium Box",
    "type": "box",
    "length": 30,
    "width": 25,
    "height": 20,
    "weight": 1.0,
    "size_unit": "cm",
    "weight_unit": "kg",
    "created_at": "2026-05-04T10:00:00Z"
  }
}
```

### 3.2 List Packaging

**Endpoint:** `GET /packaging`

**Description:** Get all packaging options.

**Postman Example:**
```http
GET https://api.terminal.africa/v1/packaging?page=1&perPage=20
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

### 3.3 Get Packaging

**Endpoint:** `GET /packaging/{packaging_id}`

**Description:** Get a specific packaging by ID.

**Postman Example:**
```http
GET https://api.terminal.africa/v1/packaging/pkg_xxx123
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

### 3.4 Delete Packaging

**Endpoint:** `DELETE /packaging/{packaging_id}`

**Description:** Delete a packaging option.

**Postman Example:**
```http
DELETE https://api.terminal.africa/v1/packaging/pkg_xxx123
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

---

## 4. Parcel Management

### 4.1 Create Parcel

**Endpoint:** `POST /parcels`

**Description:** Create a new parcel with items.

**Postman Example:**
```http
POST https://api.terminal.africa/v1/parcels
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
Content-Type: application/json

{
  "packaging": "pkg_xxx123",
  "description": "Fashion items",
  "items": [
    {
      "name": "T-Shirt",
      "quantity": 2,
      "value": 5000,
      "weight": 0.5,
      "description": "Cotton T-Shirt",
      "currency": "NGN"
    },
    {
      "name": "Jeans",
      "quantity": 1,
      "value": 8000,
      "weight": 0.8,
      "description": "Denim Jeans",
      "currency": "NGN"
    }
  ],
  "weight": 1.8,
  "weight_unit": "kg"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "parcel_id": "parcel_xxx123",
    "packaging_id": "pkg_xxx123",
    "description": "Fashion items",
    "items": [...],
    "total_weight": 1.8,
    "weight_unit": "kg",
    "total_value": 18000,
    "currency": "NGN",
    "created_at": "2026-05-04T10:00:00Z"
  }
}
```

### 4.2 List Parcels

**Endpoint:** `GET /parcels`

**Description:** Get all parcels.

**Postman Example:**
```http
GET https://api.terminal.africa/v1/parcels?page=1&perPage=20
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

### 4.3 Get Parcel

**Endpoint:** `GET /parcels/{parcel_id}`

**Description:** Get a specific parcel by ID.

**Postman Example:**
```http
GET https://api.terminal.africa/v1/parcels/parcel_xxx123
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

---

## 5. Carrier Management

### 5.1 List Carriers

**Endpoint:** `GET /carriers`

**Description:** Get all available carriers.

**Query Parameters:**
- `active` (optional): Filter by active status (true/false)
- `domestic` (optional): Filter domestic carriers (true/false)
- `regional` (optional): Filter regional carriers (true/false)
- `international` (optional): Filter international carriers (true/false)

**Postman Example:**
```http
GET https://api.terminal.africa/v1/carriers?active=true&domestic=true
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "carrier_id": "carrier_dhl",
      "name": "DHL",
      "slug": "dhl",
      "logo": "https://...",
      "active": true,
      "domestic": true,
      "regional": true,
      "international": true,
      "requires_invoice": false,
      "requires_waybill": false,
      "supports_multi_parcels": true
    },
    {
      "carrier_id": "carrier_fedex",
      "name": "FedEx",
      "slug": "fedex",
      "logo": "https://...",
      "active": true,
      "domestic": false,
      "regional": true,
      "international": true
    }
  ]
}
```

### 5.2 Enable Carrier

**Endpoint:** `POST /carriers/{carrier_id}/enable`

**Description:** Enable a carrier for your account.

**Postman Example:**
```http
POST https://api.terminal.africa/v1/carriers/carrier_dhl/enable
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

### 5.3 Disable Carrier

**Endpoint:** `POST /carriers/{carrier_id}/disable`

**Description:** Disable a carrier for your account.

**Postman Example:**
```http
POST https://api.terminal.africa/v1/carriers/carrier_dhl/disable
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

---

## 6. Rate Management

### 6.1 Get Shipping Rates

**Endpoint:** `POST /rates`

**Description:** Get shipping rates from multiple carriers.

**Postman Example:**
```http
POST https://api.terminal.africa/v1/rates
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
Content-Type: application/json

{
  "origin_address": "addr_origin123",
  "destination_address": "addr_dest456",
  "parcel": "parcel_xxx123",
  "currency": "NGN"
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "rate_id": "rate_xxx123",
      "carrier": {
        "carrier_id": "carrier_dhl",
        "name": "DHL",
        "logo": "https://..."
      },
      "amount": 3500.00,
      "currency": "NGN",
      "delivery_time": "2-3 business days",
      "pickup_time": "Same day",
      "includes_insurance": false,
      "insurance_fee": 0,
      "estimated_delivery_date": "2026-05-07"
    },
    {
      "rate_id": "rate_xxx124",
      "carrier": {
        "carrier_id": "carrier_fedex",
        "name": "FedEx",
        "logo": "https://..."
      },
      "amount": 4200.00,
      "currency": "NGN",
      "delivery_time": "1-2 business days",
      "pickup_time": "Same day"
    }
  ]
}
```

---

## 7. Shipment Management

### 7.1 Create Shipment

**Endpoint:** `POST /shipments`

**Description:** Create a new shipment using a selected rate.

**Postman Example:**
```http
POST https://api.terminal.africa/v1/shipments
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
Content-Type: application/json

{
  "rate_id": "rate_xxx123",
  "origin_address": "addr_origin123",
  "destination_address": "addr_dest456",
  "parcel": "parcel_xxx123",
  "metadata": {
    "order_id": "12345",
    "customer_name": "John Doe"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "shipment_id": "shipment_xxx123",
    "tracking_number": "TRK123456789",
    "carrier": {
      "carrier_id": "carrier_dhl",
      "name": "DHL"
    },
    "status": "pending",
    "amount": 3500.00,
    "currency": "NGN",
    "label_url": "https://terminal.africa/labels/xxx.pdf",
    "invoice_url": "https://terminal.africa/invoices/xxx.pdf",
    "tracking_url": "https://terminal.africa/track/xxx",
    "estimated_delivery_date": "2026-05-07",
    "created_at": "2026-05-04T10:00:00Z"
  }
}
```

### 7.2 List Shipments

**Endpoint:** `GET /shipments`

**Description:** Get all shipments with pagination.

**Query Parameters:**
- `page` (optional): Page number
- `perPage` (optional): Items per page
- `status` (optional): Filter by status

**Postman Example:**
```http
GET https://api.terminal.africa/v1/shipments?page=1&perPage=20&status=pending
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

**Shipment Statuses:**
- `pending` - Shipment created, awaiting pickup
- `in_transit` - Package in transit
- `out_for_delivery` - Out for delivery
- `delivered` - Successfully delivered
- `failed` - Delivery failed
- `cancelled` - Shipment cancelled

### 7.3 Get Shipment

**Endpoint:** `GET /shipments/{shipment_id}`

**Description:** Get a specific shipment by ID.

**Postman Example:**
```http
GET https://api.terminal.africa/v1/shipments/shipment_xxx123
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

### 7.4 Cancel Shipment

**Endpoint:** `POST /shipments/{shipment_id}/cancel`

**Description:** Cancel a shipment.

**Postman Example:**
```http
POST https://api.terminal.africa/v1/shipments/shipment_xxx123/cancel
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

---

## 8. Tracking

### 8.1 Track Shipment by ID

**Endpoint:** `GET /shipments/{shipment_id}/track`

**Description:** Track a shipment by Terminal shipment ID.

**Postman Example:**
```http
GET https://api.terminal.africa/v1/shipments/shipment_xxx123/track
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

**Response:**
```json
{
  "success": true,
  "data": {
    "shipment_id": "shipment_xxx123",
    "tracking_number": "TRK123456789",
    "status": "in_transit",
    "carrier": {
      "name": "DHL"
    },
    "events": [
      {
        "timestamp": "2026-05-04T10:00:00Z",
        "status": "pending",
        "description": "Shipment created",
        "location": "Lagos, Nigeria"
      },
      {
        "timestamp": "2026-05-04T14:00:00Z",
        "status": "picked_up",
        "description": "Package picked up",
        "location": "Lagos, Nigeria"
      },
      {
        "timestamp": "2026-05-05T09:00:00Z",
        "status": "in_transit",
        "description": "Package in transit",
        "location": "Abuja, Nigeria"
      }
    ],
    "estimated_delivery_date": "2026-05-07"
  }
}
```

### 8.2 Track by Tracking Number

**Endpoint:** `GET /tracking`

**Description:** Track a shipment by carrier tracking number.

**Query Parameters:**
- `tracking_number` (required): Carrier tracking number

**Postman Example:**
```http
GET https://api.terminal.africa/v1/tracking?tracking_number=TRK123456789
Authorization: Bearer sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

---

## 9. Postman Collection Setup

### Step 1: Create Environment

Create a new environment in Postman with these variables:

**Test Environment:**
```
base_url: https://api.terminal.africa/v1
secret_key: sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
public_key: pk_test_WeDJ1I1cKKkubg60rE6kXnwPJXlExlH1
```

**Live Environment:**
```
base_url: https://api.terminal.africa/v1
secret_key: sk_live_jiep2FyoHX3tImNV4eVkdVl1SXIHrFWM
public_key: pk_live_G8zfsoShEtgvDPUvHABwdF9Lw4a65HKg
```

### Step 2: Set Authorization

In Postman collection settings:
- Type: Bearer Token
- Token: `{{secret_key}}`

### Step 3: Set Headers

Add these headers to all requests:
```
Content-Type: application/json
Authorization: Bearer {{secret_key}}
```

---

## 10. Common Workflows

### Workflow 1: Complete Shipment Creation

1. **Create Origin Address** (warehouse)
2. **Create Destination Address** (customer)
3. **Create Packaging**
4. **Create Parcel** with items
5. **Get Rates** from multiple carriers
6. **Create Shipment** with selected rate
7. **Track Shipment**

### Workflow 2: Get Shipping Quote

1. **Create/Get Origin Address**
2. **Create/Get Destination Address**
3. **Create Packaging**
4. **Create Parcel**
5. **Get Rates**

### Workflow 3: Carrier Management

1. **List All Carriers**
2. **Enable Preferred Carriers**
3. **Disable Unwanted Carriers**
4. **Get Rates** (only enabled carriers will return rates)

---

## 11. Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Invalid request data",
  "errors": {
    "phone": "Phone number is required"
  }
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "message": "Authentication failed. Invalid API key."
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "email": "Invalid email format",
    "weight": "Weight must be greater than 0"
  }
}
```

---

## 12. Rate Limits

- **Test Environment**: 100 requests per minute
- **Live Environment**: 1000 requests per minute

---

## 13. Support

- **Documentation**: https://docs.terminal.africa/
- **API Reference**: https://developers.terminal.africa/
- **Support Email**: support@terminal.africa

---

**Last Updated**: 2026-05-04  
**API Version**: v1

