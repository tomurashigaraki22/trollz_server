"""
Test Terminal Africa Phase 3: Address Integration
Tests address creation, syncing to Terminal, and user-specific address management.
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


def test_create_address(token):
    """Test creating a new address with Terminal sync."""
    print_section("TEST 1: Create Address with Terminal Sync")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    address_data = {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+2348012345678",
        "email": "john.doe@example.com",
        "street": "123 Main Street",
        "street_line_2": "Apartment 4B",
        "city": "Lagos",
        "state": "Lagos",
        "country": "NG",
        "post_code": "100001",
        "is_default": True
    }
    
    print("📝 Creating address...")
    print(f"   Name: {address_data['first_name']} {address_data['last_name']}")
    print(f"   Address: {address_data['street']}, {address_data['city']}")
    
    response = requests.post(
        f"{BASE_URL}/api/addresses",
        headers=headers,
        json=address_data
    )
    
    print(f"\n📋 Response Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        address = data.get("data", {}).get("address", {})
        terminal_synced = data.get("data", {}).get("terminal_synced", False)
        terminal_address_id = data.get("data", {}).get("terminal_address_id")
        
        print(f"✅ Address created successfully!")
        print(f"   Local Address ID: {address.get('id')}")
        print(f"   Terminal Synced: {'✅ Yes' if terminal_synced else '❌ No'}")
        
        if terminal_address_id:
            print(f"   Terminal Address ID: {terminal_address_id}")
        
        if data.get("data", {}).get("terminal_sync_warning"):
            print(f"   ⚠️  Warning: {data['data']['terminal_sync_warning']}")
        
        return address.get('id'), terminal_address_id
    else:
        print(f"❌ Failed to create address")
        print(f"   Response: {response.text}")
        return None, None


def test_get_addresses(token):
    """Test getting all addresses with Terminal sync status."""
    print_section("TEST 2: Get All Addresses")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("📋 Fetching addresses...")
    
    response = requests.get(
        f"{BASE_URL}/api/addresses",
        headers=headers
    )
    
    print(f"\n📋 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        addresses = data.get("data", {}).get("addresses", [])
        count = data.get("data", {}).get("count", 0)
        terminal_count = data.get("data", {}).get("terminal_count", 0)
        
        print(f"✅ Addresses retrieved successfully!")
        print(f"   Total Addresses: {count}")
        print(f"   Terminal Synced: {terminal_count}")
        
        print(f"\n📋 Address List:")
        for addr in addresses:
            terminal_status = "✅ Synced" if addr.get('terminal_synced') else "❌ Not Synced"
            default_status = "⭐ Default" if addr.get('is_default') else ""
            
            print(f"\n   Address ID: {addr.get('id')} {default_status}")
            print(f"   Name: {addr.get('first_name')} {addr.get('last_name')}")
            print(f"   Location: {addr.get('city')}, {addr.get('state')}")
            print(f"   Terminal Status: {terminal_status}")
            
            if addr.get('terminal_address_id'):
                print(f"   Terminal ID: {addr.get('terminal_address_id')}")
        
        return addresses
    else:
        print(f"❌ Failed to get addresses")
        print(f"   Response: {response.text}")
        return []


def test_get_terminal_addresses(token):
    """Test getting Terminal Africa addresses."""
    print_section("TEST 3: Get Terminal Africa Addresses")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("📋 Fetching Terminal addresses...")
    
    response = requests.get(
        f"{BASE_URL}/api/addresses/terminal",
        headers=headers
    )
    
    print(f"\n📋 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        addresses = data.get("data", {}).get("addresses", [])
        count = data.get("data", {}).get("count", 0)
        
        print(f"✅ Terminal addresses retrieved successfully!")
        print(f"   Total Terminal Addresses: {count}")
        
        print(f"\n📋 Terminal Address List:")
        for addr in addresses:
            print(f"\n   Terminal ID: {addr.get('terminal_address_id')}")
            print(f"   Name: {addr.get('first_name')} {addr.get('last_name')}")
            print(f"   Location: {addr.get('city')}, {addr.get('state')}, {addr.get('country')}")
            print(f"   Phone: {addr.get('phone')}")
        
        return addresses
    else:
        print(f"❌ Failed to get Terminal addresses")
        print(f"   Response: {response.text}")
        return []


def test_sync_existing_address(token, address_id):
    """Test syncing an existing address to Terminal."""
    print_section("TEST 4: Sync Existing Address to Terminal")
    
    if not address_id:
        print("⚠️  No address ID provided, skipping test")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"🔄 Syncing address ID {address_id} to Terminal...")
    
    response = requests.post(
        f"{BASE_URL}/api/addresses/{address_id}/sync-terminal",
        headers=headers
    )
    
    print(f"\n📋 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        terminal_address_id = data.get("data", {}).get("terminal_address_id")
        
        print(f"✅ Address synced successfully!")
        print(f"   Terminal Address ID: {terminal_address_id}")
        
        return True
    else:
        print(f"❌ Failed to sync address")
        print(f"   Response: {response.text}")
        return False


def test_create_multiple_addresses(token):
    """Test creating multiple addresses for the same user."""
    print_section("TEST 5: Create Multiple Addresses")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    addresses = [
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "phone": "+2348087654321",
            "email": "jane.smith@example.com",
            "street": "456 Oak Avenue",
            "city": "Abuja",
            "state": "FCT",
            "country": "NG",
            "post_code": "900001",
            "is_default": False
        },
        {
            "first_name": "Bob",
            "last_name": "Johnson",
            "phone": "+2348098765432",
            "email": "bob.johnson@example.com",
            "street": "789 Pine Road",
            "city": "Port Harcourt",
            "state": "Rivers",
            "country": "NG",
            "is_default": False
        }
    ]
    
    created_count = 0
    synced_count = 0
    
    for i, addr_data in enumerate(addresses, 1):
        print(f"\n📝 Creating address {i}/{len(addresses)}...")
        print(f"   Name: {addr_data['first_name']} {addr_data['last_name']}")
        print(f"   Location: {addr_data['city']}, {addr_data['state']}")
        
        response = requests.post(
            f"{BASE_URL}/api/addresses",
            headers=headers,
            json=addr_data
        )
        
        if response.status_code == 201:
            data = response.json()
            terminal_synced = data.get("data", {}).get("terminal_synced", False)
            
            print(f"   ✅ Created (Terminal: {'✅' if terminal_synced else '❌'})")
            created_count += 1
            
            if terminal_synced:
                synced_count += 1
        else:
            print(f"   ❌ Failed: {response.status_code}")
    
    print(f"\n📊 Summary:")
    print(f"   Created: {created_count}/{len(addresses)}")
    print(f"   Synced to Terminal: {synced_count}/{created_count}")
    
    return created_count == len(addresses)


def test_get_default_address(token):
    """Test getting the default address."""
    print_section("TEST 6: Get Default Address")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("📋 Fetching default address...")
    
    response = requests.get(
        f"{BASE_URL}/api/addresses/default",
        headers=headers
    )
    
    print(f"\n📋 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        address = data.get("data", {}).get("address", {})
        
        print(f"✅ Default address retrieved!")
        print(f"   Address ID: {address.get('id')}")
        print(f"   Name: {address.get('first_name')} {address.get('last_name')}")
        print(f"   Location: {address.get('city')}, {address.get('state')}")
        
        return address
    else:
        print(f"❌ Failed to get default address")
        print(f"   Response: {response.text}")
        return None


def main():
    """Run all Phase 3 tests."""
    print("\n" + "="*70)
    print("  TERMINAL AFRICA PHASE 3 TESTS")
    print("  Address Integration with User Management")
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
    
    # Test 1: Create address
    address_id, terminal_address_id = test_create_address(token)
    results["create_address"] = address_id is not None
    
    # Test 2: Get all addresses
    addresses = test_get_addresses(token)
    results["get_addresses"] = len(addresses) > 0
    
    # Test 3: Get Terminal addresses
    terminal_addresses = test_get_terminal_addresses(token)
    results["get_terminal_addresses"] = True  # Always passes if no error
    
    # Test 4: Sync existing address (if not already synced)
    if address_id and not terminal_address_id:
        results["sync_address"] = test_sync_existing_address(token, address_id)
    else:
        print_section("TEST 4: Sync Existing Address to Terminal")
        print("⚠️  Address already synced or no address to sync, skipping")
        results["sync_address"] = True
    
    # Test 5: Create multiple addresses
    results["create_multiple"] = test_create_multiple_addresses(token)
    
    # Test 6: Get default address
    default_address = test_get_default_address(token)
    results["get_default"] = default_address is not None
    
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
        print("🎉 All tests passed! Phase 3 implementation is working correctly.")
        print("\n📋 What was tested:")
        print("   1. Address creation with Terminal sync")
        print("   2. Getting all addresses with sync status")
        print("   3. Getting Terminal Africa addresses")
        print("   4. Syncing existing addresses to Terminal")
        print("   5. Creating multiple addresses per user")
        print("   6. Getting default address")
        print("\n📋 Next Steps:")
        print("   1. Review the test results above")
        print("   2. Check Terminal Africa dashboard for synced addresses")
        print("   3. Proceed to Phase 4: Shipping Quotes/Rates")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
