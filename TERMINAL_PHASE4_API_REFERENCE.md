# Terminal Africa Phase 4 - API Reference

Complete API reference for Terminal Africa shipping endpoints.

---

## Authentication

All endpoints require JWT authentication.

**Header**:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Get Token**:
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}
```

---

## Endpoints

### 1. Get Carriers

Get available shipping carriers from Terminal Africa.

**Endpoint**: `GET /api/shipping/carriers`

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| active | boolean | No | Filter by active status |
| domestic | boolean | No | Filter domestic carriers |
| regional | boolean | No | Filter regional carriers |
| international | boolean | No | Filter international carriers |

**Example Request**:
```bash
GET /api/shipping/carriers?active=true&international=true
Authorization: Bearer YOUR_TOKEN
```

**Success Response** (200):
```json
{
  "status": "success",
  "message": "Carriers retrieved successfully",
  "data": {
    "carriers": [
      {
        "carrier_id": "CA-81957188177",
        "name": "DHL Express",
        "slug": "dhl-express",
        "logo": "https://terminal.africa/carriers/dhl.png",
        "active": true,
        "domestic": true,
        "regional": true,
        "international": true
      }
    ],
    "count": 35,
    "active_count": 21
  }
}
```

**Error Response** (500):
```json
{
  "status": "error",
  "message": "Terminal API error: Authentication failed",
  "error_code": 401
}
```

---

### 2. Get Packaging Options

Get available packaging options from Terminal Africa.

**Endpoint**: `GET /api/shipping/packaging`

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| page | integer | No | 1 | Page number |
| per_page | integer | No | 20 | Items per page (max: 100) |

**Example Request**:
```bash
GET /api/shipping/packaging?page=1&per_page=20
Authorization: Bearer YOUR_TOKEN
```

**Success Response** (200):
```json
{
  "status": "success",
  "message": "Packaging options retrieved successfully",
  "data": {
    "packaging": [
      {
        "packaging_id": "PA-123ABC",
        "name": "Small Box",
        "type": "box",
        "length": 20,
        "width": 15,
        "height": 10,
        "weight": 0.5,
        "size_unit": "cm",
        "weight_unit": "kg"
      }
    ],
    "count": 15,
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 15,
      "total_pages": 1
    }
  }
}
```

---

### 3. Create Packaging

Create a new packaging option in Terminal Africa.

**Endpoint**: `POST /api/shipping/packaging`

**Request Body**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Package name |
| type | string | Yes | Package type: `box`, `envelope`, `soft-packaging` |
| length | number | Yes | Length in size_unit |
| width | number | Yes | Width in size_unit |
| height | number | Yes | Height in size_unit |
| weight | number | Yes | Weight in weight_unit |
| size_unit | string | No | Size unit: `cm` or `in` (default: `cm`) |
| weight_unit | string | No | Weight unit: `kg` or `lb` (default: `kg`) |

**Example Request**:
```bash
POST /api/shipping/packaging
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "name": "Custom Box",
  "type": "box",
  "length": 30,
  "width": 20,
  "height": 15,
  "weight": 1.0,
  "size_unit": "cm",
  "weight_unit": "kg"
}
```

**Success Response** (201):
```json
{
  "status": "success",
  "message": "Packaging created successfully",
  "data": {
    "packaging": {
      "packaging_id": "PA-456DEF",
      "name": "Custom Box",
      "type": "box",
      "length": 30,
      "width": 20,
      "height": 15,
      "weight": 1.0,
      "size_unit": "cm",
      "weight_unit": "kg",
      "created_at": "2026-05-04T10:30:00Z"
    }
  }
}
```

**Error Response** (400):
```json
{
  "status": "error",
  "message": "'type' must be one of: box, envelope, soft-packaging"
}
```

---

### 4. Get Shipping Rates

Get shipping rates from multiple carriers.

**Endpoint**: `POST /api/shipping/rates`

**Request Body**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| origin_address_id | integer | Yes | Local address ID (must be synced to Terminal) |
| destination_address_id | integer | Yes | Local address ID (must be synced to Terminal) |
| items | array | Yes | Array of items to ship |
| packaging_id | string | No | Terminal packaging ID (uses default if not provided) |
| currency | string | No | Currency code (default: `NGN`) |

**Item Object**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Item name |
| quantity | integer | Yes | Quantity |
| value | number | Yes | Item value in currency |
| weight | number | Yes | Item weight in kg |
| description | string | No | Item description |

**Example Request**:
```bash
POST /api/shipping/rates
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "origin_address_id": 1,
  "destination_address_id": 2,
  "items": [
    {
      "name": "Product A",
      "quantity": 2,
      "value": 15000,
      "weight": 2.5,
      "description": "Electronics"
    },
    {
      "name": "Product B",
      "quantity": 1,
      "value": 8000,
      "weight": 1.0,
      "description": "Accessories"
    }
  ],
  "packaging_id": "PA-123ABC",
  "currency": "NGN"
}
```

**Success Response** (200):
```json
{
  "status": "success",
  "message": "Shipping rates retrieved successfully",
  "data": {
    "rates": [
      {
        "rate_id": "RATE-789GHI",
        "carrier": {
          "carrier_id": "CA-81957188177",
          "name": "DHL Express",
          "logo": "https://terminal.africa/carriers/dhl.png"
        },
        "amount": 5500.00,
        "currency": "NGN",
        "delivery_time": "2-3 business days",
        "service_type": "express",
        "pickup_eta": "2026-05-05",
        "delivery_eta": "2026-05-08"
      },
      {
        "rate_id": "RATE-790JKL",
        "carrier": {
          "carrier_id": "CA-31377601348",
          "name": "FedEx",
          "logo": "https://terminal.africa/carriers/fedex.png"
        },
        "amount": 6200.00,
        "currency": "NGN",
        "delivery_time": "3-5 business days",
        "service_type": "standard",
        "pickup_eta": "2026-05-05",
        "delivery_eta": "2026-05-10"
      }
    ],
    "count": 2,
    "parcel_id": "PARCEL-ABC123",
    "summary": {
      "total_weight": 6.0,
      "total_items": 3,
      "origin": "Lagos, Lagos",
      "destination": "Abuja, FCT",
      "currency": "NGN"
    }
  }
}
```

**Error Response** (400 - Addresses Not Synced):
```json
{
  "status": "error",
  "message": "Both addresses must be synced to Terminal Africa first",
  "details": {
    "origin_synced": true,
    "destination_synced": false
  }
}
```

**Error Response** (400 - No Packaging):
```json
{
  "status": "error",
  "message": "No packaging options available. Please create a packaging first."
}
```

**Error Response** (404):
```json
{
  "status": "error",
  "message": "Origin address not found"
}
```

---

## Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (invalid/missing token) |
| 404 | Not Found |
| 500 | Server Error |

---

## Data Models

### Carrier Object
```typescript
{
  carrier_id: string;        // Unique carrier ID
  name: string;              // Carrier name
  slug: string;              // URL-friendly name
  logo: string;              // Logo URL
  active: boolean;           // Active status
  domestic: boolean;         // Supports domestic shipping
  regional: boolean;         // Supports regional shipping
  international: boolean;    // Supports international shipping
}
```

### Packaging Object
```typescript
{
  packaging_id: string;      // Unique packaging ID
  name: string;              // Package name
  type: string;              // box | envelope | soft-packaging
  length: number;            // Length
  width: number;             // Width
  height: number;            // Height
  weight: number;            // Weight
  size_unit: string;         // cm | in
  weight_unit: string;       // kg | lb
  created_at?: string;       // ISO 8601 timestamp
}
```

### Rate Object
```typescript
{
  rate_id: string;           // Unique rate ID
  carrier: {
    carrier_id: string;
    name: string;
    logo: string;
  };
  amount: number;            // Rate amount
  currency: string;          // Currency code
  delivery_time: string;     // Estimated delivery time
  service_type: string;      // express | standard | economy
  pickup_eta?: string;       // Pickup date (ISO 8601)
  delivery_eta?: string;     // Delivery date (ISO 8601)
}
```

### Item Object
```typescript
{
  name: string;              // Item name
  quantity: number;          // Quantity
  value: number;             // Item value
  weight: number;            // Item weight (kg)
  description?: string;      // Item description
}
```

---

## Workflow

### Complete Rate Fetching Flow

```
1. User Authentication
   POST /api/auth/login
   ↓
