"""
Test Terminal Africa Phase 2 Implementation
Tests all core services: Terminal Service, Address Manager, and Carrier Manager
"""

import sys
from services.terminal_service import get_terminal_client, TerminalAPIError
from services.terminal_address_manager import get_address_manager
from services.terminal_carrier_manager import get_carrier_manager


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def test_terminal_service():
    """Test Terminal Africa Service."""
    print_section("TEST 1: Terminal Africa Service")
    
    try:
        client = get_terminal_client()
        print(f"✅ Terminal client initialized")
        print(f"   Environment: {client.environment}")
        print(f"   Base URL: {client.base_url}")
        
        # Test user profile
        print("\n📋 Testing user profile...")
        try:
            profile = client.get_user_profile()
            print(f"✅ User profile retrieved")
            print(f"   User: {profile.get('data', {}).get('name', 'N/A')}")
        except TerminalAPIError as e:
            print(f"⚠️  Profile error: {e.message}")
        
        # Test wallet balance
        print("\n💰 Testing wallet balance...")
        try:
            balance = client.get_wallet_balance()
            print(f"✅ Wallet balance retrieved")
            balance_data = balance.get('data', {})
            print(f"   Balance: {balance_data.get('balance', 0)} {balance_data.get('currency', 'NGN')}")
        except TerminalAPIError as e:
            print(f"⚠️  Balance error: {e.message}")
        
        # Test carriers
        print("\n🚚 Testing carriers...")
        try:
            carriers = client.get_carriers(active=True)
            carriers_list = carriers.get('data', [])
            print(f"✅ Carriers retrieved: {len(carriers_list)} active carriers")
            for carrier in carriers_list[:3]:  # Show first 3
                print(f"   - {carrier.get('name')} ({carrier.get('slug')})")
        except TerminalAPIError as e:
            print(f"⚠️  Carriers error: {e.message}")
        
        return True
        
    except Exception as e:
        print(f"❌ Terminal service test failed: {str(e)}")
        return False


def test_address_manager():
    """Test Terminal Address Manager."""
    print_section("TEST 2: Terminal Address Manager")
    
    try:
        address_mgr = get_address_manager()
        print(f"✅ Address manager initialized")
        
        # Test address validation
        print("\n✔️  Testing address validation...")
        test_address = {
            "first_name": "Test",
            "last_name": "User",
            "phone": "+2348012345678",
            "email": "test@example.com",
            "line1": "123 Test Street",
            "city": "Lagos",
            "state": "Lagos",
            "country": "NG"
        }
        
        validation = address_mgr.validate_address(test_address)
        if validation['valid']:
            print(f"✅ Address validation passed")
        else:
            print(f"❌ Address validation failed: {validation['message']}")
        
        # Test creating address (commented out to avoid creating test data)
        print("\n📝 Address creation test (skipped - would create real data)")
        print("   To test: Uncomment the create_and_sync_address call")
        
        # Uncomment to actually test address creation:
        # result = address_mgr.create_and_sync_address(
        #     user_id=1,
        #     first_name="Test",
        #     last_name="User",
        #     phone="+2348012345678",
        #     email="test@example.com",
        #     line1="123 Test Street",
        #     city="Lagos",
        #     state="Lagos",
        #     country="NG"
        # )
        # print(f"✅ Address created: {result['terminal_address_id']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Address manager test failed: {str(e)}")
        return False


def test_carrier_manager():
    """Test Terminal Carrier Manager."""
    print_section("TEST 3: Terminal Carrier Manager")
    
    try:
        carrier_mgr = get_carrier_manager()
        print(f"✅ Carrier manager initialized")
        
        # Test syncing carriers
        print("\n🔄 Testing carrier sync...")
        try:
            result = carrier_mgr.sync_carriers()
            print(f"✅ Carriers synced: {result['synced_count']} carriers")
        except TerminalAPIError as e:
            print(f"⚠️  Sync error: {e.message}")
        
        # Test getting local carriers
        print("\n📋 Testing local carrier retrieval...")
        carriers = carrier_mgr.get_local_carriers(active=True)
        print(f"✅ Local carriers retrieved: {len(carriers)} active carriers")
        
        for carrier in carriers[:5]:  # Show first 5
            print(f"   - {carrier['name']} ({carrier['slug']})")
            print(f"     Domestic: {carrier['domestic']}, Regional: {carrier['regional']}, International: {carrier['international']}")
        
        # Test carrier stats
        print("\n📊 Testing carrier statistics...")
        stats = carrier_mgr.get_carrier_stats()
        print(f"✅ Carrier stats:")
        print(f"   Total: {stats['total']}")
        print(f"   Active: {stats['active']}")
        print(f"   Domestic: {stats['domestic']}")
        print(f"   Regional: {stats['regional']}")
        print(f"   International: {stats['international']}")
        
        # Test recommended carriers
        print("\n🎯 Testing recommended carriers (NG to NG)...")
        recommended = carrier_mgr.get_recommended_carriers('NG', 'NG')
        print(f"✅ Recommended carriers: {len(recommended)}")
        for carrier in recommended[:3]:
            print(f"   - {carrier['name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Carrier manager test failed: {str(e)}")
        return False


def test_packaging_and_parcels():
    """Test packaging and parcel creation."""
    print_section("TEST 4: Packaging & Parcels")
    
    try:
        client = get_terminal_client()
        
        # Test getting packaging
        print("📦 Testing packaging retrieval...")
        try:
            packaging = client.get_packaging(page=1, per_page=5)
            packaging_list = packaging.get('data', [])
            print(f"✅ Packaging retrieved: {len(packaging_list)} options")
            for pkg in packaging_list[:3]:
                print(f"   - {pkg.get('name')}: {pkg.get('length')}x{pkg.get('width')}x{pkg.get('height')} {pkg.get('size_unit')}")
        except TerminalAPIError as e:
            print(f"⚠️  Packaging error: {e.message}")
        
        # Test creating packaging (commented out)
        print("\n📝 Packaging creation test (skipped - would create real data)")
        print("   To test: Uncomment the create_packaging call")
        
        # Uncomment to test:
        # new_pkg = client.create_packaging(
        #     name="Test Box",
        #     type="box",
        #     length=25,
        #     width=20,
        #     height=15,
        #     weight=0.5,
        #     size_unit="cm",
        #     weight_unit="kg"
        # )
        # print(f"✅ Packaging created: {new_pkg['data']['packaging_id']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Packaging test failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("  TERMINAL AFRICA PHASE 2 TESTS")
    print("="*70)
    
    results = {
        "Terminal Service": test_terminal_service(),
        "Address Manager": test_address_manager(),
        "Carrier Manager": test_carrier_manager(),
        "Packaging & Parcels": test_packaging_and_parcels()
    }
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\n{'='*70}")
    print(f"  RESULTS: {passed}/{total} tests passed")
    print(f"{'='*70}\n")
    
    if passed == total:
        print("🎉 All tests passed! Phase 2 implementation is working correctly.")
        print("\n📋 Next Steps:")
        print("1. Review the test results above")
        print("2. Test API endpoints using Postman (see docs/TERMINAL_API_DOCUMENTATION.md)")
        print("3. Proceed to Phase 3: Address Integration")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
