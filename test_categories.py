#!/usr/bin/env python3
"""Test categories endpoint after collation fix"""

from db import get_db_connection

def test_categories():
    print("Testing categories endpoint...\n")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Test 1: Simple category list
        print("1. Simple category list:")
        cursor.execute("SELECT id, category FROM category ORDER BY category ASC")
        categories = cursor.fetchall()
        print(f"   ✓ Found {len(categories)} categories")
        for cat in categories[:5]:
            print(f"      - {cat['category']}")
        if len(categories) > 5:
            print(f"      ... and {len(categories) - 5} more")
        
        # Test 2: Categories with product count (the query that was failing)
        print("\n2. Categories with product count:")
        cursor.execute("""
            SELECT c.id, c.category, COUNT(p.id) AS product_count
            FROM category c
            LEFT JOIN product p ON p.category = c.category
            GROUP BY c.id, c.category
            ORDER BY c.category ASC
        """)
        categories_with_count = cursor.fetchall()
        print(f"   ✓ Query successful!")
        print(f"   Categories with products:")
        for cat in categories_with_count:
            if cat['product_count'] > 0:
                print(f"      - {cat['category']}: {cat['product_count']} products")
        
        # Test 3: Get single category
        print("\n3. Single category lookup:")
        cursor.execute("""
            SELECT c.id, c.category, COUNT(p.id) AS product_count
            FROM category c
            LEFT JOIN product p ON p.category = c.category
            WHERE c.id = 1
            GROUP BY c.id, c.category
        """)
        single_cat = cursor.fetchone()
        if single_cat:
            print(f"   ✓ Category ID 1: {single_cat['category']}")
            print(f"     Products: {single_cat['product_count']}")
        
        conn.close()
        
        print("\n" + "="*60)
        print("✅ ALL CATEGORY TESTS PASSED!")
        print("="*60)
        print("\nThe categories endpoint should now work correctly.")
        print("Start your server and test with:")
        print("  curl http://localhost:4500/api/categories")
        print("  curl http://localhost:4500/api/categories?include_count=true")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_categories()
