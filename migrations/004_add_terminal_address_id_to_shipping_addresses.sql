-- Add terminal_address_id column to shipping_addresses table
-- This links local addresses to Terminal Africa addresses

ALTER TABLE shipping_addresses 
ADD COLUMN terminal_address_id VARCHAR(50) DEFAULT NULL,
ADD INDEX idx_terminal_address_id (terminal_address_id);
