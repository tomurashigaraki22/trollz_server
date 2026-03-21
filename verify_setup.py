#!/usr/bin/env python3
"""
Complete verification of the Trollz Store API setup
"""

from db import get_db_connection
from config import Config

def verify_setup():
    print("="*60)
    print("TROLLZ STORE API - SETUP VERIFICATION")
    print("="*60)
    
    # 1. Configuration
    print("\n📋 Configuration:")
    print(f"   Database: {Config.DB_NAME}")
    print(f"   Host: {Config.DB_HOST}:{Config.DB_PORT}")
    print(f"   User: {Config.DB_USER}")
    print(f"   Server: {Config.HOST}:{Config.PORT}")
    
    # 2. Database Connection
    print("\n🔌 Database Connection:")
    try:
        conn = get_db_connection()
        print("   ✓ Connection successful")
        
        cursor = conn.cursor()
        
        # 3. Tables
        print("\n📊 Database Tables:")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [list(t.values())[0] for t in tables]
        print(f"   Found {len(tables)} tables:")
        for table in sorted(table_names):
            print(f"      - {table}")
        
        # 4. Data Counts
        print("\n📈 Data Summary:")
        
        # Products
        cursor.execute("SELECT COUNT(*) as count FROM product")
        product_count = cursor.fetchone()['count']
        print(f"   Products: {product_count}")
        
        # Categories
        cursor.execute("SELECT COUNT(*) as count FROM category")
        category_count = cursor.fetchone()['count']
        print(f"   Categories: {category_count}")
        
        # Orders
        cursor.execute("SELECT COUNT(*) as count FROM orders")
        order_count = cursor.fetchone()['count']
        print(f"   Orders: {order_count}")
        
        # Cart
        cursor.execute("SELECT COUNT(*) as count FROM cart")
        cart_count = cursor.fetchone()['count']
        print(f"   Cart Items: {cart_count}")
        
        # Users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        user_count = cursor.fetchone()['count']
        print(f"   Users: {user_count}")
        
        # 5. Sample Data
        print("\n🛍️  Sample Products:")
        cursor.execute("SELECT id, item, category, price FROM product ORDER BY date DESC LIMIT 5")
        products = cursor.fetchall()
        for p in products:
            print(f"   [{p['id']}] {p['item'][:50]}")
            print(f"       Category: {p['category']}, Price: ₦{p['price']:,}")
        
        # 6. Categories
        print("\n🏷️  Categories:")
        cursor.execute("SELECT category FROM category ORDER BY category LIMIT 10")
        categories = cursor.fetchall()
        cat_list = [c['category'] for c in categories]
        print(f"   {', '.join(cat_list)}")
        if category_count > 10:
            print(f"   ... and {category_count - 10} more")
        
        conn.close()
        
        # 7. Status
        print("\n" + "="*60)
        if product_count > 0 and category_count > 0:
            print("✅ SETUP COMPLETE - API READY TO USE!")
        else:
            print("⚠️  WARNING: Database is empty. Run: python import_sql.py")
        print("="*60)
        
        # 8. Next Steps
        print("\n📝 Next Steps:")
        print("   1. Start the server: python app.py")
        print("   2. Test endpoints: python test_server.py")
        print("   3. Read docs: README.md and QUICKSTART.md")
        print("\n💡 Quick Test:")
        print(f"   curl http://localhost:{Config.PORT}/api/products?limit=5")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Connection failed: {e}")
        print("\n❌ SETUP INCOMPLETE")
        print("\nTroubleshooting:")
        print("   1. Check database credentials in config.py")
        print("   2. Ensure database server is running")
        print("   3. Run: python import_sql.py")
        return False

if __name__ == "__main__":
    verify_setup()
