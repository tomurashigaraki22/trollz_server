#!/usr/bin/env python3
"""
Fix all collation mismatches in the database to prevent future issues
"""

import pymysql
from config import Config

def fix_all_collations():
    print("[FIX] Standardizing all table collations to utf8mb4_unicode_ci...")
    
    conn = pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    
    try:
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = [list(t.values())[0] for t in cursor.fetchall()]
        
        print(f"\n[FIX] Found {len(tables)} tables to check")
        
        fixed_count = 0
        
        for table in tables:
            # Get table collation
            cursor.execute(f"SHOW TABLE STATUS WHERE Name = '{table}'")
            table_info = cursor.fetchone()
            
            if table_info and table_info['Collation'] != 'utf8mb4_unicode_ci':
                print(f"\n[FIX] Fixing table: {table}")
                print(f"      Current: {table_info['Collation']}")
                
                try:
                    # Convert table to utf8mb4_unicode_ci
                    cursor.execute(f"""
                        ALTER TABLE `{table}` 
                        CONVERT TO CHARACTER SET utf8mb4 
                        COLLATE utf8mb4_unicode_ci
                    """)
                    print(f"      ✓ Converted to utf8mb4_unicode_ci")
                    fixed_count += 1
                except Exception as e:
                    print(f"      ⚠️  Warning: {str(e)[:80]}")
        
        print(f"\n[FIX] Fixed {fixed_count} tables")
        
        # Verify all tables
        print("\n[FIX] Verifying table collations...")
        mismatches = []
        
        for table in tables:
            cursor.execute(f"SHOW TABLE STATUS WHERE Name = '{table}'")
            table_info = cursor.fetchone()
            
            if table_info:
                collation = table_info['Collation']
                if collation and 'utf8mb4_unicode_ci' not in collation:
                    mismatches.append(f"{table}: {collation}")
        
        if mismatches:
            print("\n⚠️  Tables still with different collations:")
            for m in mismatches:
                print(f"   - {m}")
        else:
            print("\n✅ All tables now use utf8mb4_unicode_ci!")
        
        # Test critical queries
        print("\n[FIX] Testing critical queries...")
        
        # Test 1: Categories with product count
        try:
            cursor.execute("""
                SELECT c.id, c.category, COUNT(p.id) AS product_count
                FROM category c
                LEFT JOIN product p ON p.category = c.category
                GROUP BY c.id, c.category
                LIMIT 1
            """)
            cursor.fetchone()
            print("   ✓ Categories query works")
        except Exception as e:
            print(f"   ✗ Categories query failed: {e}")
        
        # Test 2: Products by category
        try:
            cursor.execute("""
                SELECT * FROM product 
                WHERE category = 'Fashion' 
                LIMIT 1
            """)
            cursor.fetchone()
            print("   ✓ Products by category works")
        except Exception as e:
            print(f"   ✗ Products by category failed: {e}")
        
        conn.close()
        
        print("\n" + "="*60)
        print("✅ COLLATION STANDARDIZATION COMPLETE")
        print("="*60)
        print("\nAll database operations should now work without collation errors!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        conn.close()

if __name__ == "__main__":
    fix_all_collations()
