import pymysql
from config import Config


def get_db_connection():
    """Create and return a new database connection."""
    connection = pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )
    return connection


def init_db():
    """Initialize database with the exact structure from trollzstorecom_tr0llz_db.sql."""
    # First, create the database if it doesn't exist
    conn_no_db = pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )
    try:
        with conn_no_db.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            print(f"[DB] Database '{Config.DB_NAME}' ensured.")
    finally:
        conn_no_db.close()

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Execute the SQL file using mysql command line tool
            import subprocess
            import os
            
            # Check if the SQL file exists
            if os.path.exists('trollzstorecom_tr0llz_db.sql'):
                try:
                    # Use mysql command to import the SQL file
                    cmd = [
                        'mysql',
                        f'--host={Config.DB_HOST}',
                        f'--port={Config.DB_PORT}',
                        f'--user={Config.DB_USER}',
                        f'--password={Config.DB_PASSWORD}',
                        Config.DB_NAME
                    ]
                    
                    with open('trollzstorecom_tr0llz_db.sql', 'r', encoding='utf-8') as sql_file:
                        result = subprocess.run(cmd, stdin=sql_file, capture_output=True, text=True)
                        
                    if result.returncode == 0:
                        print("[DB] Database initialized successfully with trollzstorecom_tr0llz_db structure.")
                    else:
                        print(f"[DB] Warning during SQL import: {result.stderr}")
                        # Fall back to basic table creation if mysql command fails
                        create_basic_tables(cursor)
                        
                except (subprocess.SubprocessError, FileNotFoundError):
                    print("[DB] MySQL command not available, creating basic tables...")
                    create_basic_tables(cursor)
            else:
                print("[DB] SQL file not found, creating basic tables...")
                create_basic_tables(cursor)

    except Exception as e:
        print(f"[DB] Error initializing database: {e}")
        raise
    finally:
        conn.close()


def create_basic_tables(cursor):
    """Create essential tables if SQL import fails."""
    # Create users table (from the SQL file structure)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `users` (
            `id` int NOT NULL AUTO_INCREMENT,
            `name` varchar(255) NOT NULL,
            `email` varchar(255) NOT NULL,
            `password` varchar(255) NOT NULL,
            `phone` varchar(20) DEFAULT NULL,
            `address` varchar(500) DEFAULT NULL,
            `reset_token` varchar(255) DEFAULT NULL,
            `token_expiry` datetime DEFAULT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    """)
    
    # Create cart table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `cart` (
            `id` int NOT NULL AUTO_INCREMENT,
            `userid` int NOT NULL,
            `pid` int NOT NULL,
            `qty` int NOT NULL DEFAULT '1',
            `size` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
            `color` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """)
    
    # Create category table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `category` (
            `id` int NOT NULL AUTO_INCREMENT,
            `category` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
            `parent_id` int DEFAULT NULL,
            `bg_color` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
            `icon` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
            `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            KEY `fk_category_parent` (`parent_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """)
    
    # Create product table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `product` (
            `id` int NOT NULL AUTO_INCREMENT,
            `item` varchar(255) NOT NULL,
            `category` varchar(50) NOT NULL,
            `subcategory` varchar(100) NOT NULL,
            `parent_category_id` int DEFAULT NULL,
            `subcategory_id` int DEFAULT NULL,
            `price` int NOT NULL,
            `discount` int NOT NULL,
            `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            `category_id` int NOT NULL,
            `supplier` varchar(50) NOT NULL,
            `new` varchar(10) NOT NULL,
            `img` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
            `qty` int NOT NULL,
            `shipped_from_abroad` tinyint(1) DEFAULT NULL,
            `date` datetime DEFAULT CURRENT_TIMESTAMP,
            `is_flash_sale` tinyint(1) DEFAULT '0',
            `flash_sale_price` decimal(10,2) DEFAULT NULL,
            `flash_sale_start` datetime DEFAULT NULL,
            `flash_sale_end` datetime DEFAULT NULL,
            `old_price` decimal(10,2) DEFAULT NULL,
            `color_options` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
            `size_type` enum('none','shoe','cloth') DEFAULT 'none',
            `size_options` text,
            `stock` int NOT NULL DEFAULT '0',
            `views` int DEFAULT '0',
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `orders` (
            `id` int NOT NULL AUTO_INCREMENT,
            `user_id` int NOT NULL,
            `tracking` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
            `total_amount` decimal(10,2) NOT NULL,
            `payment_method` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
            `transaction_id` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
            `payment_status` varchar(50) COLLATE utf8mb4_general_ci DEFAULT 'Pending',
            `order_status` varchar(50) COLLATE utf8mb4_general_ci DEFAULT 'processing',
            `delivery_status` varchar(50) COLLATE utf8mb4_general_ci DEFAULT 'Pending',
            `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
            `address_id` int UNSIGNED DEFAULT NULL,
            `address` text COLLATE utf8mb4_general_ci NOT NULL,
            `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            `stock_restored` tinyint(1) DEFAULT '0',
            PRIMARY KEY (`id`),
            UNIQUE KEY `tracking` (`tracking`),
            KEY `user_id` (`user_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """)
    
    print("[DB] Basic tables created successfully.")
