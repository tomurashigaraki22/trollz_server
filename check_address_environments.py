"""
Check which addresses are in which Terminal environment
"""

import requests
import sys


BASE_URL = "http://localhost:4500"
TEST_USER = {
    "email": "devtomiwa9@gmail.com",
    "password": "Pityboy@22"
}


def login():
    response = requests.post(f"{BASE_URL}/api/auth/login", json=TEST_USER)
    if response.status_code == 200:
        return response.json()["data"]["token"]
    return None


def main():
    print("="*80)
    print("  ADDRESS ENVIRONMENT CHECK")
    print("="*80)
    print()
    
    token = login()
    if not token:
        print("❌ Login failed")
        return 1
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get all addresses
    response = requests.get(f"{BASE_URL}/api/addresses", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to get addresses: {response.status_code}")
        return 1
    
    addresses = response.json()["data"]["addresses"]
    
    print(f"Total Addresses: {len(addresses)}\n")
    
    # Addresses created after switching to test environment
    # Based on the summary, addresses 10-15 were created after 13:23 in test env
    # Address 4 is from live environment
    
    test_addresses = []
    live_addresses = []
    unsynced = []
    
    for addr in addresses:
        addr_id = addr['id']
        terminal_id = addr.get('terminal_address_id')
        city = addr['city']
        state = addr['state']
        
        if not terminal_id:
            unsynced.append(addr)
            continue
        
        # Address 4 is known to be from live
        # Addresses 10-15 are from test (created after 13:23)
        if addr_id == 4:
            live_addresses.append(addr)
        elif addr_id >= 10:
            test_addresses.append(addr)
        else:
            # Unknown, could be either
            live_addresses.append(addr)  # Assume live for safety
    
    print("📍 LIVE ENVIRONMENT ADDRESSES (won't work with test API):")
    print("-" * 80)
    if live_addresses:
        for addr in live_addresses:
            print(f"   ID {addr['id']:2d}: {addr['city']:15s}, {addr['state']:15s} - {addr['terminal_address_id']}")
    else:
        print("   None")
    
    print()
    print("📍 TEST ENVIRONMENT ADDRESSES (will work with test API):")
    print("-" * 80)
    if test_addresses:
        for addr in test_addresses:
            print(f"   ID {addr['id']:2d}: {addr['city']:15s}, {addr['state']:15s} - {addr['terminal_address_id']}")
    else:
        print("   None")
    
    print()
    print("📍 UNSYNCED ADDRESSES:")
    print("-" * 80)
    if unsynced:
        for addr in unsynced:
            print(f"   ID {addr['id']:2d}: {addr['city']:15s}, {addr['state']:15s} - Not synced")
    else:
        print("   None")
    
    print()
    print("="*80)
    print("RECOMMENDATION:")
    print("="*80)
    
    if len(test_addresses) >= 2:
        print(f"✅ You have {len(test_addresses)} addresses in TEST environment")
        print(f"\n   Use these address IDs for testing:")
        for i, addr in enumerate(test_addresses[:2], 1):
            print(f"   {i}. Address ID {addr['id']} - {addr['city']}, {addr['state']}")
    else:
        print(f"⚠️  You only have {len(test_addresses)} address(es) in TEST environment")
        print(f"   Need to create {2 - len(test_addresses)} more test address(es)")
        print(f"\n   Run the comprehensive test to create new addresses automatically")


if __name__ == "__main__":
    sys.exit(main())
