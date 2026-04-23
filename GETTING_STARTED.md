# Getting Started with Sendbox Integration

Welcome! This guide will help you get started with the Sendbox shipping integration for Trollz Store.

## Quick Start (5 Minutes)

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
setup_sendbox.bat
```

**Linux/Mac:**
```bash
chmod +x setup_sendbox.sh
./setup_sendbox.sh
```

### Option 2: Manual Setup

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env and add your Sendbox API key
# Get your key from: https://developers.staging.sendbox.co/

# 3. Run migrations
python run_migrations.py run

# 4. Verify setup
python test_sendbox_setup.py
```

## What You Need

1. **Sendbox API Key**
   - Register at: https://developers.staging.sendbox.co/
   - Create an application
   - Copy your API key

2. **Database Access**
   - MySQL database (already configured)
   - Migrations will add new tables and columns

3. **Python Dependencies**
   - pymysql
   - requests
   - python-dotenv
   - (Install with: `pip install -r requirements.txt`)

## Project Structure

```
trollz_server/
├── 📄 GETTING_STARTED.md          ← You are here
├── 📄 PHASE1_SETUP_GUIDE.md       ← Detailed setup guide
├── 📄 PHASE1_CHECKLIST.md         ← Implementation checklist
├── 📄 SENDBOX_INTEGRATION_PHASES.md ← Full roadmap
│
├── 📁 migrations/                 ← Database migrations
│   ├── README.md
│   └── 001_add_sendbox_fields.sql
│
├── 📁 services/                   ← Sendbox integration
│   ├── sendbox_service.py         ← API client
│   └── address_validator.py       ← Address utilities
│
├── 🔧 config.py                   ← Configuration
├── 🔧 run_migrations.py           ← Migration runner
├── 🧪 test_sendbox_setup.py       ← Setup verification
└── 📄 .env.example                ← Configuration template
```

## Phase 1 Overview

Phase 1 establishes the foundation for Sendbox integration:

### ✓ What's Implemented

1. **Configuration** (`config.py`)
   - Sendbox API settings
   - Warehouse address configuration
   - Environment switching (staging/live)

2. **Database Schema** (`migrations/`)
   - Sendbox fields in orders table
   - Shipping addresses table
   - Shipping quotes table
   - Webhook events table
   - Product weight field

3. **Sendbox Service** (`services/`)
   - Complete API client
   - Address validation
   - Error handling
   - Logging

### ⧗ What You Need to Do

1. **Get API Key**
   - Visit https://developers.staging.sendbox.co/
   - Register and create application
   - Copy API key

2. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Add your API key
   - Update warehouse address

3. **Run Migrations**
   - Execute: `python run_migrations.py run`
   - Verify: `python run_migrations.py list`

4. **Test Setup**
   - Run: `python test_sendbox_setup.py`
   - Fix any issues reported

## Common Commands

```bash
# Setup
cp .env.example .env              # Copy environment template
python run_migrations.py run      # Run migrations
python test_sendbox_setup.py      # Verify setup

# Migrations
python run_migrations.py list     # List migration status
python run_migrations.py run      # Run pending migrations

# Testing
python test_sendbox_setup.py      # Full setup test

# Development
python app.py                     # Start server
```

## Quick Test

After setup, test the integration:

```python
from services.sendbox_service import SendboxClient
from config import Config

# Initialize client
client = SendboxClient()

# Check account balance
balance = client.get_account_balance()
print(f"Balance: {balance}")

# Get warehouse address
warehouse = Config.get_warehouse_address()
print(f"Warehouse: {warehouse['city']}, {warehouse['state']}")
```

## Documentation Guide

### For Setup
1. Start here: `GETTING_STARTED.md` (this file)
2. Detailed guide: `PHASE1_SETUP_GUIDE.md`
3. Checklist: `PHASE1_CHECKLIST.md`

### For Development
1. API reference: `SENDBOX_D.md`
2. Integration plan: `SENDBOX_INTEGRATION_PHASES.md`
3. Migration guide: `migrations/README.md`

### For Understanding
1. Completion summary: `PHASE1_COMPLETION_SUMMARY.md`
2. Orders API: `ORDERS_API_DOCUMENTATION.md`
3. Main README: `README.md`

## Troubleshooting

### Issue: "API key not configured"
**Solution:** Add `SENDBOX_API_KEY` to your `.env` file

### Issue: "Authentication failed"
**Solution:** Verify your API key is correct and active

### Issue: "Migration failed"
**Solution:** Check database credentials and permissions

### Issue: "Module not found"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: "Warehouse address invalid"
**Solution:** Update warehouse configuration in `.env`

See `PHASE1_SETUP_GUIDE.md` for more troubleshooting.

## Next Steps

Once Phase 1 is complete:

### Phase 2: Shipping Quotes
- Address management API
- Shipping quotes endpoint
- Product weight management

### Phase 3: Shipment Creation
- Checkout integration
- Automatic shipment creation
- Landed cost calculator

### Phase 4: Tracking
- Tracking sync
- Webhook handler
- Customer tracking page

See `SENDBOX_INTEGRATION_PHASES.md` for the complete roadmap.

## Support

### Resources
- **Sendbox Docs:** https://developers.sendbox.co/
- **Staging Portal:** https://developers.staging.sendbox.co/
- **API Reference:** `SENDBOX_D.md`

### Getting Help
1. Check documentation in this repository
2. Review troubleshooting guides
3. Run diagnostic tests
4. Check Sendbox developer portal

## Success Criteria

Phase 1 is complete when:

- ✓ Sendbox API key configured
- ✓ Database migrations applied
- ✓ All tests passing
- ✓ Can initialize SendboxClient
- ✓ Address validation working
- ✓ API connection successful

Run `python test_sendbox_setup.py` to verify!

## Quick Reference

### Environment Variables
```bash
SENDBOX_API_KEY=your_key_here
SENDBOX_ENV=staging
WAREHOUSE_CITY=Ikeja
WAREHOUSE_STATE=Lagos
WAREHOUSE_COUNTRY=NG
```

### Key Files
- `config.py` - Configuration
- `services/sendbox_service.py` - API client
- `services/address_validator.py` - Address utilities
- `run_migrations.py` - Migration runner
- `test_sendbox_setup.py` - Setup tests

### Important URLs
- Staging: https://sandbox.staging.sendbox.co
- Live: https://live.sendbox.co
- Developer Portal: https://developers.staging.sendbox.co

---

**Ready to start?** Run the setup script or follow the manual setup steps above!

**Questions?** Check `PHASE1_SETUP_GUIDE.md` for detailed instructions.

**Issues?** See the troubleshooting section or run `python test_sendbox_setup.py` for diagnostics.

---

**Last Updated:** April 20, 2026  
**Phase:** 1 - Foundation Setup  
**Status:** Ready for Implementation
