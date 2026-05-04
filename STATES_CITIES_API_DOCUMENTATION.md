# States & Cities API Documentation

**Complete reference for Nigerian states and cities endpoints**

---

## 📋 Overview

These endpoints provide access to Nigerian states and cities data from Terminal Africa. The data includes geographic coordinates, state/city codes, and proper state-to-city relationships.

**Base URL:** `http://localhost:4500`

---

## 🌍 Get States

Get list of all Nigerian states with their details.

### Endpoint
```http
GET /api/shipping/states
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `country_code` | string | No | `NG` | Country code (Nigeria) |

### Request Example

```http
GET /api/shipping/states?country_code=NG
```

```javascript
// JavaScript/Fetch
const response = await fetch('http://localhost:4500/api/shipping/states?country_code=NG');
const data = await response.json();
```

```javascript
// Axios
const response = await axios.get('http://localhost:4500/api/shipping/states', {
  params: { country_code: 'NG' }
});
```

### Response Format

```json
{
  "status": "success",
  "message": "States retrieved successfully for NG",
  "data": {
    "states": [
      {
        "_id": "6655e70908597eace4d4c383",
        "name": "Lagos",
        "isoCode": "LA",
        "countryCode": "NG",
        "latitude": "6.52437930",
        "longitude": "3.37920570",
        "state_id": "JYMK526U3GGF",
        "id": "6655e70908597eace4d4c383",
        "updated_at": "2025-04-05T15:56:27.324Z"
      }
    ],
    "count": 37,
    "country_code": "NG"
  }
}
```

### State Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `_id` | string | MongoDB ObjectId |
| `name` | string | Full state name (e.g., "Lagos", "Abuja") |
| `isoCode` | string | 2-letter state code (e.g., "LA", "FC") |
| `countryCode` | string | Country code ("NG") |
| `latitude` | string | Geographic latitude |
| `longitude` | string | Geographic longitude |
| `state_id` | string | Terminal Africa state identifier |
| `id` | string | Same as _id |
| `updated_at` | string | Last update timestamp |

### Complete States List

| # | State Name | ISO Code | # Cities |
|---|------------|----------|----------|
| 1 | Abia | AB | 21 |
| 2 | Abuja | FC | 10 |
| 3 | Adamawa | AD | 12 |
| 4 | Akwa Ibom | AK | 6 |
| 5 | Anambra | AN | 13 |
| 6 | Bauchi | BA | 21 |
| 7 | Bayelsa | BY | 4 |
| 8 | Benue | BE | 11 |
| 9 | Borno | BO | 23 |
| 10 | Cross River | CR | 6 |
| 11 | Delta | DE | 15 |
| 12 | Ebonyi | EB | 6 |
| 13 | Edo | ED | 9 |
| 14 | Ekiti | EK | 14 |
| 15 | Enugu | EN | 15 |
| 16 | Gombe | GO | 14 |
| 17 | Imo | IM | 8 |
| 18 | Jigawa | JI | 15 |
| 19 | Kaduna | KD | 16 |
| 20 | Kano | KN | 3 |
| 21 | Katsina | KT | 14 |
| 22 | Kebbi | KE | 19 |
| 23 | Kogi | KO | 16 |
| 24 | Kwara | KW | 14 |
| 25 | **Lagos** | **LA** | **46** |
| 26 | Nasarawa | NA | 6 |
| 27 | Niger | NI | 20 |
| 28 | Ogun | OG | 16 |
| 29 | Ondo | ON | 9 |
| 30 | Osun | OS | 19 |
| 31 | Oyo | OY | 14 |
| 32 | Plateau | PL | 11 |
| 33 | Rivers | RI | 2 |
| 34 | Sokoto | SO | 10 |
| 35 | Taraba | TA | 11 |
| 36 | Yobe | YO | 17 |
| 37 | Zamfara | ZA | 11 |

---

## 🏙️ Get Cities

Get list of cities, optionally filtered by state.

### Endpoint
```http
GET /api/shipping/cities
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `country_code` | string | No | `NG` | Country code (Nigeria) |
| `state` | string | No | - | State name to filter cities |

### Request Examples

#### Get All Cities
```http
GET /api/shipping/cities?country_code=NG
```

#### Get Cities by State
```http
GET /api/shipping/cities?country_code=NG&state=Lagos
```

```javascript
// JavaScript/Fetch - All cities
const allCities = await fetch('http://localhost:4500/api/shipping/cities?country_code=NG');

// JavaScript/Fetch - Lagos cities only
const lagosCities = await fetch('http://localhost:4500/api/shipping/cities?country_code=NG&state=Lagos');
```

```javascript
// Axios - Cities by state
const response = await axios.get('http://localhost:4500/api/shipping/cities', {
  params: { 
    country_code: 'NG',
    state: 'Lagos'
  }
});
```

### Response Format

