# Terminal Africa Phase 2 Complete ✅

## Phase 2: Core Service Implementation

**Status**: ✅ COMPLETE  
**Date**: 2026-05-04

---

## What Was Implemented

### 1. Terminal Africa Service (`services/terminal_service.py`)

Complete API client for Terminal Africa with the following features:

#### Address Management
- `create_address()` - Create new addresses
- `get_addresses()` - List all addresses with pagination
- `get_address()` - Get specific address by ID
- `update_address()` - Update existing address
- `delete_address()` - Delete address

#### Packaging Management
- `create_packaging()` - Create packaging options
- `get_packaging()` - List all packaging with pagination
- `get_packaging_by_id()` - Get specific packaging
- `delete_packaging()` - Delete packaging

#### Parcel Management
- `create_parcel()` - Create parcels with items
- `get_parcels()` - List all parcels
- `get_parcel()` - Get specific parcel

#### Carrier Management
- `get_carriers()` - List available carriers with filters
- `enable_carrier()` - Enable a carrier
- `disable_carrier()` - Disable a carrier

#### Rate Management
- `get_rates()` - Get shipping rates from multiple carriers

#### Shipment Management
- `create_shipment()` - Create shipment with selected rate
- `get_shipments()` - List all shipments
- `get_shipment()` - Get specific shipment
- `cancel_shipment()` - Cancel a shipment

#### Tracking
- `track_shipment()` - Track by shipment ID
- `track_by_tracking_number()` - Track by carrier tracking number

#### Utility Methods
- `get_user_profile()` - Get user profile
- `get_wallet_balance()` - Get wallet balance

### 2. Terminal Address Manager (`services/terminal_address_manager.py`)

Manages address synchronization between local database and Terminal Africa:

- `create_and_sync_address()` - Create address in Terminal and store locally
- `get_terminal_address_id()` - Get Terminal address ID for user
- `get_user_addresses()` - Get all addresses for user
- `sync_existing_address()` - Sync existing local address to Terminal
- `update_terminal_address()` - Update address in Terminal and locally
- `delete_terminal_address()` - Delete address from Terminal and locally
- `validate_address()` - Validate address data

### 3. Terminal Carrier Manager (`services/terminal_carrier_manager.py`)

Manages carrier operations and synchronization:

- `sync_carriers()` - Fetch carriers from Terminal and sync to database
- `get_local_carriers()` - Get carriers from local database with filters
- `get_carrier_by_id()` - Get specific carrier
- `enable_carrier()` - Enable carrier in Terminal and locally
- `disable_carrier()` - Disable carrier in Terminal and locally
- `get_carrier_stats()` - Get carrier statistics
- `search_carriers()` - Search carriers by name/slug
- `get_recommended_carriers()` - Get recommended carriers based on route

---

## Key Features

### 1. **Singleton Pattern**
All services use singleton pattern for efficient resource management:
```python
from services.terminal_service import get_terminal_client
from services.terminal_address_manager import get_address_manager
from services.terminal_carrier_manager import get_carrier_manager

client = get_terminal_client()
address_mgr = get_address_manager()
carrier_mgr = get_carrier_manager()
```

### 2. **Automatic Environment Switching**
Services automatically use test or live keys based on `Config.TERMINAL_ENVIRONMENT`:
- Test: `pk_test_*` and `sk_test_*`
- Live: `pk_live_*` and `sk_live_*`

### 3. **Error Handling**
Custom `TerminalAPIError` exception with:
- Error message
- HTTP status code
- Full response data

### 4. **Comprehensive Logging**
All operations are logged for debugging and monitoring.

### 5. **Database Synchronization**
- Addresses synced to `terminal_addresses` table
- Carriers synced to `terminal_carriers` table
- Automatic updates on changes

---

## Usage Examples

### Example 1: Create and Sync Address

```python
from services.terminal_address_manager import get_address_manager

address_mgr = get_address_manager()

result = address_mgr.create_and_sync_address(
    user_id=1,
    first_name="John",
    last_name="Doe",
    phone="+2348012345678",
    email="john@example.com",
    line1="123 Main Street",
    city="Lagos",
    state="Lagos",
    country="NG",
    zip_code="100001",
    is_residential=True
)

print(f"Terminal Address ID: {result['terminal_address_id']}")
```

