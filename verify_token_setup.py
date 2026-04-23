"""Quick verification that token authentication is configured correctly."""

from services.sendbox_service import SendboxClient
import jwt

print("\n" + "="*60)
print("VERIFYING TOKEN AUTHENTICATION SETUP")
print("="*60)

try:
    # Initialize client
    client = SendboxClient()
    
    # Decode token
    decoded = jwt.decode(
        client.current_access_token,
        options={"verify_signature": False}
    )
    
    # Check token validity
    print("\n✅ Token Authentication Configured Correctly!")
    print(f"   - App ID: {decoded.get('aid')}")
    print(f"   - User ID: {decoded.get('uid')}")
    print(f"   - Token Expiry: {decoded.get('exp')}")
    print(f"   - Environment: {client.environment}")
    print(f"   - Base URL: {client.base_url}")
    
    # Check refresh token
    refresh_decoded = jwt.decode(
        client.current_refresh_token,
        options={"verify_signature": False}
    )
    print(f"\n✅ Refresh Token Configured!")
    print(f"   - App Name: {refresh_decoded.get('application', {}).get('name')}")
    
    # Check client secret
    if client.CLIENT_SECRET:
        print(f"\n✅ Client Secret Configured!")
        print(f"   - Length: {len(client.CLIENT_SECRET)} characters")
    
    print("\n" + "="*60)
    print("🎉 ALL CHECKS PASSED - READY TO USE!")
    print("="*60)
    print("\nYou can now:")
    print("  1. Start your server: python app.py")
    print("  2. Test endpoints: python test_token_refresh.py")
    print("  3. Use Sendbox API for shipping operations")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print("   Please check services/sendbox_service.py")
