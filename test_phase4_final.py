"""
Final Phase 4 Test - Complete End-to-End
Tests all Phase 4 functionality with proper error handling.
"""

import requests
import sys
import time


BASE_URL = "http://localhost:4500"
TEST_USER = {
    "email": "devtomiwa9@gmail.com",
    "password": "Pityboy@22"
}


def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def login():
    print("🔐 Logging in...")
    response = requests.post(f"{BASE_URL}/api/auth/login", json=TEST_USER)
    
    if response.status_code == 200:
        token = response.json()["data"]["token"]
        print("✅ Logged in\n")
        return token
    print(f"❌ Login failed")
    return None


def main():
    print_header("TERMINAL AFRICA PHASE 4 - FINAL TEST")
    
    token = login()
    if not token:
        return 1
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Carriers
    print_header("TEST 1: Carriers")
    response = requests.get(f"{BASE_URL}/api/shipping/carriers", headers=headers)
    if response.status_code == 200:
        data = response.json()["data"]
        print(f"✅ Carriers: {data['count']} total, {data['active_count']} active")
    else:
        print(f"❌ Failed: {response.status_code}")
        return 1
    
    # Test 2: Packaging
    print_header("TEST 2: Packaging")
    response = requests.get(f"{BASE_URL}/api/shipping/packaging", headers=headers)
    if response.status_code == 200:
        data = response.json()["data"]
        print(f"✅ Packaging: {data['count']} options available")
    else:
        print(f"❌ Failed: {response.status_code}")
        return 1
    
    # Test 3: Get synced addresses
    print_header("TEST 3: Get Synced Addresses")
    response = requests.get(f"{BASE_URL}/api/addresses", headers=headers)
    if response.status_code == 200:
        data = response.json()["data"]
        addresses = data["addresses"]
        synced = [a for a in addresses if a.get('terminal_synced')]
        
        print(f"✅ Addresses: {len(addresses)} total, {len(synced)} synced")
        
        if len(synced) < 2:
            print("\n⚠️  Need at least 2 synced addresses for rates test")
            print("Creating new addresses...")
            
            # Create 2 test addresses
            test_addresses = [
                {
                    "first_name": "Test", "last_name": "Origin",
                    "phone": "+2348012345678", "email": "test@test.com",
                    "street": "123 Test St", "city": "Lagos",
                    "state": "Lagos", "country": "NG", "post_code": "100001"
                },
                {
                    "first_name": "Test", "last_name": "Dest",
                    "phone": "+2348087654321", "email": "test2@test.com",
                    "street": "456 Test Ave", "city": "Abuja",
                    "state": "Abuja", "country": "NG", "post_code": "900001"
                }
            ]
            
            for addr in test_addresses:
                resp = requests.post(f"{BASE_URL}/api/addresses", headers=headers, json=addr)
                if resp.status_code == 201:
                    print(f"  ✅ Created: {addr['city']}")
                else:
                    print(f"  ❌ Failed to create address")
            
            # Refresh addresses
            response = requests.get(f"{BASE_URL}/api/addresses", headers=headers)
            addresses = response.json()["data"]["addresses"]
            synced = [a for a in addresses if a.get('terminal_synced')]
        
        if len(synced) < 2:
            print("❌ Still don't have 2 synced addresses")
            return 1
        
        origin = synced[0]
        dest = synced[1]
        
        print(f"\n📍 Using addresses:")
        print(f"   Origin: ID {origin['id']} - {origin['city']}, {origin['state']}")
        print(f"   Terminal ID: {origin.get('terminal_address_id')}")
        print(f"   Dest: ID {dest['id']} - {dest['city']}, {dest['state']}")
        print(f"   Terminal ID: {dest.get('terminal_address_id')}")
    else:
        print(f"❌ Failed: {response.status_code}")
        return 1
    
    # Test 4: Get Rates
    print_header("TEST 4: Get Shipping Rates")
    
    rate_data = {
        "origin_address_id": origin['id'],
        "destination_address_id": dest['id'],
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
    
    print(f"💰 Requesting rates...")
    print(f"   From: {origin['city']} → To: {dest['city']}")
    print(f"   Weight: 1.0 kg, Value: NGN 10,000")
    print()
    
    start = time.time()
    response = requests.post(
        f"{BASE_URL}/api/shipping/rates",
        headers=headers,
        json=rate_data,
        timeout=60
    )
    elapsed = time.time() - start
    
    print(f"⏱️  Response time: {elapsed:.1f}s")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()["data"]
        rates = data["rates"]
        
        print(f"\n✅ SUCCESS! Got {len(rates)} rates")
        print(f"\n📋 Available Rates:")
        
        for i, rate in enumerate(rates[:5], 1):
            carrier = rate.get('carrier_name', 'Unknown')
            amount = rate.get('amount', 0)
            currency = rate.get('currency', 'NGN')
            delivery = rate.get('delivery_time', 'N/A')
            
            print(f"\n   {i}. {carrier}")
            print(f"      Rate: {currency} {amount:,.2f}")
            print(f"      Delivery: {delivery}")
        
        print_header("🎉 ALL TESTS PASSED!")
        print("Phase 4 is COMPLETE and WORKING!")
        print("\n✅ What's working:")
        print("   1. Carrier management (39 carriers)")
        print("   2. Packaging management")
        print("   3. Address sync to Terminal")
        print("   4. Multi-carrier rate fetching")
        print("\n🚀 Ready for Phase 5: Shipment Creation")
        return 0
    else:
        print(f"\n❌ Failed to get rates")
        print(f"Response: {response.text}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
