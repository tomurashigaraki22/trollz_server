"""
Check which environment addresses are synced to
"""

import requests

BASE_URL = "http://localhost:4500"
TEST_USER = {"email": "devtomiwa9@gmail.com", "password": "Pityboy@22"}

# Login
response = requests.post(f"{BASE_URL}/api/auth/login", json=TEST_USER)
token = response.json()["data"]["token"]
headers = {"Authorization": f"Bearer {token}"}

# Get addresses
response = requests.get(f"{BASE_URL}/api/addresses", headers=headers)
addresses = response.json()["data"]["addresses"]

print("Addresses with Terminal IDs:")
print()

for addr in addresses:
    if addr.get('terminal_address_id'):
        print(f"ID {addr['id']}: {addr['city']}, {addr['state']}")
        print(f"  Terminal ID: {addr['terminal_address_id']}")
        print(f"  Created: {addr.get('created_at', 'N/A')}")
        print()

print("\n⚠️  NOTE: These Terminal IDs were created in LIVE environment")
print("   They won't work in TEST/Sandbox environment!")
print("\n💡 Solution: Create new addresses (they'll auto-sync to test env)")
