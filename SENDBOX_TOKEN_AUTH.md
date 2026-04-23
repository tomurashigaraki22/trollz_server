# Sendbox Token-Based Authentication

## Overview

The Sendbox integration now uses **OAuth 2.0 token-based authentication** with automatic token refresh. This ensures uninterrupted API access even when tokens expire.

## How It Works

### 1. Token Storage
Tokens are hardcoded directly in the `SendboxClient` class for security and simplicity:

```python
class SendboxClient:
    # Sendbox credentials (hardcoded)
    ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    REFRESH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    CLIENT_SECRET = "602c256bf4da43b4d312d54ab938aed9..."
```

### 2. Automatic Token Refresh

The system automatically refreshes tokens when:
- Token expires within 5 minutes
- Token is already expired
- Before every API request

**Token Refresh Flow:**
```
1. Check if token expires in < 5 minutes
2. If yes, call Sendbox refresh endpoint
3. Update access token (and refresh token if provided)
4. Continue with API request
```

### 3. Authentication Headers

All API requests use Bearer token authentication:
```
Authorization: Bearer {access_token}
```

## Key Features

### Automatic Expiry Detection
```python
def _is_token_expired(self) -> bool:
    """Check if token expires in less than 5 minutes."""
    decoded = jwt.decode(token, options={"verify_signature": False})
    exp_timestamp = decoded.get('exp', 0)
    buffer_time = 300  # 5 minutes
    return (exp_timestamp - current_time) < buffer_time
```

### Seamless Refresh
```python
def _refresh_access_token(self) -> bool:
    """Refresh token using refresh token and client secret."""
    response = requests.post(
        f"{base_url}/auth/refresh",
        json={
            "refresh_token": self.current_refresh_token,
            "client_secret": self.CLIENT_SECRET
        }
    )
    # Update tokens from response
```

### Pre-Request Check
```python
def _check_and_refresh_token(self):
    """Called before every API request."""
    if self._is_token_expired():
        self._refresh_access_token()
```

## Token Information

### Access Token
- **Purpose**: Authenticate API requests
- **Expiry**: Short-lived (typically 24 hours)
- **Usage**: Included in Authorization header
- **Auto-refresh**: Yes, when expiring soon

### Refresh Token
- **Purpose**: Obtain new access tokens
- **Expiry**: Long-lived (typically 30 days)
- **Usage**: Used to refresh access token
- **Auto-update**: Yes, if new one provided during refresh

### Client Secret
- **Purpose**: Authenticate refresh requests
- **Expiry**: Never (unless manually revoked)
- **Usage**: Sent with refresh token to get new access token

## Testing Token Authentication

Run the test script to verify token authentication:

```bash
python test_token_refresh.py
```

**Test Coverage:**
1. Token decoding and expiry checking
2. Automatic token refresh logic
3. API calls with token authentication
4. Shipping quotes with token auth

## API Endpoints Using Token Auth

All Sendbox API endpoints now use token authentication:

### Shipping Operations
- `POST /shipping/shipment_delivery_quote` - Get shipping quotes
- `POST /shipping/shipments` - Create shipment
- `POST /shipping/tracking` - Track shipment
- `GET /shipping/shipments` - List all shipments
- `GET /shipping/shipments/{id}` - Get shipment details

### Account Management
- `GET /payments/profile` - Get account balance
- `POST /payments/add_money` - Add money (staging only)

### Tracking
- `POST /shipping/move_tracking` - Simulate tracking update (staging only)

### Landed Cost
- `POST /shipping/landed_cost_estimate` - Calculate landed cost

## Error Handling

### Token Refresh Failures
If token refresh fails:
1. Error is logged
2. System continues with existing token
3. API request may fail with 401 error
4. Manual intervention required to update tokens

### Authentication Errors
- **401 Unauthorized**: Token invalid or expired
- **403 Forbidden**: Insufficient permissions
- Check logs for detailed error messages

## Monitoring

### Log Messages
```
INFO: Sendbox client initialized - Environment: staging
INFO: Access token expired or expiring soon, refreshing...
INFO: Refreshing Sendbox access token...
INFO: ✅ Access token refreshed successfully
INFO: Sendbox API Request: POST https://sandbox.staging.sendbox.co/...
```

### Token Expiry Warnings
The system logs when tokens are about to expire and when refresh occurs.

## Security Considerations

### Why Hardcode Tokens?
1. **Simplicity**: No need for external token storage
2. **Security**: Tokens stored in code (not in database or config files)
3. **Version Control**: Can be excluded from git using .gitignore
4. **Automatic Refresh**: Tokens stay fresh automatically

### Best Practices
1. Never commit tokens to public repositories
2. Use environment variables for production
3. Rotate tokens periodically
4. Monitor token refresh logs
5. Set up alerts for refresh failures

## Updating Tokens

If you need to update tokens manually:

1. Open `services/sendbox_service.py`
2. Update the class variables:
```python
ACCESS_TOKEN = "new_access_token_here"
REFRESH_TOKEN = "new_refresh_token_here"
CLIENT_SECRET = "new_client_secret_here"
```
3. Restart the application
4. Run test script to verify

## Troubleshooting

### Token Expired Error
**Symptom**: API calls fail with 401 error
**Solution**: 
1. Check if refresh token is valid
2. Manually update tokens if needed
3. Verify client secret is correct

### Refresh Failed
**Symptom**: Logs show "Failed to refresh token"
**Solution**:
1. Check internet connection
2. Verify Sendbox API is accessible
3. Confirm refresh token hasn't expired
4. Update tokens manually

### Invalid Token Format
**Symptom**: JWT decode errors
**Solution**:
1. Verify token format (should be JWT)
2. Check for extra spaces or characters
3. Get new tokens from Sendbox dashboard

## Migration from API Key

### Old Method (API Key)
```python
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
```

### New Method (OAuth Token)
```python
headers = {
    "Authorization": f"Bearer {access_token}",  # Auto-refreshed
    "Content-Type": "application/json"
}
```

### Benefits of Token Auth
1. **Automatic Refresh**: No manual token updates
2. **Better Security**: Short-lived access tokens
3. **Granular Permissions**: Token-based access control
4. **Audit Trail**: Track token usage and refresh

## Support

For issues with token authentication:
1. Check application logs
2. Run test script: `python test_token_refresh.py`
3. Verify tokens in Sendbox dashboard
4. Contact Sendbox support if needed

## References

- [Sendbox API Documentation](https://developers.staging.sendbox.co/)
- [OAuth 2.0 Specification](https://oauth.net/2/)
- [JWT.io - Token Decoder](https://jwt.io/)
