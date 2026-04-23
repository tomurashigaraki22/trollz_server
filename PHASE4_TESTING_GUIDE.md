# Phase 4 Testing Guide - Tracking Integration

## Quick Testing Checklist

This guide provides step-by-step instructions for testing Phase 4 tracking integration features.

---

## Prerequisites

- [ ] Phase 1, 2, and 3 completed
- [ ] Database migrations applied
- [ ] Sendbox API key configured
- [ ] Server running on http://localhost:4500

---

## Test 1: Webhook Endpoint Reception

### Test the webhook test endpoint:

```bash
curl -X POST http://localhost:4500/api/webhooks/test \
  -H "Content-Type: application/json" \
  -d '{"test": "webhook reception"}'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Test webhook received",
  "received_data": {
    "test": "webhook reception"
  }
}
```

✅ **Pass Criteria:** Status 200, success message returned

---

## Test 2: Create Order with Shipment

### Step 1: Create a shipping address

```bash
curl -X POST http://localhost:4500/api/addresses \
  -H "Authorization: Bearer YOUR_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "phone": "08001234567",
    "street": "123 Test Street",
    "city": "Lagos",
    "state": "Lagos",
    "country": "NG",
    "post_code": "100001"
  }'
```

**Note the address_id from response**

### Step 2: Get shipping quote

```bash
curl -X POST http://localhost:4500/api/shipping/quotes \
  -H "Authorization: Bearer YOUR_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "destination_address_id": 1,
    "items": [
      {
        "product_id": 55,
        "quantity": 1
      }
    ],
    "service_code": "standard"
  }'
```

**Note the quote_id from response**

### Step 3: Create order with shipping

```bash
curl -X POST http://localhost:4500/api/checkout \
  -H "Authorization: Bearer YOUR_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 1,
    "payment_method": "flutterwave",
    "transaction_id": "TEST123456",
    "items": [
      {
        "product_id": 55,
        "quantity": 1
      }
    ],
    "selected_shipping": {
      "quote_id": 1,
      "carrier": "DHL",
      "service_code": "standard",
      "shipping_cost": 5000
    }
  }'
```

**Expected Response:**
- Order created successfully
- Shipment created automatically
- `sendbox_tracking_code` present in response

✅ **Pass Criteria:** 
- Status 201
- Order has tracking number
- Shipment created = true
- Sendbox tracking code present

---

## Test 3: Track Order by Internal Tracking Number

### Use the tracking number from Test 2:

```bash
curl http://localhost:4500/api/orders/track/TS1713600000123
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "order": { /* order details */ },
    "tracking": {
      "order_tracking": "TS1713600000123",
      "sendbox_tracking_code": "SB123456789",
      "carrier": "DHL",
      "current_status": "pending",
      "order_status": "processing",
      "delivery_status": "Pending"
    }
  }
}
```

✅ **Pass Criteria:**
- Status 200
- Order details returned
- Tracking information present
- Sendbox tracking code shown

---

## Test 4: Track Shipment by Sendbox Tracking Code

### Use the Sendbox tracking code from Test 2:

```bash
curl http://localhost:4500/api/shipping/track/SB123456789
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Tracking information retrieved successfully",
  "data": {
    "tracking": {
      "sendbox_tracking_code": "SB123456789",
      "carrier": "DHL",
      "current_status": "pending",
      "tracking_timeline": [...]
    },
    "order_id": 1,
    "order_tracking": "TS1713600000123"
  }
}
```

✅ **Pass Criteria:**
- Status 200
- Tracking information returned
- Timeline present
- Order ID and tracking number shown

---

## Test 5: Simulate Webhook from Sendbox

### Send a test webhook to update order status:

```bash
curl -X POST http://localhost:4500/api/webhooks/sendbox \
  -H "Content-Type: application/json" \
  -d '{
    "event": "shipment.status_updated",
    "tracking_code": "SB123456789",
    "shipment_id": 12345,
    "status": "in_transit",
    "timestamp": "2026-04-21T14:20:00Z",
    "data": {
      "carrier": "DHL",
      "current_location": "Abuja, Nigeria"
    }
  }'
```

**Expected Response:**
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

✅ **Pass Criteria:**
- Status 200
- Webhook processed successfully
- Order status updated to "shipped"
- Delivery status updated to "in_transit"

---

## Test 6: Verify Order Status Updated

### Check that the webhook updated the order:

```bash
curl http://localhost:4500/api/orders/track/TS1713600000123
```

**Expected Changes:**
- `order_status` changed from "processing" to "shipped"
- `delivery_status` changed from "Pending" to "in_transit"
- `sendbox_status` is "in_transit"

✅ **Pass Criteria:**
- Order status reflects webhook update
- Tracking timeline shows new event

---

## Test 7: Admin Refresh Tracking

### Force refresh tracking from Sendbox:

