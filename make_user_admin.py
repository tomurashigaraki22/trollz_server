"""
Make a user an admin
"""

from db import get_db_connection

def make_admin(email):
    """Make a user an admin by email"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Check if user exists
            cursor.execute("SELECT id, email, type FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if not user:
                print(f"❌ User not found: {email}")
                return False
            
            print(f"Found user: {user['email']} (ID: {user['id']}, Type: {user.get('type', 'user')})")
            
            # Update user type to admin
            cursor.execute("UPDATE users SET type = 'admin' WHERE email = %s", (email,))
            conn.commit()
            
            print(f"✅ User {email} is now an admin")
            return True
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    email = "devtomiwa9@gmail.com"
    make_admin(email)
