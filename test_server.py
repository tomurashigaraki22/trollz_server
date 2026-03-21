#!/usr/bin/env python3
"""Quick test to verify the server works with the new database"""

import requests
import json

BASE_URL = "http://localhost:4500"

def test_endpoints():
    print("Testing Trollz Store API with new database...\n")
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("   ✓ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        print("   Make sure the server is running: python app.py")
        return
    
    # Test 2: Get products
    print("\n2. Testing products endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/products?limit=3")
        if response.status_code == 200:
            data = response.json()
            products = data['data']['products']
            total = data['data']['pagination']['total']
            print(f"   ✓ Products endpoint working")
            print(f"   Total products: {total}")
            print(f"   Returned: {len(products)} products")
            if products:
                print(f"   First product: {products[0]['item']}")
        else:
            print(f"   ✗ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 3: Get categories
    print("\n3. Testing categories endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/categories")
        if response.status_code == 200:
            data = response.json()
            categories = data['data']['categories']
            print(f"   ✓ Categories endpoint working")
            print(f"   Total categories: {len(categories)}")
            if categories:
                print(f"   Categories: {', '.join([c['category'] for c in categories[:5]])}...")
        else:
            print(f"   ✗ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 4: Search products
    print("\n4. Testing product search...")
    try:
        response = requests.get(f"{BASE_URL}/api/products/search?q=phone")
        if response.status_code == 200:
            data = response.json()
            products = data['data']['products']
            total = data['data']['pagination']['total']
            print(f"   ✓ Search endpoint working")
            print(f"   Found {total} products matching 'phone'")
        else:
            print(f"   ✗ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 5: Get products by category
    print("\n5. Testing category filter...")
    try:
        response = requests.get(f"{BASE_URL}/api/products/category/Fashion?limit=3")
        if response.status_code == 200:
            data = response.json()
            products = data['data']['products']
            total = data['data']['pagination']['total']
            print(f"   ✓ Category filter working")
            print(f"   Fashion products: {total}")
        else:
            print(f"   ✗ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "="*50)
    print("✓ All tests completed!")
    print("="*50)
    print("\nYour API is ready to use with the new database!")
    print("See QUICKSTART.md for more examples.")

if __name__ == "__main__":
    test_endpoints()
