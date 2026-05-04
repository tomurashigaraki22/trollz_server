# Terminal Africa API Documentation - Complete Reference

**Version:** 1.0  
**Date:** May 4, 2026  
**Environment:** TEST (sandbox.terminal.africa) / LIVE (api.terminal.africa)  
**Base URL:** `http://localhost:4500`

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Phase 3: Address Management](#phase-3-address-management)
4. [Phase 4: Shipping Quotes & Rates](#phase-4-shipping-quotes--rates)
5. [Phase 5: Shipment Management](#phase-5-shipment-management)
6. [Phase 6: Tracking](#phase-6-tracking)
7. [Phase 7: Admin Features](#phase-7-admin-features)
8. [Error Handling](#error-handling)
9. [Frontend Integration Guide](#frontend-integration-guide)
10. [Testing](#testing)

---

## Overview

This document provides complete API documentation for the Terminal Africa shipping integration. It covers all endpoints from Phases 3-7, including address management, rate fetching, shipment creation, tracking, and admin features.

### Key Features

- **Multi-Carrier Support**: Get rates from 39+ carriers (DHL, FedEx, Sendbox, etc.)
- **Address Management**: Create, validate, and sync addresses to Terminal Africa
- **Real-Time Rates**: Get shipping rates from multiple carriers simultaneously
- **Shipment Creation**: Create shipments with selected carriers
- **Live Tracking**: Track shipments with real-time updates
- **Admin Dashboard**: Manage carriers, packaging, and view reports

### Environments

- **TEST**: `https://sandbox.terminal.africa/v1` (for development)
- **LIVE**: `https://api.terminal.africa/v1` (for production)

---

## Authentication

### User Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 129,
      "name": "John Doe",
      "email": "user@example.com",
      "phone": "+2347012345678"
    }
  }
}
```

### Admin Login
```http
POST /api/admin/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Admin login successful",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "admin": {
      "id": 1,
      "username": "admin",
      "role": "admin"
    }
  }
}
```

### Using Authentication

Include the token in the `Authorization` header for all authenticated requests:

```http
Authorization: Bearer {token}
```

---

## Phase 3: Address Management

### 1. Create Address

Create a new shipping address and automatically sync to Terminal Africa.

```http
POST /api/addresses
Authorization: Bearer {token}
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+2347012345678",
  "email": "john@example.com",
  "street": "123 Main Street",
  "city": "Lagos",
  "state": "Lagos",
  "country": "NG",
  "post_code": "100001"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Address created successfully",
  "data": {
    "address": {
      "id": 15,
      "first_name": "John",
      "last_name": "Doe",
      "phone": "+2347012345678",
      "email": "john@example.com",
      "street": "123 Main Street",
      "city": "Lagos",
      "state": "Lagos",
      "country": "NG",
      "post_code": "100001",
      "terminal_address_id": "AD-G7O3Z0NQ1VUFH26Q",
      "created_at": "2026-05-04T10:30:00Z"
    },
    "terminal_synced": true,
    "terminal_address_id": "AD-G7O3Z0NQ1VUFH26Q"
  }
}
```

### 2. Get All Addresses

Retrieve all addresses for the authenticated user.

```http
GET /api/addresses
Authorization: Bearer {token}
```

**Response:**
```json
{
  "status": "success",
  "message": "Addresses retrieved successfully",
  "data": {
    "addresses": [
      {
        "id": 15,
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+2347012345678",
        "email": "john@example.com",
        "street": "123 Main Street",
        "city": "Lagos",
        "state": "Lagos",
        "country": "NG",
        "post_code": "100001",
        "terminal_address_id": "AD-G7O3Z0NQ1VUFH26Q"
      }
    ],
    "count": 1
  }
}
```

### 3. Get Single Address

```http
GET /api/addresses/:id
Authorization: Bearer {token}
```

### 4. Update Address

```http
PUT /api/addresses/:id
Authorization: Bearer {token}
Content-Type: application/json

{
  "street": "456 New Street",
  "city": "Abuja"
}
```

### 5. Delete Address

```http
DELETE /api/addresses/:id
Authorization: Bearer {token}
```

---

## Phase 4: Shipping Quotes & Rates

### 1. Get States

List all Nigerian states with their details (public endpoint).

```http
GET /api/shipping/states
Query Parameters:
  - country_code: NG (default)
```

**Response:**
```json
{
  "status": "success",
  "message": "States retrieved successfully for NG",
  "data": {
    "states": [
      {
        "name": "Lagos",
        "isoCode": "LA",
        "countryCode": "NG",
        "latitude": "6.52437930",
        "longitude": "3.37920570",
        "state_id": "JYMK526U3GGF"
      }
    ],
    "count": 37,
    "country_code": "NG"
  }
}
```

### 2. Get Cities

List cities, optionally filtered by state (public endpoint).

```http
GET /api/shipping/cities
Query Parameters:
  - country_code: NG (default)
  - state: State name (optional, e.g., "Lagos")
```

**Response:**
```json
{
  "status": "success",
  "message": "Cities retrieved successfully",
  "data": {
    "cities": [
      {
        "name": "Agege",
        "stateCode": "LA",
        "countryCode": "NG",
        "latitude": "6.6252564",
        "longitude": "3.3112093",
        "city_id": "O04WLJ"
      }
    ],
    "count": 46,
    "country_code": "NG",
    "state": "Lagos"
  }
}
```

### 3. Get Carriers

List all available carriers with filtering options.

```http
GET /api/shipping/carriers
Authorization: Bearer {token}

Query Parameters:
  - active: true/false (optional)
  - domestic: true/false (optional)
  - regional: true/false (optional)
  - international: true/false (optional)
```

**Response:**
```json
{
  "status": "success",
  "message": "Carriers retrieved successfully",
  "data": {
    "carriers": [
      {
        "carrier_id": "CA-4BWTMDHQKXZNP7J",
        "name": "DHL Express",
        "slug": "dhl-express",
        "active": true,
        "domestic": true,
        "regional": true,
        "international": true,
        "logo": "https://..."
      }
    ],
    "count": 39,
    "active_count": 23
  }
}
```

### 4. Get Packaging Options

List all available packaging options.

```http
GET /api/shipping/packaging
Authorization: Bearer {token}

Query Parameters:
  - page: 1 (default)
  - per_page: 20 (default, max 100)
```

**Response:**
```json
{
  "status": "success",
  "message": "Packaging options retrieved successfully",
  "data": {
    "packaging": [
      {
        "packaging_id": "PA-8NMJE0M2LR5MWEM8",
        "name": "Standard Box",
        "type": "box",
        "length": 30,
        "width": 20,
        "height": 15,
        "weight": 0.5,
        "size_unit": "cm",
        "weight_unit": "kg"
      }
    ],
    "count": 3,
    "pagination": {
      "page": 1,
      "perPage": 20,
      "total": 3
    }
  }
}
```

### 5. Create Custom Packaging

```http
POST /api/shipping/packaging
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Custom Large Box",
  "type": "box",
  "length": 40,
  "width": 30,
  "height": 25,
  "weight": 1.0,
  "size_unit": "cm",
  "weight_unit": "kg"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Packaging created successfully",
  "data": {
    "packaging": {
      "packaging_id": "PA-AYHXG1HF644WM3MQ",
      "name": "Custom Large Box",
      "type": "box",
      "length": 40,
      "width": 30,
      "height": 25,
      "weight": 1.0,
      "size_unit": "cm",
      "weight_unit": "kg"
    }
  }
}
```

### 4. Get Shipping Rates (Multi-Carrier)

Get shipping rates from multiple carriers simultaneously. **Origin address is automatically set to warehouse.**

```http
POST /api/shipping/rates
Authorization: Bearer {token}
Content-Type: application/json

