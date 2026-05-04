"""
Create Test User for Terminal Africa Phase 3 Testing
Creates a test user in the database for running Phase 3 tests.
"""

import pymysql
from config import Config
import bcrypt


def create_test_user():
    """Create a test user in the database."""
    print("\n" + "="*70)
    print("  CREATE TEST USER FOR PHASE 3 TESTING")
    print("="*70)
    
    # Test user details
    test_user = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+2348000000000"
    }
    
    try:
        # Connect to database
        print("\n📡 Connecting to database...")
        connection = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("✅ Connected successfully")
        
        with connection.cursor() as cursor:
            # Check if user already exists
            print(f"\n🔍 Checking if user exists: {test_user['email']}")
            cursor.execute(
                "SELECT id, email FROM users WHERE email = %s",
                (test_user['email'],)
            )
            existing_user = cursor.fetchone()
            
            if existing_user:
                print(f"✅ Test user already exists!")
                print(f"   User ID: {existing_user['id']}")
                print(f"   Email: {existing_user['email']}")
                print(f"\n📋 You can use this user for testing:")
                print(f"   Email: {test_user['email']}")
                print(f"   Password: {test_user['password']}")
                return True
            
            # Hash password
            print(f"\n🔐 Creating new test user...")
            hashed_password = bcrypt.hashpw(
                test_user['password'].encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
            
            # Insert user
            cursor.execute(
                """
                INSERT INTO users (email, password, first_name, last_name, phone)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    test_user['email'],
                    hashed_password,
                    test_user['first_name'],
                    test_user['last_name'],
                    test_user['phone']
                )
            )
            
            user_id = cursor.lastrowid
            connection.commit()
            
            print(f"✅ Test user created successfully!")
            print(f"   User ID: {user_id}")
            print(f"   Email: {test_user['email']}")
            print(f"   Name: {test_user['first_name']} {test_user['last_name']}")
            
            print(f"\n📋 Test User Credentials:")
            print(f"   Email: {test_user['email']}")
            print(f"   Password: {test_user['password']}")
            
            print(f"\n✅ You can now run Phase 3 tests:")
            print(f"   python test_terminal_phase3.py")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False
    finally:
        if 'connection' in locals():
            connection.close()
            print(f"\n📡 Database connection closed")


def main():
    """Main function."""
    success = create_test_user()
    
    if success:
        print("\n" + "="*70)
        print("  TEST USER READY ✅")
        print("="*70)
        print("\nNext steps:")
        print("1. Start the server: python app.py")
        print("2. Run Phase 3 tests: python test_terminal_phase3.py")
        print("3. Or test manually with Postman using the credentials above")
        print("\n")
        return 0
    else:
        print("\n" + "="*70)
        print("  FAILED TO CREATE TEST USER ❌")
        print("="*70)
        print("\nPlease check:")
        print("1. Database connection settings in config.py")
        print("2. Database is running and accessible")
        print("3. Users table exists in the database")
        print("\n")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
