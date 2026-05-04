-- Terminal Africa Integration Migration
-- Adds Terminal-specific fields and tables for multi-carrier shipping support

-- Add Terminal-specific fields to orders table
-- Note: This will fail silently if columns already exist
ALTER TABLE orders 
ADD COLUMN terminal_shipment_id VARCHAR(50),
ADD COLUMN terminal_rate_id VARCHAR(50),
ADD COLUMN terminal_carrier_id VARCHAR(50),
ADD COLUMN terminal_carrier_name VARCHAR(100),
ADD COLUMN terminal_tracking_url TEXT,
ADD COLUMN terminal_label_url TEXT,
ADD COLUMN terminal_invoice_url TEXT;

-- Create terminal_addresses table (maps to Terminal's address system)
CREATE TABLE IF NOT EXISTS terminal_addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    terminal_address_id VARCHAR(50) UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(255),
    line1 TEXT,
    line2 TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(10),
    zip VARCHAR(20),
    is_residential BOOLEAN DEFAULT TRUE,
    coordinates JSON,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_terminal_address_id (terminal_address_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create terminal_packaging table
CREATE TABLE IF NOT EXISTS terminal_packaging (
    id INT AUTO_INCREMENT PRIMARY KEY,
    terminal_packaging_id VARCHAR(50) UNIQUE,
    name VARCHAR(255),
    type ENUM('box', 'envelope', 'soft-packaging') DEFAULT 'box',
    length DECIMAL(10,2),
    width DECIMAL(10,2),
    height DECIMAL(10,2),
    weight DECIMAL(10,2),
    size_unit VARCHAR(10) DEFAULT 'cm',
    weight_unit VARCHAR(10) DEFAULT 'kg',
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_terminal_packaging_id (terminal_packaging_id),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create terminal_parcels table
CREATE TABLE IF NOT EXISTS terminal_parcels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    terminal_parcel_id VARCHAR(50) UNIQUE,
    order_id INT,
    packaging_id INT,
    description TEXT,
    items JSON,
    total_weight DECIMAL(10,2),
    weight_unit VARCHAR(10) DEFAULT 'kg',
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (packaging_id) REFERENCES terminal_packaging(id),
    INDEX idx_terminal_parcel_id (terminal_parcel_id),
    INDEX idx_order_id (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create terminal_carriers table
CREATE TABLE IF NOT EXISTS terminal_carriers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    terminal_carrier_id VARCHAR(50) UNIQUE,
    name VARCHAR(255),
    slug VARCHAR(100),
    logo TEXT,
    active BOOLEAN DEFAULT TRUE,
    domestic BOOLEAN DEFAULT FALSE,
    regional BOOLEAN DEFAULT FALSE,
    international BOOLEAN DEFAULT FALSE,
    requires_invoice BOOLEAN DEFAULT FALSE,
    requires_waybill BOOLEAN DEFAULT FALSE,
    supports_multi_parcels BOOLEAN DEFAULT FALSE,
    contact JSON,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_terminal_carrier_id (terminal_carrier_id),
    INDEX idx_slug (slug),
    INDEX idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create terminal_rates table (cache rates for performance)
CREATE TABLE IF NOT EXISTS terminal_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    terminal_rate_id VARCHAR(50) UNIQUE,
    order_id INT,
    carrier_id INT,
    amount DECIMAL(10,2),
    currency VARCHAR(10) DEFAULT 'NGN',
    delivery_time VARCHAR(255),
    pickup_time VARCHAR(255),
    includes_insurance BOOLEAN DEFAULT FALSE,
    insurance_fee DECIMAL(10,2) DEFAULT 0,
    metadata JSON,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (carrier_id) REFERENCES terminal_carriers(id),
    INDEX idx_terminal_rate_id (terminal_rate_id),
    INDEX idx_order_id (order_id),
    INDEX idx_expires_at (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default packaging options
INSERT INTO terminal_packaging (name, type, length, width, height, weight, size_unit, weight_unit, is_default)
VALUES 
    ('Small Box', 'box', 20, 15, 10, 0.5, 'cm', 'kg', TRUE),
    ('Medium Box', 'box', 30, 25, 20, 1.0, 'cm', 'kg', TRUE),
    ('Large Box', 'box', 40, 35, 30, 1.5, 'cm', 'kg', TRUE),
    ('Envelope', 'envelope', 30, 20, 2, 0.1, 'cm', 'kg', TRUE),
    ('Soft Package', 'soft-packaging', 35, 25, 5, 0.3, 'cm', 'kg', TRUE)
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;
