# Payment API Documentation

## Overview

Payment endpoints for retrieving payment gateway configuration and public keys.

## Base URL

```
http://your-server:4500/api/payment
```

## Endpoints

### 1. Get Payment Configuration

Get all payment gateway configurations (public keys only).

**Endpoint:** `GET /api/payment/config`

**Authentication:** None required

**Response:**

```json
{
  "status": "success",
  "data": {
    "flutterwave": {
      "public_key": "FLWPUBK-xxxxxxxxxxxxx",
      "enabled": true
    }
  }
}
```

**Status Codes:**
- `200` - Success
- `500` - Server error

**Example:**

```bash
curl http://localhost:4500/api/payment/config
```

```javascript
// React Native / JavaScript
fetch('http://your-server:4500/api/payment/config')
  .then(response => response.json())
  .then(data => {
    const publicKey = data.data.flutterwave.public_key;
    console.log('Flutterwave Public Key:', publicKey);
  });
```

### 2. Get Flutterwave Public Key

Get only the Flutterwave public key.

**Endpoint:** `GET /api/payment/flutterwave/public-key`

**Authentication:** None required

**Response:**

```json
{
  "status": "success",
  "data": {
    "public_key": "FLWPUBK-xxxxxxxxxxxxx"
  }
}
```

**Error Response (Not Configured):**

```json
{
  "status": "error",
  "message": "Flutterwave public key not configured"
}
```

**Status Codes:**
- `200` - Success
- `404` - Public key not configured
- `500` - Server error

**Example:**

```bash
curl http://localhost:4500/api/payment/flutterwave/public-key
```

```javascript
// React Native / JavaScript
fetch('http://your-server:4500/api/payment/flutterwave/public-key')
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      const publicKey = data.data.public_key;
      // Use public key for Flutterwave payment
      initializeFlutterwave(publicKey);
    }
  });
```

## Configuration

### Environment Variables

Add these to your `.env` file:

```env
# Flutterwave Configuration
FLUTTERWAVE_PUBLIC_KEY=FLWPUBK-your_public_key_here
FLUTTERWAVE_SECRET_KEY=FLWSECK-your_secret_key_here
FLUTTERWAVE_ENCRYPTION_KEY=your_encryption_key_here
```

### Getting Flutterwave Keys

1. Log in to https://dashboard.flutterwave.com/
2. Navigate to Settings > API
3. Copy your keys:
   - Public Key (for frontend)
   - Secret Key (for backend only)
   - Encryption Key (for backend only)

## Security Notes

### Public Key
- ✅ Safe to expose to frontend/mobile apps
- ✅ Used for initializing payments
- ✅ Can be included in client-side code

### Secret Key
- ❌ NEVER expose to frontend
- ❌ NEVER include in API responses
- ✅ Only used on backend for verification
- ✅ Keep in .env file only

### Encryption Key
- ❌ NEVER expose to frontend
- ✅ Only used on backend
- ✅ Keep in .env file only

## Mobile App Integration

### React Native Example

```javascript
import React, { useEffect, useState } from 'react';
import { PayWithFlutterwave } from 'flutterwave-react-native';

const PaymentScreen = () => {
  const [publicKey, setPublicKey] = useState('');

  useEffect(() => {
    // Fetch public key from backend
    fetch('http://your-server:4500/api/payment/flutterwave/public-key')
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          setPublicKey(data.data.public_key);
        }
      })
      .catch(error => console.error('Error fetching public key:', error));
  }, []);

  const handlePayment = () => {
    const paymentData = {
      tx_ref: `order_${Date.now()}`,
      authorization: publicKey,
      customer: {
        email: 'customer@example.com',
        phonenumber: '08012345678',
        name: 'Customer Name',
      },
      amount: 5000,
      currency: 'NGN',
      payment_options: 'card,banktransfer,ussd',
    };

    // Initialize Flutterwave payment
    PayWithFlutterwave(paymentData);
  };

  return (
    // Your payment UI
  );
};
```

### Flutter Example

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class PaymentService {
  static const String baseUrl = 'http://your-server:4500';

  Future<String?> getFlutterwavePublicKey() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/payment/flutterwave/public-key'),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['status'] == 'success') {
          return data['data']['public_key'];
        }
      }
      return null;
    } catch (e) {
      print('Error fetching public key: $e');
      return null;
    }
  }

  Future<void> initializePayment() async {
    final publicKey = await getFlutterwavePublicKey();
    
    if (publicKey != null) {
      // Initialize Flutterwave payment with public key
      // Use flutterwave_standard package
    }
  }
}
```

## Testing

### Test Endpoints

```bash
# Test payment config
curl http://localhost:4500/api/payment/config

# Test Flutterwave public key
curl http://localhost:4500/api/payment/flutterwave/public-key
```

### Run Test Script

```bash
python test_payment_endpoint.py
```

## Troubleshooting

### Public Key Not Found (404)

**Problem:** API returns 404 with "Flutterwave public key not configured"

**Solution:**
1. Check your `.env` file exists
2. Add `FLUTTERWAVE_PUBLIC_KEY=your_key_here`
3. Restart your server
4. Test again

### Empty Public Key

**Problem:** Public key is empty string

**Solution:**
1. Verify you copied the correct key from Flutterwave dashboard
2. Check for extra spaces or line breaks
3. Ensure key starts with `FLWPUBK-`

### CORS Errors

**Problem:** Browser/mobile app can't access endpoint

**Solution:**
- CORS is already enabled in `app.py`
- If still having issues, check your server's CORS configuration

## Payment Flow

### Recommended Flow

1. **Frontend:** Fetch public key from backend
   ```
   GET /api/payment/flutterwave/public-key
   ```

2. **Frontend:** Initialize Flutterwave with public key
   ```javascript
   initializeFlutterwave(publicKey)
   ```

3. **Frontend:** User completes payment

4. **Frontend:** Send payment reference to backend
   ```
   POST /api/orders/{id}/confirm
   ```

5. **Backend:** Verify payment with Flutterwave (using secret key)

6. **Backend:** Update order status

7. **Backend:** Create shipment if payment successful

## Related Documentation

- **Orders API**: `ORDERS_API_DOCUMENTATION.md`
- **Shipping API**: `ADDRESSES_SHIPPING_API_DOCUMENTATION.md`
- **Mobile Integration**: `MOBILE_APP_INTEGRATION_GUIDE.md`

## Support

For Flutterwave integration help:
- **Dashboard**: https://dashboard.flutterwave.com/
- **Documentation**: https://developer.flutterwave.com/docs
- **Support**: support@flutterwavego.com
