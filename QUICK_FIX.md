# Quick Fix for Test Failures

## The Problem

Your tests are failing with:
- **401 errors** - Token environment mismatch
- **404 error** - Address validation endpoint missing

## The Solution (2 minutes)

### Step 1: Switch to Staging Environment

Open `config.py` and find line 20:

**Change this:**
```python
SENDBOX_ENVIRONMENT = os.getenv("SENDBOX_ENV", "live")
```

**To this:**
```python
SENDBOX_ENVIRONMENT = os.getenv("SENDBOX_ENV", "staging")
```

### Step 2: Restart Server

```bash
python app.py
```

### Step 3: Test Again

```bash
python test_sendbox_quick.py
```

## Expected Result

```
✅ PASS - API Health Check
✅ PASS - Shipping Quotes
✅ PASS - Landed Cost Calculation
✅ PASS - Address Validation

Total: 4/4 tests passed

🎉 All tests passed!
```

## That's It!

Your tests should now pass. The address validation endpoint has been added, and switching to staging environment will fix the 401 errors.

## For Production

When you're ready to go live:
1. Get live tokens from https://live.sendbox.co/
2. Run: `python update_live_tokens.py`
3. Update tokens in `services/sendbox_service.py`
4. Change `config.py` back to `"live"`
5. Restart server

See `GET_LIVE_TOKENS.md` for detailed instructions.
