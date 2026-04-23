#!/usr/bin/env python3
"""
Test Sendbox Integration Setup
Verifies that Sendbox service is properly configured and can connect to the API.
"""

import sys
from config import Config
from services.sendbox_service import SendboxClient, SendboxAPIError
from services.address_validator import (
    validate_address,
    format_address_for_sendbox,
    get_state_code,
    calculate_service_type
)


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_configuration():
    """Test that configuration is properly set up."""
    print_section("Testing Configuration")
    
    print(f"✓ Sendbox Environment: {Config.SENDBOX_ENVIRONMENT}")
    print(f"✓ Sendbox Base URL: {Config.get_sendbox_base_url()}")
    
    if Config.SENDBOX_API_KEY:
        print(f"✓ API Key: {'*' * 20}{Config.SENDBOX_API_KEY[-8:]}")
    else:
        print("✗ API Key: NOT CONFIGURED")
        print("  Please set SENDBOX_API_KEY in your .env file")
        return False
    
    print(f"✓ Warehouse Location: {Config.WAREHOUSE_CITY}, {Config.WAREHOUSE_STATE}")
    
    return True


def test_address_validation():
    """Test address validation utilities."""
    print_section("Testing Address Validation")
    
    # Test valid address
    valid_address = {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+234 800 123 4567",
        "street": "123 Test Street",
        "city": "Lagos",
        "state": "Lagos",
        "country": "NG",
        "email": "john@example.com"
    }
    
    is_valid, error = validate_address(valid_address)
    if is_valid:
        print("✓ Valid address validation passed")
    else:
        print(f"✗ Valid address validation failed: {error}")
        return False
    
    # Test invalid address (missing phone)
    invalid_address = {
        "first_name": "Jane",
        "last_name": "Doe",
        "street": "456 Test Street",
        "city": "Abuja",
        "state": "FCT",
        "country": "NG"
    }
    
    is_valid, error = validate_address(invalid_address)
    if not is_valid:
        print(f"✓ Invalid address validation passed (caught: {error})")
    else:
        print("✗ Invalid address validation failed (should have caught missing phone)")
        return False
    
    # Test state code lookup
    lagos_code = get_state_code("Lagos")
    if lagos_code == "LOS":
        print(f"✓ State code lookup: Lagos -> {lagos_code}")
    else:
        print(f"✗ State code lookup failed: expected LOS, got {lagos_code}")
        return False
    
    # Test service type calculation
    service_type = calculate_service_type("NG", "NG")
    if service_type == "local":
        print(f"✓ Service type calculation: NG -> NG = {service_type}")
    else:
        print(f"✗ Service type calculation failed: expected local, got {service_type}")
        return False
    
    service_type = calculate_service_type("NG", "US")
    if service_type == "international":
        print(f"✓ Service type calculation: NG -> US = {service_type}")
    else:
        print(f"✗ Service type calculation failed: expected international, got {service_type}")
        return False
    
    return True


def test_sendbox_client():
    """Test Sendbox client initialization."""
    print_section("Testing Sendbox Client")
    
    try:
        client = SendboxClient()
        print(f"✓ Client initialized successfully")
        print(f"  Environment: {client.environment}")
        print(f"  Base URL: {client.base_url}")
        return True
    except Exception as e:
        print(f"✗ Client initialization failed: {str(e)}")
        return False


def test_api_connection():
    """Test actual API connection (if API key is configured)."""
    print_section("Testing API Connection")
    
    if not Config.SENDBOX_API_KEY:
        print("⚠ Skipping API connection test (no API key configured)")
        return True
    
    try:
        client = SendboxClient()
        
        # Try to get account balance (simple API call)
        print("Attempting to fetch account balance...")
        balance = client.get_account_balance()
        
        print("✓ API connection successful!")
        print(f"  Account Balance: {balance.get('balance', 'N/A')}")
        print(f"  Currency: {balance.get('currency', 'N/A')}")
        
        return True
        
    except SendboxAPIError as e:
        if e.status_code == 401:
            print("✗ Authentication failed - Invalid API key")
            print("  Please check your SENDBOX_API_KEY in .env file")
        elif e.status_code == 403:
            print("✗ Access forbidden - Insufficient permissions")
        else:
            print(f"✗ API error: {e.message}")
        return False
        
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        return False


def test_warehouse_address():
    """Test warehouse address configuration."""
    print_section("Testing Warehouse Address")
    
    warehouse = Config.get_warehouse_address()
    
    is_valid, error = validate_address(warehouse)
    if is_valid:
        print("✓ Warehouse address is valid")
        print(f"  Location: {warehouse['city']}, {warehouse['state']}, {warehouse['country']}")
        print(f"  Phone: {warehouse['phone']}")
        return True
    else:
        print(f"✗ Warehouse address is invalid: {error}")
        print("  Please check warehouse configuration in .env file")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("  SENDBOX INTEGRATION SETUP TEST")
    print("=" * 70)
    print("\nThis script will verify your Sendbox integration setup.")
    print("Make sure you have configured your .env file with Sendbox credentials.")
    
    results = []
    
    # Run tests
    results.append(("Configuration", test_configuration()))
    results.append(("Address Validation", test_address_validation()))
    results.append(("Sendbox Client", test_sendbox_client()))
    results.append(("Warehouse Address", test_warehouse_address()))
    results.append(("API Connection", test_api_connection()))
    
    # Print summary
    print_section("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {test_name}")
    
    print("\n" + "-" * 70)
    print(f"Results: {passed}/{total} tests passed")
    print("-" * 70)
    
    if passed == total:
        print("\n✓ All tests passed! Sendbox integration is ready.")
        print("\nNext steps:")
        print("1. Run migrations: python run_migrations.py run")
        print("2. Start implementing Phase 2 (Shipping Quotes)")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        print("\nCommon issues:")
        print("- Missing SENDBOX_API_KEY in .env file")
        print("- Invalid API key")
        print("- Incorrect warehouse address configuration")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFatal error: {str(e)}")
        sys.exit(1)
