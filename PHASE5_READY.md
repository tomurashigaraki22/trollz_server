# Phase 5 Ready - Admin Features

## Status: ✅ COMPLETE

Phase 5 of the Sendbox API integration is now complete and ready for use!

---

## What's New in Phase 5

### 🛠️ Advanced Shipment Management
- Cancel shipments with optional stock restoration
- Bulk create shipments for multiple orders
- Detailed success/failure reporting
- Audit logging for all admin actions

### 📊 Comprehensive Shipping Reports
- Summary and detailed analytics
- Carrier performance metrics
- Delivery success rates
- Cost analysis and trends
- Customizable date ranges

### 💰 Sendbox Account Management
- View account balance and info
- Fund staging account for testing
- List all Sendbox shipments
- Monitor API usage

---

## New Admin Endpoints

### Shipment Management:

**POST /api/admin/orders/<id>/cancel-shipment**
- Cancel shipment and restore stock
- Requires admin authentication

**POST /api/admin/orders/bulk-create-shipments**
- Create shipments for multiple orders
- Batch processing with detailed results

### Reports:

**GET /api/admin/reports/shipping**
- Generate shipping analytics
- Summary or detailed reports
- Date range filtering

### Account:

**GET /api/admin/sendbox/account**
- View Sendbox account info
- Check balance

**POST /api/admin/sendbox/fund-account**
- Fund staging account (staging only)

**GET /api/admin/sendbox/shipments**
- List all Sendbox shipments

---

## Quick Start Examples

### 1. Cancel a Shipment

```bash
curl -X POST http://localhost:4500/api/admin/orders/123/cancel-shipment \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "restore_stock": true,
    "reason": "Customer requested cancellation"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Shipment cancelled successfully",
  "data": {
    "order_id": 123,
    "stock_restored": true,
    "restored_items": [...]
  }
}
```

---

### 2. Bulk Create Shipments

```bash
curl -X POST http://localhost:4500/api/admin/orders/bulk-create-shipments \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "order_ids": [1, 2, 3, 4, 5],
    "service_code": "standard"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Created 4 of 5 shipments",
  "data": {
    "success": [
      {"order_id": 1, "tracking_code": "SB123456"},
      {"order_id": 2, "tracking_code": "SB123457"}
    ],
    "failed": [
      {"order_id": 5, "error": "No shipping address"}
    ],
    "total": 5
  }
}
```

---

### 3. Generate Shipping Report

```bash
# Summary report for last 30 days
curl http://localhost:4500/api/admin/reports/shipping \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"

# Detailed report with custom date range
curl "http://localhost:4500/api/admin/reports/shipping?start_date=2026-03-01&end_date=2026-04-20&report_type=detailed" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "period": {
      "start_date": "2026-03-21",
      "end_date": "2026-04-20"
    },
    "summary": {
      "total_shipments": 150,
      "total_shipping_cost": 750000,
      "avg_shipping_cost": 5000,
      "avg_delivery_days": 3.5,
      "avg_shipping_percentage": 8.5
    },
    "carriers": [...],
    "status_breakdown": [...],
    "delivery_performance": {
      "delivered": 120,
      "failed": 3,
      "cancelled": 2,
      "success_rate": 80.0
    }
  }
}
```

---

### 4. Check Sendbox Account

```bash
curl http://localhost:4500/api/admin/sendbox/account \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "account": {
      "balance": 50000,
      "currency": "NGN",
      "account_name": "Trollz Store"
    },
    "environment": "staging",
    "base_url": "https://sandbox.staging.sendbox.co"
  }
}
```

---

### 5. Fund Staging Account

```bash
curl -X POST http://localhost:4500/api/admin/sendbox/fund-account \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 10000
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Successfully added 10000 to staging account",
  "data": {
    "new_balance": 60000,
    "amount_added": 10000
  }
}
```

---

## Common Admin Workflows

### Workflow 1: Handle Customer Cancellation

1. **Customer requests cancellation**
2. **Admin cancels shipment:**
   ```bash
   POST /api/admin/orders/123/cancel-shipment
   {
     "restore_stock": true,
     "reason": "Customer requested"
   }
   ```
3. **Stock automatically restored**
4. **Process refund separately**

---

### Workflow 2: End-of-Day Batch Processing

1. **Identify paid orders without shipments:**
   ```sql
   SELECT id FROM orders 
   WHERE payment_status = 'paid' 
   AND sendbox_shipment_id IS NULL
   AND address_id IS NOT NULL;
   ```

2. **Bulk create shipments:**
   ```bash
   POST /api/admin/orders/bulk-create-shipments
   {
     "order_ids": [1, 2, 3, 4, 5]
   }
   ```

3. **Review failures:**
   - Check failed array in response
   - Fix issues (missing addresses, etc.)
   - Retry failed orders

---

### Workflow 3: Monthly Performance Review

1. **Generate monthly report:**
   ```bash
   GET /api/admin/reports/shipping?start_date=2026-03-01&end_date=2026-03-31
   ```

2. **Analyze metrics:**
   - Total shipping costs
   - Carrier performance
   - Delivery success rate
   - Average delivery time

3. **Optimize:**
   - Switch to better performing carriers
   - Adjust service codes
   - Identify problem areas

---

### Workflow 4: Daily Account Monitoring

1. **Check account balance:**
   ```bash
   GET /api/admin/sendbox/account
   ```

2. **If staging and balance low:**
   ```bash
   POST /api/admin/sendbox/fund-account
   {
     "amount": 10000
   }
   ```

