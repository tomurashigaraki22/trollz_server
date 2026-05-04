"""
Interactive Sendbox Testing Tool
Allows you to test individual endpoints interactively.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:4500/api"
auth_token = None


def print_menu():
    """Print main menu."""
    print("\n" + "="*60)
    print("  SENDBOX INTERACTIVE TESTING TOOL")
    print("="*60)
    print("\n  1. Test Shipping Quotes")
    print("  2. Test Address Validation")
    print("  3. Test Landed Cost Calculation")
    print("  4. Test Order Tracking")
    print("  5. Test Admin - Get Shipments")
    print("  6. Test Admin - Shipping Reports")
    print("  7. Test Webhook Events")
    print("  8. Set Auth Token")
    print("  9. Health Check")
    print("  0. Exit")
    print("\n" + "="*60)


def get_headers():
    """Get request headers."""
    headers = {"Content-Type": "application/json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    return headers


def print_response(response):
    """Print formatted response."""
    print(f"\nStatus Code: {response.status_code}")
    print("\nResponse:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)


def test_shipping_quotes():
    """Test shipping quotes."""
    print("\n" + "-"*60)
    print("  TEST: Shipping Quotes")
    print("-"*60)
    
    print("\nEnter destination details (or press Enter for defaults):")
    city = input("City [Lagos]: ").strip() or "Lagos"
    state = input("State [Lagos]: ").strip() or "Lagos"
    weight = input("Weight in kg [1.5]: ").strip() or "1.5"
    value = input("Total value [10000]: ").strip() or "10000"
    
    payload = {
        "destination": {
            "name": "Test Customer",
            "phone": "+2348087654321",
            "email": "test@example.com",
            "address": "123 Test Street",
            "city": city,
            "state": state,
            "country": "NG"
        },
        "weight": float(weight),
        "items": [
            {
                "name": "Test Product",
                "quantity": 1,
                "value": float(value),
                "weight": float(weight)
            }
        ],
        "total_value": float(value)
    }
    
    print("\nSending request...")
    response = requests.post(
        f"{BASE_URL}/shipping/quotes",
        json=payload,
        headers=get_headers()
    )
    
    print_response(response)


def test_address_validation():
    """Test address validation."""
    print("\n" + "-"*60)
    print("  TEST: Address Validation")
    print("-"*60)
    
    print("\nEnter address details:")
    address = input("Address: ").strip()
    city = input("City: ").strip()
    state = input("State: ").strip()
    country = input("Country [NG]: ").strip() or "NG"
    
    if not address or not city or not state:
        print("\n❌ Address, city, and state are required")
        return
    
    payload = {
        "address": address,
        "city": city,
        "state": state,
        "country": country
    }
    
    print("\nSending request...")
    response = requests.post(
        f"{BASE_URL}/addresses/validate",
        json=payload,
        headers=get_headers()
    )
    
    print_response(response)


def test_landed_cost():
    """Test landed cost calculation."""
    print("\n" + "-"*60)
    print("  TEST: Landed Cost Calculation")
    print("-"*60)
    
    print("\nEnter shipment details:")
    country = input("Destination Country [US]: ").strip() or "US"
    weight = input("Weight in kg [2.0]: ").strip() or "2.0"
    value = input("Total value [50000]: ").strip() or "50000"
    
    payload = {
        "destination": {
            "name": "Test Customer",
            "phone": "+1234567890",
            "email": "test@example.com",
            "address": "123 Test Street",
            "city": "New York",
            "state": "NY",
            "country": country
        },
        "weight": float(weight),
        "items": [
            {
                "name": "Electronics",
                "quantity": 1,
                "value": float(value),
                "weight": float(weight),
                "hts_code": "8517.12.00"
            }
        ],
        "total_value": float(value)
    }
    
    print("\nSending request...")
    response = requests.post(
        f"{BASE_URL}/shipping/landed-cost",
        json=payload,
        headers=get_headers()
    )
    
    print_response(response)


def test_order_tracking():
    """Test order tracking."""
    print("\n" + "-"*60)
    print("  TEST: Order Tracking")
    print("-"*60)
    
    tracking_code = input("\nEnter tracking code: ").strip()
    
    if not tracking_code:
        print("\n❌ Tracking code is required")
        return
    
    print("\nSending request...")
    response = requests.get(
        f"{BASE_URL}/shipping/track/{tracking_code}",
        headers=get_headers()
    )
    
    print_response(response)


def test_admin_shipments():
    """Test admin get shipments."""
    print("\n" + "-"*60)
    print("  TEST: Admin - Get Shipments")
    print("-"*60)
    
    if not auth_token:
        print("\n⚠️  Auth token not set. Use option 8 to set token.")
        return
    
    status = input("\nFilter by status (leave empty for all): ").strip()
    
    params = {}
    if status:
        params["status"] = status
    
    print("\nSending request...")
    response = requests.get(
        f"{BASE_URL}/admin/shipping/shipments",
        params=params,
        headers=get_headers()
    )
    
    print_response(response)


def test_shipping_reports():
    """Test shipping reports."""
    print("\n" + "-"*60)
    print("  TEST: Admin - Shipping Reports")
    print("-"*60)
    
    if not auth_token:
        print("\n⚠️  Auth token not set. Use option 8 to set token.")
        return
    
    print("\nSending request...")
    response = requests.get(
        f"{BASE_URL}/admin/shipping/reports",
        headers=get_headers()
    )
    
    print_response(response)


def test_webhook_events():
    """Test webhook events."""
    print("\n" + "-"*60)
    print("  TEST: Webhook Events")
    print("-"*60)
    
    if not auth_token:
        print("\n⚠️  Auth token not set. Use option 8 to set token.")
        return
    
    print("\nSending request...")
    response = requests.get(
        f"{BASE_URL}/admin/webhooks/events",
        headers=get_headers()
    )
    
    print_response(response)


def set_auth_token():
    """Set authentication token."""
    global auth_token
    
    print("\n" + "-"*60)
    print("  SET AUTH TOKEN")
    print("-"*60)
    
    print("\nOptions:")
    print("1. Enter token manually")
    print("2. Login to get token")
    print("3. Clear token")
    
    choice = input("\nChoice: ").strip()
    
    if choice == "1":
        token = input("\nEnter auth token: ").strip()
        if token:
            auth_token = token
            print("\n✅ Token set successfully")
        else:
            print("\n❌ Token cannot be empty")
    
    elif choice == "2":
        email = input("\nEmail: ").strip()
        password = input("Password: ").strip()
        
        if not email or not password:
            print("\n❌ Email and password are required")
            return
        
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                auth_token = data["data"]["token"]
                print("\n✅ Login successful, token set")
            else:
                print(f"\n❌ Login failed: {data.get('message')}")
        else:
            print(f"\n❌ Login failed: {response.status_code}")
    
    elif choice == "3":
        auth_token = None
        print("\n✅ Token cleared")


def health_check():
    """Test API health check."""
    print("\n" + "-"*60)
    print("  TEST: Health Check")
    print("-"*60)
    
    print("\nSending request...")
    response = requests.get("http://localhost:4500/")
    
    print_response(response)


def main():
    """Main interactive loop."""
    print("\n" + "="*60)
    print("  SENDBOX INTERACTIVE TESTING TOOL")
    print("="*60)
    print(f"\n  Base URL: {BASE_URL}")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n  Make sure your server is running: python app.py")
    
    while True:
        print_menu()
        choice = input("\n  Select option: ").strip()
        
        if choice == "1":
            test_shipping_quotes()
        elif choice == "2":
            test_address_validation()
        elif choice == "3":
            test_landed_cost()
        elif choice == "4":
            test_order_tracking()
        elif choice == "5":
            test_admin_shipments()
        elif choice == "6":
            test_shipping_reports()
        elif choice == "7":
            test_webhook_events()
        elif choice == "8":
            set_auth_token()
        elif choice == "9":
            health_check()
        elif choice == "0":
            print("\n  Goodbye! 👋\n")
            break
        else:
            print("\n  ❌ Invalid option. Please try again.")
        
        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Interrupted by user. Goodbye! 👋\n")
    except Exception as e:
        print(f"\n\n  ❌ Error: {str(e)}\n")