{
  "destination_address_id": 14,
  "items": [
    {
      "name": "Product Name",
      "quantity": 2,
      "value": 10000,
      "weight": 1.5,
      "description": "Product description"
    }
  ],
  "currency": "NGN"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Shipping rates retrieved successfully",
  "data": {
    "rates": [
      {
        "rate_id": "RT-Q4ZBR49K2OZ3LK8L",
        "carrier_name": "Fez Delivery",
        "carrier_id": "CA-FEZ123",
        "amount": 3547.50,
        "currency": "NGN",
        "delivery_time": "Within 5 business days",
        "estimated_days": 5
      },
      {
        "rate_id": "RT-FESMOX7ZFCNMMSKF",
        "carrier_name": "Redstar Express",
        "carrier_id": "CA-RED456",
        "amount": 11301.70,
        "currency": "NGN",
        "delivery_time": "Within 4 business days",
        "estimated_days": 4
      },
      {
        "rate_id": "RT-A5TIU5AZAK3KCBS3",
        "carrier_name": "DHL Express",
        "carrier_id": "CA-DHL789",
        "amount": 12000.74,
        "currency": "NGN",
        "delivery_time": "Within 4 business days",
        "estimated_days": 4
      }
    ],
    "count": 3,
    "parcel_id": "PC-SSEFA533A9NR6JC1",
    "warehouse_address_id": 19,
    "summary": {
      "total_weight": 3.0,
      "total_items": 2,
      "origin": "Owerri, Imo (Warehouse)",
      "destination": "Lagos, Lagos",
      "currency": "NGN"
    }
  }
}
```

**Important Notes:**
- **Origin is automatically set to warehouse address** (Owerri, Imo)
- Response time: 5-30 seconds (fetching from multiple carriers)
- Destination address must be synced to Terminal Africa
- Returns rates from 3-5 carriers typically
- `parcel_id` is required for shipment creation
- `warehouse_address_id` shows which warehouse address was used

---

## Phase 5: Shipment Management

### 1. Create Shipment

Create a shipment from a selected rate. **Origin address is automatically set to warehouse.**

```http
POST /api/shipping/shipments
Authorization: Bearer {token}
Content-Type: application/json

