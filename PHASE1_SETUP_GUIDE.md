# Phase 1 Setup Guide - Sendbox Integration Foundation

This guide walks you through setting up the foundation for Sendbox API integration (Phase 1.1, 1.2, and 1.3).

## Overview

Phase 1 establishes:
- Sendbox API configuration
- Database schema updates for shipping data
- Sendbox service client for API interactions
- Address validation utilities

## Prerequisites

- Python 3.7+
- MySQL database access
- Sendbox developer account (staging)

---

## Step 1: Register for Sendbox API Access

### 1.1 Create Sendbox Developer Account

1. Visit the Sendbox Developer Portal:
   - **Staging:** https://developers.staging.sendbox.co/
   - **Production:** https://developers.sendbox.co/ (for later)

2. Sign up for an account

3. Create a new application:
   - Name: "Trollz Store"
   - Description: "E-commerce shipping integration"
   - Webhook URL: `https://yourdomain.com/api/webhooks/sendbox` (can update later)

4. Copy your API key (keep it secure!)

### 1.2 Fund Staging Account (Staging Only)

For testing in staging environment, you need to add funds:

```bash
curl -X POST https://sandbox.staging.sendbox.co/payments/add_money \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount": 10000}'
```

---

## Step 2: Configure Environment Variables

### 2.1 Copy Example Environment File

```bash
cp .env.example .env
```

### 2.2 Update .env File

Edit `.env` and add your Sendbox credentials:

```bash
# Sendbox API Configuration
SENDBOX_API_KEY=your_actual_api_key_here
SENDBOX_ENV=staging  # Use 'staging' for testing

# Warehouse Address (update with your actual warehouse location)
WAREHOUSE_FIRST_NAME=Trollz Store
WAREHOUSE_LAST_NAME=Warehouse
WAREHOUSE_STREET=Your Warehouse Street Address
WAREHOUSE_CITY=Your City
WAREHOUSE_STATE=Your State
WAREHOUSE_COUNTRY=NG
WAREHOUSE_POST_CODE=100001
WAREHOUSE_PHONE=+234 800 000 0000
WAREHOUSE_EMAIL=warehouse@trollzstore.com
```

### 2.3 Verify Configuration

```bash
python test_sendbox_setup.py
```

This will verify:
- Configuration is loaded correctly
- API key is valid
- Warehouse address is properly formatted
- API connection works

---

## Step 3: Run Database Migrations

### 3.1 Review Migration

Check what the migration will do:

```bash
cat migrations/001_add_sendbox_fields.sql
```

The migration adds:
- Sendbox fields to `orders` table
- `shipping_addresses` table
- `shipping_quotes` table
- `webhook_events` table
- `weight` field to `product` table

### 3.2 List Migration Status

```bash
python run_migrations.py list
```

### 3.3 Run Migration

```bash
python run_migrations.py run
```

Expected output:
```
======================================================================
DATABASE MIGRATION RUNNER
======================================================================
Database: trollzstorecom_tr0llz_db
Host: 57.131.33.181:3306
Migrations directory: migrations
======================================================================

[MIGRATION] Already applied: 0 migration(s)

[MIGRATION] Found 1 pending migration(s):
  → 001_add_sendbox_fields.sql

======================================================================
EXECUTING MIGRATIONS
======================================================================

[MIGRATION] Applying: 001_add_sendbox_fields
[MIGRATION] File: migrations/001_add_sendbox_fields.sql
  ✓ Executed statement 1/X
  ✓ Executed statement 2/X
  ...
[MIGRATION] ✓ Successfully applied: 001_add_sendbox_fields

======================================================================
✓ ALL MIGRATIONS COMPLETED SUCCESSFULLY
======================================================================
```

### 3.4 Verify Migration

```bash
python run_migrations.py list
```

Should show:
```
✓ APPLIED   001_add_sendbox_fields.sql
```

---

## Step 4: Verify Database Schema

Connect to your database and verify the new tables and columns:

```sql
-- Check orders table has new columns
DESCRIBE orders;

-- Should see:
-- sendbox_shipment_id
-- sendbox_tracking_code
-- sendbox_status
-- sendbox_carrier
-- shipping_cost
-- estimated_delivery_date
-- sendbox_webhook_data

-- Check new tables exist
SHOW TABLES LIKE 'shipping_%';

-- Should see:
-- shipping_addresses
-- shipping_quotes

-- Check webhook_events table
DESCRIBE webhook_events;

-- Check product weight column
DESCRIBE product;
-- Should see 'weight' column
```

---

## Step 5: Test Sendbox Service

### 5.1 Interactive Python Test

```python
from services.sendbox_service import SendboxClient
from config import Config

# Initialize client
client = SendboxClient()

# Test account balance
balance = client.get_account_balance()
print(f"Account Balance: {balance}")

# Test warehouse address
warehouse = Config.get_warehouse_address()
print(f"Warehouse: {warehouse}")
```

