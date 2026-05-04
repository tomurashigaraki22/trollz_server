"""
Test the states and cities endpoints
"""

import requests

BASE_URL = "http://localhost:4500"

def test_get_states():
    """Test getting states for Nigeria"""
    print("="*60)
    print("Testing: GET /api/shipping/states")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/shipping/states?country_code=NG")
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        states = data["data"]["states"]
        
        print(f"\n✅ SUCCESS! Found {len(states)} states for Nigeria\n")
        print("States:")
        print("-"*60)
        
        for i, state in enumerate(states, 1):
            if isinstance(state, dict):
                name = state.get('name', state.get('state', 'Unknown'))
                print(f"{i:2d}. {name}")
            else:
                print(f"{i:2d}. {state}")
        
        print("-"*60)
        
        return True
    else:
        print(f"\n❌ FAILED")
        print(f"Response: {response.text}")
        return False


def test_get_cities():
    """Test getting cities for Lagos state"""
    print("\n" + "="*60)
    print("Testing: GET /api/shipping/cities")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/shipping/cities?country_code=NG&state=Lagos")
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        cities = data["data"]["cities"]
        
        print(f"\n✅ SUCCESS! Found {len(cities)} cities for Lagos\n")
        print("Cities (first 20):")
        print("-"*60)
        
        for i, city in enumerate(cities[:20], 1):
            if isinstance(city, dict):
                name = city.get('name', city.get('city', 'Unknown'))
                print(f"{i:2d}. {name}")
            else:
                print(f"{i:2d}. {city}")
        
        if len(cities) > 20:
            print(f"... and {len(cities) - 20} more")
        
        print("-"*60)
        
        return True
    else:
        print(f"\n❌ FAILED")
        print(f"Response: {response.text}")
        return False


if __name__ == "__main__":
    print("\n🧪 Testing Terminal Africa States & Cities Endpoints\n")
    
    # Test states
    states_ok = test_get_states()
    
    # Test cities
    cities_ok = test_get_cities()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"States Endpoint: {'✅ PASS' if states_ok else '❌ FAIL'}")
    print(f"Cities Endpoint: {'✅ PASS' if cities_ok else '❌ FAIL'}")
    print("="*60)
    
    if states_ok and cities_ok:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed")
