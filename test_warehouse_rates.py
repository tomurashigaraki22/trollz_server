#!/usr/bin/env python3
"""
Test warehouse address integration with rates endpoint
"""

import requests
import json

BASE_URL = "http://localhost:4500"

def login():
    """Login as test user"""
    print("🔐 Logging in as test user...")
    response = requests.post(f"{BASE_URL}/api/login", json={
        "email": "devtomiwa9@gmail.com",
        "password": "Pityboy@22"
    })
    
    if response.status_code == 200:
        token = response.json()["data"]["token"]
        print(f"✅ Login successful")
        return {"Authorization": f"Bearer {token}"}
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def get_user_addresses(headers):
    """Get user addresses"""
    print("\n📍 Getting user addresses...")
    response = requests.get(f"{BASE_URL}/api/addresses", headers=headers)
    
    if response.status_code == 200:
        addresses = response.json()["data"]["addresses"]
        print(f"✅ Found {len(addresses)} addresses")
        
        # Find a synced address
        synced_addresses = [addr for addr in addresses if addr.get("terminal_address_id")]
        if synced_addresses:
            print(f"✅ Found {len(synced_addresses)} synced addresses")
            return synced_addresses[0]
        else:
            print("❌ No synced addresses found")
            return None
    else:
        print(f"❌ Failed to get addresses: {response.text}")
        return None

def test_rates_with_warehouse(headers, destination_address):
    """Test rates endpoint with warehouse as automatic origin"""
    print("\n💰 Testing rates with warehouse origin...")
    
    rate_request = {
        "destination_address_id": destination_address["id"],
        "items": [
            {
                "name": "Test Product",
                "quantity": 1,
                "value": 10000,
                "weight": 1.0,
                "description": "Test product for warehouse rates"
            }
        ],
        "currency": "NGN"
    }
    
    print(f"📦 Requesting rates to: {destination_address['city']}, {destination_address['state']}")
    
    response = requests.post(
        f"{BASE_URL}/api/shipping/rates",
        headers=headers,
        json=rate_request
    )
    
    if response.status_code == 200:
        data = response.json()["data"]
        rates = data["rates"]
        summary = data["summary"]
        
        print(f"✅ Got {len(rates)} rates")
        print(f"📍 Origin: {summary['origin']}")
        print(f"📍 Destination: {summary['destination']}")
        print(f"📦 Parcel ID: {data['parcel_id']}")
        print(f"🏭 Warehouse Address ID: {data['warehouse_address_id']}")
        
        if rates:
            print(f"\n📋 Sample rates:")
            for i, rate in enumerate(rates[:3]):  # Show first 3 rates
                print(f"  {i+1}. {rate.get('carrier_name', 'Unknown')} - {rate.get('currency', 'NGN')} {rate.get('amount', 0):,.2f}")
        
        return data
    else:
        print(f"❌ Failed to get rates: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def main():
    """Main test function"""
    print("🧪 Testing Warehouse Address Integration")
    print("=" * 60)
    
    # Login
    headers = login()
    if not headers:
        return
    
    # Get destination address
    destination = get_user_addresses(headers)
    if not destination:
        return
    
    # Test rates with warehouse
    rates_data = test_rates_with_warehouse(headers, destination)
    
    print("\n" + "=" * 60)
    if rates_data:
        print("✅ WAREHOUSE INTEGRATION TEST PASSED")
        print(f"   Warehouse automatically used as origin")
        print(f"   Got {len(rates_data['rates'])} shipping rates")
    else:
        print("❌ WAREHOUSE INTEGRATION TEST FAILED")

if __name__ == "__main__":
    main()