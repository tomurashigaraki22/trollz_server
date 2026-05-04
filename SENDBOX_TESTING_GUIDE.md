# Sendbox Integration Testing Guide

## Overview

Comprehensive testing guide for the Sendbox shipping integration, covering order creation, shipping quotes, shipment tracking, and more.

## Test Scripts

### 1. Quick Test (No Database Required)
**File:** `test_sendbox_quick.py`

Tests basic Sendbox functionality without database dependencies.

```bash
python test_sendbox_quick.py
```

**Tests:**
- ✅ API Health Check
- ✅ Shipping Quotes
- ✅ Landed Cost Calculation
- ✅ Address Validation

### 2. Comprehensive Test (Full Integration)
**File:** `test_sendbox_orders.py`

Tests complete order flow including database operations.

```bash
python test_sendbox_orders.py
```

**Tests:**
- ✅ User Registration & Login
- ✅ Address Management
- ✅ Shipping Quotes
- ✅ Product Retrieval
- ✅ Order Creation with Shipping
- ✅ Payment Confirmation
- ✅ Shipment Creation
- ✅ Shipment Tracking
- ✅ Admin Endpoints

### 3. Token Authentication Test
**File:** `test_token_refresh.py`

Tests Sendbox token authentication and auto-refresh.

```bash
python test_token_refresh.py
```

**Tests:**
- ✅ Token Decoding
- ✅ Token Expiry Check
- ✅ API Call with Token Auth
- ✅ Shipping Quotes with Token

## Prerequisites

### 1. Server Running
```bash
python app.py
```

### 2. Database Setup
```bash
python check_and_create_tables.py
```

### 3. Environment Configuration

Ensure your `.env` file has:
```env
# Database
DB_HOST=your_host
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database

# Sendbox
SENDBOX_ENV=staging  # or 'live'

# Warehouse Address
WAREHOUSE_CITY=Owerri
WAREHOUSE_STATE=Imo
WAREHOUSE_COUNTRY=NG
```

### 4. Sendbox Tokens

Update `services/sendbox_service.py` with appropriate tokens:
- Staging tokens for testing
- Live tokens for production

## Test Scenarios

### Scenario 1: Basic Shipping Quote

**Endpoint:** `POST /api/shipping/quotes`

**Test Data:**
```json
{
  "destination": {
    "name": "John Doe",
    "phone": "+2348087654321",
    "email": "john@example.com",
    "address": "123 Test Street",
    "city": "Lagos",
    "state": "Lagos",
    "country": "NG"
  },
  "weight": 1.5,
  "items": [
    {
      "name": "Test Product",
      "quantity": 2,
      "value": 10000,
      "weight": 0.75
    }
  ],
  "total_value": 10000
}
```

**Expected Result:**
```json
{
  "status": "success",
  "data": {
    "quotes": [
      {
        "service_name": "Standard Delivery",
        "amount": 2500,
        "delivery_time": "3-5 business days"
      }
    ]
  }
}
```

### Scenario 2: Create Order with Shipping

**Endpoint:** `POST /api/checkout`

**Test Data:**
```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": 5000
    }
  ],
  "address_id": 1,
  "selected_shipping": {
    "service_code": "standard",
    "service_name": "Standard Delivery",
    "amount": 2500,
    "delivery_time": "3-5 business days"
  },
  "payment_method": "flutterwave"
}
```

**Expected Result:**
```json
{
  "status": "success",
  "data": {
    "order": {
      "id": 123,
      "total_amount": 12500,
      "shipping_fee": 2500,
      "status": "pending"
    }
  }
}
```

### Scenario 3: Confirm Payment (Creates Shipment)

**Endpoint:** `POST /api/orders/{id}/confirm`

**Test Data:**
```json
{
  "payment_reference": "FLW_REF_123456",
  "payment_method": "flutterwave"
}
```

**Expected Result:**
```json
{
  "status": "success",
  "data": {
    "id": 123,
    "status": "paid",
    "sendbox_tracking_code": "SB123456789",
    "sendbox_shipment_id": "12345"
  }
}
```

### Scenario 4: Track Shipment

**Endpoint:** `GET /api/shipping/track/{tracking_code}`

**Expected Result:**
```json
{
  "status": "success",
  "data": {
    "tracking_code": "SB123456789",
    "status": "in_transit",
    "current_location": "Lagos Distribution Center",
    "timeline": [
      {
        "status": "picked_up",
        "timestamp": "2026-05-04T10:00:00Z",
        "location": "Owerri"
      }
    ]
  }
}
```

## Manual Testing with cURL

### 1. Get Shipping Quotes
```bash
curl -X POST http://localhost:4500/api/shipping/quotes \
  -H "Content-Type: application/json" \
  -d '{
    "destination": {
      "name": "John Doe",
      "phone": "+2348087654321",
      "email": "john@example.com",
      "address": "123 Test Street",
      "city": "Lagos",
      "state": "Lagos",
      "country": "NG"
    },
    "weight": 1.5,
    "items": [
      {
        "name": "Test Product",
        "quantity": 2,
        "value": 10000,
        "weight": 0.75
      }
    ],
    "total_value": 10000
  }'
```

### 2. Validate Address
```bash
curl -X POST http://localhost:4500/api/addresses/validate \
  -H "Content-Type: application/json" \
  -d '{
    "address": "123 Test Street",
    "city": "Lagos",
    "state": "Lagos",
    "country": "NG"
  }'
```

