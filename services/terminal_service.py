"""
Terminal Africa API Service
Handles all interactions with the Terminal Africa shipping API.
"""

import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from config import Config


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TerminalAPIError(Exception):
    """Custom exception for Terminal Africa API errors."""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class TerminalClient:
    """
    Terminal Africa API Client
    
    Provides methods to interact with Terminal Africa shipping API including:
    - Address management
    - Packaging management
    - Parcel creation
    - Rate fetching (multiple carriers)
    - Shipment creation
    - Tracking
    - Carrier management
    """
    
    def __init__(self, environment: str = None):
        """
        Initialize Terminal Africa client.
        
        Args:
            environment: 'test' or 'live' (defaults to Config.TERMINAL_ENVIRONMENT)
        """
        self.environment = environment or Config.TERMINAL_ENVIRONMENT
        self.base_url = Config.get_terminal_base_url()
        self.secret_key = Config.get_terminal_secret_key()
        self.public_key = Config.get_terminal_public_key()
        
        logger.info(f"Terminal Africa client initialized - Environment: {self.environment}, Base URL: {self.base_url}")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        return {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Dict = None,
        params: Dict = None
    ) -> Dict:
        """
        Make HTTP request to Terminal Africa API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            TerminalAPIError: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        try:
            logger.info(f"Terminal API Request: {method} {url}")
            
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
                timeout=30
            )
            
            # Log response
            logger.info(f"Terminal API Response: {response.status_code}")
            
            # Handle different status codes
            if response.status_code in [200, 201]:
                return response.json()
            elif response.status_code == 204:
                return {"success": True, "message": "Operation completed successfully"}
            elif response.status_code == 400:
                error_data = response.json() if response.text else {}
                raise TerminalAPIError(
                    f"Bad request: {error_data.get('message', 'Invalid request')}",
                    status_code=400,
                    response_data=error_data
                )
            elif response.status_code == 401:
                raise TerminalAPIError(
                    "Authentication failed. Please check your API key.",
                    status_code=401,
                    response_data=response.json() if response.text else None
                )
            elif response.status_code == 403:
                raise TerminalAPIError(
                    "Access forbidden. Insufficient permissions.",
                    status_code=403,
                    response_data=response.json() if response.text else None
                )
            elif response.status_code == 404:
                raise TerminalAPIError(
                    "Resource not found.",
                    status_code=404,
                    response_data=response.json() if response.text else None
                )
            elif response.status_code == 422:
                error_data = response.json() if response.text else {}
                raise TerminalAPIError(
                    f"Validation error: {error_data.get('message', 'Invalid data')}",
                    status_code=422,
                    response_data=error_data
                )
            else:
                # Other errors
                error_data = response.json() if response.text else {}
                raise TerminalAPIError(
                    f"API request failed: {response.status_code}",
                    status_code=response.status_code,
                    response_data=error_data
                )
                
        except requests.exceptions.Timeout:
            raise TerminalAPIError("Request timeout. Please try again.")
        except requests.exceptions.ConnectionError:
            raise TerminalAPIError("Connection error. Please check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise TerminalAPIError(f"Request failed: {str(e)}")
    
    # ==================== ADDRESS MANAGEMENT ====================
    
    def create_address(
        self,
        first_name: str,
        last_name: str,
        phone: str,
        email: str,
        line1: str,
        city: str,
        state: str,
        country: str,
        zip_code: str = None,
        line2: str = None,
        is_residential: bool = True
    ) -> Dict:
        """
        Create a new address in Terminal Africa.
        
        Args:
            first_name: First name
            last_name: Last name
            phone: Phone number
            email: Email address
            line1: Address line 1
            city: City
            state: State
            country: Country code (e.g., 'NG')
            zip_code: Postal/ZIP code
            line2: Address line 2 (optional)
            is_residential: Whether address is residential
            
        Returns:
            Dictionary with address details including address_id
        """
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
            "line1": line1,
            "city": city,
            "state": state,
            "country": country,
            "is_residential": is_residential
        }
        
        if line2:
            payload["line2"] = line2
        if zip_code:
            payload["zip"] = zip_code
        
        logger.info(f"Creating address for {first_name} {last_name} in {city}, {state}")
        
        response = self._make_request(
            method="POST",
            endpoint="/addresses",
            data=payload
        )
        
        return response
    
    def get_addresses(self, page: int = 1, per_page: int = 20) -> Dict:
        """
        Get all addresses.
        
        Args:
            page: Page number
            per_page: Items per page
            
        Returns:
            Dictionary with addresses list and pagination info
        """
        logger.info(f"Fetching addresses - Page: {page}")
        
        response = self._make_request(
            method="GET",
            endpoint="/addresses",
            params={"page": page, "perPage": per_page}
        )
        
        return response
    
    def get_address(self, address_id: str) -> Dict:
        """
        Get a specific address by ID.
        
        Args:
            address_id: Terminal address ID
            
        Returns:
            Address details dictionary
        """
        logger.info(f"Fetching address: {address_id}")
        
        response = self._make_request(
            method="GET",
            endpoint=f"/addresses/{address_id}"
        )
        
        return response
    
    def update_address(self, address_id: str, **kwargs) -> Dict:
        """
        Update an existing address.
        
        Args:
            address_id: Terminal address ID
            **kwargs: Fields to update
            
        Returns:
            Updated address details
        """
        logger.info(f"Updating address: {address_id}")
        
        response = self._make_request(
            method="PATCH",
            endpoint=f"/addresses/{address_id}",
            data=kwargs
        )
        
        return response
    
    def delete_address(self, address_id: str) -> Dict:
        """
        Delete an address.
        
        Args:
            address_id: Terminal address ID
            
        Returns:
            Success response
        """
        logger.info(f"Deleting address: {address_id}")
        
        response = self._make_request(
            method="DELETE",
            endpoint=f"/addresses/{address_id}"
        )
        
        return response
    
    # ==================== PACKAGING MANAGEMENT ====================
    
    def create_packaging(
        self,
        name: str,
        type: str,
        length: float,
        width: float,
        height: float,
        weight: float,
        size_unit: str = "cm",
        weight_unit: str = "kg"
    ) -> Dict:
        """
        Create a new packaging option.
        
        Args:
            name: Package name
            type: 'box', 'envelope', or 'soft-packaging'
            length: Length in size_unit
            width: Width in size_unit
            height: Height in size_unit
            weight: Weight in weight_unit
            size_unit: 'cm' or 'in'
            weight_unit: 'kg' or 'lb'
            
        Returns:
            Dictionary with packaging details including packaging_id
        """
        payload = {
            "name": name,
            "type": type,
            "length": length,
            "width": width,
            "height": height,
            "weight": weight,
            "size_unit": size_unit,
            "weight_unit": weight_unit
        }
        
        logger.info(f"Creating packaging: {name} ({type})")
        
        response = self._make_request(
            method="POST",
            endpoint="/packaging",
            data=payload
        )
        
        return response
    
    def get_packaging(self, page: int = 1, per_page: int = 20) -> Dict:
        """
        Get all packaging options.
        
        Args:
            page: Page number
            per_page: Items per page
            
        Returns:
            Dictionary with packaging list and pagination info
        """
        logger.info(f"Fetching packaging options - Page: {page}")
        
        response = self._make_request(
            method="GET",
            endpoint="/packaging",
            params={"page": page, "perPage": per_page}
        )
        
        return response
    
    def get_packaging_by_id(self, packaging_id: str) -> Dict:
        """
        Get a specific packaging by ID.
        
        Args:
            packaging_id: Terminal packaging ID
            
        Returns:
            Packaging details dictionary
        """
        logger.info(f"Fetching packaging: {packaging_id}")
        
        response = self._make_request(
            method="GET",
            endpoint=f"/packaging/{packaging_id}"
        )
        
        return response
    
    def delete_packaging(self, packaging_id: str) -> Dict:
        """
        Delete a packaging option.
        
        Args:
            packaging_id: Terminal packaging ID
            
        Returns:
            Success response
        """
        logger.info(f"Deleting packaging: {packaging_id}")
        
        response = self._make_request(
            method="DELETE",
            endpoint=f"/packaging/{packaging_id}"
        )
        
        return response
    
    # ==================== PARCEL MANAGEMENT ====================
    
    def create_parcel(
        self,
        packaging_id: str,
        items: List[Dict],
        description: str = None,
        weight: float = None,
        weight_unit: str = "kg"
    ) -> Dict:
        """
        Create a new parcel.
        
        Args:
            packaging_id: Terminal packaging ID
            items: List of items with name, quantity, value, weight, etc.
            description: Parcel description
            weight: Total weight (if different from packaging weight)
            weight_unit: 'kg' or 'lb'
            
        Returns:
            Dictionary with parcel details including parcel_id
        """
        payload = {
            "packaging": packaging_id,
            "items": items
        }
        
        if description:
            payload["description"] = description
        if weight:
            payload["weight"] = weight
            payload["weight_unit"] = weight_unit
        
        logger.info(f"Creating parcel with packaging: {packaging_id}")
        
        response = self._make_request(
            method="POST",
            endpoint="/parcels",
            data=payload
        )
        
        return response
    
    def get_parcels(self, page: int = 1, per_page: int = 20) -> Dict:
        """
        Get all parcels.
        
        Args:
            page: Page number
            per_page: Items per page
            
        Returns:
            Dictionary with parcels list and pagination info
        """
        logger.info(f"Fetching parcels - Page: {page}")
        
        response = self._make_request(
            method="GET",
            endpoint="/parcels",
            params={"page": page, "perPage": per_page}
        )
        
        return response
    
    def get_parcel(self, parcel_id: str) -> Dict:
        """
        Get a specific parcel by ID.
        
        Args:
            parcel_id: Terminal parcel ID
            
        Returns:
            Parcel details dictionary
        """
        logger.info(f"Fetching parcel: {parcel_id}")
        
        response = self._make_request(
            method="GET",
            endpoint=f"/parcels/{parcel_id}"
        )
        
        return response
    
    # ==================== CARRIER MANAGEMENT ====================
    
    def get_carriers(
        self,
        active: bool = None,
        domestic: bool = None,
        regional: bool = None,
        international: bool = None
    ) -> Dict:
        """
        Get available carriers.
        
        Args:
            active: Filter by active status
            domestic: Filter domestic carriers
            regional: Filter regional carriers
            international: Filter international carriers
            
        Returns:
            Dictionary with carriers list
        """
        params = {}
        if active is not None:
            params["active"] = str(active).lower()
        if domestic is not None:
            params["domestic"] = str(domestic).lower()
        if regional is not None:
            params["regional"] = str(regional).lower()
        if international is not None:
            params["international"] = str(international).lower()
        
        logger.info("Fetching carriers")
        
        response = self._make_request(
            method="GET",
            endpoint="/carriers",
            params=params if params else None
        )
        
        return response
    
    def enable_carrier(self, carrier_id: str) -> Dict:
        """
        Enable a carrier.
        
        Args:
            carrier_id: Terminal carrier ID
            
        Returns:
            Success response
        """
        logger.info(f"Enabling carrier: {carrier_id}")
        
        response = self._make_request(
            method="POST",
            endpoint=f"/carriers/{carrier_id}/enable"
        )
        
        return response
    
    def disable_carrier(self, carrier_id: str) -> Dict:
        """
        Disable a carrier.
        
        Args:
            carrier_id: Terminal carrier ID
            
        Returns:
            Success response
        """
        logger.info(f"Disabling carrier: {carrier_id}")
        
        response = self._make_request(
            method="POST",
            endpoint=f"/carriers/{carrier_id}/disable"
        )
        
        return response
    
    # ==================== RATE MANAGEMENT ====================
    
    def get_rates(
        self,
        origin_address_id: str,
        destination_address_id: str,
        parcel_id: str,
        currency: str = "NGN"
    ) -> Dict:
        """
        Get shipping rates from multiple carriers.
        
        Args:
            origin_address_id: Terminal origin address ID
            destination_address_id: Terminal destination address ID
            parcel_id: Terminal parcel ID
            currency: Currency code (default: NGN)
            
        Returns:
            Dictionary with rates from different carriers
        """
        params = {
            "pickup_address": origin_address_id,
            "delivery_address": destination_address_id,
            "parcel_id": parcel_id,
            "currency": currency
        }
        
        logger.info(f"Fetching rates for parcel: {parcel_id}")
        logger.info(f"Pickup address: {origin_address_id}, Delivery address: {destination_address_id}")
        
        response = self._make_request(
            method="GET",
            endpoint="/rates/shipment",
            params=params
        )
        
        return response
    
    # ==================== SHIPMENT MANAGEMENT ====================
    
    def create_shipment(
        self,
        rate_id: str,
        origin_address_id: str,
        destination_address_id: str,
        parcel_id: str,
        metadata: Dict = None
    ) -> Dict:
        """
        Create a new shipment using a selected rate.
        
        Args:
            rate_id: Terminal rate ID (from get_rates)
            origin_address_id: Terminal origin address ID
            destination_address_id: Terminal destination address ID
            parcel_id: Terminal parcel ID
            metadata: Additional metadata
            
        Returns:
            Dictionary with shipment details including tracking info
        """
        payload = {
            "rate_id": rate_id,
            "origin_address": origin_address_id,
            "destination_address": destination_address_id,
            "parcel": parcel_id
        }
        
        if metadata:
            payload["metadata"] = metadata
        
        logger.info(f"Creating shipment with rate: {rate_id}")
        
        response = self._make_request(
            method="POST",
            endpoint="/shipments",
            data=payload
        )
        
        logger.info(f"Shipment created successfully - ID: {response.get('shipment_id', 'N/A')}")
        
        return response
    
    def get_shipments(self, page: int = 1, per_page: int = 20, status: str = None) -> Dict:
        """
        Get all shipments.
        
        Args:
            page: Page number
            per_page: Items per page
            status: Filter by status
            
        Returns:
            Dictionary with shipments list and pagination info
        """
        params = {"page": page, "perPage": per_page}
        if status:
            params["status"] = status
        
        logger.info(f"Fetching shipments - Page: {page}")
        
        response = self._make_request(
            method="GET",
            endpoint="/shipments",
            params=params
        )
        
        return response
    
    def get_shipment(self, shipment_id: str) -> Dict:
        """
        Get a specific shipment by ID.
        
        Args:
            shipment_id: Terminal shipment ID
            
        Returns:
            Shipment details dictionary
        """
        logger.info(f"Fetching shipment: {shipment_id}")
        
        response = self._make_request(
            method="GET",
            endpoint=f"/shipments/{shipment_id}"
        )
        
        return response
    
    def cancel_shipment(self, shipment_id: str) -> Dict:
        """
        Cancel a shipment.
        
        Args:
            shipment_id: Terminal shipment ID
            
        Returns:
            Success response
        """
        logger.info(f"Cancelling shipment: {shipment_id}")
        
        response = self._make_request(
            method="POST",
            endpoint=f"/shipments/{shipment_id}/cancel"
        )
        
        return response
    
    # ==================== TRACKING ====================
    
    def track_shipment(self, shipment_id: str) -> Dict:
        """
        Track a shipment by ID.
        
        Args:
            shipment_id: Terminal shipment ID
            
        Returns:
            Dictionary with tracking information and events
        """
        logger.info(f"Tracking shipment: {shipment_id}")
        
        response = self._make_request(
            method="GET",
            endpoint=f"/shipments/{shipment_id}/track"
        )
        
        return response
    
    def track_by_tracking_number(self, tracking_number: str) -> Dict:
        """
        Track a shipment by carrier tracking number.
        
        Args:
            tracking_number: Carrier tracking number
            
        Returns:
            Dictionary with tracking information
        """
        logger.info(f"Tracking by number: {tracking_number}")
        
        response = self._make_request(
            method="GET",
            endpoint="/tracking",
            params={"tracking_number": tracking_number}
        )
        
        return response
    
    # ==================== UTILITY METHODS ====================
    
    def get_user_profile(self) -> Dict:
        """
        Get user profile and account information.
        
        Returns:
            Dictionary with user profile
        """
        logger.info("Fetching user profile")
        
        response = self._make_request(
            method="GET",
            endpoint="/users/profile"
        )
        
        return response
    
    def get_wallet_balance(self) -> Dict:
        """
        Get wallet balance.
        
        Returns:
            Dictionary with wallet balance information
        """
        logger.info("Fetching wallet balance")
        
        response = self._make_request(
            method="GET",
            endpoint="/wallets/balance"
        )
        
        return response


# Singleton instance
_terminal_client = None


def get_terminal_client() -> TerminalClient:
    """Get or create Terminal Africa client singleton instance."""
    global _terminal_client
    if _terminal_client is None:
        _terminal_client = TerminalClient()
    return _terminal_client
