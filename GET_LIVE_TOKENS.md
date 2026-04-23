# Getting Live Environment Tokens

## Issue

Your current tokens are for the **staging environment** and won't work with the **live environment**. You're getting 401 authentication errors because the tokens are environment-specific.

## Solution

You need to get new tokens from the Sendbox **live environment** dashboard.

## Steps to Get Live Tokens

### 1. Log in to Sendbox Live Dashboard

Visit: **https://live.sendbox.co/**

- Use your Sendbox account credentials
- Make sure you're on the LIVE dashboard (not staging)

### 2. Navigate to API/Developer Section

Look for:
- "API Keys" or "Developer" section
- "Applications" or "Integrations"
- "OAuth" or "Authentication"

### 3. Get Your Live Tokens

You need to obtain:
1. **Access Token** - For API authentication
2. **Refresh Token** - For automatic token refresh
3. **Client Secret** - For token refresh requests

### 4. Update the Tokens in Your Code

Once you have the live tokens, update `services/sendbox_service.py`:

```python
class SendboxClient:
    # Sendbox credentials - LIVE ENVIRONMENT
    ACCESS_TOKEN = "your_live_access_token_here"
    REFRESH_TOKEN = "your_live_refresh_token_here"
    CLIENT_SECRET = "your_live_client_secret_here"
```

### 5. Restart Your Server

```bash
python app.py
```

### 6. Test Again

```bash
python test_token_refresh.py
```

## Current vs Required Tokens

### Current Tokens (Staging)
```
Access Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Issuer: sendbox.apps.auth-6136dfa6a1ab9d318bcfcb94
Environment: STAGING ❌
```

### Required Tokens (Live)
```
Access Token: [Need to get from live dashboard]
Issuer: Should be for live environment
Environment: LIVE ✅
```

## Alternative: Use Staging Environment for Testing

If you don't have live tokens yet, you can switch back to staging:

### Option 1: Update config.py
```python
SENDBOX_ENVIRONMENT = os.getenv("SENDBOX_ENV", "staging")
```

### Option 2: Update .env file
```env
SENDBOX_ENV=staging
```

Then restart your server and test with staging tokens.

## How to Get Tokens from Sendbox

### Method 1: OAuth Flow (Recommended)

1. Go to https://live.sendbox.co/
2. Navigate to Developer/API section
3. Create or select your application
4. Click "Generate Tokens" or "Get Access Token"
5. Copy the access token, refresh token, and client secret

### Method 2: API Key (If Available)

Some Sendbox accounts use API keys instead of OAuth tokens. Check if you have:
- API Key in your live dashboard
- If so, you may need to use a different authentication method

### Method 3: Contact Sendbox Support

If you can't find the tokens:
1. Contact Sendbox support
2. Request live environment OAuth tokens
3. Explain you need: access token, refresh token, and client secret

## Verifying Token Environment

You can check which environment your tokens are for by decoding them:

```bash
python -c "import jwt; token='YOUR_TOKEN_HERE'; print(jwt.decode(token, options={'verify_signature': False}))"
```

Look for the `iss` (issuer) field - it should indicate the environment.

## Quick Test Script

Create a file `check_token_env.py`:

```python
import jwt

# Your current access token
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

decoded = jwt.decode(token, options={"verify_signature": False})
print(f"Issuer: {decoded.get('iss')}")
print(f"App ID: {decoded.get('aid')}")
print(f"Expires: {decoded.get('exp')}")

if 'staging' in decoded.get('iss', '').lower():
    print("\n⚠️  This is a STAGING token")
    print("You need LIVE tokens for production")
else:
    print("\n✅ This appears to be a LIVE token")
```

## Once You Have Live Tokens

1. Update `services/sendbox_service.py` with new tokens
2. Restart server: `python app.py`
3. Run test: `python test_token_refresh.py`
4. Verify you see: `Environment: live` and `Sendbox API Response: 200`

## Troubleshooting

### Still Getting 401 After Updating Tokens

1. **Verify tokens are for live environment**
   - Decode token and check issuer
   - Confirm you copied from live dashboard

2. **Check token format**
   - Should be JWT format (three parts separated by dots)
   - No extra spaces or line breaks

3. **Verify client secret**
   - Must match the live environment
   - Should be a long hexadecimal string

4. **Check account status**
   - Ensure live account is active
   - Verify account is not suspended

### Can't Find Live Tokens in Dashboard

1. Check if your account has live access enabled
2. Some accounts need approval for live environment
3. Contact Sendbox support to enable live access

## Need Help?

- **Sendbox Live Dashboard**: https://live.sendbox.co/
- **Sendbox Documentation**: https://developers.sendbox.co/docs
- **Sendbox Support**: Contact through live dashboard

## Summary

Your current tokens work perfectly - they're just for the staging environment. To use the live environment, you need to:

1. ✅ Log in to https://live.sendbox.co/
2. ✅ Get live environment tokens (access, refresh, client secret)
3. ✅ Update `services/sendbox_service.py` with live tokens
4. ✅ Restart server and test

OR

Switch back to staging environment until you have live tokens ready.
