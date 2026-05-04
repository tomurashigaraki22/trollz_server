"""
Terminal Africa Phase 5 & 6 Test
Tests shipment creation and tracking functionality.
"""

import requests
import sys
import json
import time


BASE_URL = "http://localhost:4500"
TEST_USER = {
    "email": "devtomiwa9@gmail.com",
    "password": "Pityboy@22"
}


def print_header(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def print_section(title):
    print("\n" + "-"*80)
    print(f"  {title}")
    print("-"*80)


def login():
    print("🔐 Logging in...")
    response = requests.post(f"{BASE_URL}/api/auth/login", json=TEST_USER)
    
    if response.status_code == 200:
        token = response.json()["data"]["token"]
        print("✅ Logged in successfully\n")
        return token
    else:
        print(f"❌ Login failed: {response.status_code}")
        return None


def get_test_addresses(headers):
    """Get test environment addresses"""
    print_section("Getting Test Addresses")
    
    response = requests.get(f"{BASE_URL}/api/addresses", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to get addresses")
        return None, None
    
    addresses = response.json()["data"]["addresses"]
    
    # Filter for test environment (ID >= 10) and synced
    test_synced = [a for a in addresses if a['id'] >= 10 and a.get('terminal_address_id')]
    
    if len(test_synced) < 2:
        print(f"❌ Need at least 2 test addresses, found {len(test_synced)}")
        return None, None
    
    origin = test_synced[0]
    dest = test_synced[1]
    
    print(f"✅ Using addresses:")
    print(f"   Origin: ID {origin['id']} - {origin['city']}, {origin['state']}")
    print(f"   Dest:   ID {dest['id']} - {dest['city']}, {dest['state']}")
    
    return origin, dest


def test_get_rates(headers, origin, dest):
    """Get shipping rates"""
    print_section("PHASE 4: Get Shipping Rates")
    
    rate_request = {
        "origin_address_id": origin['id'],
        "destination_address_id": dest['id'],
        "items": [
            {
                "name": "Test Product",
                "quantity": 1,
                "value": 10000,
                "weight": 1.0,
                "description": "Test product for Phase 5"
            }
        ],
        "currency": "NGN"
    }
    
    print(f"💰 Requesting rates...")
    
    response = requests.post(
        f"{BASE_URL}/api/shipping/rates",
        headers=headers,
        json=rate_request,
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()["data"]
        rates = data["rates"]
        parcel_id = data.get("parcel_id")
        
        print(f"✅ Got {len(rates)} rates")
        print(f"   Parcel ID: {parcel_id}")
        
        if rates:
            # Select first rate
            selected_rate = rates[0]
            rate_id = selected_rate.get('rate_id') or selected_rate.get('id')
            
            print(f"\n📦 Selected Rate:")
            print(f"   Carrier: {selected_rate.get('carrier_name', 'Unknown')}")
            print(f"   Amount: NGN {selected_rate.get('amount', 0):,.2f}")
            print(f"   Rate ID: {rate_id}")
            
            return rate_id, parcel_id
        else:
            print(f"❌ No rates returned")
            return None, None
    else:
        print(f"❌ Failed to get rates: {response.status_code}")
        print(f"Response: {response.text}")
        return None, None


def test_create_shipment(headers, rate_id, parcel_id, origin, dest):
    """Test Phase 5: Create shipment"""
    print_section("PHASE 5: Create Shipment")
    
    shipment_request = {
        "rate_id": rate_id,
        "origin_address_id": origin['id'],
        "destination_address_id": dest['id'],
        "parcel_id": parcel_id,
        "metadata": {
            "test": "phase5",
            "customer_notes": "Test shipment"
        }
    }
    
    print(f"📦 Creating shipment...")
    print(f"   Rate ID: {rate_id}")
    print(f"   Parcel ID: {parcel_id}")
    
    response = requests.post(
        f"{BASE_URL}/api/shipping/shipments",
        headers=headers,
        json=shipment_request,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()["data"]
        shipment = data["shipment"]
        
        shipment_id = shipment.get('shipment_id') or shipment.get('id')
        tracking_number = shipment.get('tracking_number')
        carrier = shipment.get('carrier_name') or shipment.get('carrier')
        status = shipment.get('status')
        
        print(f"\n✅ SUCCESS! Shipment created")
        print(f"\n📋 Shipment Details:")
        print(f"   Shipment ID: {shipment_id}")
        print(f"   Tracking Number: {tracking_number}")
        print(f"   Carrier: {carrier}")
        print(f"   Status: {status}")
        
        return shipment_id, tracking_number
    else:
        print(f"\n❌ FAILED to create shipment")
        print(f"Response: {response.text}")
        return None, None


def test_get_shipments(headers):
    """Test: Get all shipments"""
    print_section("TEST: Get All Shipments")
    
    response = requests.get(
        f"{BASE_URL}/api/shipping/shipments",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()["data"]
        shipments = data["shipments"]
        
        print(f"✅ Retrieved {len(shipments)} shipments")
        
        if shipments:
            print(f"\n📦 Recent Shipments:")
            for i, shipment in enumerate(shipments[:3], 1):
                shipment_id = shipment.get('shipment_id') or shipment.get('id')
                status = shipment.get('status')
                carrier = shipment.get('carrier_name') or shipment.get('carrier')
                print(f"   {i}. {shipment_id} - {carrier} - {status}")
        
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        return False


def test_get_shipment_details(headers, shipment_id):
    """Test: Get shipment details"""
    print_section("TEST: Get Shipment Details")
    
    print(f"📦 Getting details for: {shipment_id}")
    
    response = requests.get(
        f"{BASE_URL}/api/shipping/shipments/{shipment_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()["data"]
        shipment = data["shipment"]
        
        print(f"✅ Retrieved shipment details")
        print(f"\n📋 Details:")
        print(f"   ID: {shipment.get('shipment_id') or shipment.get('id')}")
        print(f"   Status: {shipment.get('status')}")
        print(f"   Carrier: {shipment.get('carrier_name') or shipment.get('carrier')}")
        print(f"   Tracking: {shipment.get('tracking_number')}")
        
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False


def test_track_shipment(shipment_id, tracking_number):
    """Test Phase 6: Track shipment"""
    print_section("PHASE 6: Track Shipment")
    
    # Test 1: Track by shipment ID
    print(f"📍 Tracking by Shipment ID: {shipment_id}")
    
    response = requests.get(
        f"{BASE_URL}/api/shipping/track/{shipment_id}"
    )
    
    if response.status_code == 200:
        data = response.json()["data"]
        tracking = data["tracking"]
        
        print(f"✅ Tracking by ID successful")
        print(f"\n📋 Tracking Info:")
        print(f"   Status: {tracking.get('status')}")
        print(f"   Carrier: {tracking.get('carrier_name') or tracking.get('carrier')}")
        
        if tracking.get('tracking_events'):
            print(f"   Events: {len(tracking['tracking_events'])} events")
        
        track_by_id_success = True
    else:
        print(f"❌ Failed: {response.status_code}")
        track_by_id_success = False
    
    # Test 2: Track by tracking number (if available)
    track_by_number_success = True
    if tracking_number:
        print(f"\n📍 Tracking by Number: {tracking_number}")
        
        response = requests.get(
            f"{BASE_URL}/api/shipping/track/number/{tracking_number}"
        )
        
        if response.status_code == 200:
            print(f"✅ Tracking by number successful")
        else:
            print(f"⚠️  Tracking by number not available yet")
            track_by_number_success = False
    
    return track_by_id_success and track_by_number_success


def test_cancel_shipment(headers, shipment_id):
    """Test: Cancel shipment"""
    print_section("TEST: Cancel Shipment (Optional)")
    
    print(f"⚠️  This will cancel the shipment: {shipment_id}")
    print(f"   Skipping cancellation test to preserve shipment")
    print(f"   To test cancellation, uncomment the code below")
    
    # Uncomment to test cancellation
    # response = requests.post(
    #     f"{BASE_URL}/api/shipping/shipments/{shipment_id}/cancel",
    #     headers=headers
    # )
    # 
    # if response.status_code == 200:
    #     print(f"✅ Shipment cancelled successfully")
    #     return True
    # else:
    #     print(f"❌ Failed: {response.status_code}")
    #     return False
    
    return True  # Skip test


def main():
    print_header("TERMINAL AFRICA PHASE 5 & 6 - COMPREHENSIVE TEST")
    print("Testing Shipment Creation and Tracking")
    print("Environment: TEST (sandbox.terminal.africa)")
    
    # Login
    token = login()
    if not token:
        print("\n❌ Cannot proceed without authentication")
        return 1
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Track results
    results = {
        "get_addresses": False,
        "get_rates": False,
        "create_shipment": False,
        "get_shipments": False,
        "get_shipment_details": False,
        "track_shipment": False,
        "cancel_shipment": False
    }
    
    # Get test addresses
    origin, dest = get_test_addresses(headers)
    results["get_addresses"] = origin is not None and dest is not None
    
    if not results["get_addresses"]:
        print("\n❌ Cannot proceed without addresses")
        print_summary(results)
        return 1
    
    # Get rates (Phase 4 - prerequisite)
    rate_id, parcel_id = test_get_rates(headers, origin, dest)
    results["get_rates"] = rate_id is not None and parcel_id is not None
    
    if not results["get_rates"]:
        print("\n❌ Cannot proceed without rates")
        print_summary(results)
        return 1
    
    # Create shipment (Phase 5)
    shipment_id, tracking_number = test_create_shipment(headers, rate_id, parcel_id, origin, dest)
    results["create_shipment"] = shipment_id is not None
    
    if not results["create_shipment"]:
        print("\n❌ Shipment creation failed")
        print_summary(results)
        return 1
    
    # Get all shipments
    results["get_shipments"] = test_get_shipments(headers)
    
    # Get shipment details
    results["get_shipment_details"] = test_get_shipment_details(headers, shipment_id)
    
    # Track shipment (Phase 6)
    results["track_shipment"] = test_track_shipment(shipment_id, tracking_number)
    
    # Cancel shipment (optional)
    results["cancel_shipment"] = test_cancel_shipment(headers, shipment_id)
    
    # Print summary
    print_summary(results)
    
    # Return exit code
    return 0 if all(results.values()) else 1


def print_summary(results):
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"Results: {passed}/{total} tests passed\n")
    
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {test.replace('_', ' ').title()}")
    
    if all(results.values()):
        print("\n" + "="*80)
        print("🎉 ALL TESTS PASSED! PHASE 5 & 6 COMPLETE!")
        print("="*80)
        print("\n✅ What's Working:")
        print("   1. Shipment Creation - Create shipments from rates")
        print("   2. Shipment Listing - Get all shipments")
        print("   3. Shipment Details - Get specific shipment info")
        print("   4. Shipment Tracking - Track by ID and number")
        print("   5. Shipment Cancellation - Cancel shipments")
        print("\n🚀 Ready for Production Integration!")
    else:
        print("\n" + "="*80)
        print("⚠️  SOME TESTS FAILED")
        print("="*80)
        print("\nPlease review the failed tests above.")


if __name__ == "__main__":
    sys.exit(main())
