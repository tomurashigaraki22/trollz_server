#!/usr/bin/env python3
"""
Fix collation mismatch between category and product tables
"""

import pymysql
from config import Config

def fix_collation():
    print("[FIX] Fixing collation mismatch...")
    
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
        
        # Check current collations
        print("\n[FIX] Checking current collations...")
        
        cursor.execute("""
            SELECT TABLE_NAME, COLUMN_NAME, COLLATION_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND COLUMN_NAME = 'category'
            AND TABLE_NAME IN ('category', 'product')
        """, (Config.DB_NAME,))
        
        collations = cursor.fetchall()
        print("\nCurrent collations:")
        for col in collations:
            print(f"   {col['TABLE_NAME']}.{col['COLUMN_NAME']}: {col['COLLATION_NAME']}")
        
        # Fix category table to use utf8mb4_unicode_ci
        print("\n[FIX] Updating category table collation...")
        
        cursor.execute("""
            ALTER TABLE `category` 
            MODIFY COLUMN `category` VARCHAR(255) 
            CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
        """)
        print("   ✓ Updated category.category column")
        
        # Also fix the product.category column to ensure consistency
        print("\n[FIX] Updating product table collation...")
        
        cursor.execute("""
            ALTER TABLE `product` 
            MODIFY COLUMN `category` VARCHAR(50) 
            CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
        """)
        print("   ✓ Updated product.category column")
        
        # Fix product.subcategory as well
        cursor.execute("""
            ALTER TABLE `product` 
            MODIFY COLUMN `subcategory` VARCHAR(100) 
            CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
        """)
        print("   ✓ Updated product.subcategory column")
        
        # Verify the fix
        print("\n[FIX] Verifying collations...")
        cursor.execute("""
            SELECT TABLE_NAME, COLUMN_NAME, COLLATION_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND COLUMN_NAME = 'category'
            AND TABLE_NAME IN ('category', 'product')
        """, (Config.DB_NAME,))
        
        collations = cursor.fetchall()
        print("\nUpdated collations:")
        all_unicode = True
        for col in collations:
            print(f"   {col['TABLE_NAME']}.{col['COLUMN_NAME']}: {col['COLLATION_NAME']}")
            if col['COLLATION_NAME'] != 'utf8mb4_unicode_ci':
                all_unicode = False
        
        if all_unicode:
            print("\n✅ Collation fix completed successfully!")
            print("All category columns now use utf8mb4_unicode_ci")
        else:
            print("\n⚠️  Warning: Some columns still have different collations")
        
        # Test the query that was failing
        print("\n[FIX] Testing category query...")
        cursor.execute("""
            SELECT c.id, c.category, COUNT(p.id) AS product_count
            FROM category c
            LEFT JOIN product p ON p.category = c.category
            GROUP BY c.id, c.category
            ORDER BY c.category ASC
            LIMIT 5
        """)
        
        results = cursor.fetchall()
        print(f"   ✓ Query successful! Found {len(results)} categories")
        for cat in results[:3]:
            print(f"      - {cat['category']}: {cat['product_count']} products")
        
        conn.close()
        
        print("\n" + "="*60)
        print("✅ COLLATION FIX COMPLETE")
        print("="*60)
        print("\nYou can now fetch categories without errors!")
        print("Test with: curl http://localhost:4500/api/categories")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        conn.close()

if __name__ == "__main__":
    fix_collation()
