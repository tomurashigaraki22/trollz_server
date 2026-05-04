"""
Debug Terminal Africa API endpoints to find the correct cities endpoint
"""

import requests
from config import Config

def test_endpoints():
    """Test different endpoints that might provide state-filtered cities"""
    
    base_url = Config.get_terminal_base_url()
    secret_key = Config.get_terminal_secret_key()
    
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json"
    }
    
    # Test different endpoints
    endpoints = [
        "/cities",
        "/states/Lagos/cities",
        "/locations/cities",
        "/addresses/cities",
        "/cities/NG/Lagos",
    ]
    
    for endpoint in endpoints:
        print(f"\n{'='*60}")
        print(f"Testing: {endpoint}")
        print(f"{'='*60}")
        
        url = f"{base_url}{endpoint}"
        
        try:
            # Try with different parameters
            params_list = [
                {"country_code": "NG"},
                {"country_code": "NG", "state": "Lagos"},
                {}
            ]
            
            for params in params_list:
                print(f"\nParams: {params}")
                response = requests.get(url, headers=headers, params=params)
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                    
                    # Try to find cities data
                    cities = []
                    if isinstance(data, dict):
                        if 'data' in data:
                            cities_data = data['data']
                            if isinstance(cities_data, dict) and 'cities' in cities_data:
                                cities = cities_data['cities']
                            elif isinstance(cities_data, list):
                                cities = cities_data
                        elif 'cities' in data:
                            cities = data['cities']
                        elif isinstance(data, list):
                            cities = data
                    
                    if cities:
                        print(f"Found {len(cities)} cities")
                        if len(cities) > 0:
                            print(f"First city: {cities[0]}")
                    else:
                        print("No cities found")
                        
                elif response.status_code == 404:
                    print("Endpoint not found")
                else:
                    print(f"Error: {response.text[:200]}")
                
                break  # Only test first params for each endpoint
                
        except Exception as e:
            print(f"Exception: {str(e)}")


if __name__ == "__main__":
    test_endpoints()