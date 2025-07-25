import sys
import asyncio
import yfinance as yf
import pandas as pd
sys.path.append('C:\\bot_d')
sys.path.append('C:\\bot_d\\TradeAiCompanion')
from TradeAiCompanion.market_data_service import MarketDataService

async def test():
    # First check direct yfinance data
    print("\n=== Direct YFinance Test ===")
    ticker = yf.Ticker('AAPL')
    hist_1d = ticker.history(period='1d', interval='1d')
    hist_1m = ticker.history(period='1d', interval='1m')
    print(f"1d interval data available: {not hist_1d.empty}")
    print(f"1m interval data available: {not hist_1m.empty}")
    if not hist_1d.empty:
        print(f"1d Volume: {hist_1d['Volume'].iloc[-1]}")
    if not hist_1m.empty:
        print(f"1m Latest Volume: {hist_1m['Volume'].iloc[-1]}")
        print(f"1m Volume is zero: {hist_1m['Volume'].iloc[-1] == 0}")
        print(f"All 1m volumes are zero: {(hist_1m['Volume'] == 0).all()}")
        # Print the last 5 rows of the 1m data
        print("\nLast 5 rows of 1m data:")
        print(hist_1m.tail())
    
    # Now test through market data service
    print("\n=== Market Data Service Test ===")
    market_service = MarketDataService()
    price_data = await market_service.get_stock_price('AAPL')
    print('Symbol:', price_data.get('symbol', 'N/A'))
    print('Price:', price_data.get('price', 'N/A'))
    print('Change:', price_data.get('change', 'N/A'))
    print('Change Percent:', price_data.get('change_percent', 'N/A'))
    print('Volume:', price_data.get('volume', 'N/A'))
    print('Market Cap:', price_data.get('market_cap', 'N/A'))
    print('PE Ratio:', price_data.get('pe_ratio', 'N/A'))
    print('Source:', price_data.get('source', 'N/A'))

if __name__ == '__main__':
    asyncio.run(test())