"""
Switch Terminal Africa Environment
Easily switch between test and live environments.
"""

import os
import sys


def switch_environment(env):
    """Switch Terminal environment."""
    if env not in ['test', 'live']:
        print(f"❌ Invalid environment: {env}")
        print("   Valid options: test, live")
        return False
    
    # Check if .env file exists
    env_file = '.env'
    env_exists = os.path.exists(env_file)
    
    if env_exists:
        # Read existing .env
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Update or add TERMINAL_ENV
        found = False
        new_lines = []
        for line in lines:
            if line.startswith('TERMINAL_ENV='):
                new_lines.append(f'TERMINAL_ENV={env}\n')
                found = True
            else:
                new_lines.append(line)
        
        if not found:
            new_lines.append(f'\nTERMINAL_ENV={env}\n')
        
        # Write back
        with open(env_file, 'w') as f:
            f.writelines(new_lines)
        
        print(f"✅ Updated .env file")
    else:
        # Create new .env file
        with open(env_file, 'w') as f:
            f.write(f'TERMINAL_ENV={env}\n')
        
        print(f"✅ Created .env file")
    
    # Show environment info
    print()
    print("="*70)
    print(f"  TERMINAL AFRICA ENVIRONMENT: {env.upper()}")
    print("="*70)
    print()
    
    if env == 'test':
        print("📋 Test Environment")
        print(f"   Base URL: https://sandbox.terminal.africa/v1")
        print(f"   Public Key: pk_test_WeDJ1I1cKKkubg60rE6kXnwPJXlExlH1")
        print(f"   Secret Key: sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn")
        print()
        print("✅ Using sandbox environment for testing")
        print("   - Faster API responses")
        print("   - No real charges")
        print("   - Test data only")
    else:
        print("🚀 Live Environment")
        print(f"   Base URL: https://api.terminal.africa/v1")
        print(f"   Public Key: pk_live_G8zfsoShEtgvDPUvHABwdF9Lw4a65HKg")
        print(f"   Secret Key: sk_live_jiep2FyoHX3tImNV4eVkdVl1SXIHrFWM")
        print()
        print("⚠️  Using live environment")
        print("   - Real API calls")
        print("   - May incur charges")
        print("   - Production data")
    
    print()
    print("🔄 Please restart your server for changes to take effect:")
    print("   python app.py")
    print()
    
    return True


def main():
    """Main function."""
    print()
    print("="*70)
    print("  TERMINAL AFRICA ENVIRONMENT SWITCHER")
    print("="*70)
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python switch_terminal_env.py [test|live]")
        print()
        print("Examples:")
        print("  python switch_terminal_env.py test   # Switch to test environment")
        print("  python switch_terminal_env.py live   # Switch to live environment")
        print()
        return 1
    
    env = sys.argv[1].lower()
    success = switch_environment(env)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