### 3. Track Shipment
```bash
curl http://localhost:4500/api/shipping/track/SB123456789
```

### 4. Get Admin Reports
```bash
curl http://localhost:4500/api/admin/shipping/reports \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Testing Checklist

### Before Testing
- [ ] Server is running (`python app.py`)
- [ ] Database is set up and accessible
- [ ] Sendbox tokens are configured
- [ ] Environment is set (staging or live)
- [ ] Test products exist in database
- [ ] Warehouse address is configured

### Basic Tests
- [ ] API health check passes
- [ ] Can get shipping quotes
- [ ] Can validate addresses
- [ ] Can calculate landed costs

### Order Flow Tests
- [ ] Can register/login user
- [ ] Can create shipping address
- [ ] Can get products
- [ ] Can create order with shipping
- [ ] Can confirm payment
- [ ] Shipment is created automatically
- [ ] Can track shipment

### Admin Tests
- [ ] Can view all shipments
- [ ] Can get shipping reports
- [ ] Can view webhook events
- [ ] Can retry failed webhooks

## Common Issues & Solutions

### Issue 1: 401 Authentication Error

**Symptom:** API returns 401 when calling Sendbox endpoints

**Solution:**
- Check if tokens match environment (staging vs live)
- See `TOKEN_ENVIRONMENT_MISMATCH.md`
- Run: `python update_live_tokens.py` to update tokens

### Issue 2: No Products Found

**Symptom:** Test fails because no products in database

**Solution:**
```sql
-- Add test product
INSERT INTO product (name, description, price, stock, weight, category_id)
VALUES ('Test Product', 'Test Description', 5000, 100, 0.5, 1);
```

### Issue 3: Address Creation Fails

**Symptom:** Cannot create shipping address

**Solution:**
- Check if `shipping_addresses` table exists
- Run: `python check_and_create_tables.py`
- Verify user is authenticated

### Issue 4: Shipment Not Created

**Symptom:** Order confirmed but no shipment created

**Solution:**
- Check server logs for errors
- Verify Sendbox tokens are valid
- Ensure order has shipping information
- Check warehouse address is configured

### Issue 5: Tracking Code Not Found

**Symptom:** Cannot track shipment

**Solution:**
- Shipment may not be created yet
- Check order status is "paid"
- Verify `sendbox_tracking_code` in database
- Wait a few seconds and try again

## Test Data

### Test Users
```json
{
  "email": "testuser@example.com",
  "password": "Test123!",
  "first_name": "Test",
  "last_name": "User",
  "phone": "+2348012345678"
}
```

### Test Addresses

**Lagos (Local)**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+2348087654321",
  "address": "123 Test Street, Victoria Island",
  "city": "Lagos",
  "state": "Lagos",
  "country": "NG",
  "postal_code": "100001"
}
```

**Abuja (Local)**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "+2348098765432",
  "address": "456 Central Area",
  "city": "Abuja",
  "state": "FCT",
  "country": "NG",
  "postal_code": "900001"
}
```

**International (US)**
```json
{
  "first_name": "Mike",
  "last_name": "Johnson",
  "phone": "+1234567890",
  "address": "789 Main Street",
  "city": "New York",
  "state": "NY",
  "country": "US",
  "postal_code": "10001"
}
```

## Performance Testing

### Load Test Shipping Quotes

```bash
# Install Apache Bench
# Ubuntu: sudo apt-get install apache2-utils
# Mac: brew install ab

# Test 100 requests, 10 concurrent
ab -n 100 -c 10 -p quote_payload.json -T application/json \
  http://localhost:4500/api/shipping/quotes
```

### Stress Test Order Creation

```python
# Use locust or similar tool
# File: locustfile.py

from locust import HttpUser, task, between

class OrderUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def create_order(self):
        self.client.post("/api/checkout", json={
            "items": [{"product_id": 1, "quantity": 1, "price": 5000}],
            "address_id": 1,
            "selected_shipping": {
                "service_code": "standard",
                "amount": 2500
            }
        })
```

## Monitoring During Tests

### Watch Server Logs
```bash
# In separate terminal
tail -f app.log
```

### Monitor Database
```sql
-- Check recent orders
SELECT id, status, total_amount, sendbox_tracking_code, created_at
FROM orders
ORDER BY created_at DESC
LIMIT 10;

-- Check shipments
SELECT order_id, sendbox_shipment_id, sendbox_tracking_code, status
FROM orders
WHERE sendbox_shipment_id IS NOT NULL;
```

### Check Sendbox Dashboard
- Log in to Sendbox dashboard
- View recent shipments
- Check webhook deliveries
- Monitor account balance

## Automated Testing

### CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Test Sendbox Integration

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python test_sendbox_quick.py
```

## Documentation

- **API Documentation**: `ORDERS_API_DOCUMENTATION.md`
- **Shipping API**: `ADDRESSES_SHIPPING_API_DOCUMENTATION.md`
- **Admin API**: `ADMIN_API_DOCUMENTATION.md`
- **Mobile Integration**: `MOBILE_APP_INTEGRATION_GUIDE.md`
- **Token Auth**: `SENDBOX_TOKEN_AUTH.md`

## Support

For issues:
1. Check server logs
2. Review test output
3. Verify configuration
4. Check Sendbox dashboard
5. Review documentation

Happy Testing! 🚀
