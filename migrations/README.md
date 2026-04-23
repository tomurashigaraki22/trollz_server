# Database Migrations

This directory contains SQL migration files for the Trollz Store database schema.

## Migration Files

Migrations are numbered sequentially and should be executed in order:

- `001_add_sendbox_fields.sql` - Adds Sendbox integration fields and tables

## Running Migrations

### Run All Pending Migrations

```bash
python run_migrations.py run
```

### Run a Specific Migration

```bash
python run_migrations.py run --migration 001_add_sendbox_fields.sql
```

### List Migration Status

```bash
python run_migrations.py list
```

### Rollback a Migration

```bash
python run_migrations.py rollback --migration 001_add_sendbox_fields
```

Note: Rollback requires a corresponding `*_rollback.sql` file.

## Migration Tracking

Migrations are tracked in the `schema_migrations` table. This table is automatically created when you run migrations for the first time.

## Creating New Migrations

1. Create a new SQL file with a sequential number prefix:
   ```
   002_your_migration_name.sql
   ```

2. Write your migration SQL statements

3. Optionally create a rollback file:
   ```
   002_your_migration_name_rollback.sql
   ```

4. Run the migration:
   ```bash
   python run_migrations.py run
   ```

## Migration Best Practices

- Always test migrations on a development database first
- Use `IF NOT EXISTS` clauses where appropriate
- Include comments explaining what the migration does
- Create rollback scripts for complex migrations
- Keep migrations small and focused
- Never modify existing migration files after they've been applied

## Schema Changes in 001_add_sendbox_fields

This migration adds:

### Orders Table Updates
- `sendbox_shipment_id` - Sendbox shipment ID
- `sendbox_tracking_code` - Sendbox tracking code
- `sendbox_status` - Current Sendbox status
- `sendbox_carrier` - Carrier name
- `shipping_cost` - Shipping cost in NGN
- `estimated_delivery_date` - Estimated delivery date
- `sendbox_webhook_data` - JSON field for webhook data

### New Tables
- `shipping_addresses` - Structured address storage
- `shipping_quotes` - Shipping quote history
- `webhook_events` - Webhook event logging
- `schema_migrations` - Migration tracking

### Product Table Updates
- `weight` - Product weight in KG for shipping calculations

## Troubleshooting

### Migration Fails with "Duplicate column" Error

This is usually safe to ignore. The migration script handles this gracefully.

### Migration Fails with Permission Error

Ensure your database user has the following permissions:
- CREATE
- ALTER
- INSERT
- SELECT
- INDEX

### Need to Revert a Migration

1. Create a rollback SQL file
2. Run: `python run_migrations.py rollback --migration <name>`

### Check What Migrations Have Been Applied

```bash
python run_migrations.py list
```
