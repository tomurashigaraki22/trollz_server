"""
Debug packaging to see what IDs we're getting
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.terminal_service import get_terminal_client
import json


def main():
    print("="*70)
    print("  DEBUG: Terminal Packaging")
    print("="*70)
    print()
    
    client = get_terminal_client()
    
    print(f"Environment: {client.environment}")
    print(f"Base URL: {client.base_url}")
    print()
    
    # Get packaging
    print("📦 Fetching packaging...")
    response = client.get_packaging(page=1, per_page=10)
    
    print("\n📋 Raw Response:")
    print(json.dumps(response, indent=2))
    print()
    
    # Parse response
    if 'data' in response:
        pkg_data = response['data']
        if isinstance(pkg_data, dict) and 'packaging' in pkg_data:
            packaging_list = pkg_data['packaging']
        else:
            packaging_list = pkg_data if isinstance(pkg_data, list) else []
    else:
        packaging_list = response if isinstance(response, list) else []
    
    print(f"\n✅ Found {len(packaging_list)} packaging options")
    print()
    
    if packaging_list:
        print("📋 Packaging Details:")
        for i, pkg in enumerate(packaging_list, 1):
            print(f"\n{i}. {pkg.get('name')}")
            print(f"   packaging_id: {pkg.get('packaging_id')}")
            print(f"   id: {pkg.get('id')}")
            print(f"   _id: {pkg.get('_id')}")
            print(f"   type: {pkg.get('type')}")
            print(f"   dimensions: {pkg.get('length')}x{pkg.get('width')}x{pkg.get('height')} {pkg.get('size_unit')}")
    else:
        print("⚠️  No packaging found")
        print("\nCreating test packaging...")
        
        create_response = client.create_packaging(
            name="Test Box",
            type="box",
            length=30,
            width=20,
            height=15,
            weight=0.5,
            size_unit="cm",
            weight_unit="kg"
        )
        
        print("\n📋 Create Response:")
        print(json.dumps(create_response, indent=2))


if __name__ == "__main__":
    main()
