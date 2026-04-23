"""
Test script to verify Sendbox token-based authentication and auto-refresh.
"""

import sys
import logging
from services.sendbox_service import SendboxClient, get_sendbox_client
import jwt
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_token_decoding():
    """Test that we can decode the tokens."""
    print("\n" + "="*60)
    print("TEST 1: Token Decoding")
    print("="*60)
    
    try:
        client = SendboxClient()
        
        # Decode access token
        access_decoded = jwt.decode(
            client.current_access_token,
            options={"verify_signature": False}
        )
        
        print("\n✅ Access Token Decoded Successfully:")
        print(f"   - User ID: {access_decoded.get('uid', 'N/A')}")
        print(f"   - App ID: {access_decoded.get('aid', 'N/A')}")
        print(f"   - Issuer: {access_decoded.get('iss', 'N/A')}")
        print(f"   - Expires: {access_decoded.get('exp', 'N/A')}")
        
        # Check expiry
        exp_timestamp = access_decoded.get('exp', 0)
        current_time = time.time()
        time_until_expiry = exp_timestamp - current_time
        
        if time_until_expiry > 0:
            hours = int(time_until_expiry / 3600)
            minutes = int((time_until_expiry % 3600) / 60)
            print(f"   - Time until expiry: {hours}h {minutes}m")
        else:
            print(f"   - ⚠️  Token is EXPIRED (expired {int(-time_until_expiry/3600)} hours ago)")
        
        # Decode refresh token
        refresh_decoded = jwt.decode(
            client.current_refresh_token,
            options={"verify_signature": False}
        )
        
        print("\n✅ Refresh Token Decoded Successfully:")
        print(f"   - App ID: {refresh_decoded.get('app_id', 'N/A')}")
        print(f"   - App Name: {refresh_decoded.get('application', {}).get('name', 'N/A')}")
        print(f"   - Issuer: {refresh_decoded.get('iss', 'N/A')}")
        print(f"   - Expires: {refresh_decoded.get('exp', 'N/A')}")
        
        exp_timestamp = refresh_decoded.get('exp', 0)
        time_until_expiry = exp_timestamp - current_time
        
        if time_until_expiry > 0:
            days = int(time_until_expiry / 86400)
            print(f"   - Time until expiry: {days} days")
        else:
            print(f"   - ⚠️  Refresh token is EXPIRED")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error decoding tokens: {str(e)}")
        return False


def test_token_expiry_check():
    """Test the token expiry checking logic."""
    print("\n" + "="*60)
    print("TEST 2: Token Expiry Check")
    print("="*60)
    
    try:
        client = SendboxClient()
        is_expired = client._is_token_expired()
        
        if is_expired:
            print("\n⚠️  Token is expired or expiring soon (within 5 minutes)")
            print("   - Auto-refresh should be triggered")
        else:
            print("\n✅ Token is valid and not expiring soon")
            print("   - No refresh needed")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error checking token expiry: {str(e)}")
        return False


def test_api_call():
    """Test making an actual API call with token authentication."""
    print("\n" + "="*60)
    print("TEST 3: API Call with Token Authentication")
    print("="*60)
    
    try:
        client = get_sendbox_client()
        
        print("\n📡 Attempting to fetch account balance...")
        
        # This will automatically check and refresh token if needed
        result = client.get_account_balance()
        
        print("\n✅ API Call Successful!")
        print(f"   - Response: {result}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ API call failed: {str(e)}")
        print(f"   - Error type: {type(e).__name__}")
        return False


def test_shipping_quotes():
    """Test getting shipping quotes with token authentication."""
    print("\n" + "="*60)
    print("TEST 4: Get Shipping Quotes")
    print("="*60)
    
    try:
        client = get_sendbox_client()
        
        # Test data
        origin = {
            "name": "Trollz Store",
            "phone": "+2348012345678",
            "email": "store@trollz.com",
            "address": "LYPAS Plaza, Cluster Industrial Complex",
            "city": "Owerri",
            "state": "Imo",
            "country": "NG"
        }
        
        destination = {
            "name": "Test Customer",
            "phone": "+2348087654321",
            "email": "customer@test.com",
            "address": "123 Test Street",
            "city": "Lagos",
            "state": "Lagos",
            "country": "NG"
        }
        
        items = [{
            "name": "Test Product",
            "quantity": 1,
            "value": 5000,
            "weight": 0.5
        }]
        
        print("\n📡 Requesting shipping quotes...")
        print(f"   - Origin: {origin['city']}, {origin['state']}")
        print(f"   - Destination: {destination['city']}, {destination['state']}")
        print(f"   - Weight: 0.5kg")
        
        result = client.get_shipping_quotes(
            origin=origin,
            destination=destination,
            weight=0.5,
            items=items,
            total_value=5000
        )
        
        print("\n✅ Shipping Quotes Retrieved Successfully!")
        
        if 'quotes' in result:
            print(f"\n   Available quotes: {len(result['quotes'])}")
            for quote in result['quotes'][:3]:  # Show first 3
                print(f"   - {quote.get('service_name', 'N/A')}: ₦{quote.get('amount', 0)}")
        else:
            print(f"   - Response: {result}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to get shipping quotes: {str(e)}")
        print(f"   - Error type: {type(e).__name__}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("SENDBOX TOKEN AUTHENTICATION TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Token Decoding", test_token_decoding()))
    results.append(("Token Expiry Check", test_token_expiry_check()))
    results.append(("API Call (Account Balance)", test_api_call()))
    results.append(("Shipping Quotes", test_shipping_quotes()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Token authentication is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
