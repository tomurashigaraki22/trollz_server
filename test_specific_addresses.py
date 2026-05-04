"""
Test with specific address IDs
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.terminal_service import get_terminal_client

client = get_terminal_client()

# These are from test environment (created after 13:23)
test_addresses = [
    "AD-G7O3Z0NQ1VUFH26Q",  # ID 15 - Abuja
    "AD-51QVA4LDRUI66N8B",  # ID 14 - Lagos
]

print(f"Environment: {client.environment}")
print(f"Base URL: {client.base_url}")
print()

for addr_id in test_addresses:
    print(f"Checking: {addr_id}")
    try:
        response = client.get_address(addr_id)
        addr = response.get('data', {})
        print(f"  ✅ Found: {addr.get('city')}, {addr.get('state')}")
    except Exception as e:
        print(f"  ❌ Not found: {str(e)}")
    print()

# Now test rates with these
print("Testing rates with these addresses...")
print()

packaging_response = client.get_packaging(page=1, per_page=1)
packaging_id = packaging_response['data']['packaging'][0]['packaging_id']

items = [{
    "name": "Test",
    "quantity": 1,
    "value": 10000,
    "currency": "NGN",
    "weight": 1.0
}]

parcel_response = client.create_parcel(
    packaging_id=packaging_id,
    items=items,
    weight=1.0
)
parcel_id = parcel_response['data']['parcel_id']

print(f"Parcel created: {parcel_id}")
print()

try:
    rates_response = client.get_rates(
        origin_address_id=test_addresses[1],  # Lagos
        destination_address_id=test_addresses[0],  # Abuja
        parcel_id=parcel_id
    )
    
    rates = rates_response['data']
    print(f"✅ Got {len(rates)} rates!")
    
    for rate in rates[:3]:
        print(f"  - {rate['carrier_name']}: {rate['currency']} {rate['amount']}")
except Exception as e:
    print(f"❌ Error: {str(e)}")
