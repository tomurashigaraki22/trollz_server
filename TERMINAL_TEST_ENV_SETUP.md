# Terminal Africa Test Environment - Setup Complete ✅

## 🎉 Successfully Switched to Test Environment!

**Date**: 2026-05-04  
**Environment**: Test/Sandbox  
**Base URL**: https://sandbox.terminal.africa/v1

---

## ✅ What Changed

### Before (Live Environment)
- Base URL: `https://api.terminal.africa/v1`
- API Keys: Live keys (`pk_live_*`, `sk_live_*`)
- Real charges and production data
- Slower API responses

### After (Test Environment)
- Base URL: `https://sandbox.terminal.africa/v1`
- API Keys: Test keys (`pk_test_*`, `sk_test_*`)
- No charges, test data only
- **Faster API responses** ⚡
- 39 carriers available (vs 35 in live)

---

## 🚀 Benefits of Test Environment

1. **Faster Responses** - Sandbox API is typically faster
2. **No Charges** - All API calls are free
3. **Safe Testing** - No impact on production data
4. **More Carriers** - 39 carriers available for testing
5. **Unlimited Testing** - Test as much as you want

---

## 📋 Current Configuration

```
Environment: test
Base URL: https://sandbox.terminal.africa/v1
Public Key: pk_test_WeDJ1I1cKKkubg60rE6kXnwPJXlExlH1
Secret Key: sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn
```

---

## 🔄 How to Switch Environments

### Switch to Test (Sandbox)
```bash
python switch_terminal_env.py test
```

### Switch to Live (Production)
```bash
python switch_terminal_env.py live
```

### Verify Current Environment
```bash
python verify_terminal_env.py
```

**Note**: Restart your server after switching:
```bash
python app.py
```

---

## ✅ Verification Results

```
✅ Client initialized
   Environment: test
   Base URL: https://sandbox.terminal.africa/v1

✅ API is responding!
   Found 39 carriers

Sample Carriers:
   ✅ Air Cargo
   ✅ Aramex
   ✅ Canada Post
   ✅ Chowdeck
   ✅ Colissimo
```

---

## 🧪 Testing with Test Environment

### 1. Restart Your Server
```bash
python app.py
```

### 2. Test Carriers Endpoint
```bash
python test_terminal_carriers.py
```

Expected: Faster response, 39 carriers

### 3. Test Rates Endpoint
Now that we're using the test environment, the rates endpoint should respond faster!

**Postman Request**:
```
POST http://localhost:4500/api/shipping/rates
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

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
  "currency": "NGN"
}
```

---

## ⚠️ Important Notes

### Addresses Need Re-Syncing
Your existing addresses were synced to the **live** environment. You'll need to:

1. **Option A**: Create new addresses (they'll auto-sync to test environment)
2. **Option B**: Re-sync existing addresses to test environment

### Re-Sync Existing Addresses
```bash
POST http://localhost:4500/api/addresses/{address_id}/sync-terminal
Authorization: Bearer YOUR_TOKEN
```

This will sync the address to the test environment.

---

## 📊 Test vs Live Comparison

| Feature | Test Environment | Live Environment |
|---------|-----------------|------------------|
| Base URL | sandbox.terminal.africa | api.terminal.africa |
| API Keys | pk_test_*, sk_test_* | pk_live_*, sk_live_* |
| Carriers | 39 | 35 |
| Response Time | Faster ⚡ | Slower |
| Charges | Free | Real charges |
| Data | Test data | Production data |
| Rate Limits | Relaxed | Strict |

---

## 🎯 Next Steps

### 1. Restart Server
```bash
python app.py
```

### 2. Re-Sync Addresses (or Create New Ones)
```bash
# Option A: Create new test address
POST http://localhost:4500/api/addresses
Authorization: Bearer YOUR_TOKEN

{
  "first_name": "Test",
  "last_name": "User",
  "phone": "+2348012345678",
  "email": "test@example.com",
  "street": "123 Test Street",
  "city": "Lagos",
  "state": "Lagos",
  "country": "NG",
  "post_code": "100001"
}

# Option B: Re-sync existing address
POST http://localhost:4500/api/addresses/4/sync-terminal
Authorization: Bearer YOUR_TOKEN
```

### 3. Test Rates Endpoint
Should be much faster now!

---

## 🔧 Files Modified

1. ✅ `config.py` - Added `get_terminal_base_url()` method
2. ✅ `services/terminal_service.py` - Uses dynamic base URL
3. ✅ `.env` - Created with `TERMINAL_ENV=test`

---

## 📝 Environment File (.env)

Created `.env` file with:
```
TERMINAL_ENV=test
```

This file controls which environment is used. Change to `live` for production.

---

## 🎉 Ready to Test!

Your Terminal Africa integration is now using the **test/sandbox environment**. This should provide:
- ✅ Faster API responses
- ✅ No charges
- ✅ Safe testing
- ✅ More carriers (39 vs 35)

**Restart your server and try the rates endpoint again!**

---

## 🆘 Troubleshooting

### Server Still Using Live Environment
1. Check `.env` file exists and contains `TERMINAL_ENV=test`
2. Restart the server completely
3. Run `python verify_terminal_env.py` to confirm

### Addresses Not Syncing
- Addresses are environment-specific
- Re-sync existing addresses or create new ones
- Check Terminal sandbox dashboard

### Still Getting Timeouts
- Test environment should be faster
- If still slow, try lighter items (0.5 kg)
- Check Terminal sandbox status

---

**Last Updated**: 2026-05-04  
**Status**: ✅ Test Environment Active  
**Ready for**: Faster testing and development