### Example 2: Sync Carriers

```python
from services.terminal_carrier_manager import get_carrier_manager

carrier_mgr = get_carrier_manager()

# Sync carriers from Terminal Africa
result = carrier_mgr.sync_carriers()
print(f"Synced {result['synced_count']} carriers")

# Get active domestic carriers
carriers = carrier_mgr.get_local_carriers(active=True, domestic=True)
for carrier in carriers:
    print(f"- {carrier['name']} ({carrier['slug']})")
```

### Example 3: Create Parcel and Get Rates

```python
from services.terminal_service import get_terminal_client

client = get_terminal_client()

# Create packaging
packaging = client.create_packaging(
    name="Medium Box",
    type="box",
    length=30,
    width=25,
    height=20,
    weight=1.0,
    size_unit="cm",
    weight_unit="kg"
)
packaging_id = packaging['data']['packaging_id']

# Create parcel
parcel = client.create_parcel(
    packaging_id=packaging_id,
    items=[
        {
            "name": "T-Shirt",
            "quantity": 2,
            "value": 5000,
            "weight": 0.5,
            "description": "Cotton T-Shirt"
        }
    ],
    description="Fashion items"
)
parcel_id = parcel['data']['parcel_id']

# Get rates
rates = client.get_rates(
    origin_address_id="addr_xxx",
    destination_address_id="addr_yyy",
    parcel_id=parcel_id,
    currency="NGN"
)

# Display rates from different carriers
for rate in rates['data']:
    carrier = rate['carrier']['name']
    amount = rate['amount']
    delivery_time = rate['delivery_time']
    print(f"{carrier}: ₦{amount} - {delivery_time}")
```

### Example 4: Create Shipment

```python
from services.terminal_service import get_terminal_client

client = get_terminal_client()

# Create shipment with selected rate
shipment = client.create_shipment(
    rate_id="rate_xxx",
    origin_address_id="addr_xxx",
    destination_address_id="addr_yyy",
    parcel_id="parcel_xxx",
    metadata={"order_id": "12345"}
)

shipment_id = shipment['data']['shipment_id']
tracking_number = shipment['data']['tracking_number']
label_url = shipment['data']['label_url']

print(f"Shipment created: {shipment_id}")
print(f"Tracking: {tracking_number}")
print(f"Label: {label_url}")
```

### Example 5: Track Shipment

```python
from services.terminal_service import get_terminal_client

client = get_terminal_client()

# Track by shipment ID
tracking = client.track_shipment("shipment_xxx")

status = tracking['data']['status']
events = tracking['data']['events']

print(f"Status: {status}")
for event in events:
    print(f"- {event['timestamp']}: {event['description']}")
```

---

## API Endpoints Reference

### Terminal Africa Base URL
```
https://api.terminal.africa/v1
```

