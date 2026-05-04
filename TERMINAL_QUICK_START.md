# Terminal Africa Quick Start Guide

Quick reference for using Terminal Africa services in your application.

---

## 1. Import Services

```python
# Main Terminal service
from services.terminal_service import get_terminal_client, TerminalAPIError

# Address manager
from services.terminal_address_manager import get_address_manager

# Carrier manager
from services.terminal_carrier_manager import get_carrier_manager
```

---

## 2. Initialize Services

```python
# Get service instances (singleton pattern)
terminal = get_terminal_client()
address_mgr = get_address_manager()
carrier_mgr = get_carrier_manager()
```

---

## 3. Common Operations

### Create and Sync Address

```python
try:
    result = address_mgr.create_and_sync_address(
        user_id=user_id,
        first_name="John",
        last_name="Doe",
        phone="+2348012345678",
        email="john@example.com",
        line1="123 Main Street",
        city="Lagos",
        state="Lagos",
        country="NG",
        zip_code="100001"
    )
    
    terminal_address_id = result['terminal_address_id']
    print(f"Address created: {terminal_address_id}")
    
except TerminalAPIError as e:
    print(f"Error: {e.message}")
```

### Sync Carriers

```python
try:
    result = carrier_mgr.sync_carriers()
    print(f"Synced {result['synced_count']} carriers")
    
    # Get active carriers
    carriers = carrier_mgr.get_local_carriers(active=True)
    
except TerminalAPIError as e:
    print(f"Error: {e.message}")
```

### Create Packaging

```python
try:
    packaging = terminal.create_packaging(
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
    print(f"Packaging created: {packaging_id}")
    
except TerminalAPIError as e:
    print(f"Error: {e.message}")
```

### Create Parcel

```python
try:
    parcel = terminal.create_parcel(
        packaging_id=packaging_id,
        items=[
            {
                "name": "T-Shirt",
                "quantity": 2,
                "value": 5000,
                "weight": 0.5,
                "description": "Cotton T-Shirt",
                "currency": "NGN"
            }
        ],
        description="Fashion items"
    )
    
    parcel_id = parcel['data']['parcel_id']
    print(f"Parcel created: {parcel_id}")
    
except TerminalAPIError as e:
    print(f"Error: {e.message}")
```

### Get Shipping Rates

```python
try:
    rates = terminal.get_rates(
        origin_address_id=origin_address_id,
        destination_address_id=destination_address_id,
        parcel_id=parcel_id,
        currency="NGN"
    )
    
    # Display rates from different carriers
    for rate in rates['data']:
        carrier_name = rate['carrier']['name']
        amount = rate['amount']
        delivery_time = rate['delivery_time']
        rate_id = rate['rate_id']
        
        print(f"{carrier_name}: ₦{amount} - {delivery_time}")
    
except TerminalAPIError as e:
    print(f"Error: {e.message}")
```

### Create Shipment

```python
try:
    shipment = terminal.create_shipment(
        rate_id=selected_rate_id,
        origin_address_id=origin_address_id,
        destination_address_id=destination_address_id,
        parcel_id=parcel_id,
        metadata={
            "order_id": order_id,
            "customer_name": customer_name
        }
    )
    
    shipment_data = shipment['data']
    shipment_id = shipment_data['shipment_id']
    tracking_number = shipment_data['tracking_number']
    label_url = shipment_data['label_url']
    
    print(f"Shipment created: {shipment_id}")
    print(f"Tracking: {tracking_number}")
    print(f"Label: {label_url}")
    
except TerminalAPIError as e:
    print(f"Error: {e.message}")
```

### Track Shipment

```python
try:
    tracking = terminal.track_shipment(shipment_id)
    
    tracking_data = tracking['data']
    status = tracking_data['status']
    events = tracking_data['events']
    
    print(f"Status: {status}")
    for event in events:
        print(f"{event['timestamp']}: {event['description']}")
    
except TerminalAPIError as e:
    print(f"Error: {e.message}")
```

---

## 4. Complete Workflow Example

