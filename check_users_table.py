#!/usr/bin/env python3
"""
Check users table structure
"""

import mysql.connector
from config import Config

def check_users_table():
    """Check users table structure"""
    
    print("🔍 Checking users table structure...")
    
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        
        cursor = conn.cursor(dictionary=True)
        
        # Check users table columns
        cursor.execute('DESCRIBE users')
        columns = cursor.fetchall()
        
        print("\n📋 Users table columns:")
        print("-" * 50)
        for col in columns:
            print(f"  {col['Field']:20s} {col['Type']:20s} {col.get('Null', 'NO'):5s} {col.get('Key', ''):10s}")
        
        # Check if we have any users
        cursor.execute('SELECT COUNT(*) as count FROM users')
        count = cursor.fetchone()['count']
        print(f"\n👥 Total users in database: {count}")
        
        # Get first few users
        if count > 0:
            cursor.execute('SELECT id, email, username FROM users LIMIT 5')
            users = cursor.fetchall()
            print("\n📝 Sample users:")
            for user in users:
                print(f"  ID: {user['id']}, Email: {user.get('email', 'N/A')}, Username: {user.get('username', 'N/A')}")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Users table check complete")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    check_users_table()