3. **If production and balance low:**
   - Alert finance team
   - Fund through Sendbox portal

---

## Report Metrics Explained

### Summary Statistics:
- **total_shipments** - Number of shipments created
- **total_shipping_cost** - Sum of all shipping costs
- **avg_shipping_cost** - Average cost per shipment
- **avg_delivery_days** - Average time from creation to delivery
- **avg_shipping_percentage** - Shipping cost as % of order value

### Carrier Breakdown:
- **shipment_count** - Shipments per carrier
- **total_cost** - Total spent with carrier
- **avg_cost** - Average cost per shipment

### Delivery Performance:
- **delivered** - Successfully delivered shipments
- **failed** - Failed delivery attempts
- **cancelled** - Cancelled shipments
- **success_rate** - Percentage of successful deliveries

---

## Admin Dashboard Ideas

### Key Metrics to Display:
1. Today's shipments created
2. Current account balance
3. Pending shipments count
4. This week's delivery success rate
5. Top performing carrier
6. Average shipping cost trend

### Quick Actions:
1. Bulk create shipments for pending orders
2. View failed shipments
3. Generate today's report
4. Check account balance
5. Refresh all tracking

---

## Error Handling

### Common Errors and Solutions:

**"Order not found"**
- Verify order ID is correct
- Check order exists in database

**"No Sendbox shipment found"**
- Order doesn't have a shipment yet
- Create shipment first

**"Order is already cancelled"**
- Cannot cancel twice
- Check order status before cancelling

**"Fund account is only available in staging"**
- Cannot fund production account via API
- Use Sendbox portal for production

**"Sendbox API error"**
- Check API key is valid
- Verify internet connectivity
- Check Sendbox service status

---

## Best Practices

### Shipment Cancellation:
- Always provide a reason
- Restore stock when appropriate
- Verify order status first
- Process refunds separately

### Bulk Operations:
- Start with small batches (5-10 orders)
- Review failures before retrying
- Run during off-peak hours
- Monitor API rate limits

### Report Generation:
- Use summary reports for quick checks
- Use detailed reports for deep analysis
- Export data for further processing
- Schedule regular report generation

### Account Management:
- Monitor balance daily
- Set up low balance alerts
- Fund staging account as needed
- Track API usage patterns

---

## Security Notes

### Admin Authentication:
- All endpoints require admin token
- Tokens should be kept secure
- Rotate tokens regularly
- Log all admin actions

### Environment Protection:
- Staging operations clearly marked
- Production operations require extra confirmation
- Fund account only works in staging
- Environment displayed in responses

### Data Access:
- Admins can view all orders
- Admins can modify shipments
- All actions are logged
- Audit trail maintained

---

## Testing Checklist

### Shipment Management:
- [ ] Cancel shipment successfully
- [ ] Restore stock on cancellation
- [ ] Prevent duplicate cancellations
- [ ] Bulk create 5 shipments
- [ ] Handle mixed success/failure
- [ ] Skip existing shipments

### Reports:
- [ ] Generate summary report
- [ ] Generate detailed report
- [ ] Filter by date range
- [ ] Verify all metrics
- [ ] Test with no data
- [ ] Test with large dataset

### Account:
- [ ] View account balance
- [ ] Fund staging account
- [ ] Verify production funding blocked
- [ ] List all shipments
- [ ] Handle API errors

---

## Monitoring & Alerts

### Metrics to Monitor:
- Cancellation rate (should be low)
- Bulk operation success rate (should be high)
- Report generation time (should be fast)
- Account balance (should stay positive)
- API error rate (should be low)

### Alerts to Set Up:
- Low account balance (< 10,000 NGN)
- High cancellation rate (> 10%)
- Bulk operation failures (> 20%)
- API errors (> 5%)
- Long report generation time (> 10s)

---

## Integration with Other Phases

### Works With Phase 3:
- Uses same shipment creation logic
- Extends manual shipment creation
- Consistent error handling

### Works With Phase 4:
- Complements tracking sync
- Uses same status mapping
- Integrates with webhooks

### Enhances Overall System:
- Provides admin control
- Enables batch operations
- Offers performance insights
- Supports account monitoring

---

## Next Steps

### Immediate:
1. Test all admin endpoints
2. Generate sample reports
3. Practice bulk operations
4. Monitor account balance

### Before Production:
1. Set up admin user accounts
2. Configure production alerts
3. Document admin procedures
4. Train admin staff
5. Test with production data

### Future Enhancements:
1. Automated batch processing
2. Real-time dashboard
3. Export reports to CSV/PDF
4. Custom report templates
5. Scheduled report generation

---

## Documentation

- **Phase 5 Completion Summary:** `PHASE5_COMPLETION_SUMMARY.md`
- **API Documentation:** `ADDRESSES_SHIPPING_API_DOCUMENTATION.md`
- **Integration Plan:** `SENDBOX_INTEGRATION_PHASES.md`
- **Previous Phases:** `PHASE1-4_COMPLETION_SUMMARY.md`

---

## Support

For issues or questions:
1. Review `PHASE5_COMPLETION_SUMMARY.md` for detailed information
2. Check error messages in responses
3. Review admin action logs
4. Test in staging environment first

---

**Phase 5 Status:** ✅ COMPLETE AND READY FOR USE

**Completed:** April 20, 2026

**Next Phase:** Phase 6 - Testing & Optimization (Optional)
