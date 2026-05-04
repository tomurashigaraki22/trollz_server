"""
Run Migration 004: Add terminal_address_id to shipping_addresses table
"""

import pymysql
from config import Config


def run_migration():
    """Run the migration to add terminal_address_id column."""
    print("="*70)
    print("  RUNNING MIGRATION 004")
    print("  Add terminal_address_id to shipping_addresses")
    print("="*70)
    print()
    
    try:
        # Connect to database
        print(f"📡 Connecting to database: {Config.DB_NAME}")
        conn = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("✅ Connected successfully\n")
        
        with conn.cursor() as cursor:
            # Read migration file
            print("📄 Reading migration file...")
            with open('migrations/004_add_terminal_address_id_to_shipping_addresses.sql', 'r') as f:
                migration_sql = f.read()
            
            print("✅ Migration file loaded\n")
            
            # Check if column already exists
            print("🔍 Checking if terminal_address_id column exists...")
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = %s
                AND TABLE_NAME = 'shipping_addresses'
                AND COLUMN_NAME = 'terminal_address_id'
            """, (Config.DB_NAME,))
            
            result = cursor.fetchone()
            
            if result['count'] > 0:
                print("⚠️  Column terminal_address_id already exists")
                print("   Skipping migration\n")
                return True
            
            print("✅ Column does not exist, proceeding with migration\n")
            
            # Execute migration
            print("🔧 Adding terminal_address_id column...")
            
            # Split by semicolon and execute each statement
            statements = [s.strip() for s in migration_sql.split(';') if s.strip()]
            
            for i, statement in enumerate(statements, 1):
                if statement:
                    print(f"   Executing statement {i}/{len(statements)}...")
                    cursor.execute(statement)
            
            conn.commit()
            print("✅ Migration executed successfully\n")
            
            # Verify column was added
            print("🔍 Verifying column was added...")
            cursor.execute("""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = %s
                AND TABLE_NAME = 'shipping_addresses'
                AND COLUMN_NAME = 'terminal_address_id'
            """, (Config.DB_NAME,))
            
            column_info = cursor.fetchone()
            
            if column_info:
                print("✅ Column added successfully:")
                print(f"   Name: {column_info['COLUMN_NAME']}")
                print(f"   Type: {column_info['DATA_TYPE']}")
                print(f"   Nullable: {column_info['IS_NULLABLE']}")
                print(f"   Default: {column_info['COLUMN_DEFAULT']}")
            else:
                print("❌ Column verification failed")
                return False
            
            print()
            print("="*70)
            print("  MIGRATION 004 COMPLETE")
            print("="*70)
            print()
            print("✅ The shipping_addresses table now has terminal_address_id column")
            print("   This column will store the Terminal Africa address ID")
            print("   for synced addresses.")
            print()
            
            return True
            
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'conn' in locals():
            conn.close()
            print("📡 Database connection closed")


if __name__ == "__main__":
    import sys
    success = run_migration()
    sys.exit(0 if success else 1)
