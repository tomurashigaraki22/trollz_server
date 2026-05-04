"""
Debug Terminal Africa cities API to understand the correct parameters
"""

import requests
from config import Config

def test_cities_api():
    """Test different parameter combinations for cities API"""
    
    base_url = Config.get_terminal_base_url()
    secret_key = Config.get_terminal_secret_key()
    
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json"
    }
    
    url = f"{base_url}/cities"
    
    # Test different parameter combinations
    test_cases = [
        {"country_code": "NG"},
        {"country_code": "NG", "state": "Lagos"},
        {"country_code": "NG", "state_name": "Lagos"},
        {"country_code": "NG", "state_code": "Lagos"},
        {"country": "NG", "state": "Lagos"},
    ]
    
    for i, params in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {params}")
        print(f"{'='*60}")
        
        try:
            response = requests.get(url, headers=headers, params=params)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Handle nested response
                if 'data' in data:
                    cities_data = data['data']
                    if isinstance(cities_data, dict) and 'cities' in cities_data:
                        cities = cities_data['cities']
                    else:
                        cities = cities_data if isinstance(cities_data, list) else []
                else:
                    cities = data if isinstance(data, list) else []
                
                print(f"Cities found: {len(cities)}")
                
                if cities:
                    print(f"\nFirst 10 cities:")
                    for j, city in enumerate(cities[:10], 1):
                        if isinstance(city, dict):
                            name = city.get('name', city.get('city', 'Unknown'))
                            state = city.get('state', city.get('state_name', 'N/A'))
                            print(f"  {j:2d}. {name} (State: {state})")
                        else:
                            print(f"  {j:2d}. {city}")
                
                # Check if cities are actually filtered by state
                if len(cities) > 0 and isinstance(cities[0], dict):
                    lagos_cities = [c for c in cities if 'Lagos' in str(c.get('state', c.get('state_name', '')))]
                    print(f"\nCities with 'Lagos' in state field: {len(lagos_cities)}")
                    
                    if len(lagos_cities) > 0:
                        print("✅ State filtering appears to work!")
                    else:
                        print("❌ State filtering not working")
                
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Exception: {str(e)}")


if __name__ == "__main__":
    test_cities_api()