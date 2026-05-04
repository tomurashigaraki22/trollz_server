"""
Get state codes from Terminal Africa to understand the mapping
"""

import requests
from config import Config

def get_state_codes():
    """Get states with their codes"""
    
    base_url = Config.get_terminal_base_url()
    secret_key = Config.get_terminal_secret_key()
    
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json"
    }
    
    # Get states
    states_url = f"{base_url}/states"
    response = requests.get(states_url, headers=headers, params={"country_code": "NG"})
    
    if response.status_code == 200:
        states_data = response.json()
        
        if 'data' in states_data:
            states = states_data['data']
        else:
            states = states_data
        
        print("States and their potential codes:")
        print("="*60)
        
        for i, state in enumerate(states, 1):
            print(f"{i:2d}. {state}")
        
        print("\n" + "="*60)
    
    # Get cities to see state codes
    cities_url = f"{base_url}/cities"
    response = requests.get(cities_url, headers=headers, params={"country_code": "NG"})
    
    if response.status_code == 200:
        cities_data = response.json()
        
        if 'data' in cities_data:
            cities = cities_data['data']
        else:
            cities = cities_data
        
        # Extract unique state codes
        state_codes = {}
        for city in cities:
            if isinstance(city, dict):
                state_code = city.get('stateCode', 'N/A')
                city_name = city.get('name', 'Unknown')
                
                if state_code not in state_codes:
                    state_codes[state_code] = []
                state_codes[state_code].append(city_name)
        
        print(f"\nFound {len(state_codes)} unique state codes:")
        print("="*60)
        
        for code, cities_list in sorted(state_codes.items()):
            print(f"{code}: {len(cities_list)} cities (e.g., {', '.join(cities_list[:3])})")
        
        # Try to map state names to codes
        print(f"\nLooking for Lagos cities...")
        lagos_cities = [c for c in cities if 'Lagos' in c.get('name', '')]
        
        if lagos_cities:
            print(f"Found {len(lagos_cities)} cities with 'Lagos' in name:")
            for city in lagos_cities[:10]:
                print(f"  - {city.get('name')} (State Code: {city.get('stateCode')})")
        
        # Check what state code Lagos uses
        potential_lagos_codes = ['LA', 'LG', 'LAG']
        for code in potential_lagos_codes:
            if code in state_codes:
                print(f"\nState code '{code}' has {len(state_codes[code])} cities:")
                print(f"  Examples: {', '.join(state_codes[code][:5])}")


if __name__ == "__main__":
    get_state_codes()