### 5.2 Test Address Validation

```python
from services.address_validator import validate_address, format_address_for_sendbox

# Create test address
address = format_address_for_sendbox(
    first_name="John",
    last_name="Doe",
    phone="+234 800 123 4567",
    street="123 Test Street",
    city="Lagos",
    state="Lagos",
    country="NG",
    email="john@example.com"
)

# Validate
is_valid, error = validate_address(address)
print(f"Valid: {is_valid}, Error: {error}")
```

---

## Project Structure After Phase 1

```
trollz_server/
├── config.py                      # ✓ Updated with Sendbox config
├── .env                           # ✓ Contains Sendbox credentials
├── .env.example                   # ✓ Template for environment variables
│
├── migrations/                    # ✓ New directory
│   ├── README.md                  # Migration documentation
│   └── 001_add_sendbox_fields.sql # First migration
│
├── services/                      # ✓ New directory
│   ├── __init__.py
│   ├── sendbox_service.py         # Sendbox API client
│   └── address_validator.py       # Address utilities
│
├── run_migrations.py              # ✓ Migration runner
├── test_sendbox_setup.py          # ✓ Setup verification script
│
└── [existing files...]
```

---

## Configuration Reference

### Sendbox Environments

| Environment | Base URL | Purpose |
|-------------|----------|---------|
| Staging | https://sandbox.staging.sendbox.co | Testing and development |
| Production | https://live.sendbox.co | Live shipments |

### Service Codes

- `standard` - Standard delivery
- `premium` - Faster delivery
- `expedient` - Express delivery

### Service Types

- `local` - Within same city/state
- `nation-wide` - Within same country
- `international` - Cross-border

---

## Troubleshooting

### Issue: Migration fails with "Duplicate column" error

**Solution:** This is usually safe. The migration script handles this gracefully. If you need to re-run:

```bash
# Remove migration record
mysql -h 57.131.33.181 -u admin -p trollzstorecom_tr0llz_db \
  -e "DELETE FROM schema_migrations WHERE migration_name = '001_add_sendbox_fields'"

# Re-run migration
python run_migrations.py run
```

### Issue: "API key not configured" error

**Solution:** 
1. Check `.env` file exists
2. Verify `SENDBOX_API_KEY` is set
3. Restart your application to reload environment variables

### Issue: "Authentication failed" error

**Solution:**
1. Verify API key is correct
2. Check you're using the right environment (staging vs live)
3. Ensure API key hasn't expired
4. Verify account is active on Sendbox portal

### Issue: Database connection error during migration

**Solution:**
1. Verify database credentials in `.env`
2. Check database server is accessible
3. Ensure user has CREATE, ALTER, INSERT permissions

### Issue: Warehouse address validation fails

**Solution:**
1. Ensure phone number starts with `+` and country code
2. Verify country code is 2 letters (e.g., NG)
3. Check all required fields are filled

---

## Testing Checklist

Before moving to Phase 2, verify:

- [ ] Sendbox API key is configured
- [ ] Can connect to Sendbox API
- [ ] Database migrations completed successfully
- [ ] All new tables exist (shipping_addresses, shipping_quotes, webhook_events)
- [ ] Orders table has new Sendbox columns
- [ ] Product table has weight column
- [ ] Warehouse address is configured and valid
- [ ] `test_sendbox_setup.py` passes all tests
- [ ] Can initialize SendboxClient without errors
- [ ] Address validation works correctly

---

## Next Steps

Once Phase 1 is complete, you're ready for:

**Phase 2: Shipping Quotes Integration**
- Address management API endpoints
- Shipping quotes endpoint
- Product weight management

See `SENDBOX_INTEGRATION_PHASES.md` for Phase 2 details.

---

## Useful Commands

```bash
# Test setup
python test_sendbox_setup.py

# Run migrations
python run_migrations.py run

# List migration status
python run_migrations.py list

# Check Sendbox account balance (staging)
python -c "from services.sendbox_service import SendboxClient; print(SendboxClient().get_account_balance())"

# Validate warehouse address
python -c "from config import Config; from services.address_validator import validate_address; print(validate_address(Config.get_warehouse_address()))"
```

---

## Support Resources

- **Sendbox Documentation:** https://developers.sendbox.co/
- **Sendbox Staging Portal:** https://developers.staging.sendbox.co/
- **Migration Guide:** `migrations/README.md`
- **Integration Phases:** `SENDBOX_INTEGRATION_PHASES.md`

---

## Phase 1 Completion Criteria

Phase 1 is complete when:

1. ✓ Sendbox API credentials configured
2. ✓ Database schema updated with migrations
3. ✓ SendboxClient service created and tested
4. ✓ Address validation utilities working
5. ✓ All tests passing
6. ✓ Documentation reviewed

**Status:** Ready for Phase 2 ✓

---

**Last Updated:** April 20, 2026  
**Phase:** 1 - Foundation Setup  
**Status:** Complete