2. Create/Get Addresses
   POST /api/addresses (auto-syncs to Terminal)
   OR
   GET /api/addresses (check existing)
   ↓
3. Sync Addresses (if needed)
   POST /api/addresses/{id}/sync-terminal
   ↓
4. Get Packaging Options
   GET /api/shipping/packaging
   ↓
5. Create Custom Packaging (optional)
   POST /api/shipping/packaging
   ↓
6. Get Carriers
   GET /api/shipping/carriers
   ↓
7. Get Shipping Rates
   POST /api/shipping/rates
   ↓
8. Compare Rates & Select Carrier
   (User selects preferred rate)
   ↓
9. Create Shipment (Phase 5)
   POST /api/shipping/shipments
```

---

## Rate Comparison Example

### Request
```json
{
  "origin_address_id": 1,
  "destination_address_id": 2,
  "items": [
    {
      "name": "Laptop",
      "quantity": 1,
      "value": 250000,
      "weight": 2.5
    }
  ],
  "currency": "NGN"
}
```

### Response (Multiple Carriers)
```json
{
  "rates": [
    {
      "carrier": {"name": "DHL Express"},
      "amount": 5500,
      "delivery_time": "2-3 days"
    },
    {
      "carrier": {"name": "FedEx"},
      "amount": 6200,
      "delivery_time": "3-5 days"
    },
    {
      "carrier": {"name": "Terminal Express"},
      "amount": 4800,
      "delivery_time": "3-4 days"
    },
    {
      "carrier": {"name": "Kwik Delivery"},
      "amount": 3500,
      "delivery_time": "1-2 days"
    }
  ]
}
```

**User can now compare**:
- **Fastest**: Kwik Delivery (1-2 days, ₦3,500)
- **Cheapest**: Kwik Delivery (₦3,500)
- **Premium**: DHL Express (2-3 days, ₦5,500)

---

## Testing

### Postman Collection

Import this collection to test all endpoints:

```json
{
  "info": {
    "name": "Terminal Africa Phase 4",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Get Carriers",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{token}}"
          }
        ],
        "url": {
          "raw": "{{base_url}}/api/shipping/carriers?active=true",
          "host": ["{{base_url}}"],
          "path": ["api", "shipping", "carriers"],
          "query": [
            {
              "key": "active",
              "value": "true"
            }
          ]
        }
      }
    },
    {
      "name": "Get Packaging",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{token}}"
          }
        ],
        "url": {
          "raw": "{{base_url}}/api/shipping/packaging",
          "host": ["{{base_url}}"],
          "path": ["api", "shipping", "packaging"]
        }
      }
    },
    {
      "name": "Get Rates",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{token}}"
          },
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"origin_address_id\": 1,\n  \"destination_address_id\": 2,\n  \"items\": [\n    {\n      \"name\": \"Test Product\",\n      \"quantity\": 1,\n      \"value\": 10000,\n      \"weight\": 2.0\n    }\n  ],\n  \"currency\": \"NGN\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/api/shipping/rates",
          "host": ["{{base_url}}"],
          "path": ["api", "shipping", "rates"]
        }
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:4500"
    },
    {
      "key": "token",
      "value": "YOUR_JWT_TOKEN"
    }
  ]
}
```

---

## Rate Limits

Terminal Africa API rate limits:
- **Test Environment**: 100 requests/minute
- **Live Environment**: 1000 requests/minute

---

## Best Practices

### 1. Cache Carriers
Cache carrier list for 24 hours to reduce API calls.

### 2. Reuse Packaging
Create packaging once and reuse for similar shipments.

### 3. Address Validation
Always sync addresses before requesting rates.

### 4. Error Handling
Handle Terminal API errors gracefully with fallbacks.

### 5. Rate Comparison
Present multiple rates to users for selection.

---

## Support

- **Documentation**: `docs/TERMINAL_PHASE4_COMPLETE.md`
- **Quick Start**: `TERMINAL_PHASE4_QUICK_START.md`
- **Terminal Docs**: https://docs.terminal.africa/
- **API Reference**: https://developers.terminal.africa/

---

**Last Updated**: 2026-05-04  
**Version**: 1.0  
**Status**: Production Ready
