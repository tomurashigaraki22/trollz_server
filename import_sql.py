#!/usr/bin/env python3
"""
Import the trollzstorecom_tr0llz_db.sql file into the database.
Uses a simpler approach that reads the file and executes it line by line.
"""

import pymysql
from config import Config

def import_sql_file():
    """Import SQL file by executing it directly."""
    
    print("[IMPORT] Connecting to database...")
    conn = pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )
    
    try:
        cursor = conn.cursor()
        
        print("[IMPORT] Reading SQL file...")
        with open('trollzstorecom_tr0llz_db.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split by semicolon but be smart about it
        # This is a simple approach that works for most SQL dumps
        statements = []
        current = []
        
        for line in sql_content.split('\n'):
            # Skip MySQL-specific commands and comments
            if (line.strip().startswith('--') or 
                line.strip().startswith('/*') or
                line.strip().startswith('*/') or
                line.strip().startswith('SET ') or
                line.strip().startswith('/*!') or
                'CREATE DATABASE' in line.upper() or
                line.strip().upper().startswith('USE ')):
                continue
            
            if line.strip():
                current.append(line)
                
            # If line ends with semicolon, we have a complete statement
            if line.strip().endswith(';'):
                statement = '\n'.join(current)
                if statement.strip():
                    statements.append(statement)
                current = []
        
        print(f"[IMPORT] Executing {len(statements)} SQL statements...")
        
        success = 0
        errors = 0
        
        for i, stmt in enumerate(statements):
            if (i + 1) % 50 == 0:
                print(f"[IMPORT] Progress: {i+1}/{len(statements)}")
                conn.commit()
            
            try:
                cursor.execute(stmt)
                success += 1
            except pymysql.Error as e:
                # Ignore duplicate entry and table exists errors
                if e.args[0] not in (1050, 1062):
                    errors += 1
                    if errors <= 3:
                        print(f"[IMPORT] Error: {str(e)[:80]}...")
        
        conn.commit()
        
        print(f"\n[IMPORT] Completed: {success} successful, {errors} errors")
        
        # Verify
        print("\n[IMPORT] Verifying data...")
        cursor.execute('SELECT COUNT(*) as count FROM product')
        products = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM category')
        categories = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM orders')
        orders = cursor.fetchone()['count']
        
        print(f"✓ Products: {products}")
        print(f"✓ Categories: {categories}")
        print(f"✓ Orders: {orders}")
        
        if products > 0:
            print("\n✓ Import successful!")
            return True
        else:
            print("\n⚠️  No products imported - trying alternative method...")
            return False
        
    except Exception as e:
        print(f"[IMPORT] Error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    success = import_sql_file()
    if not success:
        print("\n[IMPORT] Trying direct file execution...")
        print("[IMPORT] Please run this command manually:")
        print(f"mysql -h {Config.DB_HOST} -P {Config.DB_PORT} -u {Config.DB_USER} -p{Config.DB_PASSWORD} {Config.DB_NAME} < trollzstorecom_tr0llz_db.sql")
