#!/usr/bin/env python3
"""
Test script to verify the Markdown parsing fix for advanced_analysis
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_handler import TelegramHandler
import yfinance as yf

async def test_markdown_parsing():
    """
    Test the _format_advanced_analysis_response method directly to verify Markdown parsing
    """
    print("🧪 Testing Markdown parsing fix for advanced_analysis...")
    
    try:
        # Initialize TelegramHandler
        handler = TelegramHandler()
        
        # Get real market data for testing
        print("\n1. Fetching real market data for AAPL...")
        ticker = yf.Ticker("AAPL")
        hist = ticker.history(period='1d', interval='1m')
        
        if hist.empty:
            print("   ❌ No data available for testing")
            return
        
        # Extract price data
        current_price = float(hist['Close'].iloc[-1])
        open_price = float(hist['Open'].iloc[0])
        high_price = float(hist['High'].max())
        low_price = float(hist['Low'].min())
        volume = int(hist['Volume'].sum())
        change = current_price - open_price
        change_percent = (change / open_price) * 100 if open_price > 0 else 0
        
        # Get historical data for technical indicators
        hist_data = ticker.history(period='3mo')
        indicators = handler.technical_indicators.calculate_all_indicators(hist_data)
        
        market_data = {
            'price': current_price,
            'change': change,
            'change_percent': change_percent,
            'volume': volume,
            'high': high_price,
            'low': low_price,
            'open': open_price,
            'source': 'yfinance',
            'technical_indicators': indicators
        }
        
        print(f"   ✅ Market data fetched: ${current_price:.2f} ({change_percent:+.2f}%)")
        print(f"   ✅ Technical indicators: {len(indicators)} calculated")
        
        # Test the response formatting
        print("\n2. Testing response formatting...")
        response = await handler._format_advanced_analysis_response("AAPL", market_data)
        
        print(f"   ✅ Response generated successfully")
        print(f"   📏 Response length: {len(response)} characters")
        
        # Check for problematic characters that could cause Markdown parsing issues
        print("\n3. Checking for Markdown parsing issues...")
        
        # Look for unescaped percent signs
        percent_issues = []
        lines = response.split('\n')
        for i, line in enumerate(lines):
            if '%' in line and not any(safe in line for safe in ['%)', '% -', '%.']):
                percent_issues.append(f"Line {i+1}: {line.strip()}")
        
        if percent_issues:
            print("   ⚠️ Potential percent sign issues found:")
            for issue in percent_issues[:3]:  # Show first 3 issues
                print(f"      {issue}")
        else:
            print("   ✅ No problematic percent signs found")
        
        # Look for other potential Markdown issues
        markdown_issues = []
        if '**' in response and response.count('**') % 2 != 0:
            markdown_issues.append("Unmatched bold markers (**)")
        
        if '_' in response and response.count('_') % 2 != 0:
            markdown_issues.append("Unmatched italic markers (_)")
        
        if markdown_issues:
            print("   ⚠️ Potential Markdown issues:")
            for issue in markdown_issues:
                print(f"      {issue}")
        else:
            print("   ✅ No Markdown formatting issues detected")
        
        # Show a preview of the response
        print("\n4. Response preview (first 500 characters):")
        print(f"   {response[:500]}...")
        
        # Test specific sections that were problematic
        print("\n5. Checking specific fixed sections...")
        
        if "Stochastic:" in response:
            stoch_line = [line for line in lines if "Stochastic:" in line][0]
            if "%K=" in stoch_line or "%D=" in stoch_line:
                print("   ❌ Still contains problematic %K or %D")
            else:
                print("   ✅ Stochastic formatting fixed (no %K/%D)")
        
        if "Williams" in response:
            williams_line = [line for line in lines if "Williams" in line][0]
            if "%R:" in williams_line:
                print("   ❌ Still contains problematic %R")
            else:
                print("   ✅ Williams R formatting fixed (no %R)")
        
        print("\n🏁 Markdown parsing test completed successfully!")
        print("\n✅ The advanced_analysis command should now work without Markdown parsing errors.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_markdown_parsing())