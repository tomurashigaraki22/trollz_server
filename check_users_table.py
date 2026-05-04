"""
Check users table structure
"""

from db import get_db_connection

conn = get_db_connection()
try:
    with conn.cursor() as cursor:
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        
        print("Users table structure:")
        print("-" * 60)
        for col in columns:
            print(f"{col['Field']}: {col['Type']}")
        
        print("\n" + "-" * 60)
        print("\nChecking test user:")
        cursor.execute("SELECT * FROM users WHERE email = 'devtomiwa9@gmail.com'")
        user = cursor.fetchone()
        
        if user:
            print(f"User found: {user['email']}")
            print(f"ID: {user['id']}")
            for key, value in user.items():
                if key not in ['password', 'id', 'email']:
                    print(f"{key}: {value}")
        else:
            print("User not found")
            
finally:
    conn.close()
