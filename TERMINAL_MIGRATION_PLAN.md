# Terminal Africa Migration Plan

## Overview

Migration from Sendbox API to Terminal Africa API - A comprehensive phase-by-phase implementation plan.

## API Comparison

### Sendbox vs Terminal Africa

| Feature | Sendbox | Terminal Africa |
|---------|---------|-----------------|
| **Authentication** | OAuth tokens | API Key (Bearer token) |
| **Base URL** | `https://live.sendbox.co` | `https://api.terminal.africa/v1` |
| **Address Management** | Limited | Full CRUD with validation |
| **Carriers** | Single carrier | Multiple carriers (DHL, FedEx, Sendbox, etc.) |
| **Packaging** | Basic | Advanced packaging management |
| **Rates** | Simple quotes | Detailed rates with multiple options |
| **Shipments** | Basic | Advanced with multi-parcel support |
| **Tracking** | Basic | Comprehensive with events |

## Key Differences

### 1. Authentication
**Sendbox:**
- OAuth 2.0 with access/refresh tokens
- Token refresh mechanism

**Terminal Africa:**
- Simple API key authentication
- Test keys: `pk_test_*` and `sk_test_*`
- Live keys: `pk_live_*` and `sk_live_*`

### 2. API Structure
**Sendbox:**
- Direct shipment creation
- Limited address management

**Terminal Africa:**
- Addresses → Packaging → Parcels → Rates → Shipments
- More structured workflow

### 3. Carriers
**Sendbox:**
- Single carrier (Sendbox)

**Terminal Africa:**
- Multiple carriers (DHL, FedEx, UPS, Sendbox, Kwik, GIG, etc.)
- Carrier selection and management

## Migration Phases

---

## Phase 1: Setup & Configuration

### 1.1 Update Configuration
**File:** `config.py`

**Changes:**
```python
# Remove Sendbox OAuth config
# Add Terminal Africa config

# Terminal Africa API Configuration
TERMINAL_TEST_PUBLIC_KEY = "pk_test_WeDJ1I1cKKkubg60rE6kXnwPJXlExlH1"
TERMINAL_TEST_SECRET_KEY = "sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn"
TERMINAL_LIVE_PUBLIC_KEY = "pk_live_G8zfsoShEtgvDPUvHABwdF9Lw4a65HKg"
TERMINAL_LIVE_SECRET_KEY = "sk_live_jiep2FyoHX3tImNV4eVkdVl1SXIHrFWM"
TERMINAL_ENVIRONMENT = os.getenv("TERMINAL_ENV", "test")  # test or live
TERMINAL_BASE_URL = "https://api.terminal.africa/v1"

@staticmethod
def get_terminal_secret_key():
    """Get the appropriate Terminal secret key based on environment."""
    if Config.TERMINAL_ENVIRONMENT == "live":
        return Config.TERMINAL_LIVE_SECRET_KEY
    return Config.TERMINAL_TEST_SECRET_KEY

@staticmethod
def get_terminal_public_key():
    """Get the appropriate Terminal public key based on environment."""
    if Config.TERMINAL_ENVIRONMENT == "live":
        return Config.TERMINAL_LIVE_PUBLIC_KEY
    return Config.TERMINAL_TEST_PUBLIC_KEY
```

### 1.2 Update Environment Variables
**File:** `.env.example`

**Add:**
```env
# Terminal Africa Configuration
TERMINAL_ENV=test  # or 'live' for production
```

### 1.3 Database Schema Updates
**New Migration:** `migrations/003_terminal_africa_fields.sql`

