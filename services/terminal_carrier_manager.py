"""
Terminal Africa Carrier Manager
Manages carrier synchronization and operations.
"""

import logging
from typing import Dict, List, Optional
from services.terminal_service import get_terminal_client, TerminalAPIError
from db import get_db_connection
import json


logger = logging.getLogger(__name__)


class TerminalCarrierManager:
    """
    Manages carriers for Terminal Africa integration.
    
    Features:
    - Fetch and sync carriers from Terminal
    - Enable/disable carriers
    - Filter carriers by type
    - Cache carrier data locally
    """
    
    def __init__(self):
        """Initialize Terminal Carrier Manager."""
        self.terminal_client = get_terminal_client()
    
    def sync_carriers(self) -> Dict:
        """
        Fetch carriers from Terminal Africa and sync to local database.
        
        Returns:
            Dictionary with sync results
        """
        try:
            logger.info("Syncing carriers from Terminal Africa")
            
            # Fetch carriers from Terminal
            response = self.terminal_client.get_carriers()
            
            # Handle nested data structure: response['data']['carriers']
            data_obj = response.get('data', {})
            if isinstance(data_obj, dict) and 'carriers' in data_obj:
                carriers_data = data_obj['carriers']
            else:
                carriers_data = data_obj if isinstance(data_obj, list) else []
            
            if not carriers_data:
                logger.warning("No carriers returned from Terminal Africa")
                return {
                    "success": False,
                    "message": "No carriers available",
                    "synced_count": 0
                }
            
            connection = get_db_connection()
            cursor = connection.cursor()
            
            synced_count = 0
            
            try:
                for carrier in carriers_data:
                    carrier_id = carrier.get('carrier_id')
                    name = carrier.get('name')
                    slug = carrier.get('slug')
                    logo = carrier.get('logo')
                    active = carrier.get('active', True)
                    domestic = carrier.get('domestic', False)
                    regional = carrier.get('regional', False)
                    international = carrier.get('international', False)
                    
                    # Additional fields
                    requires_invoice = carrier.get('requires_invoice', False)
                    requires_waybill = carrier.get('requires_waybill', False)
                    supports_multi_parcels = carrier.get('supports_multi_parcels', False)
                    contact = json.dumps(carrier.get('contact', {}))
                    metadata = json.dumps(carrier)
                    
                    # Insert or update carrier
                    cursor.execute("""
                        INSERT INTO terminal_carriers (
                            terminal_carrier_id, name, slug, logo, active,
                            domestic, regional, international,
                            requires_invoice, requires_waybill, supports_multi_parcels,
                            contact, metadata
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            name = VALUES(name),
                            slug = VALUES(slug),
                            logo = VALUES(logo),
                            active = VALUES(active),
                            domestic = VALUES(domestic),
                            regional = VALUES(regional),
                            international = VALUES(international),
                            requires_invoice = VALUES(requires_invoice),
                            requires_waybill = VALUES(requires_waybill),
                            supports_multi_parcels = VALUES(supports_multi_parcels),
                            contact = VALUES(contact),
                            metadata = VALUES(metadata),
                            updated_at = CURRENT_TIMESTAMP
                    """, (
                        carrier_id, name, slug, logo, active,
                        domestic, regional, international,
                        requires_invoice, requires_waybill, supports_multi_parcels,
                        contact, metadata
                    ))
                    
                    synced_count += 1
                
                connection.commit()
                
                logger.info(f"✅ Synced {synced_count} carriers successfully")
                
                return {
                    "success": True,
                    "message": f"Synced {synced_count} carriers",
                    "synced_count": synced_count
                }
                
            finally:
                cursor.close()
                connection.close()
                
        except TerminalAPIError as e:
            logger.error(f"Terminal API error: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error syncing carriers: {str(e)}")
            raise
    
    def get_local_carriers(
        self,
        active: bool = None,
        domestic: bool = None,
        regional: bool = None,
        international: bool = None
    ) -> List[Dict]:
        """
        Get carriers from local database with optional filters.
        
        Args:
            active: Filter by active status
            domestic: Filter domestic carriers
            regional: Filter regional carriers
            international: Filter international carriers
            
        Returns:
            List of carrier dictionaries
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            # Build query with filters
            query = "SELECT * FROM terminal_carriers WHERE 1=1"
            params = []
            
            if active is not None:
                query += " AND active = %s"
                params.append(active)
            
            if domestic is not None:
                query += " AND domestic = %s"
                params.append(domestic)
            
            if regional is not None:
                query += " AND regional = %s"
                params.append(regional)
            
            if international is not None:
                query += " AND international = %s"
                params.append(international)
            
            query += " ORDER BY name ASC"
            
            cursor.execute(query, params)
            carriers = cursor.fetchall()
            
            return carriers
            
        finally:
            cursor.close()
            connection.close()
    
    def get_carrier_by_id(self, carrier_id: str) -> Optional[Dict]:
        """
        Get a specific carrier by Terminal carrier ID.
        
        Args:
            carrier_id: Terminal carrier ID
            
        Returns:
            Carrier dictionary or None
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM terminal_carriers
                WHERE terminal_carrier_id = %s
            """, (carrier_id,))
            
            carrier = cursor.fetchone()
            return carrier
            
        finally:
            cursor.close()
            connection.close()
    
    def enable_carrier(self, carrier_id: str) -> Dict:
        """
        Enable a carrier in Terminal Africa and update locally.
        
        Args:
            carrier_id: Terminal carrier ID
            
        Returns:
            Result dictionary
        """
        try:
            logger.info(f"Enabling carrier: {carrier_id}")
            
            # Enable in Terminal Africa
            response = self.terminal_client.enable_carrier(carrier_id)
            
            # Update local database
            connection = get_db_connection()
            cursor = connection.cursor()
            
            try:
                cursor.execute("""
                    UPDATE terminal_carriers
                    SET active = TRUE, updated_at = CURRENT_TIMESTAMP
                    WHERE terminal_carrier_id = %s
                """, (carrier_id,))
                
                connection.commit()
                
                logger.info(f"✅ Carrier enabled successfully")
                
                return {
                    "success": True,
                    "message": "Carrier enabled",
                    "terminal_response": response
                }
                
            finally:
                cursor.close()
                connection.close()
                
        except TerminalAPIError as e:
            logger.error(f"Terminal API error: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error enabling carrier: {str(e)}")
            raise
    
    def disable_carrier(self, carrier_id: str) -> Dict:
        """
        Disable a carrier in Terminal Africa and update locally.
        
        Args:
            carrier_id: Terminal carrier ID
            
        Returns:
            Result dictionary
        """
        try:
            logger.info(f"Disabling carrier: {carrier_id}")
            
            # Disable in Terminal Africa
            response = self.terminal_client.disable_carrier(carrier_id)
            
            # Update local database
            connection = get_db_connection()
            cursor = connection.cursor()
            
            try:
                cursor.execute("""
                    UPDATE terminal_carriers
                    SET active = FALSE, updated_at = CURRENT_TIMESTAMP
                    WHERE terminal_carrier_id = %s
                """, (carrier_id,))
                
                connection.commit()
                
                logger.info(f"✅ Carrier disabled successfully")
                
                return {
                    "success": True,
                    "message": "Carrier disabled",
                    "terminal_response": response
                }
                
            finally:
                cursor.close()
                connection.close()
                
        except TerminalAPIError as e:
            logger.error(f"Terminal API error: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error disabling carrier: {str(e)}")
            raise
    
    def get_carrier_stats(self) -> Dict:
        """
        Get carrier statistics.
        
        Returns:
            Dictionary with carrier statistics
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN active = TRUE THEN 1 ELSE 0 END) as active,
                    SUM(CASE WHEN domestic = TRUE THEN 1 ELSE 0 END) as domestic,
                    SUM(CASE WHEN regional = TRUE THEN 1 ELSE 0 END) as regional,
                    SUM(CASE WHEN international = TRUE THEN 1 ELSE 0 END) as international
                FROM terminal_carriers
            """)
            
            stats = cursor.fetchone()
            return stats
            
        finally:
            cursor.close()
            connection.close()
    
    def search_carriers(self, query: str) -> List[Dict]:
        """
        Search carriers by name or slug.
        
        Args:
            query: Search query
            
        Returns:
            List of matching carriers
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM terminal_carriers
                WHERE name LIKE %s OR slug LIKE %s
                ORDER BY name ASC
            """, (f"%{query}%", f"%{query}%"))
            
            carriers = cursor.fetchall()
            return carriers
            
        finally:
            cursor.close()
            connection.close()
    
    def get_recommended_carriers(
        self,
        origin_country: str,
        destination_country: str
    ) -> List[Dict]:
        """
        Get recommended carriers based on origin and destination.
        
        Args:
            origin_country: Origin country code
            destination_country: Destination country code
            
        Returns:
            List of recommended carriers
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            # Determine carrier type needed
            if origin_country == destination_country:
                # Domestic
                cursor.execute("""
                    SELECT * FROM terminal_carriers
                    WHERE active = TRUE AND domestic = TRUE
                    ORDER BY name ASC
                """)
            elif origin_country in ['NG', 'GH', 'KE', 'ZA'] and destination_country in ['NG', 'GH', 'KE', 'ZA']:
                # Regional (African countries)
                cursor.execute("""
                    SELECT * FROM terminal_carriers
                    WHERE active = TRUE AND (regional = TRUE OR international = TRUE)
                    ORDER BY name ASC
                """)
            else:
                # International
                cursor.execute("""
                    SELECT * FROM terminal_carriers
                    WHERE active = TRUE AND international = TRUE
                    ORDER BY name ASC
                """)
            
            carriers = cursor.fetchall()
            return carriers
            
        finally:
            cursor.close()
            connection.close()


# Singleton instance
_carrier_manager = None


def get_carrier_manager() -> TerminalCarrierManager:
    """Get or create Terminal Carrier Manager singleton instance."""
    global _carrier_manager
    if _carrier_manager is None:
        _carrier_manager = TerminalCarrierManager()
    return _carrier_manager
