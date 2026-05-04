# Phase 4 - Postman Examples

Complete Postman collection examples for testing Terminal Africa Phase 4 endpoints.

---

## 🔐 Authentication

### 1. Login
**Method:** POST  
**URL:** `http://localhost:4500/api/auth/login`  
**Headers:**
```
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "email": "devtomiwa9@gmail.com",
  "password": "Pityboy@22"
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
      "id": 1,
      "email": "devtomiwa9@gmail.com",
      "name": "Tomiwa"
    }
  }
}
```

**Save the token** - You'll need it for all other requests!

---

## 📦 Phase 4 Endpoints

### 2. Get Carriers
**Method:** GET  
**URL:** `http://localhost:4500/api/shipping/carriers`  
**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```
**Response:**
```json
{
  "status": "success",
  "message": "Carriers retrieved successfully",
  "data": {
    "carriers": [
      {
        "name": "Fez Delivery",
        "active": true,
        "domestic": true,
        "regional": false,
        "international": false
      },
      {
        "name": "DHL Express",
        "active": true,
        "domestic": true,
        "regional": true,
        "international": true
      }
    ],
    "count": 39,
    "active_count": 23
  }
}
```

### 2a. Get Active Carriers Only
**Method:** GET  
**URL:** `http://localhost:4500/api/shipping/carriers?active=true`  
**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

---

### 3. Get Packaging Options
**Method:** GET  
**URL:** `http://localhost:4500/api/shipping/packaging`  
**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```
**Response:**
```json
{
  "status": "success",
  "message": "Packaging options retrieved successfully",
  "data": {
    "packaging": [
      {
        "packaging_id": "PA-AYHXG1HF644WM3MQ",
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
    "count": 2,
    "pagination": {
      "page": 1,
      "perPage": 20,
      "total": 2
    }
  }
}
```

### 3a. Get Packaging with Pagination
**Method:** GET  
**URL:** `http://localhost:4500/api/shipping/packaging?page=1&per_page=10`  
**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

---

### 4. Create Custom Packaging
**Method:** POST  
**URL:** `http://localhost:4500/api/shipping/packaging`  
**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "name": "My Custom Box",
  "type": "box",
  "length": 30,
  "width": 20,
  "height": 15,
  "weight": 0.5,
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
      "name": "My Custom Box",
      "type": "box",
      "length": 30,
      "width": 20,
      "height": 15,
      "weight": 0.5,
      "size_unit": "cm",
      "weight_unit": "kg",
      "created_at": "2026-05-04T14:30:00.000Z"
    }
  }
}
```

**Valid Types:**
- `box`
- `envelope`
- `soft-packaging`

---

### 5. Get Addresses (Check Sync Status)
**Method:** GET  
**URL:** `http://localhost:4500/api/addresses`  
**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
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
        "first_name": "Test",
        "last_name": "User",
        "phone": "+2348012345678",
        "email": "test@test.com",
        "street": "123 Test Street",
        "city": "Abuja",
        "state": "Abuja",
        "country": "NG",
        "post_code": "900001",
        "terminal_synced": true,
        "terminal_address_id": "AD-G7O3Z0NQ1VUFH26Q"
      },
      {
        "id": 14,
        "first_name": "Test",
        "last_name": "User2",
        "phone": "+2348087654321",
        "email": "test2@test.com",
        "street": "456 Test Avenue",
        "city": "Lagos",
        "state": "Lagos",
        "country": "NG",
        "post_code": "100001",
        "terminal_synced": true,
        "terminal_address_id": "AD-51QVA4LDRUI66N8B"
      }
    ],
    "count": 14
  }
}
```

**Note:** Look for addresses with `terminal_synced: true` and `terminal_address_id` present.

---

### 6. Get Shipping Rates (Main Endpoint)
**Method:** POST  
**URL:** `http://localhost:4500/api/shipping/rates`  
**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "origin_address_id": 15,
  "destination_address_id": 14,
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

**Response (Success):**
```json
{
  "status": "success",
  "message": "Shipping rates retrieved successfully",
  "data": {
    "rates": [
      {
        "carrier_name": "Fez Delivery",
        "amount": 3547.50,
        "currency": "NGN",
        "delivery_time": "Within 5 business days",
        "rate_id": "RT-ABC123"
      },
      {
        "carrier_name": "Redstar Express",
        "amount": 11301.70,
        "currency": "NGN",
        "delivery_time": "Within 4 business days",
        "rate_id": "RT-DEF456"
      },
      {
        "carrier_name": "DHL Express",
        "amount": 12000.74,
        "currency": "NGN",
        "delivery_time": "Within 4 business days",
        "rate_id": "RT-GHI789"
      }
    ],
    "count": 3,
    "parcel_id": "PC-SSEFA533A9NR6JC1",
    "summary": {
      "total_weight": 1.0,
      "total_items": 1,
      "origin": "Abuja, Abuja",
      "destination": "Lagos, Lagos",
      "currency": "NGN"
    }
  }
}
```

