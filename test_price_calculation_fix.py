#!/usr/bin/env python3
"""
Test script to verify price calculation fixes
This script tests the corrected change calculation logic
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from market_data_service import MarketDataService
from logger import logger

async def test_price_calculations():
    """Test price calculations for multiple stocks"""
    print("\n🧪 Testing Price Calculation Fixes")
    print("=" * 50)
    
    # Initialize market service
    market_service = MarketDataService()
    
    # Test stocks
    test_symbols = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN']
    
    for symbol in test_symbols:
        try:
            print(f"\n📊 Testing {symbol}...")
            
            # Get price data
            price_data = await market_service.get_stock_price(symbol, user_id=12345)
            
            if price_data:
                price = price_data.get('price', 'N/A')
                change = price_data.get('change', 'N/A')
                change_percent = price_data.get('change_percent', 'N/A')
                source = price_data.get('source', 'Unknown')
                
                print(f"   ✅ {symbol}: ${price}")
                print(f"   📈 Change: ${change} ({change_percent:+.2f}%)" if isinstance(change_percent, (int, float)) else f"   📈 Change: ${change} ({change_percent})")
                print(f"   🔗 Source: {source}")
                
                # Validate that change calculations make sense
                if isinstance(change, (int, float)) and isinstance(change_percent, (int, float)):
                    if abs(change_percent) > 50:  # Unrealistic daily change
                        print(f"   ⚠️  WARNING: Unusually large change percentage: {change_percent}%")
                    else:
                        print(f"   ✅ Change calculation looks reasonable")
                else:
                    print(f"   ⚠️  WARNING: Non-numeric change values")
            else:
                print(f"   ❌ Failed to get data for {symbol}")
                
        except Exception as e:
            print(f"   ❌ Error testing {symbol}: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Price calculation test completed!")
    print("\n📝 Expected behavior:")
    print("   - Change should be calculated from previous day's close")
    print("   - Change percentage should be reasonable (typically < 10% daily)")
    print("   - Different stocks should show different change values")

if __name__ == "__main__":
    asyncio.run(test_price_calculations())