"""
Check admin table and create admin user if needed
"""

from db import get_db_connection
import bcrypt

conn = get_db_connection()
try:
    with conn.cursor() as cursor:
        # Check if admin table exists
        cursor.execute("SHOW TABLES LIKE 'admin'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ Admin table does not exist")
            print("Creating admin table...")
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admin (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) DEFAULT 'admin',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("✅ Admin table created")
        else:
            print("✅ Admin table exists")
        
        # Check if admin user exists
        cursor.execute("SELECT * FROM admin WHERE username = 'admin'")
        admin = cursor.fetchone()
        
        if not admin:
            print("\nCreating admin user...")
            
            # Hash password
            password = "admin123"
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            cursor.execute(
                "INSERT INTO admin (username, password, role) VALUES (%s, %s, %s)",
                ("admin", hashed.decode('utf-8'), "admin")
            )
            conn.commit()
            
            print("✅ Admin user created")
            print(f"   Username: admin")
            print(f"   Password: {password}")
        else:
            print(f"\n✅ Admin user exists: {admin['username']}")
            print(f"   Role: {admin['role']}")
            
finally:
    conn.close()
