# Phase 4 Ready - Tracking Integration

## Status: ✅ COMPLETE

Phase 4 of the Sendbox API integration is now complete and ready for testing!

---

## What's New in Phase 4

### 🎯 Real-Time Tracking Updates
- Webhook endpoint receives automatic updates from Sendbox
- Order statuses update automatically when shipment status changes
- No manual intervention needed for tracking updates

### 📍 Enhanced Customer Tracking
- Track by internal tracking number (enhanced)
- Track by Sendbox tracking code (new)
- View tracking timeline with event history
- See current location and carrier information
- View estimated delivery date

### 🔄 Tracking Synchronization
- Automatic sync via webhooks (real-time)
- On-demand sync when customer views tracking
- Admin can force refresh tracking
- Bulk sync for multiple orders

---

## New Endpoints

### Public Endpoints:

**GET /api/orders/track/<tracking_number>**
- Enhanced with Sendbox tracking information
- Returns order details + tracking timeline
- No authentication required

**GET /api/shipping/track/<tracking_code>**
- Track by Sendbox tracking code
- Syncs latest tracking from Sendbox
- Returns comprehensive tracking info
- No authentication required

**POST /api/webhooks/sendbox**
- Receives webhooks from Sendbox
- Updates order status automatically
- Logs all webhook events

### Admin Endpoints:

**POST /api/admin/shipping/sync-tracking**
- Bulk sync tracking for multiple orders
- Requires admin authentication

**POST /api/admin/orders/<id>/refresh-tracking**
- Force refresh tracking for single order
- Requires admin authentication

---

## Quick Start

### 1. Test Webhook Endpoint

```bash
# Test webhook reception
curl -X POST http://localhost:5000/api/webhooks/test \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### 2. Track an Order

```bash
# Track by internal tracking number
curl http://localhost:5000/api/orders/track/TS1713600000123

# Track by Sendbox tracking code
curl http://localhost:5000/api/shipping/track/SB123456789
```

### 3. Admin: Refresh Tracking

```bash
# Force refresh tracking for an order
curl -X POST http://localhost:5000/api/admin/orders/1/refresh-tracking \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### 4. Admin: Bulk Sync

```bash
# Sync tracking for multiple orders
curl -X POST http://localhost:5000/api/admin/shipping/sync-tracking \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"order_ids": [1, 2, 3, 4, 5]}'
```

---

## Testing Workflow

### Complete Order-to-Tracking Flow:

1. **Create Order with Shipping**
   ```bash
   POST /api/checkout
   {
     "address_id": 1,
     "payment_method": "flutterwave",
     "transaction_id": "FLW123456",
     "items": [...],
     "selected_shipping": {
       "quote_id": 1,
       "carrier": "DHL",
       "service_code": "standard",
       "shipping_cost": 5000
     }
   }
   ```

2. **Shipment Created Automatically**
   - Order is paid → Sendbox shipment created
   - Order updated with tracking code
   - Callback URL registered for webhooks

3. **Simulate Tracking Update (Staging)**
   ```bash
   # Use Sendbox staging API to move tracking
   POST https://sandbox.staging.sendbox.co/shipping/move_tracking
   {
     "code": "SB123456789"
   }
   ```

4. **Webhook Received**
   - Sendbox sends webhook to `/api/webhooks/sendbox`
   - Order status updated automatically
   - Webhook logged to database

5. **Customer Views Tracking**
   ```bash
   GET /api/orders/track/TS1713600000123
   # or
   GET /api/shipping/track/SB123456789
   ```

6. **See Updated Status**
   - Tracking timeline shows all events
   - Current status displayed
   - Estimated delivery date shown

---

## Webhook Configuration

### Staging Environment:

1. **Callback URL in Code:**
   - Currently set in `services/shipment_manager.py`
   - Uses staging URL by default
   - Update for production deployment

2. **Sendbox Portal Configuration:**
   - Log in to https://developers.staging.sendbox.co/
   - Navigate to Webhooks settings
   - Add webhook URL: `https://yourdomain.com/api/webhooks/sendbox`
   - Select events: Shipment status updates
   - Save configuration

### Production Environment:

1. **Update Callback URL:**
   ```python
   # In services/shipment_manager.py
   callback_url = "https://yourdomain.com/api/webhooks/sendbox"
   ```

2. **Configure in Sendbox Production Portal:**
   - Log in to https://live.sendbox.co/
   - Add production webhook URL
   - Test webhook delivery

---

## Status Mapping Reference

| Sendbox Status | Order Status | Delivery Status | Description |
|----------------|--------------|-----------------|-------------|
| drafted | processing | Pending | Shipment created |
| pending | processing | Pending | Awaiting pickup |
| pickup_started | processing | Pending | Courier on the way |
| pickup_completed | shipped | in_transit | Package picked up |
| in_transit | shipped | in_transit | In transit |
| in_delivery | shipped | in_transit | Out for delivery |
| delivered | delivered | delivered | Delivered |
| cancelled | cancelled | Pending | Cancelled |
| failed | processing | Pending | Delivery failed |