{
  "rate_id": "RT-Q4ZBR49K2OZ3LK8L",
  "destination_address_id": 14,
  "parcel_id": "PC-SSEFA533A9NR6JC1",
  "metadata": {
    "order_id": 123,
    "customer_notes": "Handle with care"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Shipment created successfully",
  "data": {
    "shipment": {
      "shipment_id": "SH-SOP8TDI5N6N2XGGH",
      "tracking_number": "TN123456789",
      "carrier_name": "Fez Delivery",
      "carrier_id": "CA-FEZ123",
      "status": "draft",
      "amount": 3547.50,
      "currency": "NGN",
      "created_at": "2026-05-04T14:30:00Z"
    },
    "warehouse_address_id": 19
  }
}
```

### 2. Get All Shipments

List all shipments for the authenticated user.

```http
GET /api/shipping/shipments
Authorization: Bearer {token}

Query Parameters:
  - page: 1 (default)
  - per_page: 20 (default, max 100)
  - status: Filter by status (optional)
```

**Response:**
```json
{
  "status": "success",
  "message": "Shipments retrieved successfully",
  "data": {
    "shipments": [
      {
        "shipment_id": "SH-SOP8TDI5N6N2XGGH",
        "tracking_number": "TN123456789",
        "carrier_name": "Fez Delivery",
        "status": "in_transit",
        "created_at": "2026-05-04T14:30:00Z"
      }
    ],
    "count": 1,
    "pagination": {
      "page": 1,
      "perPage": 20,
      "total": 1
    }
  }
}
```

### 3. Get Shipment Details

Get details of a specific shipment.

```http
GET /api/shipping/shipments/:shipment_id
Authorization: Bearer {token}
```

**Response:**
```json
{
  "status": "success",
  "message": "Shipment details retrieved successfully",
  "data": {
    "shipment": {
      "shipment_id": "SH-SOP8TDI5N6N2XGGH",
      "tracking_number": "TN123456789",
      "carrier_name": "Fez Delivery",
      "carrier_id": "CA-FEZ123",
      "status": "in_transit",
      "amount": 3547.50,
      "currency": "NGN",
      "origin_address": {
        "city": "Abuja",
        "state": "Abuja",
        "country": "NG"
      },
      "destination_address": {
        "city": "Lagos",
        "state": "Lagos",
        "country": "NG"
      },
      "parcel": {
        "weight": 3.0,
        "items": 2
      },
      "created_at": "2026-05-04T14:30:00Z"
    }
  }
}
```

### 4. Cancel Shipment

Cancel a shipment.

```http
POST /api/shipping/shipments/:shipment_id/cancel
Authorization: Bearer {token}
```

**Response:**
```json
{
  "status": "success",
  "message": "Shipment cancelled successfully",
  "data": {
    "shipment_id": "SH-SOP8TDI5N6N2XGGH",
    "status": "cancelled"
  }
}
```

---

## Phase 6: Tracking

### 1. Track by Shipment ID

Track a shipment using Terminal shipment ID (public endpoint).

```http
GET /api/shipping/track/:shipment_id
```

**Response:**
```json
{
  "status": "success",
  "message": "Tracking information retrieved successfully",
  "data": {
    "tracking": {
      "shipment_id": "SH-SOP8TDI5N6N2XGGH",
      "tracking_number": "TN123456789",
      "status": "in_transit",
      "carrier_name": "Fez Delivery",
      "current_location": "Lagos, Nigeria",
      "estimated_delivery": "2026-05-08",
      "tracking_events": [
        {
          "status": "picked_up",
          "description": "Package picked up",
          "location": "Abuja, Nigeria",
          "timestamp": "2026-05-04T10:00:00Z"
        },
        {
          "status": "in_transit",
          "description": "Package in transit",
          "location": "Lagos, Nigeria",
          "timestamp": "2026-05-04T14:30:00Z"
        }
      ]
    }
  }
}
```

### 2. Track by Tracking Number

Track a shipment using carrier tracking number (public endpoint).

```http
GET /api/shipping/track/number/:tracking_number
```

**Response:** Same as track by shipment ID

**Note:** Tracking may not be available immediately for draft shipments. Wait for shipment confirmation.

---

## Phase 7: Admin Features

All admin endpoints require admin authentication.

### 1. Get Carriers (Admin)

```http
GET /api/admin/terminal/carriers
Authorization: Bearer {admin_token}

Query Parameters:
  - active: true/false (optional)
  - domestic: true/false (optional)
  - regional: true/false (optional)
  - international: true/false (optional)
```

**Response:**
```json
{
  "status": "success",
  "message": "Carriers retrieved successfully",
  "data": {
    "carriers": [...],
    "statistics": {
      "total": 39,
      "active": 23,
      "domestic": 31,
      "regional": 20,
      "international": 18
    }
  }
}
```

### 2. Enable Carrier (Admin)

```http
POST /api/admin/terminal/carriers/:carrier_id/enable
Authorization: Bearer {admin_token}
```

### 3. Disable Carrier (Admin)

```http
POST /api/admin/terminal/carriers/:carrier_id/disable
Authorization: Bearer {admin_token}
```

### 4. Get Packaging (Admin)

```http
GET /api/admin/terminal/packaging
Authorization: Bearer {admin_token}

Query Parameters:
  - page: 1 (default)
  - per_page: 50 (default, max 100)
```

### 5. Create Packaging (Admin)

```http
POST /api/admin/terminal/packaging
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "name": "Admin Custom Box",
  "type": "box",
  "length": 35,
  "width": 25,
  "height": 18,
  "weight": 0.8,
  "size_unit": "cm",
  "weight_unit": "kg"
}
```

### 6. Delete Packaging (Admin)

```http
DELETE /api/admin/terminal/packaging/:packaging_id
Authorization: Bearer {admin_token}
```

### 7. Get Shipments (Admin)

```http
GET /api/admin/terminal/shipments
Authorization: Bearer {admin_token}

