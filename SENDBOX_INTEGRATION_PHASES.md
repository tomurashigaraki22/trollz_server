# Sendbox API Integration - Phased Implementation Plan

## Overview
This document outlines a phased approach to integrate Sendbox shipping API into the Trollz Store e-commerce platform. The integration will enable automated shipping quotes, shipment creation, real-time tracking, and landed cost calculations for both local and international deliveries.

---

## Current System Analysis

### Existing Order System
- Orders table with tracking numbers (format: `TS{timestamp}{random}`)
- Order statuses: `processing`, `shipped`, `delivered`, `cancelled`
- Delivery statuses: `Pending`, `in_transit`, `delivered`
- Payment integration: Flutterwave, Paystack, Cash on Delivery
- Address field stores full delivery address as string

### Integration Points
1. Checkout flow - Get shipping quotes before order creation
2. Order creation - Create Sendbox shipment automatically
3. Order tracking - Sync Sendbox tracking with internal tracking
4. Admin dashboard - Update order status from Sendbox webhooks
5. Customer tracking - Display real-time Sendbox tracking info

---

## Phase 1: Foundation Setup (Week 1)

### 1.1 Environment Configuration
**Goal:** Set up Sendbox API credentials and configuration

**Tasks:**
- [ ] Register on Sendbox Developer Portal (staging): https://developers.staging.sendbox.co/
- [ ] Create application and obtain API keys
- [ ] Add Sendbox configuration to `config.py`:
  ```python
  # Sendbox API Configuration
  SENDBOX_STAGING_URL = "https://sandbox.staging.sendbox.co"
  SENDBOX_LIVE_URL = "https://live.sendbox.co"
  SENDBOX_API_KEY = os.getenv("SENDBOX_API_KEY", "")
  SENDBOX_ENVIRONMENT = os.getenv("SENDBOX_ENV", "staging")  # staging or live
  ```
- [ ] Update `.env` file with Sendbox credentials
- [ ] Add Sendbox base URL helper in `config.py`

**Deliverables:**
- Updated `config.py` with Sendbox settings
- Environment variables documented in README

### 1.2 Database Schema Updates
**Goal:** Extend database to support Sendbox integration

**Tasks:**
- [ ] Create migration script to add Sendbox fields to orders table:
  ```sql
  ALTER TABLE orders
  ADD COLUMN sendbox_shipment_id VARCHAR(100) NULL,
  ADD COLUMN sendbox_tracking_code VARCHAR(100) NULL,
  ADD COLUMN sendbox_status VARCHAR(50) NULL,
  ADD COLUMN sendbox_carrier VARCHAR(100) NULL,
  ADD COLUMN shipping_cost DECIMAL(10,2) DEFAULT 0.00,
  ADD COLUMN estimated_delivery_date DATE NULL,
  ADD COLUMN sendbox_webhook_data JSON NULL,
  ADD INDEX idx_sendbox_tracking (sendbox_tracking_code),
  ADD INDEX idx_sendbox_shipment (sendbox_shipment_id);
  ```
- [ ] Create `shipping_addresses` table for structured address storage:
  ```sql
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
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_default (user_id, is_default)
  );
  ```
- [ ] Create `shipping_quotes` table for quote history:
  ```sql
  CREATE TABLE shipping_quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    origin_state VARCHAR(100),
    destination_state VARCHAR(100),
    weight DECIMAL(10,2),
    service_type VARCHAR(50),
    service_code VARCHAR(50),
    carrier VARCHAR(100),
    quoted_price DECIMAL(10,2),
    currency VARCHAR(3) DEFAULT 'NGN',
    quote_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_quotes (user_id, created_at)
  );
  ```

**Deliverables:**
- Migration SQL script: `migrations/001_add_sendbox_fields.sql`
- Updated database schema documentation

### 1.3 Sendbox Service Module
**Goal:** Create reusable Sendbox API client

**Tasks:**
- [ ] Create `services/sendbox_service.py` with base API client
- [ ] Implement authentication headers
- [ ] Add error handling and logging
- [ ] Create helper methods for common operations

**Deliverables:**
- `services/sendbox_service.py` with SendboxClient class

---

## Phase 2: Shipping Quotes Integration (Week 2)

### 2.1 Address Management API
**Goal:** Enable users to save and manage shipping addresses

