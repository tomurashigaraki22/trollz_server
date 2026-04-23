# Live Environment Now Active ✅

## Configuration Updated

Your Sendbox integration is now configured to use the **LIVE production environment**.

## Changes Made

### 1. Updated `config.py`
```python
SENDBOX_ENVIRONMENT = os.getenv("SENDBOX_ENV", "live")  # Changed from "staging"
```

### 2. Updated `.env.example`
```env
SENDBOX_ENV=live  # Changed from "staging"
```

## Current Configuration

- **Environment**: LIVE (Production)
- **Base URL**: `https://live.sendbox.co`
- **Token Authentication**: Active with auto-refresh
- **Warehouse**: LYPAS Plaza, Cluster Industrial Complex, Owerri, Imo State

## Verification

Ran verification script - confirmed:
```
✅ Environment: live
✅ Base URL: https://live.sendbox.co
✅ Token Authentication: Configured
✅ All checks passed
```

## Important Notes

### Production Environment
- ⚠️ This is the LIVE production environment
- ⚠️ Real shipments will be created
- ⚠️ Real charges will apply
- ⚠️ Ensure your Sendbox account has sufficient balance

### Token Compatibility
Your current tokens should work with both staging and live environments. If you encounter authentication issues:
1. Check if tokens are environment-specific
2. Get live environment tokens from Sendbox dashboard
3. Update tokens in `services/sendbox_service.py` if needed

## Testing in Live Environment

### 1. Test Shipping Quotes
```bash
curl -X POST http://localhost:5000/api/shipping/quotes \
  -H "Content-Type: application/json" \
  -d '{
    "destination": {
      "name": "Test Customer",
      "phone": "+2348012345678",
      "address": "123 Test Street",
      "city": "Lagos",
      "state": "Lagos",
      "country": "NG"
    },
    "weight": 0.5,
    "items": [{"name": "Test Product", "quantity": 1, "value": 5000, "weight": 0.5}]
  }'
```

### 2. Monitor Logs
Watch for:
```
INFO: Sendbox client initialized - Environment: live
INFO: Sendbox API Request: POST https://live.sendbox.co/...
```

### 3. Check Account Balance
Use the admin endpoint to verify your account balance:
```bash
curl http://localhost:5000/api/admin/shipping/account
```

## Switching Back to Staging

If you need to switch back to staging for testing:

### Option 1: Environment Variable
Update your `.env` file:
```env
SENDBOX_ENV=staging
```

### Option 2: Config File
Update `config.py`:
```python
SENDBOX_ENVIRONMENT = os.getenv("SENDBOX_ENV", "staging")
```

Then restart your server.

## Production Checklist

Before going live, ensure:

- ✅ Sendbox account is verified and active
- ✅ Account has sufficient balance for shipments
- ✅ Warehouse address is correct
- ✅ Webhook URL is configured (if using webhooks)
- ✅ Test all endpoints in staging first
- ✅ Monitor logs for errors
- ✅ Set up error alerts

## API Endpoints

All endpoints now use the live Sendbox API:

### Customer Endpoints
- `POST /api/shipping/quotes` - Get real shipping quotes
- `POST /api/checkout` - Create order with real shipment
- `POST /api/orders/{id}/confirm` - Confirm payment and create real shipment
- `GET /api/shipping/track/{code}` - Track real shipments

### Admin Endpoints
- `GET /api/admin/shipping/account` - View live account balance
- `GET /api/admin/shipping/shipments` - List all live shipments
- `POST /api/admin/shipping/shipments/{id}/cancel` - Cancel live shipments
- `GET /api/admin/shipping/reports` - Live shipping reports

### Webhooks
- `POST /api/webhooks/sendbox` - Receive live delivery updates

## Monitoring

### Success Indicators
```
✅ Environment: live
✅ Sendbox API Request: POST https://live.sendbox.co/...
✅ Shipment created successfully
✅ Access token refreshed successfully
```

### Error Indicators
```
❌ Authentication failed (check tokens)
❌ Insufficient balance (add funds to account)
❌ Invalid address (verify customer address)
```

## Support

### Sendbox Live Support
- **Dashboard**: https://live.sendbox.co/
- **Documentation**: https://developers.sendbox.co/docs
- **Support**: Contact Sendbox support team

### Internal Documentation
- **Token Auth**: `SENDBOX_TOKEN_AUTH.md`
- **Integration Guide**: `MOBILE_APP_INTEGRATION_GUIDE.md`
- **API Documentation**: `ORDERS_API_DOCUMENTATION.md`

## Next Steps

1. ✅ Verify your Sendbox live account is active
2. ✅ Check account balance
3. ✅ Test shipping quotes with real addresses
4. ✅ Create a test shipment to verify everything works
5. ✅ Monitor logs for any issues
6. ✅ Set up production monitoring and alerts

## Summary

Your Sendbox integration is now configured for the **LIVE production environment**. All API calls will use `https://live.sendbox.co` and create real shipments with real charges.

Make sure to test thoroughly and monitor your account balance! 🚀
