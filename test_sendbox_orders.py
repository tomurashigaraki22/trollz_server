"""
Comprehensive Sendbox Integration Tests
Tests order creation, shipping quotes, shipments, and tracking.
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:4500"
API_BASE = f"{BASE_URL}/api"

# Test data
TEST_USER = {
    "email": "testuser@example.com",
    "password": "Test123!",
    "first_name": "Test",
    "last_name": "User",
    "phone": "+2348012345678"
}

TEST_ADDRESS = {
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+2348087654321",
    "email": "john.doe@example.com",
    "address": "123 Test Street, Victoria Island",
    "city": "Lagos",
    "state": "Lagos",
    "country": "NG",
    "postal_code": "100001",
    "is_default": True
}

# Global variables to store test data
auth_token = None
user_id = None
address_id = None
product_id = None
order_id = None
tracking_code = None


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def print_result(success, message, data=None):
    """Print test result."""
    status = "✅" if success else "❌"
    print(f"\n{status} {message}")
    if data:
        print(f"   Data: {json.dumps(data, indent=3)}")


def get_headers():
    """Get request headers with auth token."""
    headers = {"Content-Type": "application/json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    return headers


# ============================================================================
# TEST 1: USER REGISTRATION & LOGIN
# ============================================================================

def test_user_registration():
    """Test user registration."""
    print_section("TEST 1: User Registration")
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/register",
            json=TEST_USER,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code in [200, 201]:
            print_result(True, "User registered successfully", data)
            return True
        elif response.status_code == 409:
            print_result(True, "User already exists (OK for testing)", data)
            return True
        else:
            print_result(False, f"Registration failed: {data.get('message')}")
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


def test_user_login():
    """Test user login and get auth token."""
    global auth_token, user_id
    
    print_section("TEST 2: User Login")
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/login",
            json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            },
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200 and data.get("status") == "success":
            auth_token = data["data"]["token"]
            user_id = data["data"]["user"]["id"]
            print_result(True, "Login successful", {
                "user_id": user_id,
                "token": f"{auth_token[:20]}..."
            })
            return True
        else:
            print_result(False, f"Login failed: {data.get('message')}")
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


# ============================================================================
# TEST 2: ADDRESS MANAGEMENT
# ============================================================================

def test_create_address():
    """Test creating a shipping address."""
    global address_id
    
    print_section("TEST 3: Create Shipping Address")
    
    try:
        response = requests.post(
            f"{API_BASE}/addresses",
            json=TEST_ADDRESS,
            headers=get_headers()
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code in [200, 201] and data.get("status") == "success":
            address_id = data["data"]["id"]
            print_result(True, "Address created successfully", {
                "address_id": address_id,
                "city": TEST_ADDRESS["city"],
                "state": TEST_ADDRESS["state"]
            })
            return True
        else:
            print_result(False, f"Address creation failed: {data.get('message')}")
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


def test_get_addresses():
    """Test getting user addresses."""
    print_section("TEST 4: Get User Addresses")
    
    try:
        response = requests.get(
            f"{API_BASE}/addresses",
            headers=get_headers()
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200 and data.get("status") == "success":
            addresses = data.get("data", [])
            print_result(True, f"Retrieved {len(addresses)} address(es)", {
                "count": len(addresses),
                "addresses": [{"id": a["id"], "city": a["city"]} for a in addresses[:3]]
            })
            return True
        else:
            print_result(False, f"Failed to get addresses: {data.get('message')}")
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


# ============================================================================
# TEST 3: SHIPPING QUOTES
# ============================================================================

def test_get_shipping_quotes():
    """Test getting shipping quotes."""
    print_section("TEST 5: Get Shipping Quotes")
    
    try:
        payload = {
            "destination": {
                "name": f"{TEST_ADDRESS['first_name']} {TEST_ADDRESS['last_name']}",
                "phone": TEST_ADDRESS["phone"],
                "email": TEST_ADDRESS["email"],
                "address": TEST_ADDRESS["address"],
                "city": TEST_ADDRESS["city"],
                "state": TEST_ADDRESS["state"],
                "country": TEST_ADDRESS["country"]
            },
            "weight": 1.5,
            "items": [
                {
                    "name": "Test Product",
                    "quantity": 2,
                    "value": 10000,
                    "weight": 0.75
                }
            ],
            "total_value": 10000
        }
        
        response = requests.post(
            f"{API_BASE}/shipping/quotes",
            json=payload,
            headers=get_headers()
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200 and data.get("status") == "success":
            quotes = data.get("data", {}).get("quotes", [])
            print_result(True, f"Retrieved {len(quotes)} shipping quote(s)", {
                "count": len(quotes),
                "quotes": [
                    {
                        "service": q.get("service_name", "N/A"),
                        "amount": q.get("amount", 0),
                        "delivery_time": q.get("delivery_time", "N/A")
                    }
                    for q in quotes[:3]
                ]
            })
            return True
        else:
            print_result(False, f"Failed to get quotes: {data.get('message')}")
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


# ============================================================================
# TEST 4: PRODUCT & ORDER CREATION
# ============================================================================

def test_get_products():
    """Test getting products."""
    global product_id
    
    print_section("TEST 6: Get Products")
    
    try:
        response = requests.get(
            f"{API_BASE}/products",
            headers=get_headers()
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200 and data.get("status") == "success":
            products = data.get("data", [])
            if products:
                product_id = products[0]["id"]
                print_result(True, f"Retrieved {len(products)} product(s)", {
                    "count": len(products),
                    "first_product": {
                        "id": products[0]["id"],
                        "name": products[0]["name"],
                        "price": products[0]["price"]
                    }
                })
                return True
            else:
                print_result(False, "No products found in database")
                return False
        else:
            print_result(False, f"Failed to get products: {data.get('message')}")
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


def test_create_order_with_shipping():
    """Test creating an order with shipping."""
    global order_id
    
    print_section("TEST 7: Create Order with Shipping")
    
    if not product_id or not address_id:
        print_result(False, "Missing product_id or address_id")
        return False
    
    try:
        payload = {
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                    "price": 5000
                }
            ],
            "address_id": address_id,
            "selected_shipping": {
                "service_code": "standard",
                "service_name": "Standard Delivery",
                "amount": 2500,
                "delivery_time": "3-5 business days"
            },
            "payment_method": "flutterwave"
        }
        
        response = requests.post(
            f"{API_BASE}/checkout",
            json=payload,
            headers=get_headers()
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code in [200, 201] and data.get("status") == "success":
            order_id = data["data"]["order"]["id"]
            print_result(True, "Order created successfully", {
                "order_id": order_id,
                "total": data["data"]["order"]["total_amount"],
                "shipping_fee": data["data"]["order"].get("shipping_fee", 0),
                "status": data["data"]["order"]["status"]
            })
            return True
        else:
            print_result(False, f"Order creation failed: {data.get('message')}")
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


def test_get_order_details():
    """Test getting order details."""
    print_section("TEST 8: Get Order Details")
    
    if not order_id:
        print_result(False, "No order_id available")
        return False
    
    try:
        response = requests.get(
            f"{API_BASE}/orders/{order_id}",
            headers=get_headers()
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200 and data.get("status") == "success":
            order = data["data"]
            print_result(True, "Order details retrieved", {
                "order_id": order["id"],
                "status": order["status"],
                "total": order["total_amount"],
                "items_count": len(order.get("items", []))
            })
            return True
        else:
            print_result(False, f"Failed to get order: {data.get('message')}")
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


# ============================================================================
# TEST 5: PAYMENT CONFIRMATION & SHIPMENT CREATION
# ============================================================================

def test_confirm_payment():
    """Test confirming payment (creates shipment)."""
    global tracking_code
    
    print_section("TEST 9: Confirm Payment (Create Shipment)")
    
    if not order_id:
        print_result(False, "No order_id available")
        return False
    
    try:
        payload = {
            "payment_reference": f"TEST_REF_{int(time.time())}",
            "payment_method": "flutterwave"
        }
        
        response = requests.post(
            f"{API_BASE}/orders/{order_id}/confirm",
            json=payload,
            headers=get_headers()
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200 and data.get("status") == "success":
            order = data["data"]
            tracking_code = order.get("sendbox_tracking_code")
            print_result(True, "Payment confirmed & shipment created", {
                "order_id": order["id"],
                "status": order["status"],
                "tracking_code": tracking_code or "Not yet created",
                "sendbox_shipment_id": order.get("sendbox_shipment_id")
            })
            return True
        else:
            print_result(False, f"Payment confirmation failed: {data.get('message')}")
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


# ============================================================================
# TEST 6: TRACKING & SHIPMENT MANAGEMENT
# ============================================================================

def test_track_shipment():
    """Test tracking a shipment."""
    print_section("TEST 10: Track Shipment")
    
    if not tracking_code:
        print_result(False, "No tracking_code available (shipment may not be created yet)")
        return False
    
    try:
        response = requests.get(
            f"{API_BASE}/shipping/track/{tracking_code}",
            headers=get_headers()
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200 and data.get("status") == "success":
            tracking = data["data"]
            print_result(True, "Shipment tracked successfully", {
                "tracking_code": tracking_code,
                "status": tracking.get("status"),
                "current_location": tracking.get("current_location", "N/A")
            })
            return True
        else:
            print_result(False, f"Tracking failed: {data.get('message')}")
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


def test_get_user_orders():
    """Test getting user orders."""
    print_section("TEST 11: Get User Orders")
    
    try:
        response = requests.get(
            f"{API_BASE}/orders",
            headers=get_headers()
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200 and data.get("status") == "success":
            orders = data.get("data", [])
            print_result(True, f"Retrieved {len(orders)} order(s)", {
                "count": len(orders),
                "orders": [
                    {
                        "id": o["id"],
                        "status": o["status"],
                        "total": o["total_amount"]
                    }
                    for o in orders[:3]
                ]
            })
            return True
        else:
            print_result(False, f"Failed to get orders: {data.get('message')}")
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


# ============================================================================
# TEST 7: ADMIN ENDPOINTS
# ============================================================================

def test_admin_get_shipments():
    """Test admin endpoint to get all shipments."""
    print_section("TEST 12: Admin - Get All Shipments")
    
    try:
        response = requests.get(
            f"{API_BASE}/admin/shipping/shipments",
            headers=get_headers()
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200 and data.get("status") == "success":
            shipments = data.get("data", [])
            print_result(True, f"Retrieved {len(shipments)} shipment(s)", {
                "count": len(shipments)
            })
            return True
        else:
            print_result(False, f"Failed to get shipments: {data.get('message')}")
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


def test_admin_shipping_reports():
    """Test admin shipping reports."""
    print_section("TEST 13: Admin - Shipping Reports")
    
    try:
        response = requests.get(
            f"{API_BASE}/admin/shipping/reports",
            headers=get_headers()
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200 and data.get("status") == "success":
            report = data["data"]
            print_result(True, "Shipping report retrieved", {
                "total_shipments": report.get("total_shipments", 0),
                "pending": report.get("pending", 0),
                "in_transit": report.get("in_transit", 0),
                "delivered": report.get("delivered", 0)
            })
            return True
        else:
            print_result(False, f"Failed to get report: {data.get('message')}")
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("  SENDBOX INTEGRATION - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"\n  Base URL: {BASE_URL}")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n  Make sure your server is running: python app.py")
    
    input("\n  Press Enter to start tests...")
    
    results = []
    
    # Run tests in sequence
    results.append(("User Registration", test_user_registration()))
    results.append(("User Login", test_user_login()))
    
    if auth_token:
        results.append(("Create Address", test_create_address()))
        results.append(("Get Addresses", test_get_addresses()))
        results.append(("Get Shipping Quotes", test_get_shipping_quotes()))
        results.append(("Get Products", test_get_products()))
        
        if product_id and address_id:
            results.append(("Create Order with Shipping", test_create_order_with_shipping()))
            
            if order_id:
                results.append(("Get Order Details", test_get_order_details()))
                results.append(("Confirm Payment (Create Shipment)", test_confirm_payment()))
                
                if tracking_code:
                    results.append(("Track Shipment", test_track_shipment()))
                
                results.append(("Get User Orders", test_get_user_orders()))
                results.append(("Admin - Get Shipments", test_admin_get_shipments()))
                results.append(("Admin - Shipping Reports", test_admin_shipping_reports()))
    
    # Print summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    print(f"  Success Rate: {(passed/total*100):.1f}%")
    
    if passed == total:
        print("\n  🎉 All tests passed!")
    else:
        print(f"\n  ⚠️  {total - passed} test(s) failed")
    
    print("\n" + "="*70)
    print(f"  Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
