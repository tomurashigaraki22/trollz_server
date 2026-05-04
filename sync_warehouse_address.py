"""
Sync warehouse address to Terminal Africa
"""

import requests
from config import Config

def sync_warehouse_address():
    """Sync the warehouse address to Terminal Africa"""
    
    base_url = "http://localhost:4500"
    
    # First, login as admin to get token
    print("🔐 Logging in as admin...")
    login_response = requests.post(f"{base_url}/api/admin/login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    if login_response.status_code != 200:
        print(f"❌ Admin login failed: {login_response.text}")
        return None
    
    token = login_response.json()["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get warehouse address from config
    warehouse_address = Config.get_warehouse_address()
    
    print(f"\n🏭 Warehouse Address from Config:")
    print(f"  Name: {warehouse_address['first_name']} {warehouse_address['last_name']}")
    print(f"  Street: {warehouse_address['street']}")
    print(f"  City: {warehouse_address['city']}")
    print(f"  State: {warehouse_address['state']}")
    print(f"  Country: {warehouse_address['country']}")
    print(f"  Post Code: {warehouse_address['post_code']}")
    print(f"  Phone: {warehouse_address['phone']}")
    print(f"  Email: {warehouse_address['email']}")
    
    # Format for Terminal Africa
    terminal_address = {
        "first_name": warehouse_address["first_name"],
        "last_name": warehouse_address["last_name"],
        "phone": warehouse_address["phone"],
        "email": warehouse_address["email"],
        "street": warehouse_address["street"],
        "city": warehouse_address["city"],
        "state": warehouse_address["state"],
        "country": warehouse_address["country"],
        "post_code": warehouse_address["post_code"]
    }
    
    print(f"\n📤 Syncing to Terminal Africa...")
    
    # Create address via API
    response = requests.post(
        f"{base_url}/api/addresses",
        headers=headers,
        json=terminal_address
    )
    
    if response.status_code == 201:
        data = response.json()
        print(f"\n✅ SUCCESS! Warehouse address synced to Terminal Africa")
        print(f"  Address ID: {data['data']['address']['id']}")
        print(f"  Terminal Address ID: {data['data'].get('terminal_address_id', 'N/A')}")
        print(f"  Terminal Synced: {data['data'].get('terminal_synced', False)}")
        
        if data['data'].get('terminal_sync_warning'):
            print(f"  ⚠️  Warning: {data['data']['terminal_sync_warning']}")
        
        return data['data']['address']['id']
    else:
        print(f"\n❌ Failed to sync warehouse address: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Check if it's a state validation error
        if "Invalid state" in response.text:
            print(f"\n⚠️  State validation error!")
            print(f"Current state: {warehouse_address['state']}")
            print(f"Please check the list of valid states:")
            print(f"  GET /api/shipping/states")
        
        return None


def check_existing_addresses():
    """Check existing addresses to see if warehouse is already synced"""
    
    base_url = "http://localhost:4500"
    
    print("🔍 Checking existing addresses...")
    
    # Login as admin
    login_response = requests.post(f"{base_url}/api/admin/login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    if login_response.status_code != 200:
        print(f"❌ Admin login failed: {login_response.text}")
        return
    
    token = login_response.json()["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get all addresses
    response = requests.get(f"{base_url}/api/addresses", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        addresses = data["data"]["addresses"]
        
        print(f"\n📋 Found {len(addresses)} addresses:")
        print("-"*80)
        
        for i, addr in enumerate(addresses, 1):
            print(f"{i:2d}. {addr.get('first_name')} {addr.get('last_name')}")
            print(f"    {addr.get('city')}, {addr.get('state')}")
            print(f"    ID: {addr.get('id')}, Terminal ID: {addr.get('terminal_address_id', 'N/A')}")
            print()
        
        # Check for warehouse-like addresses
        warehouse_city = Config.WAREHOUSE_CITY
        warehouse_state = Config.WAREHOUSE_STATE
        
        warehouse_addresses = [
            a for a in addresses 
            if a.get('city') == warehouse_city and a.get('state') == warehouse_state
        ]
        
        if warehouse_addresses:
            print(f"\n🏭 Found {len(warehouse_addresses)} addresses in {warehouse_city}, {warehouse_state}:")
            for addr in warehouse_addresses:
                print(f"  - ID: {addr['id']}, Terminal ID: {addr.get('terminal_address_id', 'N/A')}")
                print(f"    {addr.get('street')}")
        else:
            print(f"\n❌ No addresses found in {warehouse_city}, {warehouse_state}")
    
    else:
        print(f"❌ Failed to get addresses: {response.status_code}")
        print(f"Response: {response.text}")


if __name__ == "__main__":
    print("🔄 Warehouse Address Sync Tool\n")
    
    # Check existing addresses first
    check_existing_addresses()
    
    print("\n" + "="*80)
    
    # Ask user if they want to sync
    sync = input("\nDo you want to sync the warehouse address to Terminal Africa? (y/n): ")
    
    if sync.lower() == 'y':
        address_id = sync_warehouse_address()
        
        if address_id:
            print(f"\n✅ Warehouse address ID: {address_id}")
            print(f"Use this ID as origin_address_id in shipping rates requests")
        else:
            print(f"\n❌ Failed to sync warehouse address")
    else:
        print("\nSkipping warehouse address sync")