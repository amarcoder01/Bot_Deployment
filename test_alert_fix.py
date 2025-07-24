#!/usr/bin/env python3
"""
Test script to verify alert functionality after database migration
"""

import asyncio
from alert_service import AlertService
from market_data_service import MarketDataService

async def test_alert_functionality():
    """Test if alert add/remove functionality works after migration"""
    try:
        # Initialize market service first
        market_service = MarketDataService()
        service = AlertService(market_service)
        
        print("Testing alert functionality...")
        
        # Test adding an alert
        print("\n1. Testing add alert...")
        add_result = await service.add_alert(123456789, 'AAPL', 'above', 200.0)
        print(f"Add alert result: {add_result}")
        
        if add_result.get('success'):
            alert_id = add_result.get('alert_id')
            print(f"Alert added successfully with ID: {alert_id}")
            
            # Test removing the alert
            print("\n2. Testing remove alert...")
            remove_result = await service.remove_alert('123456789', alert_id)
            print(f"Remove alert result: {remove_result}")
            
            if remove_result.get('success'):
                print("\n✅ Alert functionality is working correctly!")
                return True
            else:
                print(f"\n❌ Alert removal failed: {remove_result.get('error')}")
                return False
        else:
            print(f"\n❌ Alert addition failed: {add_result.get('error')}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error testing alert functionality: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_alert_functionality())