### Authentication
All requests require Bearer token authentication:
```
Authorization: Bearer sk_test_xxx
```

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/addresses` | Create address |
| GET | `/addresses` | List addresses |
| GET | `/addresses/{id}` | Get address |
| PATCH | `/addresses/{id}` | Update address |
| DELETE | `/addresses/{id}` | Delete address |
| POST | `/packaging` | Create packaging |
| GET | `/packaging` | List packaging |
| POST | `/parcels` | Create parcel |
| GET | `/parcels` | List parcels |
| GET | `/carriers` | List carriers |
| POST | `/carriers/{id}/enable` | Enable carrier |
| POST | `/carriers/{id}/disable` | Disable carrier |
| POST | `/rates` | Get shipping rates |
| POST | `/shipments` | Create shipment |
| GET | `/shipments` | List shipments |
| GET | `/shipments/{id}` | Get shipment |
| POST | `/shipments/{id}/cancel` | Cancel shipment |
| GET | `/shipments/{id}/track` | Track shipment |
| GET | `/users/profile` | Get user profile |
| GET | `/wallets/balance` | Get wallet balance |

---

## Database Tables Used

### `terminal_addresses`
Stores synced addresses with Terminal address IDs.

### `terminal_carriers`
Stores carrier information synced from Terminal Africa.

### `terminal_packaging`
Stores packaging options (created in Phase 1 migration).

### `terminal_parcels`
Stores parcel information (will be used in Phase 5).

### `terminal_rates`
Stores rate information for caching (will be used in Phase 4).

---

## Configuration

### Environment Variables
```env
# Terminal Africa Configuration
TERMINAL_ENV=test  # or 'live' for production
```

### Config.py Settings
```python
# Terminal Africa API Configuration
TERMINAL_TEST_PUBLIC_KEY = "pk_test_WeDJ1I1cKKkubg60rE6kXnwPJXlExlH1"
TERMINAL_TEST_SECRET_KEY = "sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn"
TERMINAL_LIVE_PUBLIC_KEY = "pk_live_G8zfsoShEtgvDPUvHABwdF9Lw4a65HKg"
TERMINAL_LIVE_SECRET_KEY = "sk_live_jiep2FyoHX3tImNV4eVkdVl1SXIHrFWM"
TERMINAL_ENVIRONMENT = "test"
TERMINAL_BASE_URL = "https://api.terminal.africa/v1"
```

---

## Testing

### Test Terminal Service
```python
from services.terminal_service import get_terminal_client

client = get_terminal_client()

# Test user profile
profile = client.get_user_profile()
print(f"User: {profile['data']['name']}")

# Test wallet balance
balance = client.get_wallet_balance()
print(f"Balance: {balance['data']['balance']}")

# Test carriers
carriers = client.get_carriers(active=True)
print(f"Active carriers: {len(carriers['data'])}")
```

### Test Address Manager
```python
from services.terminal_address_manager import get_address_manager

address_mgr = get_address_manager()

# Create test address
result = address_mgr.create_and_sync_address(
    user_id=1,
    first_name="Test",
    last_name="User",
    phone="+2348012345678",
    email="test@example.com",
    line1="Test Street",
    city="Lagos",
    state="Lagos",
    country="NG"
)

print(f"Success: {result['success']}")
print(f"Terminal ID: {result['terminal_address_id']}")
```

### Test Carrier Manager
```python
from services.terminal_carrier_manager import get_carrier_manager

carrier_mgr = get_carrier_manager()

# Sync carriers
result = carrier_mgr.sync_carriers()
print(f"Synced: {result['synced_count']} carriers")

# Get stats
stats = carrier_mgr.get_carrier_stats()
print(f"Total: {stats['total']}, Active: {stats['active']}")
```

---

## Error Handling

### TerminalAPIError
```python
from services.terminal_service import get_terminal_client, TerminalAPIError

client = get_terminal_client()

try:
    address = client.create_address(...)
except TerminalAPIError as e:
    print(f"Error: {e.message}")
    print(f"Status Code: {e.status_code}")
    print(f"Response: {e.response_data}")
```

### Common Error Codes
- `400` - Bad request (invalid data)
- `401` - Authentication failed (invalid API key)
- `403` - Forbidden (insufficient permissions)
- `404` - Resource not found
- `422` - Validation error

---

## Next Steps

### Phase 3: Address Integration
- Update address routes to use Terminal
- Integrate address validation
- Sync existing addresses

### Phase 4: Shipping Quotes/Rates
- Update shipping routes
- Implement multi-carrier rate fetching
- Add carrier selection

### Phase 5: Order & Shipment Creation
- Update order routes
- Implement Terminal shipment creation
- Store shipment details

---

## Support

### Terminal Africa Documentation
- **Docs**: https://docs.terminal.africa/
- **API Reference**: https://developers.terminal.africa/
- **Support**: support@terminal.africa

### Internal Support
- Check service logs for debugging
- Review `TerminalAPIError` details
- Test with Terminal test environment first

---

**Phase 2 Status**: ✅ COMPLETE  
**Ready for**: Phase 3 - Address Integration

