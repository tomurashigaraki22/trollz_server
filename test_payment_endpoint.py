"""
Test script for payment endpoints.
"""

import requests
import json

BASE_URL = "http://localhost:4500"


def test_get_payment_config():
    """Test getting payment configuration."""
    print("\n" + "="*60)
    print("TEST: Get Payment Config")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/payment/config")
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                print("\n✅ Payment config retrieved successfully")
                return True
        
        print("\n❌ Failed to get payment config")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def test_get_flutterwave_public_key():
    """Test getting Flutterwave public key."""
    print("\n" + "="*60)
    print("TEST: Get Flutterwave Public Key")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/payment/flutterwave/public-key")
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                public_key = data.get("data", {}).get("public_key")
                print(f"\n✅ Public key retrieved: {public_key[:20]}..." if public_key else "")
                return True
        elif response.status_code == 404:
            print("\n⚠️  Flutterwave public key not configured in .env")
            print("   Add FLUTTERWAVE_PUBLIC_KEY to your .env file")
            return True  # Not an error, just not configured
        
        print("\n❌ Failed to get public key")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("PAYMENT ENDPOINT TESTS")
    print("="*60)
    print("\nMake sure your server is running: python app.py")
    
    input("\nPress Enter to start tests...")
    
    results = []
    results.append(("Payment Config", test_get_payment_config()))
    results.append(("Flutterwave Public Key", test_get_flutterwave_public_key()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")


if __name__ == "__main__":
    main()
