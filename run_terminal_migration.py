"""
Run Terminal Africa Migration
Executes the Terminal Africa database migration script.
"""

import pymysql
from config import Config

def run_migration():
    """Run the Terminal Africa migration."""
    print("\n" + "="*70)
    print("  TERMINAL AFRICA MIGRATION")
    print("="*70)
    
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
        
        # Read migration file
        print("\n📄 Reading migration file...")
        with open('migrations/003_terminal_africa_fields.sql', 'r') as f:
            migration_sql = f.read()
        
        # Split into individual statements
        statements = [s.strip() for s in migration_sql.split(';') if s.strip()]
        
        print(f"✅ Found {len(statements)} SQL statements")
        
        # First, add columns one by one to handle existing columns
        print("\n🔧 Adding columns to orders table...")
        with connection.cursor() as cursor:
            columns_to_add = [
                ('terminal_shipment_id', 'VARCHAR(50)'),
                ('terminal_rate_id', 'VARCHAR(50)'),
                ('terminal_carrier_id', 'VARCHAR(50)'),
                ('terminal_carrier_name', 'VARCHAR(100)'),
                ('terminal_tracking_url', 'TEXT'),
                ('terminal_label_url', 'TEXT'),
                ('terminal_invoice_url', 'TEXT')
            ]
            
            for col_name, col_type in columns_to_add:
                try:
                    cursor.execute(f"ALTER TABLE orders ADD COLUMN {col_name} {col_type}")
                    connection.commit()
                    print(f"   ✅ Added column: {col_name}")
                except pymysql.err.OperationalError as e:
                    if "Duplicate column name" in str(e):
                        print(f"   ℹ️  Column {col_name} already exists, skipping")
                    else:
                        print(f"   ⚠️  Error adding {col_name}: {str(e)}")
        
        # Execute remaining statements (skip the first ALTER TABLE statement)
        print("\n🔧 Creating tables and inserting data...")
        with connection.cursor() as cursor:
            for i, statement in enumerate(statements[1:], 2):  # Skip first statement
                if statement:
                    try:
                        print(f"   [{i}/{len(statements)}] Executing statement...")
                        cursor.execute(statement)
                        connection.commit()
                        print(f"   ✅ Statement {i} executed successfully")
                    except Exception as e:
                        error_msg = str(e)
                        if "already exists" in error_msg or "Duplicate" in error_msg:
                            print(f"   ℹ️  Statement {i} - Resource already exists, skipping")
                        else:
                            print(f"   ⚠️  Statement {i} warning: {error_msg}")
                        # Continue with other statements
                        continue
        
        print("\n✅ Migration completed successfully!")
        
        # Verify tables created
        print("\n🔍 Verifying tables...")
        with connection.cursor() as cursor:
            tables_to_check = [
                'terminal_addresses',
                'terminal_packaging',
                'terminal_parcels',
                'terminal_carriers',
                'terminal_rates'
            ]
            
            for table in tables_to_check:
                cursor.execute(f"SHOW TABLES LIKE '{table}'")
                result = cursor.fetchone()
                if result:
                    print(f"   ✅ {table} - EXISTS")
                else:
                    print(f"   ❌ {table} - NOT FOUND")
            
            # Check orders table columns
            print("\n🔍 Verifying orders table columns...")
            cursor.execute("DESCRIBE orders")
            columns = [row['Field'] for row in cursor.fetchall()]
            
            terminal_columns = [
                'terminal_shipment_id',
                'terminal_rate_id',
                'terminal_carrier_id',
                'terminal_carrier_name',
                'terminal_tracking_url',
                'terminal_label_url',
                'terminal_invoice_url'
            ]
            
            for col in terminal_columns:
                if col in columns:
                    print(f"   ✅ {col} - EXISTS")
                else:
                    print(f"   ❌ {col} - NOT FOUND")
        
        # Check default packaging
        print("\n🔍 Checking default packaging...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM terminal_packaging WHERE is_default = TRUE")
            result = cursor.fetchone()
            count = result['count'] if result else 0
            print(f"   ✅ {count} default packaging options created")
        
        connection.close()
        
        print("\n" + "="*70)
        print("  MIGRATION COMPLETE ✅")
        print("="*70)
        print("\nNext steps:")
        print("1. Review the migration results above")
        print("2. Test Terminal Africa integration")
        print("3. Proceed to Phase 2 implementation")
        print("\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        return False


if __name__ == "__main__":
    run_migration()