**Tasks:**
- [ ] Create `routes/addresses.py` blueprint
- [ ] Implement endpoints:
  - `POST /api/addresses` - Save new address
  - `GET /api/addresses` - List user addresses
  - `GET /api/addresses/<id>` - Get single address
  - `PUT /api/addresses/<id>` - Update address
  - `DELETE /api/addresses/<id>` - Delete address
  - `POST /api/addresses/<id>/set-default` - Set default address
- [ ] Add address validation (state, country codes)
- [ ] Register blueprint in `app.py`

**Deliverables:**
- `routes/addresses.py` with full CRUD operations
- Address validation utilities

### 2.2 Shipping Quotes Endpoint
**Goal:** Get real-time shipping quotes from Sendbox

**Tasks:**
- [ ] Add `get_shipping_quotes()` method to SendboxClient
- [ ] Create endpoint `POST /api/shipping/quotes`
- [ ] Accept payload:
  ```json
  {
    "destination_address_id": 123,
    "items": [
      {
        "product_id": 55,
        "quantity": 2,
        "name": "Product Name",
        "value": 15000,
        "weight": 2.5
      }
    ],
    "service_code": "standard",
    "pickup_date": "2026-04-25"
  }
  ```
- [ ] Calculate total weight from items
- [ ] Get origin address from config (warehouse/store address)
- [ ] Call Sendbox API and return quotes
- [ ] Save quotes to `shipping_quotes` table
- [ ] Return formatted response with multiple carrier options

**Deliverables:**
- Shipping quotes endpoint in `routes/shipping.py`
- Quote calculation and formatting logic

### 2.3 Product Weight Management
**Goal:** Add weight field to products for shipping calculations

**Tasks:**
- [ ] Add `weight` column to products table:
  ```sql
  ALTER TABLE product
  ADD COLUMN weight DECIMAL(10,2) DEFAULT 0.50 COMMENT 'Weight in KG';
  ```
- [ ] Update product creation/update endpoints to accept weight
- [ ] Add weight to product response serialization
- [ ] Create admin UI consideration for weight input

**Deliverables:**
- Updated product schema with weight field
- Weight validation in product endpoints

---

## Phase 3: Shipment Creation (Week 3)

### 3.1 Checkout Flow Enhancement
**Goal:** Integrate shipping quotes into checkout process

**Tasks:**
- [ ] Modify `POST /api/checkout` to accept shipping quote selection:
  ```json
  {
    "address_id": 123,
    "payment_method": "flutterwave",
    "items": [...],
    "selected_shipping": {
      "quote_id": 456,
      "carrier": "DHL",
      "service_code": "standard",
      "shipping_cost": 5000
    }
  }
  ```
- [ ] Validate selected shipping quote
- [ ] Add shipping cost to order total
- [ ] Store shipping details in order record

**Deliverables:**
- Enhanced checkout endpoint with shipping selection
- Updated order total calculation

### 3.2 Automatic Shipment Creation
**Goal:** Create Sendbox shipment when order is paid

**Tasks:**
- [ ] Add `create_shipment()` method to SendboxClient
- [ ] Implement shipment creation logic:
  - Trigger on order payment confirmation
  - Map order items to Sendbox items format
  - Include HTS codes for international shipments
  - Set pickup date (next business day)
  - Include callback URL for webhooks
- [ ] Update order with Sendbox shipment ID and tracking code
- [ ] Handle creation errors gracefully
- [ ] Add retry mechanism for failed shipments

**Deliverables:**
- Shipment creation service method
- Order update logic with Sendbox data
- Error handling and logging

### 3.3 Landed Cost Calculator
**Goal:** Show customers total landed cost for international orders

**Tasks:**
- [ ] Add `calculate_landed_cost()` method to SendboxClient
- [ ] Create endpoint `POST /api/shipping/landed-cost`
- [ ] Display duties, taxes, and fees breakdown
- [ ] Integrate into checkout for international orders
- [ ] Show currency conversion rates

**Deliverables:**
- Landed cost calculation endpoint
- Cost breakdown display format

---

## Phase 4: Tracking Integration (Week 4)

### 4.1 Sendbox Tracking Sync
**Goal:** Sync Sendbox tracking status with internal orders

**Tasks:**
- [ ] Add `track_shipment()` method to SendboxClient
- [ ] Create endpoint `GET /api/shipping/track/<tracking_code>`
- [ ] Map Sendbox statuses to internal statuses:
  ```python
  SENDBOX_STATUS_MAP = {
      "drafted": "processing",
      "pending": "processing",
      "pickup_started": "processing",
      "pickup_completed": "shipped",
      "in_transit": "shipped",
      "in_delivery": "shipped",
      "delivered": "delivered"
  }
  ```