```python
from services.terminal_service import get_terminal_client, TerminalAPIError
from services.terminal_address_manager import get_address_manager
from services.terminal_carrier_manager import get_carrier_manager

def create_shipment_workflow(user_id, order_data):
    """Complete workflow to create a shipment."""
    
    try:
        terminal = get_terminal_client()
        address_mgr = get_address_manager()
        
        # Step 1: Create origin address (warehouse)
        origin_result = address_mgr.create_and_sync_address(
            user_id=user_id,
            first_name="Trollz Store",
            last_name="Warehouse",
            phone="+234 800 000 0000",
            email="warehouse@trollzstore.com",
            line1="LYPAS Plaza, Cluster Industrial Complex",
            city="Owerri",
            state="Imo",
            country="NG"
        )
        origin_address_id = origin_result['terminal_address_id']
        
        # Step 2: Create destination address (customer)
        dest_result = address_mgr.create_and_sync_address(
            user_id=user_id,
            first_name=order_data['customer_first_name'],
            last_name=order_data['customer_last_name'],
            phone=order_data['customer_phone'],
            email=order_data['customer_email'],
            line1=order_data['shipping_address'],
            city=order_data['shipping_city'],
            state=order_data['shipping_state'],
            country="NG"
        )
        dest_address_id = dest_result['terminal_address_id']
        
        # Step 3: Create packaging
        packaging = terminal.create_packaging(
            name="Order Package",
            type="box",
            length=30,
            width=25,
            height=20,
            weight=order_data['total_weight'],
            size_unit="cm",
            weight_unit="kg"
        )
        packaging_id = packaging['data']['packaging_id']
        
        # Step 4: Create parcel with order items
        parcel = terminal.create_parcel(
            packaging_id=packaging_id,
            items=order_data['items'],
            description=f"Order #{order_data['order_id']}"
        )
        parcel_id = parcel['data']['parcel_id']
        
        # Step 5: Get shipping rates
        rates = terminal.get_rates(
            origin_address_id=origin_address_id,
            destination_address_id=dest_address_id,
            parcel_id=parcel_id,
            currency="NGN"
        )
        
        # Step 6: Select cheapest rate (or let user choose)
        selected_rate = min(rates['data'], key=lambda x: x['amount'])
        rate_id = selected_rate['rate_id']
        
        # Step 7: Create shipment
        shipment = terminal.create_shipment(
            rate_id=rate_id,
            origin_address_id=origin_address_id,
            destination_address_id=dest_address_id,
            parcel_id=parcel_id,
            metadata={
                "order_id": order_data['order_id'],
                "customer_name": f"{order_data['customer_first_name']} {order_data['customer_last_name']}"
            }
        )
        
        return {
            "success": True,
            "shipment_id": shipment['data']['shipment_id'],
            "tracking_number": shipment['data']['tracking_number'],
            "label_url": shipment['data']['label_url'],
            "carrier": selected_rate['carrier']['name'],
            "amount": selected_rate['amount']
        }
        
    except TerminalAPIError as e:
        return {
            "success": False,
            "error": e.message,
            "status_code": e.status_code
        }
```

---

## 5. Error Handling

```python
from services.terminal_service import TerminalAPIError

try:
    # Your Terminal API call
    result = terminal.create_address(...)
    
except TerminalAPIError as e:
    # Handle Terminal API errors
    print(f"Error: {e.message}")
    print(f"Status Code: {e.status_code}")
    print(f"Response Data: {e.response_data}")
    
    # Handle specific error codes
    if e.status_code == 401:
        print("Authentication failed - check API key")
    elif e.status_code == 422:
        print("Validation error - check input data")
    elif e.status_code == 404:
        print("Resource not found")
    
except Exception as e:
    # Handle other errors
    print(f"Unexpected error: {str(e)}")
```

---

## 6. Configuration

### Switch Between Test and Live

```python
# In config.py
TERMINAL_ENVIRONMENT = "test"  # or "live"

# Or use environment variable
# In .env file:
TERMINAL_ENV=test  # or 'live'
```

### Get Current Configuration

```python
from config import Config

print(f"Environment: {Config.TERMINAL_ENVIRONMENT}")
print(f"Base URL: {Config.TERMINAL_BASE_URL}")
print(f"Secret Key: {Config.get_terminal_secret_key()}")
```

---

## 7. Useful Helper Functions

### Get User's Terminal Address

```python
def get_user_terminal_address(user_id):
    """Get user's Terminal address ID."""
    address_mgr = get_address_manager()
    return address_mgr.get_terminal_address_id(user_id)
```

### Get Recommended Carriers

```python
def get_shipping_carriers(origin_country, dest_country):
    """Get recommended carriers for route."""
    carrier_mgr = get_carrier_manager()
    return carrier_mgr.get_recommended_carriers(origin_country, dest_country)
```

