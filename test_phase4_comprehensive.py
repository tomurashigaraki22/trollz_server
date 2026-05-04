"""
Comprehensive Phase 4 Test - Terminal Africa Integration
Tests all Phase 4 endpoints with proper test environment setup.
"""

import requests
import sys
import json
import time


BASE_URL = "http://localhost:4500"
TEST_USER = {
    "email": "devtomiwa9@gmail.com",
    "password": "Pityboy@22"
}


def print_header(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def print_section(title):
    print("\n" + "-"*80)
    print(f"  {title}")
    print("-"*80)


def login():
    print("🔐 Logging in...")
    response = requests.post(f"{BASE_URL}/api/auth/login", json=TEST_USER)
    
    if response.status_code == 200:
        token = response.json()["data"]["token"]
        print("✅ Logged in successfully\n")
        return token
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None


def test_carriers(headers):
    """Test 1: Get carriers from Terminal Africa"""
    print_section("TEST 1: Get Carriers")
    
    response = requests.get(f"{BASE_URL}/api/shipping/carriers", headers=headers)
    
    if response.status_code == 200:
        data = response.json()["data"]
        carriers = data["carriers"]
        
        print(f"✅ SUCCESS!")
        print(f"   Total Carriers: {data['count']}")
        print(f"   Active Carriers: {data['active_count']}")
        
        # Show first 5 carriers
        print(f"\n📋 Sample Carriers:")
        for i, carrier in enumerate(carriers[:5], 1):
            name = carrier.get('name', 'Unknown')
            active = carrier.get('active', False)
            status = "✅ Active" if active else "❌ Inactive"
            print(f"   {i}. {name} - {status}")
        
        return True
    else:
        print(f"❌ FAILED: {response.status_code}")
        print(f"Response: {response.text}")
        return False


def test_packaging(headers):
    """Test 2: Get packaging options"""
    print_section("TEST 2: Get Packaging Options")
    
    response = requests.get(f"{BASE_URL}/api/shipping/packaging", headers=headers)
    
    if response.status_code == 200:
        data = response.json()["data"]
        packaging = data["packaging"]
        
        print(f"✅ SUCCESS!")
        print(f"   Total Packaging Options: {data['count']}")
        
        # Show first 3 packaging options
        print(f"\n📦 Sample Packaging:")
        for i, pkg in enumerate(packaging[:3], 1):
            name = pkg.get('name', 'Unknown')
            pkg_type = pkg.get('type', 'Unknown')
            dimensions = f"{pkg.get('length')}x{pkg.get('width')}x{pkg.get('height')} {pkg.get('size_unit', 'cm')}"
            weight = f"{pkg.get('weight')} {pkg.get('weight_unit', 'kg')}"
            print(f"   {i}. {name} ({pkg_type})")
            print(f"      Dimensions: {dimensions}")
            print(f"      Weight: {weight}")
        
        return True
    else:
        print(f"❌ FAILED: {response.status_code}")
        print(f"Response: {response.text}")
        return False


def test_create_packaging(headers):
    """Test 3: Create custom packaging"""
    print_section("TEST 3: Create Custom Packaging")
    
    packaging_data = {
        "name": "Test Box - Phase 4",
        "type": "box",
        "length": 30,
        "width": 20,
        "height": 15,
        "weight": 0.5,
        "size_unit": "cm",
        "weight_unit": "kg"
    }
    
    print(f"Creating packaging: {packaging_data['name']}")
    print(f"Dimensions: {packaging_data['length']}x{packaging_data['width']}x{packaging_data['height']} cm")
    
    response = requests.post(
        f"{BASE_URL}/api/shipping/packaging",
        headers=headers,
        json=packaging_data
    )
    
    if response.status_code == 201:
        data = response.json()["data"]
        packaging = data["packaging"]
        
        print(f"\n✅ SUCCESS!")
        print(f"   Packaging ID: {packaging.get('packaging_id')}")
        print(f"   Name: {packaging.get('name')}")
        print(f"   Type: {packaging.get('type')}")
        
        return packaging.get('packaging_id')
    else:
        print(f"❌ FAILED: {response.status_code}")
        print(f"Response: {response.text}")
        return None


def get_synced_addresses(headers):
    """Get addresses that are synced to Terminal"""
    print_section("TEST 4: Get Synced Addresses")
    
    response = requests.get(f"{BASE_URL}/api/addresses", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to get addresses: {response.status_code}")
        return None, None
    
    data = response.json()["data"]
    addresses = data["addresses"]
    
    # Filter synced addresses
    synced = [a for a in addresses if a.get('terminal_address_id')]
    
    # Filter for TEST environment addresses only (ID >= 10)
    # Addresses with ID < 10 are from LIVE environment and won't work with test API
    test_env_synced = [a for a in synced if a['id'] >= 10]
    
    print(f"📍 Addresses:")
    print(f"   Total: {len(addresses)}")
    print(f"   Synced to Terminal: {len(synced)}")
    print(f"   In TEST environment: {len(test_env_synced)}")
    
    if len(test_env_synced) >= 2:
        origin = test_env_synced[0]
        dest = test_env_synced[1]
        
        print(f"\n✅ Using TEST environment addresses:")
        print(f"   Origin: ID {origin['id']} - {origin['city']}, {origin['state']}")
        print(f"           Terminal ID: {origin['terminal_address_id']}")
        print(f"   Dest:   ID {dest['id']} - {dest['city']}, {dest['state']}")
        print(f"           Terminal ID: {dest['terminal_address_id']}")
        
        return origin, dest
    
    print(f"\n⚠️  Need at least 2 TEST environment addresses. Creating new ones...")
    return create_test_addresses(headers)


def create_test_addresses(headers):
    """Create 2 test addresses for testing"""
    print_section("Creating Test Addresses")
    
    test_addresses = [
        {
            "first_name": "Test",
            "last_name": "Origin",
            "phone": "+2348012345678",
            "email": "test.origin@test.com",
            "street": "123 Test Street",
            "city": "Lagos",
            "state": "Lagos",
            "country": "NG",
            "post_code": "100001"
        },
        {
            "first_name": "Test",
            "last_name": "Destination",
            "phone": "+2348087654321",
            "email": "test.dest@test.com",
            "street": "456 Test Avenue",
            "city": "Abuja",
            "state": "Abuja",
            "country": "NG",
            "post_code": "900001"
        }
    ]
    
    created = []
    
    for addr_data in test_addresses:
        print(f"\nCreating address: {addr_data['city']}, {addr_data['state']}")
        
        response = requests.post(
            f"{BASE_URL}/api/addresses",
            headers=headers,
            json=addr_data
        )
        
        if response.status_code == 201:
            data = response.json()["data"]
            address = data["address"]
            terminal_synced = data.get("terminal_synced", False)
            terminal_id = data.get("terminal_address_id")
            
            print(f"✅ Created: ID {address['id']}")
            print(f"   Terminal Synced: {'✅ Yes' if terminal_synced else '❌ No'}")
            
            if terminal_id:
                print(f"   Terminal ID: {terminal_id}")
                created.append(address)
            else:
                print(f"   ⚠️  Warning: Not synced to Terminal")
                if data.get("terminal_sync_warning"):
                    print(f"   Error: {data['terminal_sync_warning']}")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"Response: {response.text}")
    
    if len(created) >= 2:
        print(f"\n✅ Successfully created {len(created)} synced addresses")
        return created[0], created[1]
    else:
        print(f"\n❌ Failed to create enough synced addresses")
        return None, None


def test_create_parcel(headers, packaging_id=None):
    """Test 5: Create a parcel"""
    print_section("TEST 5: Create Parcel")
    
    # If no packaging_id provided, get one
    if not packaging_id:
        print("Getting packaging options...")
        response = requests.get(f"{BASE_URL}/api/shipping/packaging?per_page=1", headers=headers)
        if response.status_code == 200:
            packaging = response.json()["data"]["packaging"]
            if packaging:
                packaging_id = packaging[0].get('packaging_id')
                print(f"Using packaging: {packaging[0].get('name')} ({packaging_id})")
    
    if not packaging_id:
        print("❌ No packaging available")
        return None
    
    # Note: Parcel creation is done internally by the rates endpoint
    print("✅ Packaging ready for parcel creation")
    return packaging_id


def test_get_rates(headers, origin, dest):
    """Test 6: Get shipping rates"""
    print_section("TEST 6: Get Shipping Rates")
    
    rate_request = {
        "origin_address_id": origin['id'],
        "destination_address_id": dest['id'],
        "items": [
            {
                "name": "Test Product",
                "quantity": 1,
                "value": 10000,
                "weight": 1.0,
                "description": "Test product for Phase 4"
            }
        ],
        "currency": "NGN"
    }
    
    print(f"📦 Rate Request:")
    print(f"   Origin: {origin['city']}, {origin['state']} (ID: {origin['id']})")
    print(f"   Destination: {dest['city']}, {dest['state']} (ID: {dest['id']})")
    print(f"   Weight: 1.0 kg")
    print(f"   Value: NGN 10,000")
    print(f"\n⏳ Fetching rates (this may take 10-30 seconds)...")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/shipping/rates",
            headers=headers,
            json=rate_request,
            timeout=60
        )
        
        elapsed = time.time() - start_time
        
        print(f"⏱️  Response time: {elapsed:.1f}s")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()["data"]
            rates = data["rates"]
            summary = data["summary"]
            
            print(f"\n✅ SUCCESS! Got {len(rates)} rates")
            print(f"\n📊 Summary:")
            print(f"   Total Weight: {summary['total_weight']} kg")
            print(f"   Total Items: {summary['total_items']}")
            print(f"   Origin: {summary['origin']}")
            print(f"   Destination: {summary['destination']}")
            print(f"   Parcel ID: {data.get('parcel_id')}")
            
            if rates:
                print(f"\n💰 Available Rates:")
                for i, rate in enumerate(rates[:5], 1):
                    carrier = rate.get('carrier_name', rate.get('carrier', 'Unknown'))
                    amount = rate.get('amount', 0)
                    currency = rate.get('currency', 'NGN')
                    delivery = rate.get('delivery_time', rate.get('estimated_days', 'N/A'))
                    
                    print(f"\n   {i}. {carrier}")
                    print(f"      Rate: {currency} {amount:,.2f}")
                    print(f"      Delivery: {delivery}")
                
                return True
            else:
                print(f"\n⚠️  No rates returned")
                return False
        else:
            print(f"\n❌ FAILED")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"\n❌ Request timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def main():
    print_header("TERMINAL AFRICA PHASE 4 - COMPREHENSIVE TEST")
    print("Testing all Phase 4 functionality with TEST environment")
    print("Base URL: http://localhost:4500")
    print("Terminal Environment: TEST (sandbox.terminal.africa)")
    
    # Login
    token = login()
    if not token:
        print("\n❌ Cannot proceed without authentication")
        return 1
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Track results
    results = {
        "carriers": False,
        "packaging_list": False,
        "packaging_create": False,
        "addresses": False,
        "rates": False
    }
    
    # Test 1: Carriers
    results["carriers"] = test_carriers(headers)
    
    # Test 2: Packaging List
    results["packaging_list"] = test_packaging(headers)
    
    # Test 3: Create Packaging
    packaging_id = test_create_packaging(headers)
    results["packaging_create"] = packaging_id is not None
    
    # Test 4: Get/Create Addresses
    origin, dest = get_synced_addresses(headers)
    results["addresses"] = origin is not None and dest is not None
    
    if not results["addresses"]:
        print("\n❌ Cannot proceed without synced addresses")
        print_summary(results)
        return 1
    
    # Test 5: Get Rates (includes parcel creation)
    results["rates"] = test_get_rates(headers, origin, dest)
    
    # Print summary
    print_summary(results)
    
    # Return exit code
    return 0 if all(results.values()) else 1


def print_summary(results):
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"Results: {passed}/{total} tests passed\n")
    
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {test.replace('_', ' ').title()}")
    
    if all(results.values()):
        print("\n" + "="*80)
        print("🎉 ALL TESTS PASSED! PHASE 4 IS COMPLETE!")
        print("="*80)
        print("\n✅ What's Working:")
        print("   1. Carrier Management - Get available carriers")
        print("   2. Packaging Management - List and create packaging")
        print("   3. Address Sync - Addresses synced to Terminal Africa")
        print("   4. Parcel Creation - Parcels created with items")
        print("   5. Multi-Carrier Rates - Get rates from multiple carriers")
        print("\n🚀 Ready for Phase 5: Shipment Creation & Tracking")
    else:
        print("\n" + "="*80)
        print("⚠️  SOME TESTS FAILED")
        print("="*80)
        print("\nPlease review the failed tests above.")


if __name__ == "__main__":
    sys.exit(main())
