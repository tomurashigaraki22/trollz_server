#!/usr/bin/env python3
"""
Database Migration Runner
Executes SQL migration files in order and tracks applied migrations.
"""

import os
import sys
import pymysql
from config import Config
from datetime import datetime


def get_db_connection():
    """Create and return a database connection."""
    return pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )


def ensure_migrations_table(cursor):
    """Ensure the schema_migrations table exists."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            migration_name VARCHAR(255) NOT NULL UNIQUE,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_migration_name (migration_name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("[MIGRATION] Schema migrations table ensured.")


def get_applied_migrations(cursor):
    """Get list of already applied migrations."""
    cursor.execute("SELECT migration_name FROM schema_migrations ORDER BY applied_at")
    return {row['migration_name'] for row in cursor.fetchall()}


def get_pending_migrations(migrations_dir='migrations'):
    """Get list of migration files that haven't been applied yet."""
    if not os.path.exists(migrations_dir):
        print(f"[MIGRATION] Migrations directory '{migrations_dir}' not found.")
        return []
    
    # Get all .sql files in migrations directory
    migration_files = [
        f for f in os.listdir(migrations_dir)
        if f.endswith('.sql') and not f.startswith('.')
    ]
    
    # Sort by filename (assumes numbered prefix like 001_, 002_, etc.)
    migration_files.sort()
    
    return migration_files


def execute_migration(cursor, migration_file, migrations_dir='migrations'):
    """Execute a single migration file."""
    file_path = os.path.join(migrations_dir, migration_file)
    migration_name = migration_file.replace('.sql', '')
    
    print(f"\n[MIGRATION] Applying: {migration_name}")
    print(f"[MIGRATION] File: {file_path}")
    
    try:
        # Read the migration file
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split by semicolons and execute each statement
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for i, statement in enumerate(statements, 1):
            # Skip comments and empty statements
            if statement.startswith('--') or not statement:
                continue
            
            try:
                cursor.execute(statement)
                print(f"  ✓ Executed statement {i}/{len(statements)}")
            except pymysql.Error as e:
                # Check if error is about column/index already existing
                if 'Duplicate column name' in str(e) or 'Duplicate key name' in str(e):
                    print(f"  ⚠ Statement {i} skipped (already exists): {str(e)[:100]}")
                    continue
                else:
                    raise
        
        # Record the migration
        cursor.execute(
            "INSERT INTO schema_migrations (migration_name) VALUES (%s) "
            "ON DUPLICATE KEY UPDATE applied_at = CURRENT_TIMESTAMP",
            (migration_name,)
        )
        
        print(f"[MIGRATION] ✓ Successfully applied: {migration_name}")
        return True
        
    except Exception as e:
        print(f"[MIGRATION] ✗ Error applying {migration_name}: {str(e)}")
        raise


def run_migrations(migrations_dir='migrations', specific_migration=None):
    """Run all pending migrations or a specific migration."""
    print("=" * 70)
    print("DATABASE MIGRATION RUNNER")
    print("=" * 70)
    print(f"Database: {Config.DB_NAME}")
    print(f"Host: {Config.DB_HOST}:{Config.DB_PORT}")
    print(f"Migrations directory: {migrations_dir}")
    print("=" * 70)
    
    conn = get_db_connection()
    
    try:
        with conn.cursor() as cursor:
            # Ensure migrations tracking table exists
            ensure_migrations_table(cursor)
            conn.commit()
            
            # Get applied migrations
            applied = get_applied_migrations(cursor)
            print(f"\n[MIGRATION] Already applied: {len(applied)} migration(s)")
            if applied:
                for migration in sorted(applied):
                    print(f"  ✓ {migration}")
            
            # Get pending migrations
            all_migrations = get_pending_migrations(migrations_dir)
            
            if specific_migration:
                # Run specific migration
                if specific_migration not in all_migrations:
                    print(f"\n[MIGRATION] ✗ Migration '{specific_migration}' not found!")
                    return False
                
                pending = [specific_migration]
                print(f"\n[MIGRATION] Running specific migration: {specific_migration}")
            else:
                # Run all pending migrations
                pending = [m for m in all_migrations if m.replace('.sql', '') not in applied]
            
            if not pending:
                print("\n[MIGRATION] ✓ No pending migrations. Database is up to date!")
                return True
            
            print(f"\n[MIGRATION] Found {len(pending)} pending migration(s):")
            for migration in pending:
                print(f"  → {migration}")
            
            # Execute each pending migration
            print("\n" + "=" * 70)
            print("EXECUTING MIGRATIONS")
            print("=" * 70)
            
            for migration_file in pending:
                try:
                    execute_migration(cursor, migration_file, migrations_dir)
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(f"\n[MIGRATION] ✗ Migration failed: {migration_file}")
                    print(f"[MIGRATION] Error: {str(e)}")
                    print("[MIGRATION] Rolling back...")
                    return False
            
            print("\n" + "=" * 70)
            print("✓ ALL MIGRATIONS COMPLETED SUCCESSFULLY")
            print("=" * 70)
            return True
            
    except Exception as e:
        print(f"\n[MIGRATION] ✗ Fatal error: {str(e)}")
        return False
    finally:
        conn.close()