Query Parameters:
  - page: 1 (default)
  - per_page: 20 (default, max 100)
  - status: Filter by status (optional)
```

### 8. Shipping Reports (Admin)

Generate shipping analytics and reports.

```http
GET /api/admin/terminal/reports/shipping
Authorization: Bearer {admin_token}

Query Parameters:
  - start_date: YYYY-MM-DD (default: 30 days ago)
  - end_date: YYYY-MM-DD (default: today)
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "period": {
      "start_date": "2026-04-04",
      "end_date": "2026-05-04"
    },
    "summary": {
      "total_shipments": 150,
      "total_shipping_cost": 532125.00,
      "avg_shipping_cost": 3547.50
    },
    "carriers": [
      {
        "carrier": "Fez Delivery",
        "shipment_count": 80,
        "total_cost": 283800.00,
        "avg_cost": 3547.50
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
    ]
  }
}
```

---

## Error Handling

### Error Response Format

All errors follow this format:

```json
{
  "status": "error",
  "message": "Error description",
  "error_code": 400
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

### Common Errors

#### 1. Authentication Errors

```json
{
  "status": "error",
  "message": "Token is missing",
  "error_code": 401
}
```

```json
{
  "status": "error",
  "message": "Token has expired",
  "error_code": 401
}
```

```json
{
  "status": "error",
  "message": "Admin access required",
  "error_code": 403
}
```

#### 2. Validation Errors

```json
{
  "status": "error",
  "message": "'origin_address_id' is required",
  "error_code": 400
}
```

#### 3. Terminal API Errors

```json
{
  "status": "error",
  "message": "Terminal API error: Resource not found",
  "error_code": 404
}
```

---

## Frontend Integration Guide

### Complete Shipping Workflow

Here's a step-by-step guide to implement the complete shipping workflow in your frontend:

#### Step 1: User Authentication

```javascript
// Login user
const loginResponse = await fetch('http://localhost:4500/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});

const loginData = await loginResponse.json();
const token = loginData.data.token;
```

#### Step 2: Create/Get Addresses

```javascript
// Create new address
const addressResponse = await fetch('http://localhost:4500/api/addresses', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    first_name: 'John',
    last_name: 'Doe',
    phone: '+2347012345678',
    email: 'john@example.com',
    street: '123 Main Street',
    city: 'Lagos',
    state: 'Lagos',
    country: 'NG',
    post_code: '100001'
  })
});

const addressData = await addressResponse.json();
const addressId = addressData.data.address.id;
```

#### Step 3: Get Shipping Rates

```javascript
// Get rates from multiple carriers (origin automatically set to warehouse)
const ratesResponse = await fetch('http://localhost:4500/api/shipping/rates', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    destination_address_id: 14,
    items: [
      {
        name: 'Product Name',
        quantity: 1,
        value: 10000,
        weight: 1.5,
        description: 'Product description'
      }
    ],
    currency: 'NGN'
  })
});

const ratesData = await ratesResponse.json();
const rates = ratesData.data.rates;
const parcelId = ratesData.data.parcel_id;

// Display rates to user for selection
rates.forEach(rate => {
  console.log(`${rate.carrier_name}: NGN ${rate.amount}`);
});
```

#### Step 4: Create Shipment

```javascript
// User selects a rate
const selectedRate = rates[0];

// Create shipment
const shipmentResponse = await fetch('http://localhost:4500/api/shipping/shipments', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    rate_id: selectedRate.rate_id,
    origin_address_id: 15,
    destination_address_id: 14,
    parcel_id: parcelId,
    metadata: {
      order_id: 123
    }
  })
});

const shipmentData = await shipmentResponse.json();
const shipmentId = shipmentData.data.shipment.shipment_id;
const trackingNumber = shipmentData.data.shipment.tracking_number;
```

#### Step 5: Track Shipment

```javascript
// Track shipment (public endpoint - no auth required)
const trackingResponse = await fetch(`http://localhost:4500/api/shipping/track/${shipmentId}`);

const trackingData = await trackingResponse.json();
const tracking = trackingData.data.tracking;

console.log(`Status: ${tracking.status}`);
console.log(`Location: ${tracking.current_location}`);
console.log(`Estimated Delivery: ${tracking.estimated_delivery}`);

// Display tracking events
tracking.tracking_events.forEach(event => {
  console.log(`${event.timestamp}: ${event.description} at ${event.location}`);
});
```

### React Example

```jsx
import React, { useState, useEffect } from 'react';

function ShippingComponent() {
  const [token, setToken] = useState('');
  const [rates, setRates] = useState([]);
  const [selectedRate, setSelectedRate] = useState(null);
  const [shipment, setShipment] = useState(null);

  // Step 1: Get rates
  const getRates = async () => {
    const response = await fetch('http://localhost:4500/api/shipping/rates', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        origin_address_id: 15,
        destination_address_id: 14,
        items: [{
          name: 'Product',
          quantity: 1,
          value: 10000,
          weight: 1.5
        }],
        currency: 'NGN'
      })
    });

    const data = await response.json();
    setRates(data.data.rates);
  };

  // Step 2: Create shipment
  const createShipment = async (rate) => {
    const response = await fetch('http://localhost:4500/api/shipping/shipments', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        rate_id: rate.rate_id,
        origin_address_id: 15,
        destination_address_id: 14,
        parcel_id: rates.parcel_id
      })
    });

    const data = await response.json();
    setShipment(data.data.shipment);
  };

  return (
    <div>
      <h2>Shipping Rates</h2>
      {rates.map(rate => (
        <div key={rate.rate_id}>
          <p>{rate.carrier_name}: NGN {rate.amount}</p>
          <button onClick={() => createShipment(rate)}>
            Select
          </button>
        </div>
      ))}

      {shipment && (
        <div>
          <h3>Shipment Created</h3>
          <p>Tracking: {shipment.tracking_number}</p>
          <p>Status: {shipment.status}</p>
        </div>
      )}
    </div>
  );
}
```

---

## Testing

### Test Credentials

**User Account:**
- Email: `devtomiwa9@gmail.com`
- Password: `Pityboy@22`

**Admin Account:**
- Username: `admin`
- Password: `admin123`

### Test Environment

- **Base URL:** `http://localhost:4500`
- **Terminal Environment:** TEST (sandbox.terminal.africa)
- **Test Addresses:** Use addresses with ID >= 10

