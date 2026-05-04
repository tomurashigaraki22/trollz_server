"""
Test detailed data structure for states and cities endpoints
"""

import requests
import json

BASE_URL = "http://localhost:4500"

def test_states_structure():
    """Test states endpoint and show full data structure"""
    print("="*80)
    print("STATES ENDPOINT - DETAILED STRUCTURE")
    print("="*80)
    
    response = requests.get(f"{BASE_URL}/api/shipping/states?country_code=NG")
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"Response Structure:")
        print(f"  Status: {data.get('status')}")
        print(f"  Message: {data.get('message')}")
        print(f"  Data Keys: {list(data.get('data', {}).keys())}")
        
        states = data["data"]["states"]
        print(f"\nFirst State Full Structure:")
        print(json.dumps(states[0], indent=2))
        
        print(f"\nLagos State Full Structure:")
        lagos_state = next((s for s in states if s.get('name') == 'Lagos'), None)
        if lagos_state:
            print(json.dumps(lagos_state, indent=2))
        
        return True
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return False


def test_cities_structure():
    """Test cities endpoint and show full data structure"""
    print("\n" + "="*80)
    print("CITIES ENDPOINT - DETAILED STRUCTURE")
    print("="*80)
    
    response = requests.get(f"{BASE_URL}/api/shipping/cities?country_code=NG&state=Lagos")
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"Response Structure:")
        print(f"  Status: {data.get('status')}")
        print(f"  Message: {data.get('message')}")
        print(f"  Data Keys: {list(data.get('data', {}).keys())}")
        
        cities = data["data"]["cities"]
        print(f"\nFirst City Full Structure:")
        print(json.dumps(cities[0], indent=2))
        
        print(f"\nLagos City Full Structure:")
        lagos_city = next((c for c in cities if c.get('name') == 'Lagos'), None)
        if lagos_city:
            print(json.dumps(lagos_city, indent=2))
        else:
            print("Lagos city not found in the list")
        
        # Check for postal codes
        cities_with_postal = [c for c in cities if c.get('postalCode') or c.get('postal_code') or c.get('zipCode')]
        print(f"\nCities with postal codes: {len(cities_with_postal)}")
        
        if cities_with_postal:
            print("Example city with postal code:")
            print(json.dumps(cities_with_postal[0], indent=2))
        
        return True
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return False


def test_all_cities():
    """Test cities endpoint without state filter"""
    print("\n" + "="*80)
    print("ALL CITIES ENDPOINT - SAMPLE STRUCTURE")
    print("="*80)
    
    response = requests.get(f"{BASE_URL}/api/shipping/cities?country_code=NG")
    
    if response.status_code == 200:
        data = response.json()
        cities = data["data"]["cities"]
        
        print(f"Total cities: {len(cities)}")
        
        # Sample cities from different states
        sample_cities = cities[:5]
        print(f"\nSample Cities Structure:")
        for i, city in enumerate(sample_cities, 1):
            print(f"\nCity {i}:")
            print(json.dumps(city, indent=2))
        
        return True
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return False


if __name__ == "__main__":
    print("🔍 Testing Detailed Data Structure for States & Cities\n")
    
    # Test states
    states_ok = test_states_structure()
    
    # Test cities (Lagos)
    cities_ok = test_cities_structure()
    
    # Test all cities
    all_cities_ok = test_all_cities()
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"States Structure: {'✅ PASS' if states_ok else '❌ FAIL'}")
    print(f"Cities Structure: {'✅ PASS' if cities_ok else '❌ FAIL'}")
    print(f"All Cities: {'✅ PASS' if all_cities_ok else '❌ FAIL'}")