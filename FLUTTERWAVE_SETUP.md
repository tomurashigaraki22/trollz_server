# Flutterwave Payment Setup ✅

## What Was Added

Created payment endpoints to securely provide Flutterwave public key to your mobile app.

## New Endpoints

### 1. Get Payment Config
```
GET /api/payment/config
```
Returns all payment gateway configurations.

### 2. Get Flutterwave Public Key
```
GET /api/payment/flutterwave/public-key
```
Returns only the Flutterwave public key.

## Setup Steps

### 1. Add Flutterwave Keys to .env

Get your keys from https://dashboard.flutterwave.com/settings/apis

Add to your `.env` file:
```env
FLUTTERWAVE_PUBLIC_KEY=FLWPUBK-your_public_key_here
FLUTTERWAVE_SECRET_KEY=FLWSECK-your_secret_key_here
FLUTTERWAVE_ENCRYPTION_KEY=your_encryption_key_here
```

### 2. Restart Server

```bash
python app.py
```

### 3. Test Endpoint

```bash
curl http://localhost:4500/api/payment/flutterwave/public-key
```

Expected response:
```json
{
  "status": "success",
  "data": {
    "public_key": "FLWPUBK-xxxxxxxxxxxxx"
  }
}
```

## Mobile App Usage

### Fetch Public Key

```javascript
// React Native / JavaScript
fetch('http://your-server:4500/api/payment/flutterwave/public-key')
  .then(response => response.json())
  .then(data => {
    const publicKey = data.data.public_key;
    // Use public key to initialize Flutterwave
  });
```

### Initialize Payment

```javascript
const paymentData = {
  tx_ref: `order_${Date.now()}`,
  authorization: publicKey, // From backend
  customer: {
    email: 'customer@example.com',
    phonenumber: '08012345678',
    name: 'Customer Name',
  },
  amount: 5000,
  currency: 'NGN',
  payment_options: 'card,banktransfer,ussd',
};

PayWithFlutterwave(paymentData);
```

## Files Created

1. `routes/payment.py` - Payment endpoints
2. `PAYMENT_API_DOCUMENTATION.md` - Full API documentation
3. `test_payment_endpoint.py` - Test script
4. `FLUTTERWAVE_SETUP.md` - This guide

## Files Modified

1. `app.py` - Registered payment blueprint
2. `config.py` - Added Flutterwave configuration
3. `.env.example` - Added Flutterwave keys template

## Security

### ✅ Safe to Expose
- Public Key - Used by frontend/mobile apps

### ❌ Never Expose
- Secret Key - Backend only
- Encryption Key - Backend only

The endpoint only returns the public key, keeping secret keys secure.

## Testing

Run the test script:
```bash
python test_payment_endpoint.py
```

Or test manually:
```bash
# Get payment config
curl http://localhost:4500/api/payment/config

# Get public key only
curl http://localhost:4500/api/payment/flutterwave/public-key
```

## Next Steps

1. ✅ Add Flutterwave keys to `.env`
2. ✅ Restart server
3. ✅ Test endpoint
4. ✅ Update mobile app to fetch public key from backend
5. ✅ Initialize Flutterwave payments with fetched key

## Documentation

- **Full API Docs**: `PAYMENT_API_DOCUMENTATION.md`
- **Mobile Integration**: `MOBILE_APP_INTEGRATION_GUIDE.md`

Your payment endpoint is ready! 🚀
