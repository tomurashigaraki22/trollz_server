"""
Debug shipment creation with Terminal Africa
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.terminal_service import get_terminal_client, TerminalAPIError
import json


def main():
    print("="*80)
    print("  DEBUG: Shipment Creation")
    print("="*80)
    print()
    
    client = get_terminal_client()
    
    print(f"Environment: {client.environment}")
    print(f"Base URL: {client.base_url}")
    print()
    
    # Step 1: Get addresses
    print("STEP 1: Get Addresses")
    print("-" * 80)
    addresses_response = client.get_addresses(page=1, per_page=10)
    
    if 'data' in addresses_response:
        addr_data = addresses_response['data']
        if isinstance(addr_data, dict) and 'addresses' in addr_data:
            addresses = addr_data['addresses']
        else:
            addresses = addr_data if isinstance(addr_data, list) else []
    else:
        addresses = addresses_response if isinstance(addresses_response, list) else []
    
    print(f"✅ Found {len(addresses)} addresses")
    
    if len(addresses) < 2:
        print("❌ Need at least 2 addresses")
        return
    
    origin_addr = addresses[0]
    dest_addr = addresses[1]
    
    origin_id = origin_addr.get('address_id') or origin_addr.get('id')
    dest_id = dest_addr.get('address_id') or dest_addr.get('id')
    
    print(f"   Origin: {origin_id} - {origin_addr.get('city')}, {origin_addr.get('state')}")
    print(f"   Destination: {dest_id} - {dest_addr.get('city')}, {dest_addr.get('state')}")
    print()
    
    # Step 2: Get packaging
    print("STEP 2: Get Packaging")
    print("-" * 80)
    packaging_response = client.get_packaging(page=1, per_page=1)
    packaging_list = packaging_response['data']['packaging']
    
    if not packaging_list:
        print("❌ No packaging found")
        return
    
    packaging = packaging_list[0]
    packaging_id = packaging['packaging_id']
    print(f"✅ Packaging ID: {packaging_id}")
    print()
    
    # Step 3: Create parcel
    print("STEP 3: Create Parcel")
    print("-" * 80)
    
    items = [
        {
            "name": "Test Product",
            "quantity": 1,
            "value": 10000,
            "currency": "NGN",
            "weight": 1.0,
            "description": "Test product"
        }
    ]
    
    try:
        parcel_response = client.create_parcel(
            packaging_id=packaging_id,
            items=items,
            description="Test shipment",
            weight=1.0,
            weight_unit="kg"
        )
        
        parcel_data = parcel_response.get('data', parcel_response)
        parcel_id = parcel_data.get('parcel_id') or parcel_data.get('id')
        
        print(f"✅ Parcel ID: {parcel_id}")
        print()
        
    except TerminalAPIError as e:
        print(f"❌ Create Parcel Error: {e.message}")
        return
    
    # Step 4: Get rates
    print("STEP 4: Get Rates")
    print("-" * 80)
    
    try:
        rates_response = client.get_rates(
            origin_address_id=origin_id,
            destination_address_id=dest_id,
            parcel_id=parcel_id,
            currency="NGN"
        )
        
        rates_data = rates_response.get('data', [])
        rates = rates_data if isinstance(rates_data, list) else []
        
        print(f"✅ Got {len(rates)} rates")
        
        if not rates:
            print("❌ No rates returned")
            return
        
        # Select first rate
        selected_rate = rates[0]
        rate_id = selected_rate.get('rate_id') or selected_rate.get('id')
        
        print(f"   Selected Rate ID: {rate_id}")
        print(f"   Carrier: {selected_rate.get('carrier_name', 'Unknown')}")
        print(f"   Amount: {selected_rate.get('amount', 0)}")
        print()
        
    except TerminalAPIError as e:
        print(f"❌ Get Rates Error: {e.message}")
        return
    
    # Step 5: Create shipment
    print("STEP 5: Create Shipment")
    print("-" * 80)
    print(f"Rate ID: {rate_id}")
    print(f"Pickup Address: {origin_id}")
    print(f"Delivery Address: {dest_id}")
    print(f"Parcel ID: {parcel_id}")
    print()
    
    # Test the exact payload
    payload = {
        "rate_id": rate_id,
        "pickup_address": origin_id,
        "delivery_address": dest_id,
        "parcel": parcel_id
    }
    
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print()
    
    try:
        shipment_response = client.create_shipment(
            rate_id=rate_id,
            origin_address_id=origin_id,
            destination_address_id=dest_id,
            parcel_id=parcel_id
        )
        
        print("✅ Shipment created!")
        print(f"Response: {json.dumps(shipment_response, indent=2)}")
        
    except TerminalAPIError as e:
        print(f"❌ Create Shipment Error: {e.message}")
        print(f"   Status Code: {e.status_code}")
        if e.response_data:
            print(f"   Response: {json.dumps(e.response_data, indent=2)}")


if __name__ == "__main__":
    main()