**Changes:**
```sql
-- Add Terminal-specific fields to orders table
ALTER TABLE orders 
ADD COLUMN terminal_shipment_id VARCHAR(50),
ADD COLUMN terminal_rate_id VARCHAR(50),
ADD COLUMN terminal_carrier_id VARCHAR(50),
ADD COLUMN terminal_carrier_name VARCHAR(100),
ADD COLUMN terminal_tracking_url TEXT,
ADD COLUMN terminal_label_url TEXT,
ADD COLUMN terminal_invoice_url TEXT;

-- Create terminal_addresses table (maps to Terminal's address system)
CREATE TABLE IF NOT EXISTS terminal_addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    terminal_address_id VARCHAR(50) UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(255),
    line1 TEXT,
    line2 TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(10),
    zip VARCHAR(20),
    is_residential BOOLEAN DEFAULT TRUE,
    coordinates JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create terminal_packaging table
CREATE TABLE IF NOT EXISTS terminal_packaging (
    id INT AUTO_INCREMENT PRIMARY KEY,
    terminal_packaging_id VARCHAR(50) UNIQUE,
    name VARCHAR(255),
    type ENUM('box', 'envelope', 'soft-packaging') DEFAULT 'box',
    length DECIMAL(10,2),
    width DECIMAL(10,2),
    height DECIMAL(10,2),
    weight DECIMAL(10,2),
    size_unit VARCHAR(10) DEFAULT 'cm',
    weight_unit VARCHAR(10) DEFAULT 'kg',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create terminal_parcels table
CREATE TABLE IF NOT EXISTS terminal_parcels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    terminal_parcel_id VARCHAR(50) UNIQUE,
    order_id INT,
    packaging_id INT,
    description TEXT,
    items JSON,
    total_weight DECIMAL(10,2),
    weight_unit VARCHAR(10) DEFAULT 'kg',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (packaging_id) REFERENCES terminal_packaging(id)
);

-- Create terminal_carriers table
CREATE TABLE IF NOT EXISTS terminal_carriers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    terminal_carrier_id VARCHAR(50) UNIQUE,
    name VARCHAR(255),
    slug VARCHAR(100),
    logo TEXT,
    active BOOLEAN DEFAULT TRUE,
    domestic BOOLEAN DEFAULT FALSE,
    regional BOOLEAN DEFAULT FALSE,
    international BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## Phase 2: Core Service Implementation

### 2.1 Create Terminal Africa Service
**New File:** `services/terminal_service.py`

**Features:**
- API key authentication
- Address management
- Packaging management
- Parcel creation
- Rate fetching
- Shipment creation
- Tracking

### 2.2 Create Terminal Address Manager
**New File:** `services/terminal_address_manager.py`

**Features:**
- Sync local addresses to Terminal
- Address validation
- Address CRUD operations

### 2.3 Create Terminal Carrier Manager
**New File:** `services/terminal_carrier_manager.py`

**Features:**
- Fetch available carriers
- Enable/disable carriers
- Carrier filtering

---

## Phase 3: Address Integration

### 3.1 Update Address Routes
**File:** `routes/addresses.py`

**Changes:**
- Sync addresses to Terminal when created
- Store Terminal address_id
- Use Terminal validation

### 3.2 Address Validation
**Update:** `services/address_validator.py`

**Add:**
- Terminal address validation API integration
- Fallback to local validation

---

## Phase 4: Shipping Quotes/Rates

### 4.1 Update Shipping Routes
**File:** `routes/shipping.py`

**Changes:**
- Replace Sendbox quotes with Terminal rates
- Support multiple carriers
- Add carrier selection
- Include packaging options

### 4.2 New Endpoints
- `GET /api/shipping/carriers` - List available carriers
- `POST /api/shipping/rates` - Get rates from multiple carriers
- `GET /api/shipping/packaging` - List packaging options

---

## Phase 5: Order & Shipment Creation

### 5.1 Update Order Routes
**File:** `routes/orders.py`

**Changes:**
- Create Terminal parcel when order confirmed
- Get rates from Terminal
- Create Terminal shipment
- Store Terminal shipment details

### 5.2 Shipment Manager
**Update:** `services/shipment_manager.py`

**Changes:**
- Replace Sendbox shipment creation with Terminal
- Handle multi-carrier support
- Store shipping labels and invoices

---

## Phase 6: Tracking Integration

### 6.1 Update Tracking
**File:** `services/tracking_sync.py`

**Changes:**
- Use Terminal tracking API
- Parse Terminal tracking events
- Map Terminal statuses to internal statuses

### 6.2 Webhook Handler
**File:** `routes/webhooks.py`

**Add:**
- Terminal webhook endpoint
- Terminal event processing

---

## Phase 7: Admin Features

### 7.1 Admin Shipping Routes
**File:** `routes/admin_shipping.py`

**Changes:**
- List Terminal shipments
- Carrier management
- Packaging management
- Shipment cancellation

### 7.2 New Admin Endpoints
- `GET /api/admin/terminal/carriers` - Manage carriers
- `POST /api/admin/terminal/carriers/enable` - Enable carrier
- `GET /api/admin/terminal/packaging` - Manage packaging
- `POST /api/admin/terminal/packaging` - Create packaging

---

## Phase 8: Testing & Migration

### 8.1 Parallel Running
- Run both Sendbox and Terminal in parallel
- Feature flag to switch between providers
- Gradual migration of orders

### 8.2 Data Migration
- Migrate existing Sendbox data to Terminal format
- Update tracking codes
- Sync addresses

### 8.3 Testing
- Test all endpoints with Terminal API
- Verify carrier selection
- Test multi-parcel shipments
- Validate tracking

---

## Implementation Priority

### High Priority (Must Have)
1. ✅ Configuration setup
2. ✅ Terminal service implementation
3. ✅ Address integration
4. ✅ Rate fetching
5. ✅ Shipment creation
6. ✅ Tracking

### Medium Priority (Should Have)
1. ⚠️ Multiple carrier support
2. ⚠️ Packaging management
3. ⚠️ Admin carrier management
4. ⚠️ Webhook integration

### Low Priority (Nice to Have)
1. 📋 Drop-off locations
2. 📋 Insurance options
3. 📋 Cash on delivery
4. 📋 Multi-parcel shipments

---

## Breaking Changes

### API Changes
1. **Shipping Quotes Response**
   - Old: Simple quote with single carrier
   - New: Multiple rates from different carriers

2. **Shipment Creation**
   - Old: Direct shipment creation
   - New: Requires rate selection first

3. **Tracking**
   - Old: Simple tracking code
   - New: Detailed tracking with events

### Database Changes
1. New tables for Terminal entities
2. Additional fields in orders table
3. Address format changes

---

## Backward Compatibility

### Strategy
1. Keep Sendbox code for existing shipments
2. Use Terminal for new shipments
3. Provide migration script for old data
4. Feature flag to switch providers

### Migration Script
**File:** `migrate_sendbox_to_terminal.py`

**Features:**
- Migrate addresses
- Update tracking codes
- Sync shipment data

---

## Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Setup | 1 day | None |
| Phase 2: Core Service | 2 days | Phase 1 |
| Phase 3: Addresses | 1 day | Phase 2 |
| Phase 4: Rates | 2 days | Phase 2, 3 |
| Phase 5: Shipments | 2 days | Phase 4 |
| Phase 6: Tracking | 1 day | Phase 5 |
| Phase 7: Admin | 2 days | Phase 5 |
| Phase 8: Testing | 2 days | All phases |
| **Total** | **13 days** | |

---

## Risk Assessment

### High Risk
1. **API Compatibility**: Terminal API structure is different
2. **Data Migration**: Existing Sendbox data needs migration
3. **Carrier Selection**: Users need to choose carriers

### Medium Risk
1. **Testing Coverage**: Need comprehensive testing
2. **Performance**: Multiple carrier API calls
3. **Error Handling**: Different error formats

### Low Risk
1. **Configuration**: Simple key-based auth
2. **Documentation**: Well-documented API

---

## Success Criteria

### Technical
- ✅ All endpoints working with Terminal API
- ✅ Successful rate fetching from multiple carriers
- ✅ Shipment creation and tracking working
- ✅ Webhook integration functional
- ✅ Admin features operational

### Business
- ✅ No disruption to existing orders
- ✅ Improved carrier options for users
- ✅ Better tracking visibility
- ✅ Cost optimization through carrier selection

---

## Next Steps

1. **Review and Approve Plan**
2. **Set Up Terminal Account**
3. **Start Phase 1 Implementation**
4. **Create Feature Branch**
5. **Begin Development**

---

## Support & Documentation

- **Terminal Africa Docs**: https://docs.terminal.africa/
- **API Reference**: https://developers.terminal.africa/
- **Support**: support@terminal.africa

---

**Document Version**: 1.0  
**Last Updated**: 2026-05-04  
**Status**: Ready for Implementation
