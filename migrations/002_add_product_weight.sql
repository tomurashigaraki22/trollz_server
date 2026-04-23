-- Migration: 002_add_product_weight
-- Description: Add weight column to product table for shipping calculations
-- Date: 2026-04-20
-- Phase: 2.3 - Product Weight Management

-- Add weight column to product table if it doesn't exist
-- Note: This might already exist from migration 001, but we ensure it here
ALTER TABLE product
ADD COLUMN IF NOT EXISTS weight DECIMAL(10,2) DEFAULT 0.50 COMMENT 'Product weight in KG';

-- Update existing products with default weight if NULL
UPDATE product SET weight = 0.50 WHERE weight IS NULL OR weight = 0;

-- Record this migration
INSERT INTO schema_migrations (migration_name) 
VALUES ('002_add_product_weight')
ON DUPLICATE KEY UPDATE applied_at = CURRENT_TIMESTAMP;
