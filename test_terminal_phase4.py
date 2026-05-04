"""
Test Terminal Africa Phase 4: Shipping Quotes/Rates
Tests carrier listing, packaging management, and multi-carrier rate fetching.
"""

import requests
import json
import sys


# Configuration
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


def login_user(email, password):
    """Login and get JWT token."""
    print(f"🔐 Logging in as {email}...")
    
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": email, "password": password}
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("data", {}).get("token")
        user = data.get("data", {}).get("user", {})
        print(f"✅ Logged in successfully")
        print(f"   User ID: {user.get('id')}")
        print(f"   Name: {user.get('first_name')} {user.get('last_name')}")
        print(f"   Email: {user.get('email')}")
        return token, user
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None, None


def test_get_carriers(token):
    """Test getting available carriers from Terminal Africa."""
    print_section("TEST 1: Get Available Carriers")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("🚚 Fetching carriers...")
    
    response = requests.get(
        f"{BASE_URL}/api/shipping/carriers",
        headers=headers
    )
    
    print(f"\n📋 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        carriers = data.get("data", {}).get("carriers", [])
        count = data.get("data", {}).get("count", 0)
        active_count = data.get("data", {}).get("active_count", 0)
        
        print(f"✅ Carriers retrieved successfully!")
        print(f"   Total Carriers: {count}")
        print(f"   Active Carriers: {active_count}")
        print(f"   Inactive Carriers: {count - active_count}")
        
        # Display first 10 carriers
        print(f"\n📋 Sample Carriers (showing first 10):")
        for i, carrier in enumerate(carriers[:10], 1):
            name = carrier.get('name', 'Unknown')
            carrier_id = carrier.get('carrier_id', carrier.get('id', 'N/A'))
            active = carrier.get('active', False)
            
            services = []
            if carrier.get('domestic'):
                services.append("Domestic")
            if carrier.get('regional'):
                services.append("Regional")
            if carrier.get('international'):
                services.append("International")
            
            status = "✅" if active else "❌"
            print(f"\n   {i}. {name} {status}")
            print(f"      ID: {carrier_id}")
            print(f"      Services: {', '.join(services) if services else 'None'}")
        
        return carriers
    else:
        print(f"❌ Failed to get carriers")
        print(f"   Response: {response.text}")
        return []


def test_get_active_carriers(token):
    """Test filtering active carriers only."""
    print_section("TEST 2: Get Active Carriers Only")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("🚚 Fetching active carriers...")
    
    response = requests.get(
        f"{BASE_URL}/api/shipping/carriers?active=true",
        headers=headers
    )
    
    print(f"\n📋 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        carriers = data.get("data", {}).get("carriers", [])
        count = data.get("data", {}).get("count", 0)
        
        print(f"✅ Active carriers retrieved successfully!")
        print(f"   Active Carriers: {count}")
        
        # Verify all are active
        all_active = all(c.get('active', False) for c in carriers)
        print(f"   All Active: {'✅ Yes' if all_active else '❌ No'}")
        
        return carriers
    else:
        print(f"❌ Failed to get active carriers")
        print(f"   Response: {response.text}")
        return []


def test_get_packaging(token):
    """Test getting packaging options."""
    print_section("TEST 3: Get Packaging Options")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("📦 Fetching packaging options...")
    
    response = requests.get(
        f"{BASE_URL}/api/shipping/packaging",
        headers=headers
    )
    
    print(f"\n📋 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        packaging = data.get("data", {}).get("packaging", [])
        count = data.get("data", {}).get("count", 0)
        
        print(f"✅ Packaging options retrieved successfully!")
        print(f"   Total Packaging Options: {count}")
        
        # Display packaging options
        print(f"\n📋 Packaging Options:")
        for i, pkg in enumerate(packaging[:10], 1):
            name = pkg.get('name', 'Unknown')
            pkg_type = pkg.get('type', 'N/A')
            length = pkg.get('length', 0)
            width = pkg.get('width', 0)
            height = pkg.get('height', 0)
            weight = pkg.get('weight', 0)
            size_unit = pkg.get('size_unit', 'cm')
            weight_unit = pkg.get('weight_unit', 'kg')
            
            print(f"\n   {i}. {name} ({pkg_type})")
            print(f"      Dimensions: {length}x{width}x{height} {size_unit}")
            print(f"      Weight: {weight} {weight_unit}")
        
        return packaging
    else:
        print(f"❌ Failed to get packaging")
        print(f"   Response: {response.text}")
        return []


def test_create_packaging(token):
    """Test creating a new packaging option."""
    print_section("TEST 4: Create Custom Packaging")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    packaging_data = {
        "name": "Test Small Box",
        "type": "box",
        "length": 20,
        "width": 15,
        "height": 10,
        "weight": 0.5,
        "size_unit": "cm",
        "weight_unit": "kg"
    }
    
    print("📦 Creating custom packaging...")
    print(f"   Name: {packaging_data['name']}")
    print(f"   Type: {packaging_data['type']}")
    print(f"   Dimensions: {packaging_data['length']}x{packaging_data['width']}x{packaging_data['height']} cm")
    print(f"   Weight: {packaging_data['weight']} kg")
    
    response = requests.post(
        f"{BASE_URL}/api/shipping/packaging",
        headers=headers,
        json=packaging_data
    )
    
    print(f"\n📋 Response Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        packaging = data.get("data", {}).get("packaging", {})
        
        print(f"✅ Packaging created successfully!")
        print(f"   Packaging ID: {packaging.get('packaging_id', packaging.get('id', 'N/A'))}")
        print(f"   Name: {packaging.get('name')}")
        
        return packaging
    else:
        print(f"❌ Failed to create packaging")
        print(f"   Response: {response.text}")
        return None


def test_get_shipping_rates(token):
    """Test getting shipping rates from multiple carriers."""
    print_section("TEST 5: Get Shipping Rates")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # First, get user's addresses
    print("📋 Fetching user addresses...")
    addr_response = requests.get(
        f"{BASE_URL}/api/addresses",
        headers=headers
    )
    
    if addr_response.status_code != 200:
        print(f"❌ Failed to get addresses: {addr_response.status_code}")
        return False
    
    addresses = addr_response.json().get("data", {}).get("addresses", [])
    
    if len(addresses) < 2:
        print(f"⚠️  Need at least 2 addresses to test rates (found {len(addresses)})")
        print("   Please create more addresses first")
        return False
    
    # Use first two addresses
    origin_id = addresses[0]['id']
    dest_id = addresses[1]['id']
    
    print(f"   Origin: {addresses[0]['city']}, {addresses[0]['state']}")
    print(f"   Destination: {addresses[1]['city']}, {addresses[1]['state']}")
    
    # Check if addresses are synced to Terminal
    origin_synced = addresses[0].get('terminal_synced', False)
    dest_synced = addresses[1].get('terminal_synced', False)
    
    if not origin_synced or not dest_synced:
        print(f"\n⚠️  Addresses not synced to Terminal:")
        print(f"   Origin Synced: {'✅' if origin_synced else '❌'}")
        print(f"   Destination Synced: {'✅' if dest_synced else '❌'}")
        print("   Please sync addresses first using Phase 3 endpoints")
        return False
    
    # Prepare rate request
    rate_data = {
        "origin_address_id": origin_id,
        "destination_address_id": dest_id,
        "items": [
            {
                "name": "Test Product",
                "quantity": 2,
                "value": 15000,
                "weight": 2.5,
                "description": "Test product for rate calculation"
            }
        ],
        "currency": "NGN"
    }
    
    print(f"\n💰 Fetching shipping rates...")
    print(f"   Items: {len(rate_data['items'])}")
    print(f"   Total Weight: {sum(item['weight'] * item['quantity'] for item in rate_data['items'])} kg")
    
    response = requests.post(
        f"{BASE_URL}/api/shipping/rates",
        headers=headers,
        json=rate_data
    )
    
    print(f"\n📋 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        rates = data.get("data", {}).get("rates", [])
        count = data.get("data", {}).get("count", 0)
        summary = data.get("data", {}).get("summary", {})
        
        print(f"✅ Shipping rates retrieved successfully!")
        print(f"   Available Rates: {count}")
        print(f"   Total Weight: {summary.get('total_weight')} kg")
        print(f"   Total Items: {summary.get('total_items')}")
        
        # Display rates
        if rates:
            print(f"\n📋 Available Rates:")
            for i, rate in enumerate(rates[:10], 1):
                carrier = rate.get('carrier', {})
                carrier_name = carrier.get('name', 'Unknown')
                amount = rate.get('amount', 0)
                currency = rate.get('currency', 'NGN')
                delivery_time = rate.get('delivery_time', 'N/A')
                
                print(f"\n   {i}. {carrier_name}")
                print(f"      Rate: {currency} {amount:,.2f}")
                print(f"      Delivery Time: {delivery_time}")
        else:
            print(f"\n⚠️  No rates available for this route")
        
        return True
    else:
        print(f"❌ Failed to get shipping rates")
        print(f"   Response: {response.text}")
        return False


def test_international_carriers(token):
    """Test filtering international carriers."""
    print_section("TEST 6: Get International Carriers")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("🌍 Fetching international carriers...")
    
    response = requests.get(
        f"{BASE_URL}/api/shipping/carriers?international=true&active=true",
        headers=headers
    )
    
    print(f"\n📋 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        carriers = data.get("data", {}).get("carriers", [])
        count = data.get("data", {}).get("count", 0)
        
        print(f"✅ International carriers retrieved successfully!")
        print(f"   International Carriers: {count}")
        
        # Display carriers
        print(f"\n📋 International Carriers:")
        for i, carrier in enumerate(carriers[:10], 1):
            name = carrier.get('name', 'Unknown')
            print(f"   {i}. {name}")
        
        return carriers
    else:
        print(f"❌ Failed to get international carriers")
        print(f"   Response: {response.text}")
        return []


def main():
    """Run all Phase 4 tests."""
    print("\n" + "="*70)
    print("  TERMINAL AFRICA PHASE 4 TESTS")
    print("  Shipping Quotes/Rates with Multi-Carrier Support")
    print("="*70)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print(f"\n✅ Server is running at {BASE_URL}")
    except:
        print(f"\n❌ Server is not running at {BASE_URL}")
        print("   Please start the server with: python app.py")
        return 1
    
    # Login
    print_section("USER AUTHENTICATION")
    token, user = login_user(TEST_USER["email"], TEST_USER["password"])
    
    if not token:
        print("\n❌ Authentication failed. Please check credentials.")
        print(f"   Expected user: {TEST_USER['email']}")
        print("   Make sure this user exists in the database.")
        return 1
    
    # Run tests
    results = {}
    
    # Test 1: Get all carriers
    carriers = test_get_carriers(token)
    results["get_carriers"] = len(carriers) > 0
    
    # Test 2: Get active carriers
    active_carriers = test_get_active_carriers(token)
    results["get_active_carriers"] = len(active_carriers) > 0
    
    # Test 3: Get packaging
    packaging = test_get_packaging(token)
    results["get_packaging"] = len(packaging) > 0
    
    # Test 4: Create packaging
    new_packaging = test_create_packaging(token)
    results["create_packaging"] = new_packaging is not None
    
    # Test 5: Get shipping rates
    results["get_rates"] = test_get_shipping_rates(token)
    
    # Test 6: Get international carriers
    intl_carriers = test_international_carriers(token)
    results["get_international_carriers"] = len(intl_carriers) > 0
    
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
        print("🎉 All tests passed! Phase 4 implementation is working correctly.")
        print("\n📋 What was tested:")
        print("   1. Getting all available carriers")
        print("   2. Filtering active carriers")
        print("   3. Getting packaging options")
        print("   4. Creating custom packaging")
        print("   5. Getting shipping rates from multiple carriers")
        print("   6. Filtering international carriers")
        print("\n📋 Next Steps:")
        print("   1. Review the test results above")
        print("   2. Check Terminal Africa dashboard for created resources")
        print("   3. Proceed to Phase 5: Order & Shipment Creation")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
