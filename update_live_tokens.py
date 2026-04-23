"""
Helper script to update Sendbox tokens for live environment.
Run this script and paste your live tokens when prompted.
"""

import jwt
import sys


def validate_token(token, token_type):
    """Validate and decode a JWT token."""
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        print(f"\n✅ {token_type} is valid JWT")
        print(f"   - Issuer: {decoded.get('iss', 'N/A')}")
        print(f"   - App ID: {decoded.get('aid') or decoded.get('app_id', 'N/A')}")
        
        if 'exp' in decoded:
            import time
            exp_timestamp = decoded.get('exp', 0)
            time_until_expiry = exp_timestamp - time.time()
            
            if time_until_expiry > 0:
                days = int(time_until_expiry / 86400)
                hours = int((time_until_expiry % 86400) / 3600)
                print(f"   - Expires in: {days} days, {hours} hours")
            else:
                print(f"   - ⚠️  Token is EXPIRED")
                return False
        
        # Check if it's a staging token
        issuer = decoded.get('iss', '').lower()
        if 'staging' in issuer:
            print(f"   - ⚠️  WARNING: This appears to be a STAGING token")
            print(f"   - Make sure you got this from https://live.sendbox.co/")
        
        return True
        
    except Exception as e:
        print(f"\n❌ {token_type} validation failed: {str(e)}")
        return False


def main():
    print("\n" + "="*60)
    print("SENDBOX LIVE TOKENS UPDATE HELPER")
    print("="*60)
    print("\nThis script will help you update your Sendbox tokens")
    print("for the LIVE environment.")
    print("\nMake sure you have:")
    print("1. Logged in to https://live.sendbox.co/")
    print("2. Generated/copied your live tokens")
    print("3. Have: Access Token, Refresh Token, and Client Secret")
    
    print("\n" + "="*60)
    print("STEP 1: Access Token")
    print("="*60)
    access_token = input("\nPaste your LIVE Access Token: ").strip()
    
    if not validate_token(access_token, "Access Token"):
        print("\n❌ Invalid access token. Please try again.")
        return 1
    
    print("\n" + "="*60)
    print("STEP 2: Refresh Token")
    print("="*60)
    refresh_token = input("\nPaste your LIVE Refresh Token: ").strip()
    
    if not validate_token(refresh_token, "Refresh Token"):
        print("\n❌ Invalid refresh token. Please try again.")
        return 1
    
    print("\n" + "="*60)
    print("STEP 3: Client Secret")
    print("="*60)
    client_secret = input("\nPaste your LIVE Client Secret: ").strip()
    
    if not client_secret or len(client_secret) < 32:
        print("\n⚠️  Client secret seems too short. Are you sure it's correct?")
        confirm = input("Continue anyway? (yes/no): ").strip().lower()
        if confirm != 'yes':
            return 1
    else:
        print(f"\n✅ Client Secret received ({len(client_secret)} characters)")
    
    # Generate the code to update
    print("\n" + "="*60)
    print("UPDATE INSTRUCTIONS")
    print("="*60)
    print("\nTo update your tokens, open: services/sendbox_service.py")
    print("\nFind these lines (around line 45-47):")
    print("```python")
    print('ACCESS_TOKEN = "..."')
    print('REFRESH_TOKEN = "..."')
    print('CLIENT_SECRET = "..."')
    print("```")
    print("\nReplace them with:")
    print("```python")
    print(f'ACCESS_TOKEN = "{access_token}"')
    print(f'REFRESH_TOKEN = "{refresh_token}"')
    print(f'CLIENT_SECRET = "{client_secret}"')
    print("```")
    
    # Offer to create a file with the tokens
    print("\n" + "="*60)
    save = input("\nSave tokens to a file for easy copy-paste? (yes/no): ").strip().lower()
    
    if save == 'yes':
        with open('live_tokens_update.txt', 'w') as f:
            f.write("# Copy these lines and paste them in services/sendbox_service.py\n")
            f.write("# Replace the existing ACCESS_TOKEN, REFRESH_TOKEN, and CLIENT_SECRET lines\n\n")
            f.write(f'ACCESS_TOKEN = "{access_token}"\n')
            f.write(f'REFRESH_TOKEN = "{refresh_token}"\n')
            f.write(f'CLIENT_SECRET = "{client_secret}"\n')
        
        print("\n✅ Tokens saved to: live_tokens_update.txt")
        print("   Open this file and copy the lines to services/sendbox_service.py")
    
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("\n1. Update services/sendbox_service.py with the new tokens")
    print("2. Restart your server: python app.py")
    print("3. Test the connection: python test_token_refresh.py")
    print("4. You should see: Environment: live, API Response: 200")
    
    print("\n✅ Done! Update your tokens and restart the server.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        sys.exit(1)
