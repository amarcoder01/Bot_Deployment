#!/usr/bin/env python3
"""
Final test to verify the advanced analysis formatting fix
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_handler import TelegramHandler
import yfinance as yf
from enhanced_technical_indicators import EnhancedTechnicalIndicators

async def test_formatting_directly():
    """Test the formatting method directly with real data"""
    print("🧪 Testing Advanced Analysis Formatting Fix...\n")
    
    try:
        # Create handler instance
        handler = TelegramHandler()
        
        # Get real market data for AAPL
        print("📊 Fetching real market data for AAPL...")
        ticker = yf.Ticker('AAPL')
        hist = ticker.history(period='1d')
        info = ticker.info
        
        if hist.empty:
            print("❌ No data available for AAPL")
            return False
        
        # Get current data
        current_data = hist.iloc[-1]
        price = current_data['Close']
        
        # Create market data dict
        market_data = {
            'price': price,
            'change': current_data['Close'] - current_data['Open'],
            'change_percent': ((current_data['Close'] - current_data['Open']) / current_data['Open']) * 100,
            'volume': current_data['Volume'],
            'high': current_data['High'],
            'low': current_data['Low'],
            'open': current_data['Open'],
            'source': 'yfinance'
        }
        
        # Get technical indicators
        print("📈 Calculating technical indicators...")
        tech_calc = EnhancedTechnicalIndicators()
        hist_extended = ticker.history(period='3mo')  # Get more data for indicators
        
        if len(hist_extended) >= 20:
            tech_indicators = tech_calc.calculate_all_indicators(hist_extended)
            market_data['technical_indicators'] = tech_indicators
        
        # Test the formatting method directly
        print("🔧 Testing formatting method...")
        formatted_response = await handler._format_advanced_analysis_response('AAPL', market_data)
        
        print("✅ Formatting completed successfully!")
        print(f"📄 Response length: {len(formatted_response)} characters")
        
        # Check for problematic formatting
        problematic_patterns = [
            '**',  # Bold markdown
            '%K',  # Unescaped percent
            '%D',  # Unescaped percent
        ]
        
        issues_found = []
        for pattern in problematic_patterns:
            if pattern in formatted_response:
                count = formatted_response.count(pattern)
                issues_found.append(f"{pattern} ({count} occurrences)")
        
        if issues_found:
            print(f"❌ Found problematic formatting patterns: {issues_found}")
            print("\n📄 Response preview (first 500 chars):")
            print(formatted_response[:500])
            print("\n📄 Response end (last 200 chars):")
            print(formatted_response[-200:])
            return False
        else:
            print("✅ No problematic formatting patterns found!")
            print("\n📄 Response preview (first 400 chars):")
            print(formatted_response[:400])
            print("...")
            print("\n📄 Response end (last 150 chars):")
            print(formatted_response[-150:])
            return True
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_formatting_directly())
    if success:
        print("\n🎉 All formatting tests passed! The advanced analysis command should now work without Markdown parsing errors.")
    else:
        print("\n❌ Formatting issues still exist. Please check the output above.")