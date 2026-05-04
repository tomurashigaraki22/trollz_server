#!/usr/bin/env python3
"""
Create warehouse address directly in database and Terminal Africa
"""

import pymysql
import requests
import json
from config import Config

def get_db_connection():
    """Create database connection"""
    return pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )

def create_warehouse_user():
    """Create a special warehouse user if it doesn't exist"""
    
    print("🔍 Checking for warehouse user...")
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Check if warehouse user exists
            cursor.execute(
                "SELECT id FROM users WHERE email = %s",
                ("warehouse@trollzstore.com",)
            )
            user = cursor.fetchone()
            
            if user:
                print(f"✅ Warehouse user already exists with ID: {user['id']}")
                return user['id']
            
            # Create warehouse user
            print("👤 Creating warehouse user...")
            cursor.execute(
                """
                INSERT INTO users (name, email, password, phone, role, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    "Trollz Store Warehouse",
                    "warehouse@trollzstore.com",
                    "warehouse_password_hash",  # We won't use this for login
                    "+234 800 000 0000",
                    "Customer",  # Role
                    0  # Status
                )
            )
            user_id = cursor.lastrowid
            print(f"✅ Created warehouse user with ID: {user_id}")
            return user_id
            
    finally:
        conn.close()

def create_warehouse_address_in_db(user_id):
    """Create warehouse address in database"""
    
    print("🏭 Creating warehouse address in database...")
    
    warehouse_address = Config.get_warehouse_address()
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Check if warehouse address already exists
            cursor.execute(
                """
                SELECT id FROM shipping_addresses 
                WHERE user_id = %s AND city = %s AND state = %s
                """,
                (user_id, warehouse_address["city"], warehouse_address["state"])
            )
            existing = cursor.fetchone()
            
            if existing:
                print(f"✅ Warehouse address already exists with ID: {existing['id']}")
                return existing['id']
            
            # Create new warehouse address
            cursor.execute(
                """
                INSERT INTO shipping_addresses
                    (user_id, first_name, last_name, phone, email, street, street_line_2,
                     city, state, country, post_code, is_default)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    user_id,
                    warehouse_address["first_name"],
                    warehouse_address["last_name"],
                    warehouse_address["phone"],
                    warehouse_address["email"],
                    warehouse_address["street"],
                    warehouse_address["street_line_2"],
                    warehouse_address["city"],
                    warehouse_address["state"],
                    warehouse_address["country"],
                    warehouse_address["post_code"],
                    True  # Set as default
                )
            )
            address_id = cursor.lastrowid
            print(f"✅ Created warehouse address with ID: {address_id}")
            return address_id
            
    finally:
        conn.close()

def sync_warehouse_to_terminal(address_id):
    """Sync warehouse address to Terminal Africa"""
    
    print("📤 Syncing warehouse address to Terminal Africa...")
    
    # Get address details from database
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT first_name, last_name, phone, email, street, street_line_2,
                       city, state, country, post_code
                FROM shipping_addresses
                WHERE id = %s
                """,
                (address_id,)
            )
            address = cursor.fetchone()
    finally:
        conn.close()
    
    if not address:
        print("❌ Address not found in database")
        return None
    
    # Prepare Terminal Africa API request
    base_url = Config.get_terminal_base_url()
    secret_key = Config.get_terminal_secret_key()
    
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json"
    }
    
    terminal_address = {
        "first_name": address["first_name"],
        "last_name": address["last_name"],
        "phone": address["phone"],
        "email": address["email"],
        "street": address["street"],
        "city": address["city"],
        "state": address["state"],
        "country": address["country"],
        "post_code": address["post_code"]
    }
    
    if address.get("street_line_2"):
        terminal_address["street_line_2"] = address["street_line_2"]
    
    print(f"🌍 Sending to Terminal Africa API: {base_url}/addresses")
    
    try:
        response = requests.post(
            f"{base_url}/addresses",
            headers=headers,
            json=terminal_address,
            timeout=30
        )
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            
            # Check different response structures
            terminal_address_id = None
            
            # Try different possible locations for address_id
            if data.get("data") and isinstance(data["data"], dict):
                if "address_id" in data["data"]:
                    terminal_address_id = data["data"]["address_id"]
                elif "id" in data["data"]:
                    terminal_address_id = data["data"]["id"]
                elif "_id" in data["data"]:
                    terminal_address_id = data["data"]["_id"]
            
            if terminal_address_id:
                print(f"✅ Success! Terminal Africa address ID: {terminal_address_id}")
                
                # Update database with Terminal Africa ID
                conn = get_db_connection()
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            """
                            UPDATE shipping_addresses
                            SET terminal_address_id = %s, terminal_synced = TRUE
                            WHERE id = %s
                            """,
                            (terminal_address_id, address_id)
                        )
                    print(f"✅ Updated database with Terminal Africa ID")
                finally:
                    conn.close()
                
                return terminal_address_id
            else:
                print(f"⚠️  Created in Terminal but no address_id found in response")
                print(f"Response structure: {json.dumps(data, indent=2)}")
                return None
        else:
            print(f"❌ Failed to create address in Terminal Africa")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def main():
    """Main function"""
    
    print("🔄 Warehouse Address Setup Tool")
    print("=" * 60)
    
    # Step 1: Create warehouse user
    user_id = create_warehouse_user()
    
    # Step 2: Create warehouse address in database
    address_id = create_warehouse_address_in_db(user_id)
    
    # Step 3: Sync to Terminal Africa
    terminal_address_id = sync_warehouse_to_terminal(address_id)
    
    print("\n" + "=" * 60)
    
    if terminal_address_id:
        print(f"✅ WAREHOUSE ADDRESS SETUP COMPLETE")
        print(f"   Database Address ID: {address_id}")
        print(f"   Terminal Africa ID: {terminal_address_id}")
        print(f"\n📝 Use this Terminal Africa ID as origin_address_id in rates requests")
    else:
        print(f"⚠️  Warehouse address created in database but not synced to Terminal Africa")
        print(f"   Database Address ID: {address_id}")
        print(f"   You may need to sync it manually or check Terminal Africa API")

if __name__ == "__main__":
    main()