def rollback_migration(migration_name, migrations_dir='migrations'):
    """Rollback a specific migration (if rollback file exists)."""
    rollback_file = f"{migration_name}_rollback.sql"
    file_path = os.path.join(migrations_dir, rollback_file)
    
    if not os.path.exists(file_path):
        print(f"[ROLLBACK] ✗ Rollback file not found: {rollback_file}")
        return False
    
    print(f"[ROLLBACK] Rolling back: {migration_name}")
    
    conn = get_db_connection()
    
    try:
        with conn.cursor() as cursor:
            # Read and execute rollback file
            with open(file_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement.startswith('--') or not statement:
                    continue
                cursor.execute(statement)
            
            # Remove from migrations table
            cursor.execute(
                "DELETE FROM schema_migrations WHERE migration_name = %s",
                (migration_name,)
            )
            
            conn.commit()
            print(f"[ROLLBACK] ✓ Successfully rolled back: {migration_name}")
            return True
            
    except Exception as e:
        conn.rollback()
        print(f"[ROLLBACK] ✗ Error: {str(e)}")
        return False
    finally:
        conn.close()


def list_migrations(migrations_dir='migrations'):
    """List all migrations and their status."""
    print("=" * 70)
    print("MIGRATION STATUS")
    print("=" * 70)
    
    conn = get_db_connection()
    
    try:
        with conn.cursor() as cursor:
            ensure_migrations_table(cursor)
            applied = get_applied_migrations(cursor)
            all_migrations = get_pending_migrations(migrations_dir)
            
            if not all_migrations:
                print("No migration files found.")
                return
            
            print(f"\nTotal migrations: {len(all_migrations)}")
            print(f"Applied: {len(applied)}")
            print(f"Pending: {len(all_migrations) - len(applied)}\n")
            
            for migration_file in all_migrations:
                migration_name = migration_file.replace('.sql', '')
                status = "✓ APPLIED" if migration_name in applied else "⧗ PENDING"
                print(f"{status:12} {migration_file}")
                
    finally:
        conn.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Database Migration Runner')
    parser.add_argument(
        'command',
        choices=['run', 'list', 'rollback'],
        help='Command to execute'
    )
    parser.add_argument(
        '--migration',
        help='Specific migration to run or rollback'
    )
    parser.add_argument(
        '--dir',
        default='migrations',
        help='Migrations directory (default: migrations)'
    )
    
    args = parser.parse_args()
    
    try:
        if args.command == 'run':
            success = run_migrations(args.dir, args.migration)
            sys.exit(0 if success else 1)
        elif args.command == 'list':
            list_migrations(args.dir)
        elif args.command == 'rollback':
            if not args.migration:
                print("Error: --migration required for rollback")
                sys.exit(1)
            success = rollback_migration(args.migration, args.dir)
            sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[MIGRATION] Interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[MIGRATION] Fatal error: {str(e)}")
        sys.exit(1)
