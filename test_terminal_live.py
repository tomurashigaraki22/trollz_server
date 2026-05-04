"""
Test Terminal Africa with Live API Keys
Tests carriers, user profile, and wallet balance with live credentials.
"""

import sys
from services.terminal_service import get_terminal_client, TerminalAPIError
from services.terminal_carrier_manager import get_carrier_manager


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def test_live_connection():
    """Test Terminal Africa live API connection."""
    print_section("TERMINAL AFRICA LIVE API TEST")
    
    try:
        client = get_terminal_client()
        print(f"✅ Terminal client initialized")
        print(f"   Environment: {client.environment}")
        print(f"   Base URL: {client.base_url}")
        print(f"   Using: {'Live' if client.environment == 'live' else 'Test'} API Keys")
        
        # Test 1: Carriers
        print_section("TEST 1: Available Carriers")
        try:
            carriers_response = client.get_carriers()
            
            # Debug: Print raw response structure
            print(f"📋 Raw Response Type: {type(carriers_response)}")
            print(f"📋 Response Keys: {carriers_response.keys() if isinstance(carriers_response, dict) else 'Not a dict'}")
            
            # Handle different response formats
            if isinstance(carriers_response, dict):
                data_obj = carriers_response.get('data', {})
                # Check if data contains 'carriers' key
                if isinstance(data_obj, dict) and 'carriers' in data_obj:
                    carriers_list = data_obj['carriers']
                else:
                    carriers_list = data_obj if isinstance(data_obj, list) else []
            else:
                carriers_list = carriers_response
            
            print(f"✅ Carriers retrieved successfully!")
            print(f"\n🚚 Total Carriers: {len(carriers_list)}")
            
            # Count by type (handle both dict and string items)
            active_count = 0
            domestic_count = 0
            regional_count = 0
            international_count = 0
            
            for c in carriers_list:
                if isinstance(c, dict):
                    if c.get('active'):
                        active_count += 1
                    if c.get('domestic'):
                        domestic_count += 1
                    if c.get('regional'):
                        regional_count += 1
                    if c.get('international'):
                        international_count += 1
            
            print(f"\n📊 Carrier Statistics:")
            print(f"   Active: {active_count}")
            print(f"   Domestic: {domestic_count}")
            print(f"   Regional: {regional_count}")
            print(f"   International: {international_count}")
            
            print(f"\n📋 Carrier List:")
            for carrier in carriers_list:
                if isinstance(carrier, dict):
                    name = carrier.get('name', 'Unknown')
                    slug = carrier.get('slug', 'N/A')
                    active = "✅" if carrier.get('active') else "❌"
                    types = []
                    if carrier.get('domestic'):
                        types.append("Domestic")
                    if carrier.get('regional'):
                        types.append("Regional")
                    if carrier.get('international'):
                        types.append("International")
                    
                    print(f"   {active} {name} ({slug})")
                    print(f"      Types: {', '.join(types) if types else 'None'}")
                else:
                    print(f"   - {carrier} (type: {type(carrier)})")
            
        except TerminalAPIError as e:
            print(f"❌ Carriers error: {e.message}")
            print(f"   Status Code: {e.status_code}")
            if e.response_data:
                print(f"   Response: {e.response_data}")
            return False
        
        # Test 2: Sync Carriers to Database
        print_section("TEST 2: Sync Carriers to Database")
        try:
            carrier_mgr = get_carrier_manager()
            result = carrier_mgr.sync_carriers()
            
            print(f"✅ Carriers synced to database!")
            print(f"   Synced: {result['synced_count']} carriers")
            
            # Get stats
            stats = carrier_mgr.get_carrier_stats()
            print(f"\n📊 Database Statistics:")
            print(f"   Total: {stats['total']}")
            print(f"   Active: {stats['active']}")
            print(f"   Domestic: {stats['domestic']}")
            print(f"   Regional: {stats['regional']}")
            print(f"   International: {stats['international']}")
            
        except Exception as e:
            print(f"❌ Sync error: {str(e)}")
            return False
        
        # Test 3: Get Active Carriers from Database
        print_section("TEST 3: Query Local Carriers")
        try:
            carrier_mgr = get_carrier_manager()
            
            # Get active carriers
            active_carriers = carrier_mgr.get_local_carriers(active=True)
            print(f"✅ Active carriers from database: {len(active_carriers)}")
            
            # Get domestic carriers
            domestic_carriers = carrier_mgr.get_local_carriers(active=True, domestic=True)
            print(f"✅ Active domestic carriers: {len(domestic_carriers)}")
            
            # Get international carriers
            international_carriers = carrier_mgr.get_local_carriers(active=True, international=True)
            print(f"✅ Active international carriers: {len(international_carriers)}")
            
            # Show recommended carriers for Nigeria to Nigeria
            print(f"\n🎯 Recommended Carriers (NG → NG):")
            recommended = carrier_mgr.get_recommended_carriers('NG', 'NG')
            for carrier in recommended[:5]:
                print(f"   - {carrier['name']} ({carrier['slug']})")
            
        except Exception as e:
            print(f"❌ Query error: {str(e)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run live API tests."""
    print("\n" + "="*70)
    print("  TERMINAL AFRICA LIVE API TEST")
    print("="*70)
    print("\n⚠️  WARNING: This test uses LIVE API keys!")
    print("   Make sure you have activated your Terminal Africa account.")
    print("\n")
    
    success = test_live_connection()
    
    # Summary
    print_section("TEST SUMMARY")
    
    if success:
        print("🎉 All tests passed! Terminal Africa live API is working correctly.")
        print("\n✅ What was tested:")
        print("   1. Carriers list retrieval")
        print("   2. Carriers sync to database")
        print("   3. Local carrier queries")
        print("\n📋 Next Steps:")
        print("   1. Review carrier list above")
        print("   2. Enable/disable carriers as needed")
        print("   3. Test address creation")
        print("   4. Test packaging and parcels")
        print("   5. Test rate fetching")
        print("   6. Proceed to Phase 3 implementation")
        return 0
    else:
        print("❌ Tests failed. Please check the errors above.")
        print("\n🔍 Troubleshooting:")
        print("   1. Verify API keys are correct in config.py")
        print("   2. Check if Terminal Africa account is activated")
        print("   3. Ensure you have internet connection")
        print("   4. Contact Terminal Africa support if issues persist")
        return 1


if __name__ == "__main__":
    sys.exit(main())