- [ ] Update order status based on Sendbox tracking
- [ ] Store tracking history in `sendbox_webhook_data` JSON field

**Deliverables:**
- Tracking sync service
- Status mapping configuration
- Enhanced tracking endpoint

### 4.2 Webhook Handler
**Goal:** Receive real-time updates from Sendbox

**Tasks:**
- [ ] Create `routes/webhooks.py` blueprint
- [ ] Implement `POST /api/webhooks/sendbox` endpoint
- [ ] Verify webhook authenticity (if Sendbox provides signature)
- [ ] Parse webhook payload
- [ ] Update order status automatically
- [ ] Log all webhook events
- [ ] Send customer notifications on status changes

**Deliverables:**
- Webhook handler endpoint
- Webhook event logging
- Automated status updates

### 4.3 Customer Tracking Page Enhancement
**Goal:** Show rich tracking information to customers

**Tasks:**
- [ ] Enhance `GET /api/orders/track/<tracking_number>` response
- [ ] Include Sendbox tracking timeline
- [ ] Show carrier information
- [ ] Display estimated delivery date
- [ ] Add tracking map/visualization data (if available)
- [ ] Return formatted tracking events

**Deliverables:**
- Enhanced tracking response format
- Tracking timeline data structure

---

## Phase 5: Admin Features (Week 5)

### 5.1 Admin Shipment Management
**Goal:** Give admins control over Sendbox shipments

**Tasks:**
- [ ] Create admin endpoints:
  - `POST /api/admin/orders/<id>/create-shipment` - Manually create shipment
  - `POST /api/admin/orders/<id>/cancel-shipment` - Cancel Sendbox shipment
  - `GET /api/admin/orders/<id>/sendbox-details` - View full Sendbox data
  - `POST /api/admin/orders/<id>/refresh-tracking` - Force tracking update
- [ ] Add shipment creation for existing orders
- [ ] Implement shipment cancellation with stock restoration
- [ ] Add bulk shipment creation for multiple orders

**Deliverables:**
- Admin shipment management endpoints
- Bulk operations support

### 5.2 Shipping Reports
**Goal:** Provide shipping analytics for admins

**Tasks:**
- [ ] Create endpoint `GET /api/admin/reports/shipping`
- [ ] Generate reports:
  - Total shipping costs by period
  - Most used carriers
  - Average delivery times
  - Failed shipments
  - Shipping cost vs order value ratio
- [ ] Add date range filters
- [ ] Export to CSV/JSON

**Deliverables:**
- Shipping reports endpoint
- Analytics calculations

### 5.3 Sendbox Account Management
**Goal:** Monitor Sendbox account status

**Tasks:**
- [ ] Add `get_account_balance()` method to SendboxClient
- [ ] Create endpoint `GET /api/admin/sendbox/account`
- [ ] Display account balance
- [ ] Show recent transactions
- [ ] Add low balance alerts
- [ ] For staging: Implement fund account feature

**Deliverables:**
- Account status endpoint
- Balance monitoring

---

## Phase 6: Testing & Optimization (Week 6)

### 6.1 Staging Environment Testing
**Goal:** Thoroughly test all Sendbox integrations

**Tasks:**
- [ ] Fund staging account using `POST /payments/add_money`
- [ ] Test complete order flow:
  1. Get shipping quotes
  2. Create order with shipping
  3. Create Sendbox shipment
  4. Simulate tracking updates
  5. Verify webhook handling
- [ ] Test edge cases:
  - Invalid addresses
  - Insufficient stock
  - Payment failures
  - Shipment creation failures
  - Webhook failures
- [ ] Test international shipments with landed costs
- [ ] Verify all status mappings
- [ ] Test admin operations

**Deliverables:**
- Test cases documentation
- Bug fixes and improvements

### 6.2 Error Handling & Resilience
**Goal:** Ensure system handles failures gracefully

**Tasks:**
- [ ] Implement retry logic for API calls
- [ ] Add circuit breaker for Sendbox API
- [ ] Create fallback mechanisms:
  - Manual shipment creation if auto-creation fails
  - Manual tracking updates if webhooks fail
- [ ] Add comprehensive error logging
- [ ] Create admin alerts for critical failures
- [ ] Implement queue system for shipment creation (optional)

**Deliverables:**
- Robust error handling
- Retry and fallback mechanisms
- Monitoring and alerting

### 6.3 Performance Optimization
**Goal:** Optimize API calls and database queries

