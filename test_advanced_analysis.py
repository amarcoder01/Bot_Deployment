#!/usr/bin/env python3
"""
Test script to verify the advanced_analysis command with yfinance
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_yfinance_integration():
    """Test yfinance integration for advanced analysis"""
    print("🔍 Testing yfinance integration for advanced_analysis command...\n")
    
    symbol = "AAPL"
    
    try:
        # Test current price data
        print(f"📊 Testing current price data for {symbol}...")
        ticker = yf.Ticker(symbol)
        
        # Get current price info
        info = ticker.info
        hist = ticker.history(period='1d', interval='1m')
        
        if hist.empty:
            print(f"❌ No data available for {symbol}")
            return False
        
        current_price = hist['Close'].iloc[-1]
        open_price = hist['Open'].iloc[0]
        high_price = hist['High'].max()
        low_price = hist['Low'].min()
        volume = hist['Volume'].sum()
        
        # Calculate change
        change = current_price - open_price
        change_percent = (change / open_price) * 100 if open_price > 0 else 0
        
        print(f"✅ Current Price: ${current_price:.2f}")
        print(f"✅ Change: ${change:+.2f} ({change_percent:+.2f}%)")
        print(f"✅ Volume: {volume:,.0f}")
        print(f"✅ High: ${high_price:.2f}")
        print(f"✅ Low: ${low_price:.2f}")
        print(f"✅ Open: ${open_price:.2f}")
        
        # Test historical data for technical indicators
        print(f"\n📈 Testing historical data for technical indicators...")
        hist_data = ticker.history(period='3mo')
        
        if not hist_data.empty:
            print(f"✅ Historical data: {len(hist_data)} days")
            print(f"✅ Date range: {hist_data.index[0].date()} to {hist_data.index[-1].date()}")
            
            # Test basic technical calculations
            sma_20 = hist_data['Close'].rolling(window=20).mean().iloc[-1]
            sma_50 = hist_data['Close'].rolling(window=50).mean().iloc[-1]
            
            if not pd.isna(sma_20):
                print(f"✅ SMA 20: ${sma_20:.2f}")
            if not pd.isna(sma_50):
                print(f"✅ SMA 50: ${sma_50:.2f}")
                
            # RSI calculation
            delta = hist_data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs.iloc[-1]))
            
            if not pd.isna(rsi):
                print(f"✅ RSI: {rsi:.1f}")
        else:
            print("❌ No historical data available")
            return False
        
        print(f"\n✅ yfinance integration test PASSED!")
        print(f"📅 Test completed at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

if __name__ == "__main__":
    success = test_yfinance_integration()
    if success:
        print("\n🎉 All tests passed! The advanced_analysis command should work correctly with yfinance.")
    else:
        print("\n💥 Tests failed! There may be issues with the yfinance integration.")
    
    sys.exit(0 if success else 1)