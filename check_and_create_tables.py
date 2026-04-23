"""
Check and create Sendbox tables if they don't exist
"""

from db import get_db_connection

def check_and_create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if shipping_addresses exists
    cursor.execute("SHOW TABLES LIKE 'shipping_addresses'")
    if not cursor.fetchone():
        print("❌ shipping_addresses table does not exist")
        print("Creating shipping_addresses table...")
        
        cursor.execute("""
            CREATE TABLE shipping_addresses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(255),
                street VARCHAR(255) NOT NULL,
                street_line_2 VARCHAR(255),
                city VARCHAR(100) NOT NULL,
                state VARCHAR(100) NOT NULL,
                country VARCHAR(2) DEFAULT 'NG',
                post_code VARCHAR(20),
                lng DECIMAL(10,7),
                lat DECIMAL(10,7),
                is_default BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_user_addresses (user_id),
                INDEX idx_user_default (user_id, is_default)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ shipping_addresses table created")
    else:
        print("✅ shipping_addresses table exists")
    
    # Check if shipping_quotes exists
    cursor.execute("SHOW TABLES LIKE 'shipping_quotes'")
    if not cursor.fetchone():
        print("❌ shipping_quotes table does not exist")
        print("Creating shipping_quotes table...")
        
        cursor.execute("""
            CREATE TABLE shipping_quotes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                origin_state VARCHAR(100),
                origin_city VARCHAR(100),
                destination_state VARCHAR(100),
                destination_city VARCHAR(100),
                weight DECIMAL(10,2) COMMENT 'Total weight in KG',
                service_type VARCHAR(50) COMMENT 'local, international, nation-wide',
                service_code VARCHAR(50) COMMENT 'standard, premium, expedient',
                carrier VARCHAR(100) COMMENT 'Carrier name',
                quoted_price DECIMAL(10,2) COMMENT 'Quoted shipping price',
                currency VARCHAR(3) DEFAULT 'NGN',
                quote_data JSON COMMENT 'Full quote response from Sendbox',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NULL COMMENT 'Quote expiration time',
                INDEX idx_user_quotes (user_id, created_at),
                INDEX idx_quote_expiry (expires_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ shipping_quotes table created")
    else:
        print("✅ shipping_quotes table exists")
    
    # Check if webhook_events exists
    cursor.execute("SHOW TABLES LIKE 'webhook_events'")
    if not cursor.fetchone():
        print("❌ webhook_events table does not exist")
        print("Creating webhook_events table...")
        
        cursor.execute("""
            CREATE TABLE webhook_events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_type VARCHAR(100) NOT NULL COMMENT 'Type of webhook event',
                order_id INT NULL,
                sendbox_tracking_code VARCHAR(100),
                payload JSON NOT NULL COMMENT 'Full webhook payload',
                processed BOOLEAN DEFAULT FALSE,
                processed_at TIMESTAMP NULL,
                error_message TEXT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE SET NULL,
                INDEX idx_event_type (event_type),
                INDEX idx_tracking_code (sendbox_tracking_code),
                INDEX idx_processed (processed, created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ webhook_events table created")
    else:
        print("✅ webhook_events table exists")
    
    # Check if orders table has sendbox columns
    cursor.execute("SHOW COLUMNS FROM orders LIKE 'sendbox_shipment_id'")
    if not cursor.fetchone():
        print("❌ orders table missing Sendbox columns")
        print("Adding Sendbox columns to orders table...")
        
        cursor.execute("""
            ALTER TABLE orders
            ADD COLUMN sendbox_shipment_id VARCHAR(100) NULL COMMENT 'Sendbox shipment ID',
            ADD COLUMN sendbox_tracking_code VARCHAR(100) NULL COMMENT 'Sendbox tracking code',
            ADD COLUMN sendbox_status VARCHAR(50) NULL COMMENT 'Current Sendbox shipment status',
            ADD COLUMN sendbox_carrier VARCHAR(100) NULL COMMENT 'Shipping carrier name',
            ADD COLUMN shipping_cost DECIMAL(10,2) DEFAULT 0.00 COMMENT 'Shipping cost in NGN',
            ADD COLUMN estimated_delivery_date DATE NULL COMMENT 'Estimated delivery date',
            ADD COLUMN sendbox_webhook_data JSON NULL COMMENT 'Raw webhook data from Sendbox',
            ADD INDEX idx_sendbox_tracking (sendbox_tracking_code),
            ADD INDEX idx_sendbox_shipment (sendbox_shipment_id),
            ADD INDEX idx_sendbox_status (sendbox_status)
        """)
        print("✅ Sendbox columns added to orders table")
    else:
        print("✅ orders table has Sendbox columns")
    
    # Check if product table has weight column
    cursor.execute("SHOW COLUMNS FROM product LIKE 'weight'")
    if not cursor.fetchone():
        print("❌ product table missing weight column")
        print("Adding weight column to product table...")
        
        cursor.execute("""
            ALTER TABLE product
            ADD COLUMN weight DECIMAL(10,2) DEFAULT 0.50 COMMENT 'Product weight in KG'
        """)
        print("✅ weight column added to product table")
    else:
        print("✅ product table has weight column")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ ALL TABLES CHECKED AND CREATED SUCCESSFULLY")
    print("="*60)

if __name__ == '__main__':
    check_and_create_tables()
