"""
Simple test for rates endpoint
"""

import requests
import json


BASE_URL = "http://localhost:4500"
TEST_USER = {
    "email": "devtomiwa9@gmail.com",
    "password": "Pityboy@22"
}


def main():
    # Login
    print("🔐 Logging in...")
    response = requests.post(f"{BASE_URL}/api/auth/login", json=TEST_USER)
    token = response.json()["data"]["token"]
    print("✅ Logged in\n")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get addresses
    print("📋 Getting addresses...")
    response = requests.get(f"{BASE_URL}/api/addresses", headers=headers)
    addresses = response.json()["data"]["addresses"]
    
    synced_addresses = [a for a in addresses if a.get('terminal_synced')]
    print(f"✅ Found {len(synced_addresses)} synced addresses\n")
    
    if len(synced_addresses) < 2:
        print("❌ Need at least 2 synced addresses")
        return 1
    
    # Get rates
    print("💰 Getting shipping rates...")
    rate_data = {
        "origin_address_id": synced_addresses[0]['id'],
        "destination_address_id": synced_addresses[1]['id'],
        "items": [
            {
                "name": "Test Product",
                "quantity": 1,
                "value": 10000,
                "weight": 1.0,
                "description": "Test"
            }
        ],
        "currency": "NGN"
    }
    
    print(f"   Origin: {synced_addresses[0]['city']}")
    print(f"   Destination: {synced_addresses[1]['city']}")
    print(f"   Weight: 1.0 kg")
    print()
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/shipping/rates",
            headers=headers,
            json=rate_data,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            rates = data["data"]["rates"]
            print(f"✅ Got {len(rates)} rates!\n")
            
            for i, rate in enumerate(rates[:5], 1):
                carrier = rate.get('carrier', {})
                print(f"{i}. {carrier.get('name', 'Unknown')}")
                print(f"   Amount: {rate.get('currency', 'NGN')} {rate.get('amount', 0):,.2f}")
                print(f"   Delivery: {rate.get('delivery_time', 'N/A')}")
                print()
            
            return 0
        else:
            print(f"❌ Failed: {response.status_code}")
            print(response.text)
            return 1
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (30s)")
        return 1
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
