# ⚠️ ACTION REQUIRED: Token Environment Mismatch

## Quick Summary

Your system is configured for **LIVE** environment but has **STAGING** tokens. This causes 401 authentication errors.

## Choose One Option

### Option A: Get Live Tokens (For Production) ✅

**When:** You're ready to go live with real shipments

**Steps:**
1. Visit https://live.sendbox.co/
2. Get live tokens from API/Developer section
3. Run: `python update_live_tokens.py`
4. Paste your live tokens when prompted
5. Update `services/sendbox_service.py` with the new tokens
6. Restart: `python app.py`
7. Test: `python test_token_refresh.py`

**Guide:** See `GET_LIVE_TOKENS.md` for detailed instructions

### Option B: Switch to Staging (For Testing) ✅

**When:** You want to test with current tokens first

**Steps:**
1. Open `config.py`
2. Line 20: Change `"live"` to `"staging"`
   ```python
   SENDBOX_ENVIRONMENT = os.getenv("SENDBOX_ENV", "staging")
   ```
3. Save file
4. Restart: `python app.py`
5. Test: `python test_token_refresh.py`
6. Should see: ✅ All tests pass

## Current Status

```
Environment:  LIVE (https://live.sendbox.co)
Tokens:       STAGING
Result:       401 Authentication Error ❌
```

## After Fix

### Option A (Live Tokens)
```
Environment:  LIVE (https://live.sendbox.co)
Tokens:       LIVE
Result:       200 Success ✅
```

### Option B (Staging)
```
Environment:  STAGING (https://sandbox.staging.sendbox.co)
Tokens:       STAGING
Result:       200 Success ✅
```

## Files to Help

- **GET_LIVE_TOKENS.md** - How to get live tokens
- **update_live_tokens.py** - Helper script to update tokens
- **TOKEN_ENVIRONMENT_MISMATCH.md** - Detailed explanation
- **test_token_refresh.py** - Test your setup

## Quick Commands

### To switch to staging (quick fix):
```bash
# Edit config.py line 20
# Change: SENDBOX_ENVIRONMENT = os.getenv("SENDBOX_ENV", "live")
# To:     SENDBOX_ENVIRONMENT = os.getenv("SENDBOX_ENV", "staging")

python app.py
python test_token_refresh.py
```

### To update live tokens:
```bash
python update_live_tokens.py
# Follow prompts, then:
python app.py
python test_token_refresh.py
```

## That's It!

Choose your option and follow the steps. Your integration will work perfectly once the tokens match the environment! 🚀
