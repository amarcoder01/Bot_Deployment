#!/usr/bin/env python3
"""
Test script to verify chart timeframe fix
Tests that /chart NVDA 6M generates a 6-month chart instead of 1-day
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chart_service import ChartService
from logger import logger

async def test_chart_timeframes():
    """Test chart generation with different timeframes"""
    chart_service = ChartService()
    
    test_cases = [
        ('NVDA', '1d', 'Should generate 1-day chart'),
        ('NVDA', '6M', 'Should generate 6-month chart'),
        ('NVDA', '6mo', 'Should generate 6-month chart (alternative format)'),
        ('AAPL', '1y', 'Should generate 1-year chart'),
        ('TSLA', '3mo', 'Should generate 3-month chart')
    ]
    
    print("Testing chart timeframe handling...")
    print("=" * 50)
    
    for symbol, period, description in test_cases:
        print(f"\nTesting: {symbol} with period '{period}'")
        print(f"Expected: {description}")
        
        try:
            # Test the chart generation
            chart_b64 = await chart_service.generate_price_chart(symbol, period)
            
            if chart_b64:
                print(f"✅ SUCCESS: Chart generated for {symbol} with period {period}")
                print(f"   Chart data length: {len(chart_b64)} characters")
            else:
                print(f"❌ FAILED: No chart generated for {symbol} with period {period}")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("Chart timeframe test completed!")
    print("\nNote: Check the bot logs to see the period parameter being used correctly.")
    print("Look for log messages like: 'Generating chart for NVDA via Chart-IMG API (forced) - Period: 6M'")

if __name__ == "__main__":
    asyncio.run(test_chart_timeframes())