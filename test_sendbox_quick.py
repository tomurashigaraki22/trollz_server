"""
Quick Sendbox Test - Tests basic Sendbox functionality without database dependencies.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:4500/api"


def print_test(title):
    """Print test header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def print_result(success, message, data=None):
    """Print test result."""
    status = "✅" if success else "❌"
    print(f"\n{status} {message}")
    if data:
        print(json.dumps(data, indent=2))


# ============================================================================
# TEST 1: SHIPPING QUOTES
# ============================================================================

def test_shipping_quotes():
    """Test getting shipping quotes."""
    print_test("TEST 1: Get Shipping Quotes")
    
    payload = {
        "destination": {
            "name": "John Doe",
            "phone": "+2348087654321",
            "email": "john@example.com",
            "address": "123 Test Street, Victoria Island",
            "city": "Lagos",
            "state": "Lagos",
            "country": "NG"
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
    
    try:
        response = requests.post(
            f"{BASE_URL}/shipping/quotes",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200:
            quotes = data.get("data", {}).get("quotes", [])
            print_result(True, f"Retrieved {len(quotes)} shipping quotes", {
                "quotes": [
                    {
                        "service": q.get("service_name"),
                        "amount": q.get("amount"),
                        "delivery_time": q.get("delivery_time")
                    }
                    for q in quotes[:3]
                ]
            })
            return True
        else:
            print_result(False, f"Failed: {data.get('message')}", data)
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


# ============================================================================
# TEST 2: CALCULATE LANDED COST
# ============================================================================

def test_landed_cost():
    """Test calculating landed cost for international shipments."""
    print_test("TEST 2: Calculate Landed Cost")
    
    payload = {
        "destination": {
            "name": "John Doe",
            "phone": "+1234567890",
            "email": "john@example.com",
            "address": "123 Test Street",
            "city": "New York",
            "state": "NY",
            "country": "US"
        },
        "weight": 2.0,
        "items": [
            {
                "name": "Electronics",
                "quantity": 1,
                "value": 50000,
                "weight": 2.0,
                "hts_code": "8517.12.00"
            }
        ],
        "total_value": 50000
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/shipping/landed-cost",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200:
            cost_data = data.get("data", {})
            print_result(True, "Landed cost calculated", {
                "shipping_cost": cost_data.get("shipping_cost"),
                "duties": cost_data.get("duties"),
                "taxes": cost_data.get("taxes"),
                "total": cost_data.get("total_landed_cost")
            })
            return True
        else:
            print_result(False, f"Failed: {data.get('message')}", data)
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


# ============================================================================
# TEST 3: VALIDATE ADDRESS
# ============================================================================

def test_validate_address():
    """Test address validation."""
    print_test("TEST 3: Validate Address")
    
    payload = {
        "address": "123 Test Street, Victoria Island",
        "city": "Lagos",
        "state": "Lagos",
        "country": "NG"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/addresses/validate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200:
            validation = data.get("data", {})
            print_result(True, "Address validated", {
                "valid": validation.get("valid"),
                "message": validation.get("message")
            })
            return True
        else:
            print_result(False, f"Failed: {data.get('message')}", data)
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


# ============================================================================
# TEST 4: HEALTH CHECK
# ============================================================================

def test_health_check():
    """Test API health check."""
    print_test("TEST 4: API Health Check")
    
    try:
        response = requests.get(f"http://localhost:4500/")
        
        print(f"\nStatus Code: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200:
            print_result(True, "API is running", data)
            return True
        else:
            print_result(False, "API health check failed", data)
            return False
            
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run quick tests."""
    print("\n" + "="*60)
    print("  SENDBOX QUICK TEST SUITE")
    print("="*60)
    print(f"\n  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("  Make sure your server is running: python app.py")
    
    input("\n  Press Enter to start tests...")
    
    results = []
    
    # Run tests
    results.append(("API Health Check", test_health_check()))
    results.append(("Shipping Quotes", test_shipping_quotes()))
    results.append(("Landed Cost Calculation", test_landed_cost()))
    results.append(("Address Validation", test_validate_address()))
    
    # Summary
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  🎉 All tests passed!")
    else:
        print(f"\n  ⚠️  {total - passed} test(s) failed")
        print("\n  Note: Some tests may fail if:")
        print("  - Sendbox tokens are not configured for live environment")
        print("  - Server is not running")
        print("  - Database is not set up")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
