# Token Environment Mismatch - Action Required

## Current Situation

Your Sendbox integration is configured to use the **LIVE environment** (`https://live.sendbox.co`), but your tokens are from the **STAGING environment**. This is why you're getting 401 authentication errors.

## Test Results

```
✅ Token Decoding: PASS (tokens are valid JWT)
✅ Token Expiry Check: PASS (tokens not expired)
❌ API Call: FAIL (401 - Authentication failed)
❌ Shipping Quotes: FAIL (401 - Authentication failed)
```

## The Problem

```
Configuration:  LIVE environment (https://live.sendbox.co)
Tokens:         STAGING environment
Result:         401 Authentication Error ❌
```

## The Solution

You have two options:

### Option 1: Get Live Tokens (Recommended for Production)

Get new tokens from the live Sendbox dashboard and update your code.

**Steps:**
1. Visit https://live.sendbox.co/
2. Navigate to API/Developer section
3. Get your live tokens (access token, refresh token, client secret)
4. Run the helper script: `python update_live_tokens.py`
5. Follow the prompts to update your tokens
6. Restart server and test

**Detailed Guide:** See `GET_LIVE_TOKENS.md`

### Option 2: Switch Back to Staging (For Testing)

Use staging environment until you have live tokens ready.

**Steps:**
1. Update `config.py`:
   ```python
   SENDBOX_ENVIRONMENT = os.getenv("SENDBOX_ENV", "staging")
   ```
2. Restart server: `python app.py`
3. Test: `python test_token_refresh.py`
4. Should see: Environment: staging, API Response: 200 ✅

## Quick Fix Commands

### To Switch to Staging (Temporary)
```bash
# Update config.py line 20
# Change: SENDBOX_ENVIRONMENT = os.getenv("SENDBOX_ENV", "live")
# To:     SENDBOX_ENVIRONMENT = os.getenv("SENDBOX_ENV", "staging")

python app.py
```

### To Update Live Tokens (Permanent)
```bash
# Run the helper script
python update_live_tokens.py

# Follow prompts to enter your live tokens
# Then restart server
python app.py
```

## Understanding the Issue

### Staging vs Live Environments

| Aspect | Staging | Live |
|--------|---------|------|
| URL | https://sandbox.staging.sendbox.co | https://live.sendbox.co |
| Tokens | Staging tokens | Live tokens |
| Shipments | Test shipments | Real shipments |
| Charges | Test charges | Real charges |
| Dashboard | https://developers.staging.sendbox.co/ | https://live.sendbox.co/ |

### Your Current Tokens

```
Issuer: sendbox.apps.auth-6136dfa6a1ab9d318bcfcb94
Environment: STAGING
Valid Until: 1415 hours (59 days)
Status: Valid but wrong environment ⚠️
```

### What You Need

```
Issuer: Should be for live environment
Environment: LIVE
Source: https://live.sendbox.co/
Status: Need to obtain ⚠️
```

## Files to Help You

1. **GET_LIVE_TOKENS.md** - Detailed guide on getting live tokens
2. **update_live_tokens.py** - Helper script to update tokens easily
3. **test_token_refresh.py** - Test script to verify tokens work
4. **LIVE_ENVIRONMENT_ACTIVE.md** - Live environment documentation

## Recommended Action

### For Immediate Testing
Switch back to staging environment (Option 2 above) so you can continue testing with your current tokens.

### For Production Deployment
Get live tokens from Sendbox (Option 1 above) and update your code before deploying to production.

## How to Get Live Tokens

### Step-by-Step

1. **Log in to Live Dashboard**
   - Go to: https://live.sendbox.co/
   - Use your Sendbox credentials

2. **Find API/Developer Section**
   - Look for "API Keys", "Developer", or "Applications"
   - May be under Settings or Account

3. **Generate/Copy Tokens**
   - Access Token (JWT format)
   - Refresh Token (JWT format)
   - Client Secret (long hex string)

4. **Update Your Code**
   - Run: `python update_live_tokens.py`
   - Or manually update `services/sendbox_service.py`

5. **Test**
   - Restart: `python app.py`
   - Test: `python test_token_refresh.py`
   - Should see: 200 responses ✅

## Need Help?

### Can't Find Live Tokens?
- Check if your account has live access enabled
- Contact Sendbox support
- May need account approval for live environment

### Tokens Not Working?
- Verify you copied from live dashboard (not staging)
- Check token format (should be JWT)
- Ensure no extra spaces or line breaks
- Verify account is active

### Want to Test First?
- Switch to staging environment
- Test with current tokens
- Get live tokens when ready for production

## Summary

Your setup is correct, you just need tokens that match your environment:

- ✅ Code is configured for LIVE
- ✅ Tokens are valid (but for STAGING)
- ⚠️ Need LIVE tokens to match LIVE environment

**Quick Fix:** Switch to staging temporarily, or get live tokens from https://live.sendbox.co/

Run `python update_live_tokens.py` when you have your live tokens ready!