```json
{
  "status": "success",
  "message": "Cities retrieved successfully",
  "data": {
    "cities": [
      {
        "_id": "6655f66408597eace4daa4e8",
        "name": "Agege",
        "stateCode": "LA",
        "countryCode": "NG",
        "latitude": "6.6252564",
        "longitude": "3.3112093",
        "city_id": "O04WLJ",
        "id": "6655f66408597eace4daa4e8",
        "updated_at": "2025-04-05T14:42:53.131Z"
      }
    ],
    "count": 46,
    "country_code": "NG",
    "state": "Lagos"
  }
}
```

### City Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `_id` | string | MongoDB ObjectId |
| `name` | string | City name (e.g., "Agege", "Ikeja") |
| `stateCode` | string | 2-letter state code (e.g., "LA") |
| `countryCode` | string | Country code ("NG") |
| `latitude` | string | Geographic latitude |
| `longitude` | string | Geographic longitude |
| `city_id` | string | Terminal Africa city identifier |
| `id` | string | Same as _id |
| `updated_at` | string | Last update timestamp |

### Lagos Cities (Sample)

Lagos state has **46 cities**. Here are some examples:

| City Name | State Code | Latitude | Longitude |
|-----------|------------|----------|-----------|
| Agege | LA | 6.6252564 | 3.3112093 |
| Ajah | LA | 6.4698803 | 3.5663896 |
| Ajao | LA | 6.5355999 | 3.3411999 |
| Ajeromi | LA | 6.4598803 | 3.3263896 |
| Alimosho | LA | 6.6252564 | 3.3112093 |
| Apapa | LA | 6.4598803 | 3.3663896 |
| Badagry | LA | 6.4319444 | 2.8877778 |
| Festac Town | LA | 6.4598803 | 3.2863896 |
| Gbagada | LA | 6.5355999 | 3.3811999 |
| Ikeja | LA | 6.5955999 | 3.3411999 |
| Ikorodu | LA | 6.6155999 | 3.5111999 |
| Lagos | LA | 6.4540348 | 3.3952517 |
| Lagos Island | LA | 6.4540348 | 3.4252517 |
| Lekki | LA | 6.4698803 | 3.5863896 |
| Surulere | LA | 6.4998803 | 3.3563896 |
| Victoria Island | LA | 6.4298803 | 3.4163896 |
| Yaba | LA | 6.5155999 | 3.3711999 |

---

## 🔧 Frontend Integration

### React Hook Example

```jsx
import { useState, useEffect } from 'react';

function useStatesAndCities() {
  const [states, setStates] = useState([]);
  const [cities, setCities] = useState([]);
  const [selectedState, setSelectedState] = useState('');
  const [loading, setLoading] = useState(false);

  // Fetch states on component mount
  useEffect(() => {
    fetchStates();
  }, []);

  // Fetch cities when state changes
  useEffect(() => {
    if (selectedState) {
      fetchCities(selectedState);
    } else {
      setCities([]);
    }
  }, [selectedState]);

  const fetchStates = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:4500/api/shipping/states?country_code=NG');
      const data = await response.json();
      setStates(data.data.states);
    } catch (error) {
      console.error('Error fetching states:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCities = async (stateName) => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:4500/api/shipping/cities?country_code=NG&state=${encodeURIComponent(stateName)}`
      );
      const data = await response.json();
      setCities(data.data.cities);
    } catch (error) {
      console.error('Error fetching cities:', error);
    } finally {
      setLoading(false);
    }
  };

  return {
    states,
    cities,
    selectedState,
    setSelectedState,
    loading
  };
}

