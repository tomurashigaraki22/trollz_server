# Sendbox Integration Setup Complete! ✅

## What Was Done

### 1. Database Migrations Applied ✅
All required tables have been created:
- ✅ `shipping_addresses` - Store customer shipping addresses
- ✅ `shipping_quotes` - Store shipping quote history
- ✅ `webhook_events` - Log Sendbox webhook events
- ✅ `orders` table updated with Sendbox fields
- ✅ `product` table updated with weight field

### 2. Warehouse Address Updated ✅
Your pickup location has been configured:
- **Address:** LYPAS Plaza, Cluster Industrial Complex, Owerri
- **City:** Owerri
- **State:** Imo
- **Country:** Nigeria (NG)

This address will be used as the origin for all shipping calculations.

---

## Quick Test

### Test the Address API

```bash
# 1. Login to get token (replace with your credentials)
curl -X POST http://localhost:4500/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your_email@example.com",
    "password": "your_password"
  }'

# 2. Create a shipping address (use token from step 1)
curl -X POST http://localhost:4500/api/addresses \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "phone": "08001234567",
    "street": "123 Test Street",
    "city": "Lagos",
    "state": "Lagos",
    "country": "NG"
  }'

# 3. List your addresses
curl http://localhost:4500/api/addresses \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Next Steps

### 1. Configure Sendbox API Key

Update your `.env` file with your Sendbox API key:

```bash
# Get your API key from: https://developers.staging.sendbox.co/
SENDBOX_API_KEY=your_actual_sendbox_api_key_here
SENDBOX_ENV=staging
```

### 2. Update Warehouse Phone Number

Update the warehouse phone number in `.env`:

```bash
WAREHOUSE_PHONE=+234_YOUR_ACTUAL_PHONE_NUMBER
WAREHOUSE_EMAIL=your_actual_email@trollzstore.com
```

### 3. Test Shipping Quotes

Once you have the Sendbox API key configured:

```bash
curl -X POST http://localhost:4500/api/shipping/quotes \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "destination_address_id": 1,
    "items": [
      {
        "product_id": 1,
        "quantity": 1
      }
    ]
  }'