**Response Time:** 5-10 seconds (fetches from multiple carriers)

---

### 6a. Get Rates with Multiple Items
**Method:** POST  
**URL:** `http://localhost:4500/api/shipping/rates`  
**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "origin_address_id": 15,
  "destination_address_id": 14,
  "items": [
    {
      "name": "Product 1",
      "quantity": 2,
      "value": 5000,
      "weight": 0.5,
      "description": "First product"
    },
    {
      "name": "Product 2",
      "quantity": 1,
      "value": 10000,
      "weight": 1.5,
      "description": "Second product"
    }
  ],
  "currency": "NGN"
}
```

---

## ⚠️ Important Notes

### Address Requirements
- **Both addresses MUST be synced to Terminal Africa**
- Check `terminal_synced: true` and `terminal_address_id` is present
- For TEST environment, use addresses with ID >= 10

### Test Environment Addresses
Use these address IDs for testing:
- **Address 10:** Lagos, Lagos
- **Address 11:** Abuja, Abuja
- **Address 12:** Lagos, Lagos
- **Address 13:** Abuja, Abuja
- **Address 14:** Lagos, Lagos
- **Address 15:** Abuja, Abuja

### Don't Use These (LIVE Environment)
- Address 4, 7, 8 (synced to LIVE, won't work with TEST API)

---

## 🐛 Common Errors

### Error 1: "Pickup address must be provided"
```json
{
  "status": "error",
  "message": "Terminal API error: Bad request: Pickup address must be provided",
  "error_code": 400
}
```
**Cause:** Using address from LIVE environment with TEST API  
**Solution:** Use addresses with ID >= 10

---

### Error 2: "Address not synced to Terminal"
```json
{
  "status": "error",
  "message": "Both addresses must be synced to Terminal Africa first",
  "details": {
    "origin_synced": false,
    "destination_synced": true
  }
}
```
**Cause:** Address doesn't have `terminal_address_id`  
**Solution:** Create new address via API (auto-syncs) or use synced addresses

---

### Error 3: "No packaging options available"
```json
{
  "status": "error",
  "message": "No packaging options available. Please create a packaging first."
}
```
**Cause:** No packaging in Terminal account  
**Solution:** Create packaging using endpoint #4

---

## 📋 Postman Collection Setup

### Environment Variables
Create a Postman environment with these variables:

| Variable | Value |
|----------|-------|
| `base_url` | `http://localhost:4500` |
| `token` | (Set after login) |
| `origin_address_id` | `15` |
| `dest_address_id` | `14` |

### Using Variables in Postman
- URL: `{{base_url}}/api/shipping/carriers`
- Header: `Authorization: Bearer {{token}}`
- Body: `"origin_address_id": {{origin_address_id}}`

---

## 🧪 Testing Workflow

### Step-by-Step Test
1. **Login** (Endpoint #1) → Save token
2. **Get Carriers** (Endpoint #2) → Verify 39 carriers
3. **Get Packaging** (Endpoint #3) → Check available packaging
4. **Create Packaging** (Endpoint #4) → Create custom box
5. **Get Addresses** (Endpoint #5) → Find synced addresses (ID >= 10)
6. **Get Rates** (Endpoint #6) → Use synced addresses

### Expected Results
- Carriers: 39 total, 23 active
- Packaging: 2+ options
- Rates: 3-5 carriers with prices

---

## 📊 Response Times

| Endpoint | Expected Time |
|----------|--------------|
| Login | < 1 second |
| Get Carriers | < 1 second |
| Get Packaging | < 1 second |
| Create Packaging | 1-2 seconds |
| Get Addresses | < 1 second |
| **Get Rates** | **5-10 seconds** |

---

## 💡 Tips

1. **Save Token After Login**
   - Copy token from login response
   - Set as environment variable in Postman
   - Use `{{token}}` in Authorization header

2. **Check Address Sync Status**
   - Always verify `terminal_synced: true`
   - Check `terminal_address_id` is present
   - Use addresses with ID >= 10 for testing

3. **Rate Fetching Takes Time**
   - 5-10 seconds is normal
   - Fetches from multiple carriers
   - Don't timeout too early

4. **Use Environment Variables**
   - Makes testing easier
   - Can switch between test/live
   - Reusable across requests

---

## 🚀 Ready to Test!

Import these examples into Postman and start testing Phase 4 endpoints!

**Server:** http://localhost:4500  
**Environment:** TEST (sandbox.terminal.africa)  
**Status:** ✅ All endpoints working