```bash
curl -X POST http://localhost:4500/api/admin/orders/1/refresh-tracking \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Tracking information refreshed successfully",
  "data": {
    "sendbox_status": "in_transit",
    "order_status": "shipped",
    "delivery_status": "in_transit",
    "tracking_data": { /* full tracking data */ }
  }
}
```

✅ **Pass Criteria:**
- Status 200
- Tracking refreshed successfully
- Latest status from Sendbox

---

## Test 8: Bulk Sync Tracking

### Sync tracking for multiple orders:

```bash
curl -X POST http://localhost:4500/api/admin/shipping/sync-tracking \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "order_ids": [1, 2, 3]
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Synced 2 of 3 orders",
  "data": {
    "success": [1, 2],
    "failed": [
      {
        "order_id": 3,
        "error": "No tracking code found"
      }
    ],
    "total": 3
  }
}
```

✅ **Pass Criteria:**
- Status 200
- Success/failed breakdown provided
- Orders with tracking codes synced

---

## Test 9: Check Webhook Logs

### Query the database to verify webhook logging:

```sql
-- View recent webhooks
SELECT * FROM webhook_events 
ORDER BY created_at DESC 
LIMIT 10;

-- Check webhook was processed
SELECT 
  event_type, 
  sendbox_tracking_code, 
  processed, 
  error_message,
  created_at 
FROM webhook_events 
WHERE sendbox_tracking_code = 'SB123456789';
```

✅ **Pass Criteria:**
- Webhook logged in database
- `processed` = TRUE
- No error message
- Correct tracking code

---

## Test 10: Error Handling

### Test webhook with invalid tracking code:

```bash
curl -X POST http://localhost:4500/api/webhooks/sendbox \
  -H "Content-Type: application/json" \
  -d '{
    "event": "shipment.status_updated",
    "tracking_code": "INVALID_CODE",
    "status": "in_transit"
  }'
```

**Expected Response:**
```json
{
  "status": "error",
  "message": "Order not found for tracking code"
}
```

✅ **Pass Criteria:**
- Status 404
- Error message clear
- Webhook logged with error

### Test tracking with invalid code:

```bash
curl http://localhost:4500/api/shipping/track/INVALID_CODE
```

**Expected Response:**
```json
{
  "status": "error",
  "message": "Shipment not found for tracking code"
}
```

✅ **Pass Criteria:**
- Status 404
- Error message clear

---

## Staging Environment Testing

### If using Sendbox staging environment:

1. **Fund Staging Account:**
```bash
curl -X POST https://sandbox.staging.sendbox.co/payments/add_money \
  -H "Authorization: YOUR_SENDBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount": 10000}'
```

2. **Create Real Shipment:**
- Follow Test 2 to create order
- Verify shipment created in Sendbox portal

3. **Simulate Tracking Update:**
```bash
curl -X POST https://sandbox.staging.sendbox.co/shipping/move_tracking \
  -H "Authorization: YOUR_SENDBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "SB123456789"}'
```

4. **Verify Webhook Received:**
- Check webhook_events table
- Verify order status updated

---

## Test Results Summary

| Test | Description | Status | Notes |
|------|-------------|--------|-------|
| 1 | Webhook endpoint reception | ⬜ | |
| 2 | Create order with shipment | ⬜ | |
| 3 | Track by internal tracking | ⬜ | |
| 4 | Track by Sendbox code | ⬜ | |
| 5 | Simulate webhook | ⬜ | |
| 6 | Verify status updated | ⬜ | |
| 7 | Admin refresh tracking | ⬜ | |
| 8 | Bulk sync tracking | ⬜ | |
| 9 | Check webhook logs | ⬜ | |
| 10 | Error handling | ⬜ | |

**Legend:** ⬜ Not tested | ✅ Passed | ❌ Failed

---

## Common Issues and Solutions

### Issue: Webhook not updating order

**Solution:**
1. Check webhook payload format
2. Verify tracking code matches
3. Check webhook_events table for errors
4. Review application logs

### Issue: Tracking not syncing

**Solution:**
1. Verify Sendbox API key is valid
2. Check internet connectivity
3. Test with admin refresh endpoint
4. Review error logs

### Issue: Status not mapping correctly

**Solution:**
1. Check Sendbox status value in webhook
2. Review `map_sendbox_status_to_internal()` function
3. Update status mapping if needed

---

## Production Readiness Checklist

Before deploying to production:

- [ ] All tests passed in staging
- [ ] Webhook URL updated to production domain
- [ ] Webhooks configured in Sendbox production portal
- [ ] Webhook signature verification implemented (if available)
- [ ] Error monitoring set up
- [ ] Customer notification system ready
- [ ] Documentation updated
- [ ] Team trained on tracking features

---

## Support

For issues during testing:
1. Check `PHASE4_COMPLETION_SUMMARY.md` for detailed information
2. Review `PHASE4_READY.md` for troubleshooting
3. Check application logs
4. Query webhook_events table for webhook issues

---

**Testing Guide Version:** 1.0
**Last Updated:** April 20, 2026
**Phase:** 4 - Tracking Integration
