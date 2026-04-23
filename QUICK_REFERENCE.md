# Sendbox Integration - Quick Reference Card

## 🚀 Status: READY TO USE

---

## 📋 Essential Information

**Warehouse Location:** LYPAS Plaza, Cluster Industrial Complex, Owerri, Imo State, Nigeria

**Database:** trollzstorecom_tr0llz_db ✅ All tables created

**API Base:** http://localhost:4500

**Documentation:** `MOBILE_APP_INTEGRATION_GUIDE.md`

---

## 🔑 Most Used Endpoints

### Create Address
```bash
POST /api/addresses
Authorization: Bearer {token}

{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "08001234567",
  "street": "123 Main St",
  "city": "Lagos",
  "state": "Lagos",
  "country": "NG"
}
```

### Get Shipping Quotes
```bash
POST /api/shipping/quotes
Authorization: Bearer {token}

{
  "destination_address_id": 1,
  "items": [
    {"product_id": 55, "quantity": 1}
  ]
}
```

### Checkout with Shipping
```bash
POST /api/checkout
Authorization: Bearer {token}

{
  "address_id": 1,
  "payment_method": "flutterwave",
  "transaction_id": "FLW123",
  "items": [{"product_id": 55, "quantity": 1}],
  "selected_shipping": {
    "quote_id": 123,
    "shipping_cost": 5000
  }
}
```

### Track Order
```bash
GET /api/orders/track/{tracking_number}
# No authentication required
```

---

## 📊 Order Statuses

| Status | Meaning |
|--------|---------|
| processing | Order being processed |
| shipped | Package shipped |
| delivered | Package delivered |
| cancelled | Order cancelled |

## 🚚 Sendbox Statuses

| Status | Display |
|--------|---------|
| pending | Awaiting Pickup |
| pickup_completed | Picked Up |
| in_transit | In Transit |
| in_delivery | Out for Delivery |
| delivered | Delivered |

---

## ⚠️ Common Errors

| Error | Solution |
|-------|----------|
| "Address not found" | Create address first |
| "Quote expired" | Request new quote (24hr expiry) |
| "Sendbox API error" | Check API key in .env |
| "Insufficient stock" | Reduce quantity |

---

## 🔧 Configuration

### Required in .env:
```bash
SENDBOX_API_KEY=your_key_here
SENDBOX_ENV=staging
WAREHOUSE_PHONE=+234_YOUR_PHONE
WAREHOUSE_EMAIL=your_email@trollzstore.com
```

---

## 📱 Mobile App Integration

**Main Guide:** `MOBILE_APP_INTEGRATION_GUIDE.md`

**Key Flows:**
1. Address Management → Shipping Quotes → Checkout
2. Order List → Order Details → Track Shipment

**Best Practices:**
- Cache addresses locally
- Validate quotes before checkout
- Handle errors gracefully
- Show loading states

---

## 🧪 Testing

```bash
# Run all tests
python run_tests.py

# Check tables
python check_and_create_tables.py
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `MOBILE_APP_INTEGRATION_GUIDE.md` | Frontend integration |
| `ADMIN_API_DOCUMENTATION.md` | Admin endpoints |
| `FINAL_SETUP_SUMMARY.md` | Complete summary |
| `SETUP_COMPLETE.md` | Setup guide |

---

## 🆘 Quick Help

**Tables missing?** Run: `python check_and_create_tables.py`

**API not working?** Check: Sendbox API key in `.env`

**Need examples?** See: `MOBILE_APP_INTEGRATION_GUIDE.md`

**Testing?** Run: `python run_tests.py`

---

## ✅ Checklist

- [x] Database tables created
- [x] Warehouse configured (Owerri)
- [ ] Sendbox API key added to .env
- [ ] Warehouse phone/email updated
- [ ] Mobile app integration started
- [ ] Testing completed

---

**Quick Start:** Add Sendbox API key to `.env` → Test address creation → Get shipping quotes → Complete checkout

**Support:** Check documentation files or review error messages in API responses
