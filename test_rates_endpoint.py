"""
Test different rates endpoint formats
"""

import requests
from config import Config

BASE_URL = Config.get_terminal_base_url()
SECRET_KEY = Config.get_terminal_secret_key()

headers = {
    "Authorization": f"Bearer {SECRET_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "origin_address": "AD-27B44IEBPXKLSKHR",
    "destination_address": "AD-7EU6KL7WALWDNXHP",
    "parcel": "PC-GNCKHEX6HOP6GNFY",
    "currency": "NGN"
}

endpoints_to_try = [
    "/rates",
    "/rates/shipment",
    "/shipment/rates",
    "/quotes",
    "/shipments/rates"
]

print("Testing different rates endpoints...")
print(f"Base URL: {BASE_URL}")
print()

for endpoint in endpoints_to_try:
    url = f"{BASE_URL}{endpoint}"
    print(f"Trying: POST {url}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code != 404:
            print(f"  ✅ Found working endpoint!")
            print(f"  Response: {response.text[:200]}")
            break
        else:
            print(f"  ❌ 404 Not Found")
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
    
    print()