### Format Shipping Rate

```python
def format_rate(rate):
    """Format rate for display."""
    return {
        "carrier": rate['carrier']['name'],
        "amount": f"₦{rate['amount']:,.2f}",
        "delivery_time": rate['delivery_time'],
        "rate_id": rate['rate_id']
    }
```

---

## 8. Testing

### Test Connection

```python
from services.terminal_service import get_terminal_client

terminal = get_terminal_client()

try:
    profile = terminal.get_user_profile()
    print("✅ Connected to Terminal Africa")
    print(f"User: {profile['data']['name']}")
except Exception as e:
    print(f"❌ Connection failed: {str(e)}")
```

### Test Carrier Sync

```python
from services.terminal_carrier_manager import get_carrier_manager

carrier_mgr = get_carrier_manager()

try:
    result = carrier_mgr.sync_carriers()
    print(f"✅ Synced {result['synced_count']} carriers")
except Exception as e:
    print(f"❌ Sync failed: {str(e)}")
```

---

## 9. Common Patterns

### Pattern 1: Get or Create Address

```python
def get_or_create_terminal_address(user_id, address_data):
    """Get existing Terminal address or create new one."""
    address_mgr = get_address_manager()
    
    # Try to get existing address
    terminal_address_id = address_mgr.get_terminal_address_id(user_id)
    
    if terminal_address_id:
        return terminal_address_id
    
    # Create new address
    result = address_mgr.create_and_sync_address(
        user_id=user_id,
        **address_data
    )
    
    return result['terminal_address_id']
```

### Pattern 2: Compare Rates

```python
def compare_shipping_rates(rates_data):
    """Compare and sort shipping rates."""
    rates = rates_data['data']
    
    # Sort by price
    by_price = sorted(rates, key=lambda x: x['amount'])
    
    # Sort by delivery time (assuming format like "2-3 business days")
    def get_days(rate):
        time_str = rate['delivery_time']
        # Extract first number
        import re
        match = re.search(r'\d+', time_str)
        return int(match.group()) if match else 999
    
    by_speed = sorted(rates, key=get_days)
    
    return {
        "cheapest": by_price[0],
        "fastest": by_speed[0],
        "all_rates": rates
    }
```

### Pattern 3: Retry Logic

```python
import time

def create_shipment_with_retry(max_retries=3, **kwargs):
    """Create shipment with retry logic."""
    terminal = get_terminal_client()
    
    for attempt in range(max_retries):
        try:
            return terminal.create_shipment(**kwargs)
        except TerminalAPIError as e:
            if e.status_code in [500, 502, 503, 504]:
                # Server error, retry
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
            raise
```

---

## 10. Best Practices

### 1. Always Use Try-Except

```python
try:
    result = terminal.create_address(...)
except TerminalAPIError as e:
    # Handle error
    pass
```

### 2. Cache Carrier Data

```python
# Sync carriers once per day, not on every request
carrier_mgr.sync_carriers()
```

### 3. Store Terminal IDs

```python
# Always store Terminal IDs in your database
# - terminal_address_id
# - terminal_shipment_id
# - terminal_rate_id
```

### 4. Use Metadata

```python
# Store order information in shipment metadata
shipment = terminal.create_shipment(
    ...,
    metadata={
        "order_id": "12345",
        "customer_id": "67890",
        "notes": "Handle with care"
    }
)
```

### 5. Log All Operations

```python
import logging

logger = logging.getLogger(__name__)

try:
    result = terminal.create_shipment(...)
    logger.info(f"Shipment created: {result['data']['shipment_id']}")
except TerminalAPIError as e:
    logger.error(f"Shipment creation failed: {e.message}")
```

---

## 11. Resources

### Documentation
- **Phase 2 Complete**: `docs/TERMINAL_PHASE2_COMPLETE.md`
- **API Documentation**: `docs/TERMINAL_API_DOCUMENTATION.md`
- **Migration Plan**: `TERMINAL_MIGRATION_PLAN.md`

### Testing
- **Test Suite**: `test_terminal_phase2.py`
- **Postman**: Use API documentation for collection

### Support
- **Terminal Africa Docs**: https://docs.terminal.africa/
- **API Reference**: https://developers.terminal.africa/
- **Support**: support@terminal.africa

---

**Quick Start Version**: 1.0  
**Last Updated**: 2026-05-04