**Tasks:**
- [ ] Cache shipping quotes for similar requests
- [ ] Batch shipment creation for multiple orders
- [ ] Optimize tracking queries with indexes
- [ ] Implement rate limiting for Sendbox API calls
- [ ] Add request/response caching where appropriate
- [ ] Monitor API response times

**Deliverables:**
- Performance improvements
- Caching strategy
- Rate limiting implementation

---

## Phase 7: Production Deployment (Week 7)

### 7.1 Production Configuration
**Goal:** Prepare for live Sendbox API usage

**Tasks:**
- [ ] Obtain production Sendbox API keys
- [ ] Update environment variables for production
- [ ] Configure production webhook URL
- [ ] Set up production origin address (warehouse)
- [ ] Update all API URLs to live endpoints
- [ ] Configure production callback URLs

**Deliverables:**
- Production configuration
- Environment setup documentation

### 7.2 Data Migration
**Goal:** Migrate existing orders if needed

**Tasks:**
- [ ] Analyze existing orders without Sendbox data
- [ ] Create migration script for historical orders (optional)
- [ ] Backfill shipping costs from historical data
- [ ] Update order statuses to match new system

**Deliverables:**
- Migration scripts
- Data validation reports

### 7.3 Monitoring & Logging
**Goal:** Set up production monitoring

**Tasks:**
- [ ] Configure application logging for Sendbox operations
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Create dashboard for Sendbox metrics:
  - Shipments created per day
  - Failed shipments
  - Average shipping costs
  - Delivery success rate
- [ ] Set up alerts for:
  - Sendbox API failures
  - Webhook failures
  - Low account balance
  - High failure rates

**Deliverables:**
- Logging configuration
- Monitoring dashboard
- Alert system

### 7.4 Documentation & Training
**Goal:** Document system and train team

**Tasks:**
- [ ] Update API documentation with shipping endpoints
- [ ] Create admin user guide for Sendbox features
- [ ] Document troubleshooting procedures
- [ ] Create runbook for common issues
- [ ] Train support team on tracking and shipment management
- [ ] Document webhook handling and debugging

**Deliverables:**
- Complete API documentation
- Admin user guide
- Troubleshooting runbook
- Training materials

---

## Phase 8: Advanced Features (Future Enhancements)

### 8.1 Multi-Warehouse Support
- Support multiple origin addresses
- Route orders to nearest warehouse
- Warehouse-specific inventory

### 8.2 Shipping Rules Engine
- Automatic carrier selection based on rules
- Free shipping thresholds
- Shipping discounts and promotions
- Zone-based pricing

### 8.3 Returns Management
- Create return shipments via Sendbox
- Return tracking
- Refund automation

### 8.4 Customer Preferences
- Preferred carriers
- Delivery time windows
- Special delivery instructions
- SMS/Email tracking notifications

---

## Technical Architecture

### Service Layer Structure
```
services/
├── sendbox_service.py       # Main Sendbox API client
├── shipping_calculator.py   # Shipping cost calculations
├── address_validator.py     # Address validation
└── tracking_sync.py         # Tracking synchronization
```

### Route Structure
```
routes/
├── addresses.py             # Address management
├── shipping.py              # Shipping quotes & operations
├── webhooks.py              # Sendbox webhook handler
└── orders.py                # Enhanced with shipping
```

### Database Tables
- `orders` - Enhanced with Sendbox fields
- `shipping_addresses` - Structured address storage
- `shipping_quotes` - Quote history
- `webhook_events` - Webhook log (optional)

---

## Risk Mitigation

### Technical Risks
1. **Sendbox API Downtime**
   - Mitigation: Fallback to manual shipment creation
   - Queue failed requests for retry

2. **Webhook Delivery Failures**
   - Mitigation: Polling mechanism as backup
   - Manual tracking refresh option

3. **Address Validation Issues**
   - Mitigation: Allow manual address override
   - Provide address correction suggestions

### Business Risks
1. **Shipping Cost Accuracy**
   - Mitigation: Regular quote validation
   - Admin review for high-value shipments

2. **International Shipment Complexity**
   - Mitigation: Phased rollout (local first, then international)
   - Clear customer communication about customs

---

## Success Metrics

### Phase Completion Metrics
- [ ] 100% of new orders create Sendbox shipments automatically
- [ ] Shipping quotes displayed in <2 seconds
- [ ] 95%+ webhook delivery success rate
- [ ] Zero manual tracking updates needed
- [ ] Admin can manage all shipments from dashboard