// Usage in component
function AddressForm() {
  const { states, cities, selectedState, setSelectedState, loading } = useStatesAndCities();

  return (
    <form>
      <div>
        <label>State:</label>
        <select 
          value={selectedState} 
          onChange={(e) => setSelectedState(e.target.value)}
          disabled={loading}
        >
          <option value="">Select State</option>
          {states.map(state => (
            <option key={state.isoCode} value={state.name}>
              {state.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label>City:</label>
        <select disabled={!selectedState || loading}>
          <option value="">Select City</option>
          {cities.map(city => (
            <option key={city.city_id} value={city.name}>
              {city.name}
            </option>
          ))}
        </select>
      </div>

      {loading && <p>Loading...</p>}
    </form>
  );
}
```

### Vanilla JavaScript Example

```javascript
class LocationSelector {
  constructor(stateSelectId, citySelectId) {
    this.stateSelect = document.getElementById(stateSelectId);
    this.citySelect = document.getElementById(citySelectId);
    this.baseUrl = 'http://localhost:4500';
    
    this.init();
  }

  async init() {
    await this.loadStates();
    this.stateSelect.addEventListener('change', (e) => {
      this.loadCities(e.target.value);
    });
  }

  async loadStates() {
    try {
      const response = await fetch(`${this.baseUrl}/api/shipping/states?country_code=NG`);
      const data = await response.json();
      
      this.stateSelect.innerHTML = '<option value="">Select State</option>';
      
      data.data.states.forEach(state => {
        const option = document.createElement('option');
        option.value = state.name;
        option.textContent = state.name;
        this.stateSelect.appendChild(option);
      });
    } catch (error) {
      console.error('Error loading states:', error);
    }
  }

  async loadCities(stateName) {
    if (!stateName) {
      this.citySelect.innerHTML = '<option value="">Select City</option>';
      return;
    }

    try {
      const response = await fetch(
        `${this.baseUrl}/api/shipping/cities?country_code=NG&state=${encodeURIComponent(stateName)}`
      );
      const data = await response.json();
      
      this.citySelect.innerHTML = '<option value="">Select City</option>';
      
      data.data.cities.forEach(city => {
        const option = document.createElement('option');
        option.value = city.name;
        option.textContent = city.name;
        this.citySelect.appendChild(option);
      });
    } catch (error) {
      console.error('Error loading cities:', error);
    }
  }
}

// Usage
const locationSelector = new LocationSelector('state-select', 'city-select');
```

---

## 📱 Mobile/Flutter Example

```dart
class LocationService {
  static const String baseUrl = 'http://localhost:4500';

  static Future<List<State>> getStates() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/shipping/states?country_code=NG'),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final List<dynamic> statesJson = data['data']['states'];
      return statesJson.map((json) => State.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load states');
    }
  }

  static Future<List<City>> getCities(String stateName) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/shipping/cities?country_code=NG&state=${Uri.encodeComponent(stateName)}'),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final List<dynamic> citiesJson = data['data']['cities'];
      return citiesJson.map((json) => City.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load cities');
    }
  }
}

class State {
  final String name;
  final String isoCode;
  final String latitude;
  final String longitude;

  State({required this.name, required this.isoCode, required this.latitude, required this.longitude});

  factory State.fromJson(Map<String, dynamic> json) {
    return State(
      name: json['name'],
      isoCode: json['isoCode'],
      latitude: json['latitude'],
      longitude: json['longitude'],
    );
  }
}

class City {
  final String name;
  final String stateCode;
  final String latitude;
  final String longitude;

  City({required this.name, required this.stateCode, required this.latitude, required this.longitude});

  factory City.fromJson(Map<String, dynamic> json) {
    return City(
      name: json['name'],
      stateCode: json['stateCode'],
      latitude: json['latitude'],
      longitude: json['longitude'],
    );
  }
}
```

---

## ⚠️ Important Notes

### 1. No Postal Codes
- Terminal Africa API does not provide postal codes
- If you need postal codes, you'll need to maintain a separate mapping
- Consider using latitude/longitude for location-based services

### 2. State Name Matching
- Use exact state names for filtering: "Lagos", "Abuja", "Rivers"
- State names are case-sensitive
- Use the complete state name, not abbreviations

### 3. Performance
- States endpoint: < 1 second response time
- Cities endpoint (all): ~1-2 seconds (497 cities)
- Cities endpoint (filtered): < 1 second

### 4. Caching Recommendations
- Cache states data (rarely changes)
- Cache cities data for 24 hours
- Use state-specific caching for cities

### 5. Error Handling
```javascript
try {
  const response = await fetch('/api/shipping/states');
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const data = await response.json();
  
  if (data.status !== 'success') {
    throw new Error(data.message || 'API error');
  }
  
  return data.data.states;
} catch (error) {
  console.error('Error fetching states:', error);
  // Handle error appropriately
}
```

---

## 🧪 Testing

### Test States Endpoint
```bash
curl "http://localhost:4500/api/shipping/states?country_code=NG"
```

### Test Cities Endpoint
```bash
# All cities
curl "http://localhost:4500/api/shipping/cities?country_code=NG"

# Lagos cities only
curl "http://localhost:4500/api/shipping/cities?country_code=NG&state=Lagos"
```

### Test Script
```bash
python test_states_endpoint.py
```

---

## 📊 Response Times

| Endpoint | Response Time | Data Size |
|----------|---------------|-----------|
| Get States | < 1 second | 37 states |
| Get All Cities | 1-2 seconds | 497 cities |
| Get Cities (Lagos) | < 1 second | 46 cities |
| Get Cities (Rivers) | < 1 second | 2 cities |

---

## 🔗 Related Endpoints

- **Address Creation:** `POST /api/addresses` - Use state/city names from these endpoints
- **Shipping Rates:** `POST /api/shipping/rates` - Requires addresses with valid states/cities
- **Address Validation:** Validates against these state/city lists

---

## 📞 Support

- **Base URL:** `http://localhost:4500`
- **Environment:** TEST (sandbox.terminal.africa)
- **Documentation:** This file
- **Test Script:** `test_states_endpoint.py`

---

**Version:** 1.0  
**Last Updated:** May 4, 2026  
**Status:** ✅ Production Ready