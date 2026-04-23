-- Migration: 001_add_sendbox_fields
-- Description: Add Sendbox integration fields to orders table
-- Date: 2026-04-20
-- Phase: 1.2 - Database Schema Updates

-- Add Sendbox-related columns to orders table
ALTER TABLE orders
ADD COLUMN IF NOT EXISTS sendbox_shipment_id VARCHAR(100) NULL COMMENT 'Sendbox shipment ID',
ADD COLUMN IF NOT EXISTS sendbox_tracking_code VARCHAR(100) NULL COMMENT 'Sendbox tracking code',
ADD COLUMN IF NOT EXISTS sendbox_status VARCHAR(50) NULL COMMENT 'Current Sendbox shipment status',
ADD COLUMN IF NOT EXISTS sendbox_carrier VARCHAR(100) NULL COMMENT 'Shipping carrier name',
ADD COLUMN IF NOT EXISTS shipping_cost DECIMAL(10,2) DEFAULT 0.00 COMMENT 'Shipping cost in NGN',
ADD COLUMN IF NOT EXISTS estimated_delivery_date DATE NULL COMMENT 'Estimated delivery date',
ADD COLUMN IF NOT EXISTS sendbox_webhook_data JSON NULL COMMENT 'Raw webhook data from Sendbox';

-- Add indexes for better query performance
ALTER TABLE orders
ADD INDEX IF NOT EXISTS idx_sendbox_tracking (sendbox_tracking_code),
ADD INDEX IF NOT EXISTS idx_sendbox_shipment (sendbox_shipment_id),
ADD INDEX IF NOT EXISTS idx_sendbox_status (sendbox_status);

-- Create shipping_addresses table for structured address storage
CREATE TABLE IF NOT EXISTS shipping_addresses (
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
    lng DECIMAL(10,7) COMMENT 'Longitude for mapping',
    lat DECIMAL(10,7) COMMENT 'Latitude for mapping',
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_addresses (user_id),
    INDEX idx_user_default (user_id, is_default)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create shipping_quotes table for quote history
CREATE TABLE IF NOT EXISTS shipping_quotes (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create webhook_events table for logging Sendbox webhooks
CREATE TABLE IF NOT EXISTS webhook_events (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add weight column to product table for shipping calculations
ALTER TABLE product
ADD COLUMN IF NOT EXISTS weight DECIMAL(10,2) DEFAULT 0.50 COMMENT 'Product weight in KG';

-- Create migration tracking table
CREATE TABLE IF NOT EXISTS schema_migrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    migration_name VARCHAR(255) NOT NULL UNIQUE,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_migration_name (migration_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Record this migration
INSERT INTO schema_migrations (migration_name) 
VALUES ('001_add_sendbox_fields')
ON DUPLICATE KEY UPDATE applied_at = CURRENT_TIMESTAMP;
