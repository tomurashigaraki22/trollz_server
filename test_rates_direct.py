"""
Test rates endpoint directly with Terminal API
"""

import requests
from config import Config

BASE_URL = Config.get_terminal_base_url()
SECRET_KEY = Config.get_terminal_secret_key()

headers = {
    "Authorization": f"Bearer {SECRET_KEY}"
}

# Use the addresses and parcel from our debug test
params = {
    "pickup_address": "AD-27B44IEBPXKLSKHR",
    "delivery_address": "AD-7EU6KL7WALWDNXHP",
    "parcel_id": "PC-YG3JJ7U018K2V09X",
    "currency": "NGN"
}

url = f"{BASE_URL}/rates/shipment"

print(f"Testing: GET {url}")
print(f"Params: {params}")
print()

response = requests.get(url, headers=headers, params=params, timeout=30)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")
