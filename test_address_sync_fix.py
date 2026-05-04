"""
Test Address Sync Fix
Verify that addresses are properly synced to Terminal and terminal_address_id is stored.
"""

import requests
import json


BASE_URL = "http://localhost:4500"
TEST_USER = {
    "email": "devtomiwa9@gmail.com",
    "password": "Pityboy@22"
}


def login():
    """Login and get token."""
    print("🔐 Logging in...")
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=TEST_USER
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data["data"]["token"]
        print("✅ Logged in successfully\n")
        return token
    else:
        print(f"❌ Login failed: {response.status_code}")
        return None


def test_create_address_with_sync(token):
    """Test creating an address and verify it syncs to Terminal."""
    print("="*70)
    print("TEST: Create Address with Terminal Sync")
    print("="*70)
    print()
    
    headers = {"Authorization": f"Bearer {token}"}
    
    address_data = {
        "first_name": "Test",
        "last_name": "User",
        "phone": "+2348012345678",
        "email": "test@example.com",
        "street": "123 Test Street",
        "city": "Lagos",
        "state": "Lagos",
        "country": "NG",
        "post_code": "100001",
        "is_default": False
    }
    
    print("📝 Creating address...")
    response = requests.post(
        f"{BASE_URL}/api/addresses",
        headers=headers,
        json=address_data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        address = data["data"]["address"]
        terminal_synced = data["data"]["terminal_synced"]
        terminal_address_id = data["data"].get("terminal_address_id")
        
        print(f"✅ Address created!")
        print(f"   Local ID: {address['id']}")
        print(f"   Terminal Synced: {'✅ Yes' if terminal_synced else '❌ No'}")
        
        if terminal_address_id:
            print(f"   Terminal Address ID: {terminal_address_id}")
            print(f"\n✅ SUCCESS: Address synced and terminal_address_id stored!")
            return address['id'], terminal_address_id
        else:
            print(f"\n⚠️  WARNING: Address created but not synced to Terminal")
            if data["data"].get("terminal_sync_warning"):
                print(f"   Error: {data['data']['terminal_sync_warning']}")
            return address['id'], None
    else:
        print(f"❌ Failed to create address")
        print(f"Response: {response.text}")
        return None, None


def test_get_addresses(token):
    """Test getting addresses and verify terminal_synced status."""
    print("\n" + "="*70)
    print("TEST: Get Addresses with Sync Status")
    print("="*70)
    print()
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("📋 Fetching addresses...")
    response = requests.get(
        f"{BASE_URL}/api/addresses",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        addresses = data["data"]["addresses"]
        count = data["data"]["count"]
        terminal_count = data["data"]["terminal_count"]
        
        print(f"✅ Addresses retrieved!")
        print(f"   Total: {count}")
        print(f"   Synced to Terminal: {terminal_count}")
        print()
        
        for addr in addresses:
            synced = addr.get('terminal_synced', False)
            terminal_id = addr.get('terminal_address_id')
            
            print(f"Address ID {addr['id']}:")
            print(f"  Name: {addr['first_name']} {addr['last_name']}")
            print(f"  Location: {addr['city']}, {addr['state']}")
            print(f"  Terminal Synced: {'✅ Yes' if synced else '❌ No'}")
            if terminal_id:
                print(f"  Terminal ID: {terminal_id}")
            print()
        
        return addresses
    else:
        print(f"❌ Failed to get addresses")
        print(f"Response: {response.text}")
        return []


def test_sync_existing_address(token, address_id):
    """Test syncing an existing address."""
    print("="*70)
    print(f"TEST: Sync Existing Address (ID: {address_id})")
    print("="*70)
    print()
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"🔄 Syncing address {address_id}...")
    response = requests.post(
        f"{BASE_URL}/api/addresses/{address_id}/sync-terminal",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        terminal_address_id = data["data"]["terminal_address_id"]
        
        print(f"✅ Address synced!")
        print(f"   Terminal Address ID: {terminal_address_id}")
        return terminal_address_id
    else:
        print(f"❌ Failed to sync address")
        print(f"Response: {response.text}")
        return None


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("  ADDRESS SYNC FIX VERIFICATION")
    print("="*70)
    print()
    
    # Login
    token = login()
    if not token:
        print("❌ Cannot proceed without authentication")
        return 1
    
    # Test 1: Create address with sync
    address_id, terminal_id = test_create_address_with_sync(token)
    
    # Test 2: Get addresses and verify sync status
    addresses = test_get_addresses(token)
    
    # Test 3: If we have an unsynced address, sync it
    unsynced_addresses = [a for a in addresses if not a.get('terminal_synced')]
    if unsynced_addresses:
        print("="*70)
        print(f"Found {len(unsynced_addresses)} unsynced address(es)")
        print("="*70)
        print()
        
        for addr in unsynced_addresses[:1]:  # Sync first one only
            test_sync_existing_address(token, addr['id'])
    
    # Final verification
    print("\n" + "="*70)
    print("  FINAL VERIFICATION")
    print("="*70)
    print()
    
    addresses = test_get_addresses(token)
    synced_count = sum(1 for a in addresses if a.get('terminal_synced'))
    
    print("="*70)
    print(f"  RESULT: {synced_count}/{len(addresses)} addresses synced")
    print("="*70)
    print()
    
    if synced_count >= 2:
        print("✅ SUCCESS: At least 2 addresses are synced to Terminal!")
        print("   You can now test Phase 4 rates endpoint.")
        return 0
    else:
        print("⚠️  WARNING: Less than 2 addresses synced.")
        print("   Create more addresses or sync existing ones.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
