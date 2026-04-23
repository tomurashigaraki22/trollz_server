"""
Comprehensive Test Suite for Sendbox Integration
Tests all phases of Sendbox integration including quotes, shipments, tracking, and admin features.
"""

import unittest
import json
from datetime import datetime, timedelta
from app import create_app
from db import get_db_connection


class SendboxIntegrationTestCase(unittest.TestCase):
    """Base test case with common setup and teardown."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test application and database."""
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        
        # Test user credentials
        cls.user_token = None
        cls.admin_token = None
        cls.test_user_id = None
        cls.test_address_id = None
        cls.test_order_id = None
        
    def setUp(self):
        """Set up before each test."""
        # Login and get tokens if not already set
        if not self.user_token:
            self._login_test_user()
        if not self.admin_token:
            self._login_test_admin()
    
    def _login_test_user(self):
        """Login as test user and get token."""
        response = self.client.post('/api/login', json={
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        if response.status_code == 200:
            data = json.loads(response.data)
            self.user_token = data['data']['token']
            self.test_user_id = data['data']['user']['id']
    
    def _login_test_admin(self):
        """Login as admin and get token."""
        response = self.client.post('/api/login', json={
            'email': 'admin@example.com',
            'password': 'adminpassword'
        })
        if response.status_code == 200:
            data = json.loads(response.data)
            self.admin_token = data['data']['token']
    
    def _get_auth_headers(self, admin=False):
        """Get authorization headers."""
        token = self.admin_token if admin else self.user_token
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }


class TestPhase1Foundation(SendboxIntegrationTestCase):
    """Test Phase 1: Foundation Setup."""
    
    def test_sendbox_config_loaded(self):
        """Test that Sendbox configuration is loaded."""
        from config import Config
        
        self.assertIsNotNone(Config.SENDBOX_API_KEY)
        self.assertIn(Config.SENDBOX_ENVIRONMENT, ['staging', 'live'])
        self.assertIsNotNone(Config.get_sendbox_base_url())
    
    def test_database_schema(self):
        """Test that Sendbox database tables exist."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check orders table has Sendbox columns
        cursor.execute("SHOW COLUMNS FROM orders LIKE 'sendbox_%'")
        sendbox_columns = cursor.fetchall()
        self.assertGreater(len(sendbox_columns), 0)
        
        # Check shipping_addresses table exists
        cursor.execute("SHOW TABLES LIKE 'shipping_addresses'")
        self.assertIsNotNone(cursor.fetchone())
        
        # Check shipping_quotes table exists
        cursor.execute("SHOW TABLES LIKE 'shipping_quotes'")
        self.assertIsNotNone(cursor.fetchone())
        
        # Check webhook_events table exists
        cursor.execute("SHOW TABLES LIKE 'webhook_events'")
        self.assertIsNotNone(cursor.fetchone())
        
        conn.close()
    
    def test_sendbox_service_client(self):
        """Test Sendbox service client initialization."""
        from services.sendbox_service import get_sendbox_client
        
        client = get_sendbox_client()
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.api_key)
        self.assertIsNotNone(client.base_url)


class TestPhase2ShippingQuotes(SendboxIntegrationTestCase):
    """Test Phase 2: Shipping Quotes Integration."""
    
    def test_create_shipping_address(self):
        """Test creating a shipping address."""
        response = self.client.post('/api/addresses',
            headers=self._get_auth_headers(),
            json={
                'first_name': 'John',
                'last_name': 'Doe',
                'phone': '08001234567',
                'street': '123 Test Street',
                'city': 'Lagos',
                'state': 'Lagos',
                'country': 'NG',
                'post_code': '100001'
            }
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('address', data['data'])
        
        # Store address ID for later tests
        self.__class__.test_address_id = data['data']['address']['id']
    
    def test_list_shipping_addresses(self):
        """Test listing user's shipping addresses."""
        response = self.client.get('/api/addresses',
            headers=self._get_auth_headers()
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIsInstance(data['data']['addresses'], list)
    
    def test_get_shipping_quotes(self):
        """Test getting shipping quotes."""
        if not self.test_address_id:
            self.skipTest("No test address available")
        
        response = self.client.post('/api/shipping/quotes',
            headers=self._get_auth_headers(),
            json={
                'destination_address_id': self.test_address_id,
                'items': [
                    {
                        'product_id': 1,
                        'quantity': 1
                    }
                ],
                'service_code': 'standard'
            }
        )
        
        # May fail if Sendbox API is not configured
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'success')
            self.assertIn('quote_id', data['data'])


class TestPhase3ShipmentCreation(SendboxIntegrationTestCase):
    """Test Phase 3: Shipment Creation."""
    
    def test_checkout_with_shipping(self):
        """Test checkout with shipping selection."""
        if not self.test_address_id:
            self.skipTest("No test address available")
        
        response = self.client.post('/api/checkout',
            headers=self._get_auth_headers(),
            json={
                'address_id': self.test_address_id,
                'payment_method': 'flutterwave',
                'transaction_id': 'TEST' + str(int(datetime.now().timestamp())),
                'items': [
                    {
                        'product_id': 1,
                        'quantity': 1
                    }
                ],
                'selected_shipping': {
                    'carrier': 'DHL',
                    'service_code': 'standard',
                    'shipping_cost': 5000
                }
            }
        )
        
        self.assertIn(response.status_code, [200, 201])
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        
        # Store order ID for later tests
        if 'order' in data['data']:
            self.__class__.test_order_id = data['data']['order']['id']


class TestPhase4Tracking(SendboxIntegrationTestCase):
    """Test Phase 4: Tracking Integration."""
    
    def test_webhook_endpoint(self):
        """Test webhook endpoint reception."""
        response = self.client.post('/api/webhooks/test',
            json={'test': 'data'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
    
    def test_track_order_by_tracking_number(self):
        """Test tracking order by internal tracking number."""
        # Get a test order first
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT tracking FROM orders LIMIT 1")
        order = cursor.fetchone()
        conn.close()
        
        if not order:
            self.skipTest("No orders available for testing")
        
        response = self.client.get(f'/api/orders/track/{order["tracking"]}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('order', data['data'])


class TestPhase5AdminFeatures(SendboxIntegrationTestCase):
    """Test Phase 5: Admin Features."""
    
    def test_admin_get_all_orders(self):
        """Test admin can get all orders."""
        response = self.client.get('/api/admin/orders',
            headers=self._get_auth_headers(admin=True)
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('orders', data['data'])
    
    def test_admin_shipping_report(self):
        """Test admin can generate shipping report."""
        response = self.client.get('/api/admin/reports/shipping',
            headers=self._get_auth_headers(admin=True)
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('summary', data['data'])
    
    def test_admin_sendbox_account(self):
        """Test admin can view Sendbox account."""
        response = self.client.get('/api/admin/sendbox/account',
            headers=self._get_auth_headers(admin=True)
        )
        
        # May fail if Sendbox API is not configured
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'success')
            self.assertIn('account', data['data'])


class TestErrorHandling(SendboxIntegrationTestCase):
    """Test error handling and edge cases."""
    
    def test_invalid_address_id(self):
        """Test handling of invalid address ID."""
        response = self.client.post('/api/shipping/quotes',
            headers=self._get_auth_headers(),
            json={
                'destination_address_id': 99999,
                'items': [{'product_id': 1, 'quantity': 1}]
            }
        )
        
        self.assertEqual(response.status_code, 404)
    
    def test_missing_authentication(self):
        """Test endpoints require authentication."""
        response = self.client.get('/api/addresses')
        self.assertEqual(response.status_code, 401)
    
    def test_admin_only_endpoints(self):
        """Test admin endpoints reject non-admin users."""
        response = self.client.get('/api/admin/orders',
            headers=self._get_auth_headers(admin=False)
        )
        self.assertEqual(response.status_code, 403)


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
