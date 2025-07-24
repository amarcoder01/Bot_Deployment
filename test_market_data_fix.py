#!/usr/bin/env python3
"""
Test script to verify the market data fetching fix with detailed debugging
"""

import asyncio
import sys
import os
import aiohttp
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from real_market_data import RealMarketDataService, YahooFinanceSource, GoogleFinanceSource, FinnhubSource

async def test_individual_sources():
    """Test each data source individually"""
    print("Testing individual data sources for AAPL...")
    
    async with aiohttp.ClientSession() as session:
        # Test Yahoo Finance
        print("\n1. Testing Yahoo Finance...")
        yahoo = YahooFinanceSource()
        try:
            yahoo_data = await yahoo.get_price('AAPL', session)
            if yahoo_data:
                print(f"✅ Yahoo Finance: ${yahoo_data.get('price', 'N/A')}")
            else:
                print("❌ Yahoo Finance: No data returned")
        except Exception as e:
            print(f"❌ Yahoo Finance error: {e}")
        
        # Test Google Finance
        print("\n2. Testing Google Finance...")
        google = GoogleFinanceSource()
        try:
            google_data = await google.get_price('AAPL', session)
            if google_data:
                print(f"✅ Google Finance: ${google_data.get('price', 'N/A')}")
            else:
                print("❌ Google Finance: No data returned")
        except Exception as e:
            print(f"❌ Google Finance error: {e}")
        
        # Test Finnhub
        print("\n3. Testing Finnhub...")
        finnhub = FinnhubSource()
        try:
            finnhub_data = await finnhub.get_price('AAPL', session)
            if finnhub_data:
                print(f"✅ Finnhub: ${finnhub_data.get('price', 'N/A')}")
            else:
                print("❌ Finnhub: No data returned")
                print(f"   API Key: {'Set' if finnhub.api_key else 'Missing'}")
        except Exception as e:
            print(f"❌ Finnhub error: {e}")

async def test_yahoo_api_directly():
    """Test Yahoo Finance API directly to see raw response"""
    print("\n\nTesting Yahoo Finance API directly...")
    
    async with aiohttp.ClientSession() as session:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
        params = {
            'interval': '1m',
            'range': '1d'
        }
        
        try:
            async with session.get(url, params=params) as response:
                print(f"Status: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    print(f"Response keys: {list(data.keys())}")
                    
                    if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                        result = data['chart']['result'][0]
                        meta = result.get('meta', {})
                        print(f"Meta keys: {list(meta.keys())}")
                        print(f"Regular Market Price: {meta.get('regularMarketPrice')}")
                        print(f"Symbol: {meta.get('symbol')}")
                    else:
                        print("No chart/result data in response")
                        print(f"Full response: {data}")
                else:
                    text = await response.text()
                    print(f"Error response: {text[:500]}")
        except Exception as e:
            print(f"Direct API test error: {e}")

async def test_market_data():
    """Test market data fetching for AAPL"""
    print("Testing RealMarketDataService...")
    
    async with RealMarketDataService() as service:
        # Test get_stock_price
        print("\n4. Testing RealMarketDataService.get_stock_price...")
        price_data = await service.get_stock_price('AAPL')
        if price_data:
            print(f"✅ Successfully got price data: ${price_data.get('price', 'N/A')} from {price_data.get('source', 'unknown')}")
            return True
        else:
            print("❌ Failed to get price data from RealMarketDataService")
            return False

if __name__ == "__main__":
    try:
        print("🔍 Debugging market data fetching issue...\n")
        
        # Test individual sources
        asyncio.run(test_individual_sources())
        
        # Test Yahoo API directly
        asyncio.run(test_yahoo_api_directly())
        
        # Test the service
        result = asyncio.run(test_market_data())
        
        if result:
            print("\n🎉 Market data fetching is now working properly!")
            sys.exit(0)
        else:
            print("\n❌ Market data fetching still has issues.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)