---

## Tracking Response Example

```json
{
  "status": "success",
  "data": {
    "order": {
      "id": 1,
      "tracking": "TS1713600000123",
      "order_status": "shipped",
      "delivery_status": "in_transit",
      "total_amount": 55000,
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
          "timestamp": "2026-04-20T10:30:00Z"
        },
        {
          "status": "in_transit",
          "description": "Package is in transit to destination",
          "location": "Abuja, Nigeria",
          "timestamp": "2026-04-21T14:20:00Z"
        }
      ],
      "last_updated": "2026-04-21T14:20:00Z",
      "current_location": "Abuja, Nigeria"
    }
  }
}
```

---

## Database Tables

### webhook_events
Logs all incoming webhooks:
- `event_type` - Type of webhook event
- `order_id` - Associated order ID
- `sendbox_tracking_code` - Tracking code
- `payload` - Full webhook payload (JSON)
- `processed` - Whether webhook was processed successfully
- `error_message` - Error if processing failed
- `created_at` - When webhook was received

### Query Webhook Logs:
```sql
-- View recent webhooks
SELECT * FROM webhook_events 
ORDER BY created_at DESC 
LIMIT 10;

-- View failed webhooks
SELECT * FROM webhook_events 
WHERE processed = FALSE;

-- View webhooks for specific order
SELECT * FROM webhook_events 
WHERE order_id = 1;
```

---

## Troubleshooting

### Webhooks Not Received:

1. **Check webhook URL is accessible:**
   ```bash
   curl -X POST https://yourdomain.com/api/webhooks/test \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```

2. **Verify Sendbox configuration:**
   - Check webhook URL in Sendbox portal
   - Ensure URL is publicly accessible
   - Verify events are selected

3. **Review webhook logs:**
   ```sql
   SELECT * FROM webhook_events 
   WHERE processed = FALSE 
   ORDER BY created_at DESC;
   ```

### Tracking Not Updating:

1. **Check Sendbox API connectivity:**
   ```bash
   # Test tracking endpoint
   curl http://localhost:5000/api/shipping/track/SB123456789
   ```

2. **Force refresh tracking:**
   ```bash
   curl -X POST http://localhost:5000/api/admin/orders/1/refresh-tracking \
     -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
   ```

3. **Check order has tracking code:**
   ```sql
   SELECT id, tracking, sendbox_tracking_code, sendbox_status 
   FROM orders 
   WHERE id = 1;
   ```

### Status Not Mapping Correctly:

1. **Review webhook payload:**
   ```sql
   SELECT payload FROM webhook_events 
   WHERE order_id = 1 
   ORDER BY created_at DESC 
   LIMIT 1;
   ```

2. **Check status mapping:**
   - Review `services/shipment_manager.py`
   - Function: `map_sendbox_status_to_internal()`
   - Update mapping if needed

---

## Next Steps

### Testing Checklist:
- [ ] Test webhook endpoint reception
- [ ] Create order with shipment
- [ ] Simulate tracking update in staging
- [ ] Verify webhook updates order
- [ ] Test tracking by internal tracking number
- [ ] Test tracking by Sendbox tracking code
- [ ] Test admin refresh tracking
- [ ] Test bulk sync tracking
- [ ] Review webhook logs
- [ ] Test error handling

### Before Production:
- [ ] Update callback URL to production domain
- [ ] Configure webhooks in Sendbox production portal
- [ ] Test webhook delivery in production
- [ ] Set up monitoring for webhook failures
- [ ] Create customer notification system
- [ ] Document webhook signature verification (if available)

### Optional Enhancements:
- [ ] Customer email notifications on status changes
- [ ] SMS tracking updates
- [ ] Tracking page with map visualization
- [ ] Proactive delivery issue alerts
- [ ] Estimated delivery time predictions

---

## Documentation

- **Phase 4 Completion Summary:** `PHASE4_COMPLETION_SUMMARY.md`
- **API Documentation:** `ADDRESSES_SHIPPING_API_DOCUMENTATION.md` (to be updated)
- **Integration Plan:** `SENDBOX_INTEGRATION_PHASES.md`
- **Sendbox API Reference:** `SENDBOX_D.md`

---

## Support

For issues or questions:
1. Review `PHASE4_COMPLETION_SUMMARY.md` for detailed information
2. Check webhook logs in `webhook_events` table
3. Test endpoints with provided curl commands
4. Review Sendbox API documentation

---

**Phase 4 Status:** ✅ COMPLETE AND READY FOR TESTING

**Completed:** April 20, 2026

**Next Phase:** Phase 5 - Admin Features (Optional)
