# Sendbox Authentication Configuration

## ✅ TOKEN AUTHENTICATION NOW ACTIVE

Your Sendbox integration now uses **OAuth 2.0 token-based authentication** with automatic token refresh. The tokens are already configured and hardcoded in the system.

## Current Authentication Method

### Token-Based Authentication (Active)
- **Access Token**: Hardcoded in `services/sendbox_service.py`
- **Refresh Token**: Hardcoded in `services/sendbox_service.py`
- **Client Secret**: Hardcoded in `services/sendbox_service.py`
- **Auto-Refresh**: Enabled (tokens refresh automatically before expiry)

### How It Works
1. System uses hardcoded access token for API requests
2. Before each request, checks if token expires in < 5 minutes
3. If expiring soon, automatically refreshes using refresh token
4. New access token is used for subsequent requests
5. No manual intervention required

## Verify Token Authentication

Run the token authentication test:

```bash
python test_token_refresh.py
```

This will verify:
- ✅ Token decoding and expiry checking
- ✅ Automatic token refresh logic
- ✅ API calls with token authentication
- ✅ Shipping quotes functionality

## Test Your Integration

### 1. Check Server Logs

Start your server and check for:
```
INFO:services.sendbox_service:Sendbox client initialized - Environment: staging
INFO:services.sendbox_service:Access token expires in X hours
```

### 2. Test API Endpoints

```bash
# Get shipping quotes
curl -X POST http://localhost:5000/api/shipping/quotes \
  -H "Content-Type: application/json" \
  -d '{
    "destination": {
      "name": "Test Customer",
      "phone": "+2348012345678",
      "address": "123 Test St",
      "city": "Lagos",
      "state": "Lagos",
      "country": "NG"
    },
    "weight": 0.5,
    "items": [{"name": "Test", "quantity": 1, "value": 5000, "weight": 0.5}]
  }'
```

### 3. Monitor Token Refresh

Watch logs for automatic token refresh:
```
INFO:services.sendbox_service:Access token expired or expiring soon, refreshing...
INFO:services.sendbox_service:Refreshing Sendbox access token...
INFO:services.sendbox_service:✅ Access token refreshed successfully
```

## Token Information

### Access Token
- **Expiry**: ~24 hours from issue date
- **Auto-Refresh**: Yes, when < 5 minutes remaining
- **Location**: `services/sendbox_service.py` (class variable)

### Refresh Token
- **Expiry**: ~30 days from issue date
- **Usage**: Automatically used to get new access tokens
- **Location**: `services/sendbox_service.py` (class variable)

### Client Secret
- **Expiry**: Never (unless manually revoked)
- **Usage**: Required for token refresh
- **Location**: `services/sendbox_service.py` (class variable)

## Troubleshooting

### Token Refresh Failed
**Symptom**: Logs show "Failed to refresh token"

**Solutions**:
1. Check internet connection
2. Verify Sendbox API is accessible
3. Confirm refresh token hasn't expired (check expiry date)
4. If refresh token expired, update tokens manually

### API Calls Failing with 401 Error
**Symptom**: API returns "Authentication failed"

**Solutions**:
1. Check if access token is expired
2. Verify token refresh is working (check logs)
3. Manually update tokens if needed
4. Ensure client secret is correct

### How to Update Tokens Manually

If you need to update tokens:

1. Get new tokens from Sendbox dashboard
2. Open `services/sendbox_service.py`
3. Update the class variables:
```python
ACCESS_TOKEN = "new_access_token_here"
REFRESH_TOKEN = "new_refresh_token_here"
CLIENT_SECRET = "new_client_secret_here"
```
4. Restart the server
5. Run test: `python test_token_refresh.py`

## Legacy API Key Method (Deprecated)

The old API key method is no longer used. If you have `SENDBOX_API_KEY` in your `.env` file, it will be ignored.

### Migration Complete
- ❌ Old: API Key authentication
- ✅ New: OAuth 2.0 token authentication with auto-refresh

## Documentation

For detailed information about token authentication:
- **Token Auth Guide**: `SENDBOX_TOKEN_AUTH.md`
- **Integration Guide**: `MOBILE_APP_INTEGRATION_GUIDE.md`
- **Setup Summary**: `FINAL_SETUP_SUMMARY.md`

## Next Steps

Your authentication is fully configured. You can now:

1. ✅ Test shipping quotes: `POST /api/shipping/quotes`
2. ✅ Create shipments: `POST /api/orders/{id}/confirm`
3. ✅ Track shipments: `GET /api/shipping/track/{code}`
4. ✅ Configure webhooks: `POST /api/webhooks/sendbox`
5. ✅ Monitor token refresh in logs

## Environment Variables

Your `.env` file should include:

```env
# Database
DB_HOST=localhost
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name

# Sendbox Configuration
SENDBOX_ENVIRONMENT=staging  # or 'live' for production

# Warehouse Address
SENDBOX_WAREHOUSE_NAME=Trollz Store
SENDBOX_WAREHOUSE_PHONE=+2348012345678
SENDBOX_WAREHOUSE_EMAIL=store@trollz.com
SENDBOX_WAREHOUSE_ADDRESS=LYPAS Plaza, Cluster Industrial Complex
SENDBOX_WAREHOUSE_CITY=Owerri
SENDBOX_WAREHOUSE_STATE=Imo
SENDBOX_WAREHOUSE_COUNTRY=NG

# Flask
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

**Note**: `SENDBOX_API_KEY` is no longer needed with token authentication.
