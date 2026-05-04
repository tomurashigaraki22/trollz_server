# Phase 4 Quick Reference - Terminal Africa Integration

## 🚀 Quick Start

### 1. Login
```bash
curl -X POST http://localhost:4500/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"devtomiwa9@gmail.com","password":"Pityboy@22"}'
```

Save the token from response.

---

## 📋 Available Endpoints

### 1. Get Carriers
```bash
curl -X GET "http://localhost:4500/api/shipping/carriers" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Filter by active carriers:**
```bash
curl -X GET "http://localhost:4500/api/shipping/carriers?active=true" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 2. Get Packaging Options
```bash
curl -X GET "http://localhost:4500/api/shipping/packaging" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 3. Create Custom Packaging
```bash
curl -X POST "http://localhost:4500/api/shipping/packaging" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Custom Box",
    "type": "box",
    "length": 30,
    "width": 20,
    "height": 15,
    "weight": 0.5,
    "size_unit": "cm",
    "weight_unit": "kg"
  }'
```

**Valid types:** `box`, `envelope`, `soft-packaging`

---

### 4. Get Shipping Rates
```bash
curl -X POST "http://localhost:4500/api/shipping/rates" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "origin_address_id": 15,
    "destination_address_id": 14,
    "items": [
      {
        "name": "Product Name",
        "quantity": 1,
        "value": 10000,
        "weight": 1.0,
        "description": "Product description"
      }
    ],
    "currency": "NGN"
  }'
```

**Important:** Both addresses must be synced to Terminal Africa (have `terminal_address_id`).

---

## 🧪 Testing

### Run Comprehensive Test
```bash
python test_phase4_comprehensive.py
```

### Check Address Environments
```bash
python check_address_environments.py
```

---

## 📍 Address Requirements

### For Testing (TEST Environment)
Use addresses with **ID >= 10** (these are synced to TEST environment):
- Address ID 10: Lagos, Lagos
- Address ID 11: Abuja, Abuja
- Address ID 12: Lagos, Lagos
- Address ID 13: Abuja, Abuja
- Address ID 14: Lagos, Lagos
- Address ID 15: Abuja, Abuja

### Create New Address
```bash
curl -X POST "http://localhost:4500/api/addresses" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+2348012345678",
    "email": "john@example.com",
    "street": "123 Main Street",
    "city": "Lagos",
    "state": "Lagos",
    "country": "NG",
    "post_code": "100001"
  }'
```

New addresses automatically sync to Terminal Africa.

---

## 💡 Tips

### 1. Check if Address is Synced
```bash
curl -X GET "http://localhost:4500/api/addresses" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Look for `terminal_address_id` field in response.

### 2. Environment Switching
Edit `.env` file:
```env
TERMINAL_ENV=test   # For testing
TERMINAL_ENV=live   # For production
```

Restart server after changing.

### 3. Rate Fetching Tips
- Response time: 5-10 seconds (fetches from multiple carriers)
- Returns 3-5 rates typically
- Rates include carrier name, amount, delivery time
- Parcel is created automatically

---

## 🔍 Troubleshooting

### "Pickup address must be provided"
**Cause:** Using address from LIVE environment with TEST API  
**Solution:** Use addresses with ID >= 10

### "Address not synced to Terminal"
**Cause:** Address doesn't have `terminal_address_id`  
**Solution:** Create new address via API (auto-syncs)

### "No packaging options available"
**Cause:** No packaging in Terminal account  
**Solution:** Create packaging first using create packaging endpoint

---

## 📊 Expected Response Times

| Endpoint | Response Time |
|----------|--------------|
| Get Carriers | < 1 second |
| Get Packaging | < 1 second |
| Create Packaging | < 2 seconds |
| Get Rates | 5-10 seconds |

---

## ✅ Test Results

All Phase 4 endpoints tested and working:
- ✅ Carriers (39 total, 23 active)
- ✅ Packaging (list and create)
- ✅ Address sync
- ✅ Multi-carrier rates

---

## 🚀 Next: Phase 5

Phase 4 complete! Next steps:
1. Create shipment from selected rate
2. Track shipment
3. Cancel shipment
4. Webhook integration

---

## 📞 Support

- **Server:** http://localhost:4500
- **Environment:** TEST (sandbox.terminal.africa)
- **Test User:** devtomiwa9@gmail.com
- **Documentation:** See `docs/TERMINAL_PHASE4_COMPLETE.md`
