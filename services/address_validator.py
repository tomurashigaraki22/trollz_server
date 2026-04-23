"""
Address Validation and Formatting Utilities
Validates and formats addresses for Sendbox API.
"""

from typing import Dict, Tuple, Optional


# Nigerian states with their codes
NIGERIAN_STATES = {
    "abia": "ABI",
    "adamawa": "ADA",
    "akwa ibom": "AKW",
    "anambra": "ANA",
    "bauchi": "BAU",
    "bayelsa": "BAY",
    "benue": "BEN",
    "borno": "BOR",
    "cross river": "CRO",
    "delta": "DEL",
    "ebonyi": "EBO",
    "edo": "EDO",
    "ekiti": "EKI",
    "enugu": "ENU",
    "gombe": "GOM",
    "imo": "IMO",
    "jigawa": "JIG",
    "kaduna": "KAD",
    "kano": "KAN",
    "katsina": "KAT",
    "kebbi": "KEB",
    "kogi": "KOG",
    "kwara": "KWA",
    "lagos": "LOS",
    "nasarawa": "NAS",
    "niger": "NIG",
    "ogun": "OGU",
    "ondo": "OND",
    "osun": "OSU",
    "oyo": "OYO",
    "plateau": "PLA",
    "rivers": "RIV",
    "sokoto": "SOK",
    "taraba": "TAR",
    "yobe": "YOB",
    "zamfara": "ZAM",
    "abuja": "ABV",
    "fct": "ABV"
}


# Common country codes
COUNTRY_CODES = {
    "nigeria": "NG",
    "united states": "US",
    "united kingdom": "GB",
    "ghana": "GH",
    "south africa": "ZA",
    "kenya": "KE",
    "france": "FR",
    "germany": "DE",
    "canada": "CA",
    "australia": "AU"
}


def get_state_code(state_name: str) -> Optional[str]:
    """
    Get state code from state name.
    
    Args:
        state_name: State name (case-insensitive)
        
    Returns:
        State code or None if not found
    """
    if not state_name:
        return None
    
    state_lower = state_name.lower().strip()
    return NIGERIAN_STATES.get(state_lower)


def get_country_code(country_name: str) -> Optional[str]:
    """
    Get country code from country name.
    
    Args:
        country_name: Country name (case-insensitive)
        
    Returns:
        Country code or None if not found
    """
    if not country_name:
        return None
    
    country_lower = country_name.lower().strip()
    return COUNTRY_CODES.get(country_lower)


def validate_address(address: Dict) -> Tuple[bool, Optional[str]]:
    """
    Validate address dictionary for Sendbox API.
    
    Args:
        address: Address dictionary
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ["first_name", "last_name", "street", "city", "state", "country", "phone"]
    
    # Check required fields
    for field in required_fields:
        if field not in address or not address[field]:
            return False, f"Missing required field: {field}"
    
    # Validate country code
    country = address.get("country", "")
    if len(country) != 2:
        return False, "Country must be a 2-letter country code (e.g., NG, US, GB)"
    
    # Validate phone number format
    phone = address.get("phone", "")
    if not phone.startswith("+"):
        return False, "Phone number must start with country code (e.g., +234)"
    
    # Validate email if provided
    email = address.get("email")
    if email and "@" not in email:
        return False, "Invalid email format"
    
    return True, None


def format_address_for_sendbox(
    first_name: str,
    last_name: str,
    phone: str,
    street: str,
    city: str,
    state: str,
    country: str = "NG",
    email: str = None,
    street_line_2: str = None,
    post_code: str = None,
    lng: float = None,
    lat: float = None
) -> Dict:
    """
    Format address data for Sendbox API.
    
    Args:
        first_name: First name
        last_name: Last name
        phone: Phone number with country code
        street: Street address
        city: City name
        state: State name
        country: Country code (default: NG)
        email: Email address (optional)
        street_line_2: Additional street info (optional)
        post_code: Postal code (optional)
        lng: Longitude (optional)
        lat: Latitude (optional)
        
    Returns:
        Formatted address dictionary
    """
    address = {
        "first_name": first_name.strip(),
        "last_name": last_name.strip(),
        "phone": phone.strip(),
        "street": street.strip(),
        "city": city.strip(),
        "state": state.strip(),
        "country": country.upper().strip(),
        "email": email.strip() if email else None,
        "street_line_2": street_line_2.strip() if street_line_2 else "",
        "post_code": post_code.strip() if post_code else None,
        "lng": lng,
        "lat": lat,
        "name": None
    }
    
    return address


def parse_full_address(full_address: str) -> Dict:
    """
    Parse a full address string into components.
    This is a basic parser - may need enhancement for complex addresses.
    
    Args:
        full_address: Full address as string
        
    Returns:
        Dictionary with parsed address components
    """
    # This is a simple implementation
    # In production, you might want to use a proper address parsing library
    
    parts = [p.strip() for p in full_address.split(",")]
    
    parsed = {
        "street": parts[0] if len(parts) > 0 else "",
        "city": parts[1] if len(parts) > 1 else "",
        "state": parts[2] if len(parts) > 2 else "",
        "country": "NG"
    }
    
    return parsed


def format_phone_number(phone: str, default_country_code: str = "+234") -> str:
    """
    Format phone number with country code.
    
    Args:
        phone: Phone number
        default_country_code: Default country code to add if missing
        
    Returns:
        Formatted phone number with country code
    """
    phone = phone.strip().replace(" ", "").replace("-", "")
    
    # If already has country code
    if phone.startswith("+"):
        return phone
    
    # Remove leading zero if present
    if phone.startswith("0"):
        phone = phone[1:]
    
    # Add default country code
    return f"{default_country_code} {phone}"


def calculate_service_type(origin_country: str, destination_country: str) -> str:
    """
    Determine service type based on origin and destination countries.
    
    Args:
        origin_country: Origin country code
        destination_country: Destination country code
        
    Returns:
        Service type: 'local', 'nation-wide', or 'international'
    """
    if origin_country != destination_country:
        return "international"
    
    # For Nigeria, we can differentiate between local and nation-wide
    # For now, default to local
    return "local"


def is_international_shipment(origin_country: str, destination_country: str) -> bool:
    """
    Check if shipment is international.
    
    Args:
        origin_country: Origin country code
        destination_country: Destination country code
        
    Returns:
        True if international, False otherwise
    """
    return origin_country.upper() != destination_country.upper()
