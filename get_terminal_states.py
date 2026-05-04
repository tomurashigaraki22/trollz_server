"""
Get list of states supported by Terminal Africa for Nigeria
"""

import requests
from config import Config

def get_terminal_states():
    """Fetch list of states from Terminal Africa API"""
    
    base_url = Config.get_terminal_base_url()
    secret_key = Config.get_terminal_secret_key()
    
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json"
    }
    
    # Terminal Africa endpoint for getting states
    url = f"{base_url}/states"
    
    try:
        print(f"Fetching states from Terminal Africa...")
        print(f"URL: {url}")
        print(f"Environment: {Config.TERMINAL_ENVIRONMENT}")
        
        response = requests.get(url, headers=headers, params={"country_code": "NG"})
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Handle nested response
            if 'data' in data:
                states_data = data['data']
                if isinstance(states_data, dict) and 'states' in states_data:
                    states = states_data['states']
                else:
                    states = states_data if isinstance(states_data, list) else []
            else:
                states = data if isinstance(data, list) else []
            
            print(f"\n✅ Found {len(states)} states for Nigeria:\n")
            print("="*60)
            
            for i, state in enumerate(states, 1):
                if isinstance(state, dict):
                    name = state.get('name', state.get('state', 'Unknown'))
                    code = state.get('code', state.get('state_code', 'N/A'))
                    print(f"{i:2d}. {name:30s} (Code: {code})")
                else:
                    print(f"{i:2d}. {state}")
            
            print("="*60)
            
            # Save to file
            with open('terminal_nigeria_states.txt', 'w') as f:
                f.write("Terminal Africa - Nigeria States\n")
                f.write("="*60 + "\n\n")
                for state in states:
                    if isinstance(state, dict):
                        name = state.get('name', state.get('state', 'Unknown'))
                        code = state.get('code', state.get('state_code', 'N/A'))
                        f.write(f"{name} (Code: {code})\n")
                    else:
                        f.write(f"{state}\n")
            
            print(f"\n✅ States saved to: terminal_nigeria_states.txt")
            
            return states
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


if __name__ == "__main__":
    get_terminal_states()
