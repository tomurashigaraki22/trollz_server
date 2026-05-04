# Postman Test Guide - Shipping Rates API

## Step 1: Login to Get Token

**Method**: `POST`  
**URL**: `http://localhost:4500/api/auth/login`

**Headers**:
```
Content-Type: application/json
```

**Body** (raw JSON):
```json
{
  "email": "devtomiwa9@gmail.com",
  "password": "Pityboy@22"
}
```

**Expected Response**:
```json
{
  "status": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 129,
      "email": "devtomiwa9@gmail.com"
    }
  }
}
```

**Copy the token** from the response!

---

## Step 2: Get Your Addresses

**Method**: `GET`  
**URL**: `http://localhost:4500/api/addresses`

**Headers**:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Expected Response**:
```json
{
  "status": "success",
  "data": {
    "addresses": [
      {
        "id": 4,
        "first_name": "John",
        "last_name": "Doe",
        "city": "Lagos",
        "state": "Lagos",
        "terminal_synced": true,
        "terminal_address_id": "AD-K9F1NPOAWHBFOW0D"
      },
      {
        "id": 7,
        "first_name": "Test",
        "last_name": "User",
        "city": "Lagos",
        "state": "Lagos",
        "terminal_synced": true,
        "terminal_address_id": "AD-E0S6FEEXXCFTSB5Y"
      }
    ],
    "count": 6,
    "terminal_count": 2
  }
}
```

**Note the IDs** of addresses where `terminal_synced: true`

---

## Step 3: Get Shipping Rates

**Method**: `POST`  
**URL**: `http://localhost:4500/api/shipping/rates`

**Headers**:
```
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json
```

**Body** (raw JSON):
```json
{
  "origin_address_id": 4,
  "destination_address_id": 7,
  "items": [
    {
      "name": "Test Product",
      "quantity": 1,
      "value": 10000,
      "weight": 1.0,
      "description": "Test product for shipping"
    }
  ],
  "currency": "NGN"
}
```

**Body Parameters Explained**:
- `origin_address_id`: Your origin address ID (must be synced to Terminal)
- `destination_address_id`: Your destination address ID (must be synced to Terminal)
- `items`: Array of items to ship
  - `name`: Item name (required)
  - `quantity`: Number of items (required)
  - `value`: Item value in NGN (required)
  - `weight`: Item weight in kg (required)
  - `description`: Item description (optional)
- `currency`: Currency code (default: "NGN")

**Expected Response** (if successful):
```json
{
  "status": "success",
  "message": "Shipping rates retrieved successfully",
  "data": {
    "rates": [
      {
        "rate_id": "RATE-123ABC",
        "carrier": {
          "carrier_id": "CA-81957188177",
          "name": "DHL Express",
          "logo": "https://..."
        },
        "amount": 5500.00,
        "currency": "NGN",
        "delivery_time": "2-3 business days",
        "service_type": "express"
      },
      {
        "rate_id": "RATE-456DEF",
        "carrier": {
          "carrier_id": "CA-31377601348",
          "name": "FedEx",
          "logo": "https://..."
        },
        "amount": 6200.00,
        "currency": "NGN",
        "delivery_time": "3-5 business days",
        "service_type": "standard"
      }
    ],
    "count": 2,
    "parcel_id": "PARCEL-789GHI",
    "summary": {
      "total_weight": 1.0,
      "total_items": 1,
      "origin": "Lagos, Lagos",
      "destination": "Lagos, Lagos",
      "currency": "NGN"
    }
  }
}
```

---

## Alternative: Test with Multiple Items

**Body** (raw JSON):
```json
{
  "origin_address_id": 4,
  "destination_address_id": 7,
  "items": [
    {
      "name": "Laptop",
      "quantity": 1,
      "value": 250000,
      "weight": 2.5,
      "description": "Dell Laptop"
    },
    {
      "name": "Mouse",
      "quantity": 2,
      "value": 5000,
      "weight": 0.2,
      "description": "Wireless Mouse"
    }
  ],
  "currency": "NGN"
}
```

---

## Alternative: Specify Custom Packaging

**Body** (raw JSON):
```json
{
  "origin_address_id": 4,
  "destination_address_id": 7,
  "items": [
    {
      "name": "Test Product",
      "quantity": 1,
      "value": 10000,
      "weight": 1.0
    }
  ],
  "packaging_id": "PA-SXNKHAJ02QNVI8GJ",
  "currency": "NGN"
}
```

---

## Troubleshooting

### Error: "Addresses not synced"
```json
{
  "status": "error",
  "message": "Both addresses must be synced to Terminal Africa first",
  "details": {
    "origin_synced": false,
    "destination_synced": false
  }
}
```

**Solution**: Sync your addresses first:
```
POST http://localhost:4500/api/addresses/{address_id}/sync-terminal
Authorization: Bearer YOUR_TOKEN
```

### Error: "Address not found"
```json
{
  "status": "error",
  "message": "Origin address not found"
}
```

**Solution**: Use address IDs that belong to your user account.

### Error: "No packaging options available"
```json
{
  "status": "error",
  "message": "No packaging options available. Please create a packaging first."
}
```

**Solution**: The system should have default packaging. Check:
```
GET http://localhost:4500/api/shipping/packaging
Authorization: Bearer YOUR_TOKEN
```

### Request Timeout
If the request takes more than 30 seconds, it's a Terminal API performance issue.

**Try**:
1. Reduce item weight (try 0.5 kg instead of 1.0 kg)
2. Use same city for origin and destination
3. Try different addresses
4. Check Terminal Africa dashboard for API status

---

## Quick Copy-Paste for Postman

### 1. Login Request
```
POST http://localhost:4500/api/auth/login
Content-Type: application/json

{
  "email": "devtomiwa9@gmail.com",
  "password": "Pityboy@22"
}
```

### 2. Get Addresses
```
GET http://localhost:4500/api/addresses
Authorization: Bearer YOUR_TOKEN_HERE
```

### 3. Get Rates
```
POST http://localhost:4500/api/shipping/rates
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "origin_address_id": 4,
  "destination_address_id": 7,
  "items": [
    {
      "name": "Test Product",
      "quantity": 1,
      "value": 10000,
      "weight": 1.0,
      "description": "Test"
    }
  ],
  "currency": "NGN"
}
```

---

## Your Current Synced Addresses

Based on the test results, you have:

**Address ID 4**:
- Name: John Doe
- Location: Lagos, Lagos
- Terminal ID: AD-K9F1NPOAWHBFOW0D
- ✅ Synced

**Address ID 7**:
- Name: Test User
- Location: Lagos, Lagos
- Terminal ID: AD-E0S6FEEXXCFTSB5Y
- ✅ Synced

Use these IDs in your Postman test!

---

## Expected Behavior

1. **Fast Response** (< 5 seconds): Rates returned successfully
2. **Slow Response** (5-30 seconds): Terminal API is processing
3. **Timeout** (> 30 seconds): Terminal API performance issue

If you get a timeout, try:
- Reducing weight to 0.5 kg
- Using lighter items (value < 5000)
- Testing at different times of day
- Checking Terminal Africa status page

---

## Notes

- Both addresses must have `terminal_synced: true`
- Items must include: name, quantity, value, weight
- Currency is automatically added to items
- Packaging is optional (uses default if not specified)
- Response may take 10-30 seconds (Terminal API can be slow)

---

**Last Updated**: 2026-05-04  
**Server**: http://localhost:4500  
**Environment**: Live API
