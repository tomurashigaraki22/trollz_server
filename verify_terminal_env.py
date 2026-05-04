"""
Verify Terminal Africa Environment
Check which environment is active and test connectivity.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from services.terminal_service import get_terminal_client, TerminalAPIError


def verify_environment():
    """Verify Terminal environment configuration."""
    print("\n" + "="*70)
    print("  TERMINAL AFRICA ENVIRONMENT VERIFICATION")
    print("="*70 + "\n")
    
    # Show configuration
    print("📋 Current Configuration:")
    print(f"   Environment: {Config.TERMINAL_ENVIRONMENT}")
    print(f"   Base URL: {Config.get_terminal_base_url()}")
    print(f"   Public Key: {Config.get_terminal_public_key()[:20]}...")
    print(f"   Secret Key: {Config.get_terminal_secret_key()[:20]}...")
    print()
    
    # Test connectivity
    print("🔌 Testing API Connectivity...")
    print()
    
    try:
        client = get_terminal_client()
        
        print(f"✅ Client initialized")
        print(f"   Environment: {client.environment}")
        print(f"   Base URL: {client.base_url}")
        print()
        
        # Test carriers endpoint
        print("🚚 Testing carriers endpoint...")
        response = client.get_carriers()
        
        # Handle nested response
        if 'data' in response:
            carriers_data = response['data']
            if isinstance(carriers_data, dict) and 'carriers' in carriers_data:
                carriers = carriers_data['carriers']
            else:
                carriers = carriers_data if isinstance(carriers_data, list) else []
        else:
            carriers = response if isinstance(response, list) else []
        
        print(f"✅ API is responding!")
        print(f"   Found {len(carriers)} carriers")
        print()
        
        # Show sample carriers
        if carriers:
            print("📋 Sample Carriers:")
            for carrier in carriers[:5]:
                if isinstance(carrier, dict):
                    name = carrier.get('name', 'Unknown')
                    active = carrier.get('active', False)
                    status = "✅" if active else "❌"
                    print(f"   {status} {name}")
            print()
        
        print("="*70)
        print("  ✅ VERIFICATION SUCCESSFUL")
        print("="*70)
        print()
        print(f"Terminal Africa {Config.TERMINAL_ENVIRONMENT.upper()} environment is working correctly!")
        print()
        
        return True
        
    except TerminalAPIError as e:
        print(f"❌ API Error: {e.message}")
        if e.status_code:
            print(f"   Status Code: {e.status_code}")
        print()
        print("="*70)
        print("  ❌ VERIFICATION FAILED")
        print("="*70)
        print()
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        print()
        print("="*70)
        print("  ❌ VERIFICATION FAILED")
        print("="*70)
        print()
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = verify_environment()
    sys.exit(0 if success else 1)
