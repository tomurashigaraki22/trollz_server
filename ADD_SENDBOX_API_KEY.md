# How to Add Sendbox API Key

## Issue
You're seeing this warning:
```
WARNING:services.sendbox_service:Sendbox API key not configured!
```

This means the Sendbox API key is missing from your environment variables.

---

## Solution

### Step 1: Get Your Sendbox API Key

1. Go to **Sendbox Staging Portal**: https://developers.staging.sendbox.co/
2. Sign up or log in
3. Create an application
4. Copy your API key

### Step 2: Add to .env File

Open your `.env` file and add:

```bash
# Sendbox API Configuration
SENDBOX_API_KEY=your_actual_sendbox_api_key_here
SENDBOX_ENV=staging
```

**Example:**
```bash
SENDBOX_API_KEY=sk_test_1234567890abcdefghijklmnopqrstuvwxyz
SENDBOX_ENV=staging
```

### Step 3: Update Warehouse Contact Info

While you're in the `.env` file, also update:

```bash
# Warehouse Contact
WAREHOUSE_PHONE=+234_YOUR_ACTUAL_PHONE_NUMBER
WAREHOUSE_EMAIL=your_actual_email@trollzstore.com
```

### Step 4: Restart Your Server

After updating `.env`, restart your Flask server:

```bash
# Stop the server (Ctrl+C)
# Then start it again
python app.py
```

---

## Verify Configuration

Test that the API key is loaded:

```bash
python -c "from config import Config; print('API Key configured:', bool(Config.SENDBOX_API_KEY))"
```

Should output:
```
API Key configured: True
```

---

## Test Shipping Quotes

Once configured, test getting shipping quotes:

```bash
curl -X POST http://localhost:4500/api/shipping/quotes \
  -H "Authorization: Bearer YOUR_USER_TOKEN" \
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

## If You Don't Have a Sendbox Account Yet

### For Testing Without Sendbox:

You can still use the address management features without a Sendbox API key:
- Create addresses ✅
- List addresses ✅
- Update addresses ✅
- Delete addresses ✅

But you'll need the API key for:
- Getting shipping quotes ❌
- Creating shipments ❌
- Tracking shipments ❌

### Sign Up for Sendbox:

1. Visit: https://developers.staging.sendbox.co/
2. Click "Sign Up"
3. Fill in your details
4. Verify your email
5. Create an application
6. Copy your API key
7. Add to `.env` file

---

## Production vs Staging

### Staging (for testing):
```bash
SENDBOX_API_KEY=sk_test_...
SENDBOX_ENV=staging
```
- Use for development and testing
- Free to use
- Can fund account manually for testing

### Production (for live):
```bash
SENDBOX_API_KEY=sk_live_...
SENDBOX_ENV=live
```
- Use for production
- Real shipments
- Real charges

---

## Common Issues

### Issue: "API key not configured"
**Solution:** Add `SENDBOX_API_KEY` to `.env` file

### Issue: "Authentication failed"
**Solution:** Check that your API key is correct and not expired

### Issue: "Changes not taking effect"
**Solution:** Restart your Flask server after updating `.env`

### Issue: "Still getting errors"
**Solution:** Check that `.env` file is in the root directory of your project

---

## Quick Checklist

- [ ] Created Sendbox account
- [ ] Got API key from Sendbox portal
- [ ] Added `SENDBOX_API_KEY` to `.env`
- [ ] Added `SENDBOX_ENV=staging` to `.env`
- [ ] Updated warehouse phone/email
- [ ] Restarted Flask server
- [ ] Tested configuration
- [ ] Tested shipping quotes

---

## Example .env File

Here's what your `.env` file should look like:

```bash
# Database Configuration
DB_HOST=57.131.33.181
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=your_password
DB_NAME=trollzstorecom_tr0llz_db

# JWT Configuration
JWT_SECRET=trollz_store_jwt_secret_key_2026
JWT_EXPIRATION_HOURS=72

# Flask Configuration
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=4500

# Sendbox API Configuration
SENDBOX_API_KEY=sk_test_your_actual_key_here
SENDBOX_ENV=staging

# Warehouse/Origin Address Configuration
WAREHOUSE_FIRST_NAME=Trollz Store
WAREHOUSE_LAST_NAME=Warehouse
WAREHOUSE_STREET=LYPAS Plaza, Cluster Industrial Complex
WAREHOUSE_STREET_LINE_2=
WAREHOUSE_CITY=Owerri
WAREHOUSE_STATE=Imo
WAREHOUSE_COUNTRY=NG
WAREHOUSE_POST_CODE=460001
WAREHOUSE_PHONE=+234_YOUR_PHONE_NUMBER
WAREHOUSE_EMAIL=your_email@trollzstore.com
```

---

## Need Help?

1. Check that `.env` file exists in project root
2. Verify API key is correct (no extra spaces)
3. Make sure you restarted the server
4. Check server logs for any other errors

---

**Next Step:** Add your Sendbox API key to `.env` and restart the server!
