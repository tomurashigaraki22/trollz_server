"""
Sendbox API Service
Handles all interactions with the Sendbox shipping API with automatic token refresh.
"""

import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from config import Config
import jwt
import time


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SendboxAPIError(Exception):
    """Custom exception for Sendbox API errors."""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class SendboxClient:
    """
    Sendbox API Client
    
    Provides methods to interact with Sendbox shipping API including:
    - Getting shipping quotes
    - Creating shipments
    - Tracking shipments
    - Calculating landed costs
    - Automatic token refresh
    """
    
    # Sendbox credentials
    ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2OWQ2MWE5OGEyOGIyYTAwMjI3NzY4YWIiLCJhaWQiOiI2OWU5ZmJlNGEyOGIyYTAwMjVhOGRmMTUiLCJ0d29fZmEiOmZhbHNlLCJpbnN0YW5jZV9pZCI6IjYxMzZkZmE2YTFhYjlkMzE4YmNmY2I5NCIsImVudGl0eV9pZCI6bnVsbCwiaXNzIjoic2VuZGJveC5hcHBzLmF1dGgtNjEzNmRmYTZhMWFiOWQzMThiY2ZjYjk0IiwiZXhwIjoxNzgyMDM5NjUyfQ.YYFC2n1ypUfInDXjHFkXALpDVMO7Oo3kIKYajVKCi58"
    REFRESH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBsaWNhdGlvbiI6eyJwayI6IjY5ZTlmYmU0YTI4YjJhMDAyNWE4ZGYxNSIsImRlc2NyaXB0aW9uIjoiQW4gZWNvbW1lcmNlIHN0b3JlIGJhc2VkIGluIE5pZ2VyaWEiLCJuYW1lIjoiVHJvbGx6IFN0b3JlIn0sImFwcF9pZCI6IjY5ZTlmYmU0YTI4YjJhMDAyNWE4ZGYxNSIsImlzcyI6InNlbmRib3guYXBwcy5hdXRoIiwiZXhwIjoxODExNTAyMDUyfQ.BZZco3ieQemGKpCVJmuh4LIvpt3RMkz6GH123-Q8c6c"
    CLIENT_SECRET = "602c256bf4da43b4d312d54ab938aed9141dee460c4770d75b90261da26e7721a621e5e8123702bdb142d32baa4caf813ccde029c115621c26db843b20297b38"
    
    def __init__(self, api_key: str = None, environment: str = None):
        """
        Initialize Sendbox client.
        
        Args:
            api_key: Sendbox API key (defaults to Config.SENDBOX_API_KEY)
            environment: 'staging' or 'live' (defaults to Config.SENDBOX_ENVIRONMENT)
        """
        self.api_key = api_key or Config.SENDBOX_API_KEY
        self.environment = environment or Config.SENDBOX_ENVIRONMENT
        self.base_url = Config.get_sendbox_base_url()
        
        # Token management
        self.current_access_token = self.ACCESS_TOKEN
        self.current_refresh_token = self.REFRESH_TOKEN
        self.token_expiry = None
        
        # Check if token needs refresh on initialization
        self._check_and_refresh_token()
        
        logger.info(f"Sendbox client initialized - Environment: {self.environment}")
    
    def _is_token_expired(self) -> bool:
        """Check if the current access token is expired or about to expire."""
        try:
            # Decode token without verification to check expiry
            decoded = jwt.decode(self.current_access_token, options={"verify_signature": False})
            exp_timestamp = decoded.get('exp', 0)
            
            # Check if token expires in less than 5 minutes
            current_time = time.time()
            buffer_time = 300  # 5 minutes buffer
            
            return (exp_timestamp - current_time) < buffer_time
        except Exception as e:
            logger.warning(f"Error checking token expiry: {str(e)}")
            return True  # Assume expired if we can't decode
    
    def _refresh_access_token(self) -> bool:
        """
        Refresh the access token using the refresh token.
        
        Returns:
            bool: True if refresh successful, False otherwise
        """
        try:
            logger.info("Refreshing Sendbox access token...")
            
            refresh_url = f"{self.base_url}/auth/refresh"
            
            response = requests.post(
                refresh_url,
                json={
                    "refresh_token": self.current_refresh_token,
                    "client_secret": self.CLIENT_SECRET
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.current_access_token = data.get('access_token', self.current_access_token)
                
                # Update refresh token if provided
                if 'refresh_token' in data:
                    self.current_refresh_token = data['refresh_token']
                
                logger.info("✅ Access token refreshed successfully")
                return True
            else:
                logger.error(f"Failed to refresh token: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error refreshing token: {str(e)}")
            return False
    
    def _check_and_refresh_token(self):
        """Check if token is expired and refresh if needed."""
        if self._is_token_expired():
            logger.info("Access token expired or expiring soon, refreshing...")
            self._refresh_access_token()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        # Check and refresh token before each request
        self._check_and_refresh_token()
        
        return {
            "Authorization": f"Bearer {self.current_access_token}",
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
        Make HTTP request to Sendbox API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            SendboxAPIError: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        try:
            logger.info(f"Sendbox API Request: {method} {url}")
            
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
                timeout=30
            )
            
            # Log response
            logger.info(f"Sendbox API Response: {response.status_code}")
            
            # Handle different status codes
            if response.status_code in [200, 201]:
                return response.json()
            elif response.status_code == 401:
                raise SendboxAPIError(
                    "Authentication failed. Please check your API key.",
                    status_code=401,
                    response_data=response.json() if response.text else None
                )
            elif response.status_code == 403:
                raise SendboxAPIError(
                    "Access forbidden. Insufficient permissions.",
                    status_code=403,
                    response_data=response.json() if response.text else None
                )
            elif response.status_code == 404:
                raise SendboxAPIError(
                    "Resource not found.",
                    status_code=404,
                    response_data=response.json() if response.text else None
                )
            elif response.status_code == 409:
                # Validation error
                error_data = response.json() if response.text else {}
                error_msg = str(error_data)
                raise SendboxAPIError(
                    f"Validation error: {error_msg}",
                    status_code=409,
                    response_data=error_data
                )
            else:
                # Other errors
                error_data = response.json() if response.text else {}
                raise SendboxAPIError(
                    f"API request failed: {response.status_code}",
                    status_code=response.status_code,
                    response_data=error_data
                )
                
        except requests.exceptions.Timeout:
            raise SendboxAPIError("Request timeout. Please try again.")
        except requests.exceptions.ConnectionError:
            raise SendboxAPIError("Connection error. Please check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise SendboxAPIError(f"Request failed: {str(e)}")
    
    def get_shipping_quotes(
        self,
        origin: Dict,
        destination: Dict,
        weight: float,
        items: List[Dict],
        service_code: str = "standard",
        service_type: str = "local",
        pickup_date: str = None,
        dimension: Dict = None,
        total_value: float = 0,
        currency: str = "NGN"
    ) -> Dict:
        """
        Get shipping quotes from Sendbox.
        
        Args:
            origin: Origin address dictionary
            destination: Destination address dictionary
            weight: Total weight in KG
            items: List of items with name, quantity, value, weight
            service_code: 'standard', 'premium', or 'expedient'
            service_type: 'local', 'international', or 'nation-wide'
            pickup_date: Pickup date in ISO format (defaults to tomorrow)
            dimension: Package dimensions {length, width, height} in cm
            total_value: Total value of items
            currency: Currency code (default: NGN)
            
        Returns:
            Dictionary with shipping quotes
        """
        if not pickup_date:
            # Default to tomorrow
            tomorrow = datetime.now() + timedelta(days=1)
            pickup_date = tomorrow.strftime("%Y-%m-%d")
        
        if not dimension:
            # Default dimensions
            dimension = {"length": 30, "width": 20, "height": 15}
        
        payload = {
            "origin": origin,
            "destination": destination,
            "weight": weight,
            "dimension": dimension,
            "incoming_option": "pickup",
            "region": origin.get("country", "NG"),
            "service_type": service_type,
            "package_type": "general",
            "total_value": total_value,
            "currency": currency,
            "channel_code": "api",
            "pickup_date": pickup_date,
            "items": items,
            "service_code": service_code
        }
        
        # Add customs option for international shipments
        if service_type == "international":
            payload["customs_option"] = "recipient"
        
        logger.info(f"Requesting shipping quotes - Weight: {weight}kg, Service: {service_code}")
        
        response = self._make_request(
            method="POST",
            endpoint="/shipping/shipment_delivery_quote",
            data=payload
        )
        
        return response
    
    def create_shipment(
        self,
        origin: Dict,
        destination: Dict,
        weight: float,
        items: List[Dict],
        service_code: str = "standard",
        service_type: str = "local",
        pickup_date: str = None,
        dimension: Dict = None,
        total_value: float = 0,
        currency: str = "NGN",
        callback_url: str = None
    ) -> Dict:
        """
        Create a new shipment with Sendbox.
        
        Args:
            origin: Origin address dictionary
            destination: Destination address dictionary
            weight: Total weight in KG
            items: List of items with name, quantity, value, weight, hts_code
            service_code: 'standard', 'premium', or 'expedient'
            service_type: 'local', 'international', or 'nation-wide'
            pickup_date: Pickup date in ISO format
            dimension: Package dimensions
            total_value: Total value of items
            currency: Currency code
            callback_url: Webhook URL for tracking updates
            
        Returns:
            Dictionary with shipment details including tracking code
        """
        if not pickup_date:
            tomorrow = datetime.now() + timedelta(days=1)
            pickup_date = tomorrow.strftime("%Y-%m-%d")
        
        if not dimension:
            dimension = {"length": 30, "width": 20, "height": 15}
        
        payload = {
            "origin": origin,
            "destination": destination,
            "weight": weight,
            "dimension": dimension,
            "incoming_option": "pickup",
            "region": origin.get("country", "NG"),
            "service_type": service_type,
            "package_type": "general",
            "total_value": total_value,
            "currency": currency,
            "channel_code": "api",
            "pickup_date": pickup_date,
            "items": items,
            "service_code": service_code
        }
        
        # Add customs option for international shipments
        if service_type == "international":
            payload["customs_option"] = "recipient"
        
        # Add callback URL if provided
        if callback_url:
            payload["callback_url"] = callback_url
        
        logger.info(f"Creating shipment - Service: {service_code}, Type: {service_type}")
        
        response = self._make_request(
            method="POST",
            endpoint="/shipping/shipments",
            data=payload
        )
        
        logger.info(f"Shipment created successfully - Tracking: {response.get('tracking_code', 'N/A')}")
        
        return response
    
    def track_shipment(self, tracking_code: str) -> Dict:
        """
        Track a shipment by tracking code.
        
        Args:
            tracking_code: Sendbox tracking code
            
        Returns:
            Dictionary with tracking information
        """
        logger.info(f"Tracking shipment: {tracking_code}")
        
        response = self._make_request(
            method="POST",
            endpoint="/shipping/tracking",
            data={"code": tracking_code}
        )
        
        return response
    
    def get_shipments(self) -> List[Dict]:
        """
        Get all shipments.
        
        Returns:
            List of shipment dictionaries
        """
        logger.info("Fetching all shipments")
        
        response = self._make_request(
            method="GET",
            endpoint="/shipping/shipments"
        )
        
        return response
    
    def get_shipment(self, shipment_id: int) -> Dict:
        """
        Get a specific shipment by ID.
        
        Args:
            shipment_id: Sendbox shipment ID
            
        Returns:
            Shipment details dictionary
        """
        logger.info(f"Fetching shipment: {shipment_id}")
        
        response = self._make_request(
            method="GET",
            endpoint=f"/shipping/shipments/{shipment_id}"
        )
        
        return response
    
    def calculate_landed_cost(
        self,
        origin: Dict,
        destination: Dict,
        weight: float,
        items: List[Dict],
        service_code: str = "standard",
        pickup_date: str = None,
        dimension: Dict = None,
        total_value: float = 0,
        currency: str = "NGN"
    ) -> Dict:
        """
        Calculate landed cost for international shipments.
        
        Args:
            origin: Origin address dictionary
            destination: Destination address dictionary
            weight: Total weight in KG
            items: List of items with hts_code, value, etc.
            service_code: Service code
            pickup_date: Pickup date
            dimension: Package dimensions
            total_value: Total value
            currency: Currency code
            
        Returns:
            Dictionary with landed cost breakdown (duties, taxes, fees)
        """
        if not pickup_date:
            tomorrow = datetime.now() + timedelta(days=1)
            pickup_date = tomorrow.strftime("%Y-%m-%d")
        
        if not dimension:
            dimension = {"length": 30, "width": 20, "height": 15}
        
        payload = {
            "origin": origin,
            "destination": destination,
            "weight": weight,
            "dimension": dimension,
            "incoming_option": "pickup",
            "region": origin.get("country", "NG"),
            "service_type": "international",
            "package_type": "general",
            "total_value": total_value,
            "currency": currency,
            "channel_code": "api",
            "pickup_date": pickup_date,
            "items": items,
            "service_code": service_code,
            "customs_option": "sender"
        }
        
        logger.info(f"Calculating landed cost - Value: {total_value} {currency}")
        
        response = self._make_request(
            method="POST",
            endpoint="/shipping/landed_cost_estimate",
            data=payload
        )
        
        return response
    
    def get_account_balance(self) -> Dict:
        """
        Get Sendbox account balance and profile.
        
        Returns:
            Dictionary with account information
        """
        logger.info("Fetching account balance")
        
        response = self._make_request(
            method="GET",
            endpoint="/payments/profile"
        )
        
        return response
    
    def add_money_staging(self, amount: float) -> Dict:
        """
        Add money to staging account (staging environment only).
        
        Args:
            amount: Amount to add
            
        Returns:
            Response dictionary
        """
        if self.environment != "staging":
            raise SendboxAPIError("add_money is only available in staging environment")
        
        logger.info(f"Adding {amount} to staging account")
        
        response = self._make_request(
            method="POST",
            endpoint="/payments/add_money",
            data={"amount": amount}
        )
        
        return response
    
    def simulate_tracking_update(self, tracking_code: str) -> Dict:
        """
        Simulate tracking status update (staging environment only).
        
        Args:
            tracking_code: Tracking code to update
            
        Returns:
            Response dictionary
        """
        if self.environment != "staging":
            raise SendboxAPIError("simulate_tracking_update is only available in staging")
        
        logger.info(f"Simulating tracking update for: {tracking_code}")
        
        response = self._make_request(
            method="POST",
            endpoint="/shipping/move_tracking",
            data={"code": tracking_code}
        )
        
        return response


# Singleton instance
_sendbox_client = None


def get_sendbox_client() -> SendboxClient:
    """Get or create Sendbox client singleton instance."""
    global _sendbox_client
    if _sendbox_client is None:
        _sendbox_client = SendboxClient()
    return _sendbox_client