### Running Tests

```bash
# Phase 3: Address Management
python test_terminal_phase3.py

# Phase 4: Rates and Packaging
python test_phase4_comprehensive.py

# Phase 5 & 6: Shipments and Tracking
python test_phase5_phase6.py

# Phase 7: Admin Features
python test_phase7_admin.py

# Phase 8.3: End-to-End
python test_phase8_3_comprehensive.py
```

---

## Status Codes

### Shipment Status

| Status | Description |
|--------|-------------|
| `draft` | Shipment created but not confirmed |
| `pending` | Shipment pending pickup |
| `confirmed` | Shipment confirmed by carrier |
| `in_transit` | Shipment in transit |
| `out_for_delivery` | Out for delivery |
| `delivered` | Successfully delivered |
| `cancelled` | Shipment cancelled |
| `failed` | Delivery failed |
| `returned` | Shipment returned |

---

## Rate Limiting

- No rate limiting currently implemented
- Recommended: Cache rates for 5-10 minutes
- Avoid excessive rate requests

---

## Best Practices

### 1. Address Management
- Always validate addresses before creating shipments
- Store `terminal_address_id` for future use
- Use TEST environment addresses (ID >= 10) for testing

### 2. Rate Fetching
- Cache rates for 5-10 minutes to reduce API calls
- Show loading indicator (rates take 5-30 seconds)
- Handle timeout errors gracefully

### 3. Shipment Creation
- Always use `rate_id` from rates response
- Store `shipment_id` and `tracking_number` in your database
- Handle draft status appropriately

### 4. Tracking
- Tracking may not be available immediately for draft shipments
- Poll tracking endpoint every 5-10 minutes for updates
- Use webhooks for real-time updates (Phase 6)

### 5. Error Handling
- Always check response status
- Display user-friendly error messages
- Log errors for debugging

---

## Support

- **Documentation:** https://docs.terminal.africa/
- **API Reference:** https://developers.terminal.africa/
- **Support:** support@terminal.africa

---

**Document Version:** 1.0  
**Last Updated:** May 4, 2026  
**Status:** ✅ Complete and Tested

