"""
Terminal Africa Address Manager
Manages address synchronization between local database and Terminal Africa API.
"""

import logging
from typing import Dict, Optional, List
from services.terminal_service import get_terminal_client, TerminalAPIError
from db import get_db_connection


logger = logging.getLogger(__name__)


class TerminalAddressManager:
    """
    Manages addresses for Terminal Africa integration.
    
    Features:
    - Sync local addresses to Terminal
    - Create and validate addresses
    - Cache Terminal address IDs locally
    """
    
    def __init__(self):
        """Initialize Terminal Address Manager."""
        self.terminal_client = get_terminal_client()
    
    def create_and_sync_address(
        self,
        user_id: int,
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
        Create address in Terminal Africa and store locally.
        
        Args:
            user_id: Local user ID
            first_name: First name
            last_name: Last name
            phone: Phone number
            email: Email address
            line1: Address line 1
            city: City
            state: State
            country: Country code
            zip_code: Postal code
            line2: Address line 2
            is_residential: Whether residential
            
        Returns:
            Dictionary with local and Terminal address details
        """
        try:
            # Create address in Terminal Africa
            logger.info(f"Creating Terminal address for user {user_id}")
            
            terminal_response = self.terminal_client.create_address(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                line1=line1,
                city=city,
                state=state,
                country=country,
                zip_code=zip_code,
                line2=line2,
                is_residential=is_residential
            )
            
            # Extract Terminal address ID
            terminal_address_id = terminal_response.get('data', {}).get('address_id')
            
            if not terminal_address_id:
                raise TerminalAPIError("Terminal address ID not returned")
            
            # Store in local database
            connection = get_db_connection()
            cursor = connection.cursor()
            
            try:
                cursor.execute("""
                    INSERT INTO terminal_addresses (
                        user_id, terminal_address_id, first_name, last_name,
                        phone, email, line1, line2, city, state, country, zip,
                        is_residential, metadata
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    user_id, terminal_address_id, first_name, last_name,
                    phone, email, line1, line2, city, state, country, zip_code,
                    is_residential, None
                ))
                
                connection.commit()
                local_address_id = cursor.lastrowid
                
                logger.info(f"✅ Address synced - Local ID: {local_address_id}, Terminal ID: {terminal_address_id}")
                
                return {
                    "success": True,
                    "local_address_id": local_address_id,
                    "terminal_address_id": terminal_address_id,
                    "terminal_response": terminal_response
                }
                
            finally:
                cursor.close()
                connection.close()
                
        except TerminalAPIError as e:
            logger.error(f"Terminal API error: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error creating address: {str(e)}")
            raise
    
    def get_terminal_address_id(self, user_id: int, local_address_id: int = None) -> Optional[str]:
        """
        Get Terminal address ID for a user.
        
        Args:
            user_id: Local user ID
            local_address_id: Specific local address ID (optional)
            
        Returns:
            Terminal address ID or None
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            if local_address_id:
                cursor.execute("""
                    SELECT terminal_address_id FROM terminal_addresses
                    WHERE user_id = %s AND id = %s
                    LIMIT 1
                """, (user_id, local_address_id))
            else:
                # Get most recent address
                cursor.execute("""
                    SELECT terminal_address_id FROM terminal_addresses
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (user_id,))
            
            result = cursor.fetchone()
            return result['terminal_address_id'] if result else None
            
        finally:
            cursor.close()
            connection.close()
    
    def get_user_addresses(self, user_id: int) -> List[Dict]:
        """
        Get all Terminal addresses for a user.
        
        Args:
            user_id: Local user ID
            
        Returns:
            List of address dictionaries
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM terminal_addresses
                WHERE user_id = %s
                ORDER BY created_at DESC
            """, (user_id,))
            
            addresses = cursor.fetchall()
            return addresses
            
        finally:
            cursor.close()
            connection.close()
    
    def sync_existing_address(
        self,
        user_id: int,
        address_data: Dict
    ) -> Dict:
        """
        Sync an existing local address to Terminal Africa.
        
        Args:
            user_id: Local user ID
            address_data: Address data dictionary
            
        Returns:
            Sync result dictionary
        """
        return self.create_and_sync_address(
            user_id=user_id,
            first_name=address_data.get('first_name', ''),
            last_name=address_data.get('last_name', ''),
            phone=address_data.get('phone', ''),
            email=address_data.get('email', ''),
            line1=address_data.get('line1', address_data.get('street', '')),
            line2=address_data.get('line2', address_data.get('street_line_2')),
            city=address_data.get('city', ''),
            state=address_data.get('state', ''),
            country=address_data.get('country', 'NG'),
            zip_code=address_data.get('zip', address_data.get('post_code')),
            is_residential=address_data.get('is_residential', True)
        )
    
    def update_terminal_address(
        self,
        terminal_address_id: str,
        **kwargs
    ) -> Dict:
        """
        Update an address in Terminal Africa.
        
        Args:
            terminal_address_id: Terminal address ID
            **kwargs: Fields to update
            
        Returns:
            Update result dictionary
        """
        try:
            logger.info(f"Updating Terminal address: {terminal_address_id}")
            
            response = self.terminal_client.update_address(
                address_id=terminal_address_id,
                **kwargs
            )
            
            # Update local database if needed
            connection = get_db_connection()
            cursor = connection.cursor()
            
            try:
                # Build update query dynamically
                update_fields = []
                update_values = []
                
                field_mapping = {
                    'first_name': 'first_name',
                    'last_name': 'last_name',
                    'phone': 'phone',
                    'email': 'email',
                    'line1': 'line1',
                    'line2': 'line2',
                    'city': 'city',
                    'state': 'state',
                    'country': 'country',
                    'zip': 'zip',
                    'is_residential': 'is_residential'
                }
                
                for api_field, db_field in field_mapping.items():
                    if api_field in kwargs:
                        update_fields.append(f"{db_field} = %s")
                        update_values.append(kwargs[api_field])
                
                if update_fields:
                    update_values.append(terminal_address_id)
                    query = f"""
                        UPDATE terminal_addresses
                        SET {', '.join(update_fields)}
                        WHERE terminal_address_id = %s
                    """
                    cursor.execute(query, update_values)
                    connection.commit()
                
                logger.info(f"✅ Address updated successfully")
                
                return {
                    "success": True,
                    "terminal_response": response
                }
                
            finally:
                cursor.close()
                connection.close()
                
        except TerminalAPIError as e:
            logger.error(f"Terminal API error: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error updating address: {str(e)}")
            raise
    
    def delete_terminal_address(self, terminal_address_id: str) -> Dict:
        """
        Delete an address from Terminal Africa and local database.
        
        Args:
            terminal_address_id: Terminal address ID
            
        Returns:
            Delete result dictionary
        """
        try:
            logger.info(f"Deleting Terminal address: {terminal_address_id}")
            
            # Delete from Terminal Africa
            response = self.terminal_client.delete_address(terminal_address_id)
            
            # Delete from local database
            connection = get_db_connection()
            cursor = connection.cursor()
            
            try:
                cursor.execute("""
                    DELETE FROM terminal_addresses
                    WHERE terminal_address_id = %s
                """, (terminal_address_id,))
                
                connection.commit()
                
                logger.info(f"✅ Address deleted successfully")
                
                return {
                    "success": True,
                    "terminal_response": response
                }
                
            finally:
                cursor.close()
                connection.close()
                
        except TerminalAPIError as e:
            logger.error(f"Terminal API error: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error deleting address: {str(e)}")
            raise
    
    def validate_address(self, address_data: Dict) -> Dict:
        """
        Validate an address using Terminal Africa API.
        
        Args:
            address_data: Address data to validate
            
        Returns:
            Validation result dictionary
        """
        # Terminal Africa validates addresses during creation
        # This is a placeholder for future validation endpoint
        required_fields = ['first_name', 'last_name', 'phone', 'email', 'line1', 'city', 'state', 'country']
        
        missing_fields = [field for field in required_fields if not address_data.get(field)]
        
        if missing_fields:
            return {
                "valid": False,
                "errors": missing_fields,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }
        
        return {
            "valid": True,
            "message": "Address validation passed"
        }


# Singleton instance
_address_manager = None


def get_address_manager() -> TerminalAddressManager:
    """Get or create Terminal Address Manager singleton instance."""
    global _address_manager
    if _address_manager is None:
        _address_manager = TerminalAddressManager()
    return _address_manager