### Business Metrics
- Reduction in shipping-related customer support tickets
- Improved delivery time accuracy
- Increased customer satisfaction with tracking
- Reduced shipping costs through carrier optimization

---

## Timeline Summary

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| Phase 1: Foundation | Week 1 | Config, DB schema, base service |
| Phase 2: Quotes | Week 2 | Address management, shipping quotes |
| Phase 3: Shipments | Week 3 | Checkout integration, shipment creation |
| Phase 4: Tracking | Week 4 | Tracking sync, webhooks |
| Phase 5: Admin | Week 5 | Admin features, reports |
| Phase 6: Testing | Week 6 | Comprehensive testing, optimization |
| Phase 7: Production | Week 7 | Deployment, monitoring |
| Phase 8: Advanced | Future | Enhanced features |

**Total Estimated Time:** 7 weeks for core integration

---

## Next Steps

1. Review and approve this integration plan
2. Set up Sendbox staging account
3. Begin Phase 1: Foundation Setup
4. Schedule weekly progress reviews
5. Assign development resources to each phase

---

## Support & Resources

- **Sendbox Documentation:** https://developers.sendbox.co/
- **Sendbox Staging Portal:** https://developers.staging.sendbox.co/
- **Sendbox Support:** Contact via developer portal
- **Internal Documentation:** See `SENDBOX_D.md` for API reference

---

## Appendix

### A. Sample Sendbox Payloads

#### Shipping Quote Request
```json
{
  "origin": {
    "first_name": "Trollz Store",
    "last_name": "Warehouse",
    "street": "10 Warehouse Street",
    "state": "Lagos",
    "city": "Ikeja",
    "country": "NG",
    "post_code": "100001",
    "phone": "+234 800 000 0000"
  },
  "destination": {
    "first_name": "John",
    "last_name": "Doe",
    "street": "123 Customer Street",
    "state": "Abuja",
    "city": "Maitama",
    "country": "NG",
    "post_code": "900001",
    "phone": "+234 800 111 1111"
  },
  "weight": 2.5,
  "dimension": {
    "length": 30,
    "width": 20,
    "height": 15
  },
  "incoming_option": "pickup",
  "region": "NG",
  "service_type": "local",
  "package_type": "general",
  "total_value": 50000,
  "currency": "NGN",
  "channel_code": "api",
  "pickup_date": "2026-04-25",
  "service_code": "standard"
}
```

#### Shipment Creation Request
```json
{
  "origin": { /* same as above */ },
  "destination": { /* same as above */ },
  "weight": 2.5,
  "dimension": { /* same as above */ },
  "incoming_option": "pickup",
  "region": "NG",
  "service_type": "local",
  "package_type": "general",
  "total_value": 50000,
  "currency": "NGN",
  "channel_code": "api",
  "pickup_date": "2026-04-25",
  "items": [
    {
      "name": "Midea Refrigerator",
      "quantity": 1,
      "value": 50000,
      "weight": 2.5,
      "description": "173L Double Door Refrigerator"
    }
  ],
  "service_code": "standard",
  "callback_url": "https://yourdomain.com/api/webhooks/sendbox"
}
```

### B. Status Mapping Reference

| Sendbox Status | Internal Order Status | Internal Delivery Status |
|----------------|----------------------|-------------------------|
| drafted | processing | Pending |
| pending | processing | Pending |
| pickup_started | processing | Pending |
| pickup_completed | shipped | in_transit |
| in_transit | shipped | in_transit |
| in_delivery | shipped | in_transit |
| delivered | delivered | delivered |

### C. Environment Variables Checklist

```bash
# Sendbox Configuration
SENDBOX_API_KEY=your_sendbox_api_key_here
SENDBOX_ENV=staging  # or 'live' for production
SENDBOX_WEBHOOK_SECRET=your_webhook_secret  # if provided by Sendbox

# Warehouse/Origin Address
WAREHOUSE_FIRST_NAME=Trollz Store
WAREHOUSE_LAST_NAME=Warehouse
WAREHOUSE_STREET=10 Warehouse Street
WAREHOUSE_CITY=Ikeja
WAREHOUSE_STATE=Lagos
WAREHOUSE_COUNTRY=NG
WAREHOUSE_POST_CODE=100001
WAREHOUSE_PHONE=+234 800 000 0000
WAREHOUSE_EMAIL=warehouse@trollzstore.com
```

---

**Document Version:** 1.0  
**Last Updated:** April 20, 2026  
**Author:** Development Team  
**Status:** Ready for Review