```

---

## Database Tables Created

### shipping_addresses
Stores customer shipping addresses with:
- User information (first name, last name, phone, email)
- Address details (street, city, state, country, postal code)
- Coordinates (latitude, longitude) for mapping
- Default address flag

### shipping_quotes
Stores shipping quote history with:
- Origin and destination details
- Weight and service type
- Carrier and quoted price
- Quote data (JSON)
- Expiration timestamp

### webhook_events
Logs all Sendbox webhook events with:
- Event type
- Order ID and tracking code
- Full payload (JSON)
- Processing status
- Error messages (if any)

### orders (updated)
Added Sendbox fields:
- `sendbox_shipment_id` - Sendbox shipment ID
- `sendbox_tracking_code` - Sendbox tracking code
- `sendbox_status` - Current Sendbox status
- `sendbox_carrier` - Carrier name (DHL, FedEx, etc.)
- `shipping_cost` - Shipping cost
- `estimated_delivery_date` - Estimated delivery date
- `sendbox_webhook_data` - Latest webhook data (JSON)

### product (updated)
Added weight field:
- `weight` - Product weight in KG (default: 0.50)

---

## Warehouse Configuration

Your warehouse address is now configured as:

```
Trollz Store Warehouse
LYPAS Plaza, Cluster Industrial Complex
Owerri, Imo State
Nigeria (NG)
Postal Code: 460001
```

This address will be used as the **origin** for all shipping calculations. Shipping costs will be calculated from Owerri to the customer's delivery address.

---

## API Endpoints Available

### Address Management:
- `POST /api/addresses` - Create shipping address
- `GET /api/addresses` - List user addresses
- `GET /api/addresses/<id>` - Get single address
- `PUT /api/addresses/<id>` - Update address
- `DELETE /api/addresses/<id>` - Delete address
- `POST /api/addresses/<id>/set-default` - Set default
- `GET /api/addresses/default` - Get default address

### Shipping Quotes:
- `POST /api/shipping/quotes` - Get shipping quotes
- `GET /api/shipping/quotes/<id>` - Get quote by ID
- `GET /api/shipping/quotes/history` - Quote history
- `POST /api/shipping/landed-cost` - Calculate landed cost

### Checkout:
- `POST /api/checkout` - Create order with shipping

### Tracking:
- `GET /api/orders/track/<tracking_number>` - Track order
- `GET /api/shipping/track/<tracking_code>` - Track by Sendbox code

### Webhooks:
- `POST /api/webhooks/sendbox` - Receive Sendbox webhooks
- `POST /api/webhooks/test` - Test webhook

### Admin:
- `POST /api/admin/orders/<id>/create-shipment` - Create shipment
- `POST /api/admin/orders/<id>/cancel-shipment` - Cancel shipment
- `GET /api/admin/orders/<id>/sendbox-details` - View Sendbox data
- `POST /api/admin/orders/<id>/refresh-tracking` - Refresh tracking
- `POST /api/admin/orders/bulk-create-shipments` - Bulk create
- `GET /api/admin/reports/shipping` - Shipping reports
- `GET /api/admin/sendbox/account` - Account info
- `POST /api/admin/sendbox/fund-account` - Fund staging account

---

## Documentation Available

### For Backend Team:
- `PHASE1_COMPLETION_SUMMARY.md` - Foundation setup
- `PHASE2_COMPLETION_SUMMARY.md` - Shipping quotes
- `PHASE3_COMPLETION_SUMMARY.md` - Shipment creation
- `PHASE4_COMPLETION_SUMMARY.md` - Tracking integration
- `PHASE5_COMPLETION_SUMMARY.md` - Admin features
- `PHASE6_COMPLETION_SUMMARY.md` - Testing & optimization
- `ADMIN_API_DOCUMENTATION.md` - Admin API reference
- `ADDRESSES_SHIPPING_API_DOCUMENTATION.md` - Shipping API docs

### For Frontend/Mobile Team:
- `MOBILE_APP_INTEGRATION_GUIDE.md` - Complete integration guide
- `PHASE6_READY.md` - Quick start guide

### For Testing:
- `PHASE4_TESTING_GUIDE.md` - Testing procedures
- `tests/test_sendbox_integration.py` - Test suite
- `run_tests.py` - Test runner

---

## Troubleshooting

### Issue: "Table doesn't exist"
**Solution:** ✅ Already fixed! Migrations have been applied.

### Issue: "Sendbox API error"
**Solution:** Make sure you have:
1. Valid Sendbox API key in `.env`
2. Correct environment (staging/live)
3. Internet connectivity

### Issue: "Address not found"
**Solution:** Create a shipping address first using `POST /api/addresses`

### Issue: "Quote expired"
**Solution:** Quotes expire after 24 hours. Request a new quote.

---

## Support

For issues or questions:
1. Check the relevant documentation file
2. Review error messages in API responses
3. Check application logs
4. Test in staging environment first

---

## What's Next?

### Immediate:
1. ✅ Database tables created
2. ✅ Warehouse address configured
3. [ ] Add Sendbox API key to `.env`
4. [ ] Update warehouse phone/email
5. [ ] Test address creation
6. [ ] Test shipping quotes

### Before Production:
1. [ ] Get production Sendbox API key
2. [ ] Configure production webhook URL
3. [ ] Test complete order flow
4. [ ] Set up monitoring and alerts
5. [ ] Train support team

---

**Setup Status:** ✅ COMPLETE

**Database:** ✅ Migrated

**Warehouse:** ✅ Configured (Owerri, Imo State)

**Ready for:** Testing with Sendbox API key

---

**Date:** April 20, 2026

**Version:** 1.0
