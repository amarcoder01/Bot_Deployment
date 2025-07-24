#!/usr/bin/env python3
"""
Test script to verify market context calculations in deep analysis
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from market_data_service import MarketDataService
from telegram_handler import TelegramHandler
import asyncio

async def test_market_context():
    """Test the market context calculation"""
    print("Testing Market Context Calculations...")
    print("=" * 50)
    
    # Initialize services
    market_service = MarketDataService()
    
    # Test SPY data
    print("\n📊 Testing SPY data:")
    spy_data = await market_service.get_stock_price('SPY')
    if spy_data:
        print(f"  Price: ${spy_data['price']}")
        print(f"  Change: {spy_data['change']}")
        print(f"  Change %: {spy_data['change_percent']}%")
        print(f"  Formatted: {spy_data['change_percent']:+.3f}%")
    else:
        print("  ❌ Failed to get SPY data")
    
    # Test QQQ data
    print("\n💻 Testing QQQ data:")
    qqq_data = await market_service.get_stock_price('QQQ')
    if qqq_data:
        print(f"  Price: ${qqq_data['price']}")
        print(f"  Change: {qqq_data['change']}")
        print(f"  Change %: {qqq_data['change_percent']}%")
        print(f"  Formatted: {qqq_data['change_percent']:+.3f}%")
    else:
        print("  ❌ Failed to get QQQ data")
    
    # Test VIX data (use mock data if real VIX fails)
    print("\n😰 Testing VIX data:")
    vix_data = await market_service.get_stock_price('VIX')
    if not vix_data:
        print("  ❌ Failed to get VIX data - using mock data for testing")
        vix_data = {'price': 15.33, 'change': 0.0, 'change_percent': 0.0}
        print(f"  Mock Price: {vix_data['price']}")
        print(f"  Mock Change: {vix_data['change']}")
        print(f"  Mock Change %: {vix_data['change_percent']}%")
    else:
        print(f"  Price: {vix_data['price']}")
        print(f"  Change: {vix_data['change']}")
        print(f"  Change %: {vix_data['change_percent']}%")
    
    # Test market context formatting
    print("\n🌍 MARKET CONTEXT SIMULATION:")
    print("=" * 30)
    
    if spy_data and qqq_data and vix_data:
        # Simulate the market context display
        spy_perf = spy_data['change_percent']
        qqq_perf = qqq_data['change_percent']
        vix_level = vix_data['price']
        
        print(f"📊 SPY Performance: {spy_perf:+.3f}%")
        print(f"💻 QQQ Performance: {qqq_perf:+.3f}%")
        print(f"😰 VIX Level: {vix_level}")
        
        # Determine market regime based on VIX
        if vix_level < 12:
            regime = "Low Volatility"
        elif vix_level < 20:
            regime = "Neutral"
        elif vix_level < 30:
            regime = "Elevated Volatility"
        else:
            regime = "High Volatility"
        
        print(f"🎭 Market Regime: {regime}")
        
        # Test signal strength calculation (simplified)
        print("\n🎯 SIGNAL STRENGTH TEST:")
        print("=" * 25)
        
        # Mock some sentiment data for testing
        mock_sentiment_score = 0.65  # Example sentiment
        mock_confidence = 0.8        # Example confidence
        
        signal_strength = mock_sentiment_score * mock_confidence * 100
        print(f"Mock Sentiment Score: {mock_sentiment_score}")
        print(f"Mock Confidence: {mock_confidence}")
        print(f"💪 Signal Strength: {signal_strength:.1f}%")
        
        if signal_strength == 0.0:
            print("⚠️  WARNING: Signal strength is 0.0% - this indicates an issue!")
        
    else:
        print("❌ Cannot simulate market context - missing data")

if __name__ == "__main__":
    asyncio.run(test_market_context())