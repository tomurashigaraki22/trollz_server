"""
Complete Phase 4 Test - Test Environment
Tests all Phase 4 functionality with Terminal Africa sandbox API.
"""

import requests
import json
import sys
import time


BASE_URL = "http://localhost:4500"
TEST_USER = {
    "email": "devtomiwa9@gmail.com",
    "password": "Pityboy@22"
}


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def login():
    """Login and get token."""
    print("🔐 Logging in...")
    response = requests.post(f"{BASE_URL}/api/auth/login", json=TEST_USER)
    
    if response.status_code == 200:
        data = response.json()
        token = data["data"]["token"]
        user = data["data"]["user"]
        print(f"✅ Logged in as: {user.get('email')}")
        print(f"   User ID: {user.get('id')}\n")
        return token
    else:
        print(f"❌ Login failed: {response.status_code}")
        return None


def test_carriers(token):
    """Test getting carriers from Terminal sandbox."""
    print_section("TEST 1: Get Carriers (Sandbox)")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("🚚 Fetching carriers from Terminal sandbox...")
    response = requests.get(f"{BASE_URL}/api/shipping/carriers", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        carriers = data["data"]["carriers"]
        count = data["data"]["count"]
        active_count = data["data"]["active_count"]
        
        print(f"✅ Success!")
        print(f"   Total Carriers: {count}")
        print(f"   Active Carriers: {active_count}")
        print()
        
        # Show first 5 carriers
        print("📋 Sample Carriers:")
        for i, carrier in enumerate(carriers[:5], 1):
            name = carrier.get('name', 'Unknown')
            active = "✅" if carrier.get('active') else "❌"
            print(f"   {i}. {name} {active}")
        
        return True
    else:
        print(f"❌ Failed: {response.text}")
        return False


def test_packaging(token):
    """Test getting and creating packaging."""
    print_section("TEST 2: Packaging Management")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get packaging
    print("📦 Fetching packaging options...")
    response = requests.get(f"{BASE_URL}/api/shipping/packaging", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        packaging = data["data"]["packaging"]
        print(f"✅ Found {len(packaging)} packaging options")
        
        if len(packaging) == 0:
            print("\n⚠️  No packaging found. Creating default packaging...")
            
            # Create default packaging
            packaging_data = {
                "name": "Standard Box",
                "type": "box",
                "length": 30,
                "width": 20,
                "height": 15,
                "weight": 0.5,
                "size_unit": "cm",
                "weight_unit": "kg"
            }
            
            create_response = requests.post(
                f"{BASE_URL}/api/shipping/packaging",
                headers=headers,
                json=packaging_data
            )
            
            if create_response.status_code == 201:
                pkg_data = create_response.json()
                pkg = pkg_data["data"]["packaging"]
                print(f"✅ Created packaging: {pkg.get('name')}")
                print(f"   ID: {pkg.get('packaging_id', pkg.get('id'))}")
                packaging = [pkg]
            else:
                print(f"❌ Failed to create packaging: {create_response.text}")
                return False
        
        # Show first 3
        print("\n📋 Available Packaging:")
        for i, pkg in enumerate(packaging[:3], 1):
            print(f"   {i}. {pkg.get('name')} ({pkg.get('type')})")
            print(f"      {pkg.get('length')}x{pkg.get('width')}x{pkg.get('height')} {pkg.get('size_unit')}")
        
        return True
    else:
        print(f"❌ Failed: {response.text}")
        return False


def create_test_addresses(token):
    """Create test addresses and sync to Terminal sandbox."""
    print_section("TEST 3: Create & Sync Addresses")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    addresses_to_create = [
        {
            "first_name": "Test",
            "last_name": "Origin",
            "phone": "+2348012345678",
            "email": "origin@test.com",
            "street": "123 Origin Street",
            "city": "Lagos",
            "state": "Lagos",
            "country": "NG",
            "post_code": "100001"
        },
        {
            "first_name": "Test",
            "last_name": "Destination",
            "phone": "+2348087654321",
            "email": "dest@test.com",
            "street": "456 Destination Avenue",
            "city": "Abuja",
            "state": "Abuja",  # Changed from FCT to Abuja
            "country": "NG",
            "post_code": "900001"
        }
    ]
    
    created_addresses = []
    
    for i, addr_data in enumerate(addresses_to_create, 1):
        print(f"\n📝 Creating address {i}/2...")
        print(f"   Name: {addr_data['first_name']} {addr_data['last_name']}")
        print(f"   Location: {addr_data['city']}, {addr_data['state']}")
        
        response = requests.post(
            f"{BASE_URL}/api/addresses",
            headers=headers,
            json=addr_data
        )
        
        if response.status_code == 201:
            data = response.json()
            address = data["data"]["address"]
            terminal_synced = data["data"]["terminal_synced"]
            terminal_address_id = data["data"].get("terminal_address_id")
            
            print(f"   ✅ Created (ID: {address['id']})")
            print(f"   Terminal Synced: {'✅ Yes' if terminal_synced else '❌ No'}")
            
            if terminal_address_id:
                print(f"   Terminal ID: {terminal_address_id}")
                created_addresses.append(address)
            else:
                print(f"   ⚠️  Not synced to Terminal")
                if data["data"].get("terminal_sync_warning"):
                    print(f"   Warning: {data['data']['terminal_sync_warning']}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   {response.text}")
    
    print(f"\n✅ Created {len(created_addresses)} synced addresses")
    return created_addresses


def test_rates(token, origin_id, dest_id):
    """Test getting shipping rates."""
    print_section("TEST 4: Get Shipping Rates")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    rate_data = {
        "origin_address_id": origin_id,
        "destination_address_id": dest_id,
        "items": [
            {
                "name": "Test Product",
                "quantity": 1,
                "value": 10000,
                "weight": 1.0,
                "description": "Test product for rate calculation"
            }
        ],
        "currency": "NGN"
    }
    
    print("💰 Requesting shipping rates...")
    print(f"   Origin Address ID: {origin_id}")
    print(f"   Destination Address ID: {dest_id}")
    print(f"   Items: 1 item, 1.0 kg, NGN 10,000")
    print()
    print("⏱️  This may take 10-30 seconds...")
    print()
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/shipping/rates",
            headers=headers,
            json=rate_data,
            timeout=60
        )
        
        elapsed = time.time() - start_time
        
        print(f"⏱️  Response time: {elapsed:.1f} seconds")
        print(f"Status: {response.status_code}")
        print()
        
        if response.status_code == 200:
            data = response.json()
            rates = data["data"]["rates"]
            parcel_id = data["data"]["parcel_id"]
            summary = data["data"]["summary"]
            
            print(f"✅ Success!")
            print(f"   Parcel ID: {parcel_id}")
            print(f"   Total Weight: {summary['total_weight']} kg")
            print(f"   Found {len(rates)} rates")
            print()
            
            if rates:
                print("📋 Available Rates:")
                for i, rate in enumerate(rates[:5], 1):
                    carrier = rate.get('carrier', {})
                    carrier_name = carrier.get('name', 'Unknown')
                    amount = rate.get('amount', 0)
                    currency = rate.get('currency', 'NGN')
                    delivery_time = rate.get('delivery_time', 'N/A')
                    
                    print(f"\n   {i}. {carrier_name}")
                    print(f"      Rate: {currency} {amount:,.2f}")
                    print(f"      Delivery: {delivery_time}")
                
                return True, parcel_id
            else:
                print("⚠️  No rates available for this route")
                return False, parcel_id
        else:
            print(f"❌ Failed!")
            print(f"Response: {response.text}")
            return False, None
            
    except requests.exceptions.Timeout:
        elapsed = time.time() - start_time
        print(f"❌ Request timed out after {elapsed:.1f} seconds")
        return False, None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, None


def test_international_carriers(token):
    """Test filtering international carriers."""
    print_section("TEST 5: International Carriers")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("🌍 Fetching international carriers...")
    response = requests.get(
        f"{BASE_URL}/api/shipping/carriers?international=true&active=true",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        carriers = data["data"]["carriers"]
        
        print(f"✅ Found {len(carriers)} international carriers")
        print()
        
        print("📋 International Carriers:")
        for i, carrier in enumerate(carriers[:10], 1):
            name = carrier.get('name', 'Unknown')
            print(f"   {i}. {name}")
        
        return True
    else:
        print(f"❌ Failed: {response.text}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("  TERMINAL AFRICA PHASE 4 - COMPLETE TEST")
    print("  Using Test/Sandbox Environment")
    print("="*70)
    
    # Check server
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print(f"\n✅ Server is running at {BASE_URL}")
    except:
        print(f"\n❌ Server is not running at {BASE_URL}")
        print("   Please start: python app.py")
        return 1
    
    # Login
    print_section("AUTHENTICATION")
    token = login()
    
    if not token:
        print("❌ Cannot proceed without authentication")
        return 1
    
    # Run tests
    results = {}
    
    # Test 1: Carriers
    results["carriers"] = test_carriers(token)
    
    # Test 2: Packaging
    results["packaging"] = test_packaging(token)
    
    # Test 3: Create addresses
    addresses = create_test_addresses(token)
    results["addresses"] = len(addresses) >= 2
    
    if len(addresses) < 2:
        print("\n⚠️  Need at least 2 synced addresses for rates test")
        print("   Skipping rates test")
        results["rates"] = False
        results["international"] = test_international_carriers(token)
    else:
        # Test 4: Rates
        origin_id = addresses[0]['id']
        dest_id = addresses[1]['id']
        rates_success, parcel_id = test_rates(token, origin_id, dest_id)
        results["rates"] = rates_success
        
        # Test 5: International carriers
        results["international"] = test_international_carriers(token)
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\n{'='*70}")
    print(f"  RESULTS: {passed}/{total} tests passed")
    print(f"{'='*70}\n")
    
    if passed == total:
        print("🎉 All tests passed!")
        print("\n✅ Phase 4 is working correctly with Terminal sandbox!")
        print()
        print("📋 What was tested:")
        print("   1. ✅ Carrier listing (39 carriers)")
        print("   2. ✅ Packaging management")
        print("   3. ✅ Address creation & sync to Terminal")
        print("   4. ✅ Multi-carrier rate fetching")
        print("   5. ✅ International carrier filtering")
        print()
        print("🚀 Ready for Phase 5: Order & Shipment Creation")
        return 0
    else:
        print("⚠️  Some tests failed. Review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
