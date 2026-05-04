"""
Quick test to verify Terminal Africa carriers endpoint with live API keys.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.terminal_service import get_terminal_client, TerminalAPIError


def test_carriers():
    """Test fetching carriers from Terminal Africa."""
    print("\n" + "="*70)
    print("  TESTING TERMINAL AFRICA CARRIERS (LIVE API)")
    print("="*70 + "\n")
    
    try:
        client = get_terminal_client()
        
        print(f"🔧 Environment: {client.environment}")
        print(f"🔑 Using API Key: {client.secret_key[:20]}...")
        
        print("\n🚚 Testing carriers...")
        response = client.get_carriers()
        
        # Handle nested response structure
        if 'data' in response:
            carriers_data = response['data']
            
            # Check if carriers is nested further
            if isinstance(carriers_data, dict) and 'carriers' in carriers_data:
                carriers = carriers_data['carriers']
            else:
                carriers = carriers_data if isinstance(carriers_data, list) else []
        else:
            carriers = response if isinstance(response, list) else []
        
        print(f"✅ Success! Found {len(carriers)} carriers\n")
        
        # Display carriers
        active_count = 0
        for carrier in carriers:
            if isinstance(carrier, dict):
                name = carrier.get('name', 'Unknown')
                carrier_id = carrier.get('carrier_id', carrier.get('id', 'N/A'))
                active = carrier.get('active', False)
                domestic = carrier.get('domestic', False)
                regional = carrier.get('regional', False)
                international = carrier.get('international', False)
                
                if active:
                    active_count += 1
                
                status = "✅ Active" if active else "❌ Inactive"
                
                services = []
                if domestic:
                    services.append("Domestic")
                if regional:
                    services.append("Regional")
                if international:
                    services.append("International")
                
                print(f"  {name}")
                print(f"    ID: {carrier_id}")
                print(f"    Status: {status}")
                print(f"    Services: {', '.join(services) if services else 'None'}")
                print()
        
        print(f"📊 Summary:")
        print(f"   Total Carriers: {len(carriers)}")
        print(f"   Active Carriers: {active_count}")
        print(f"   Inactive Carriers: {len(carriers) - active_count}")
        
        return True
        
    except TerminalAPIError as e:
        print(f"⚠️  Carriers error: {e.message}")
        if e.status_code:
            print(f"   Status Code: {e.status_code}")
        if e.response_data:
            print(f"   Response: {e.response_data}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_carriers()
    sys.exit(0 if success else 1)
