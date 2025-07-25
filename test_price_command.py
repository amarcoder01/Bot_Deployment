import sys
import asyncio
sys.path.append('C:\\bot_d')
sys.path.append('C:\\bot_d\\TradeAiCompanion')
from TradeAiCompanion.ui_components import TradingBotUI
from TradeAiCompanion.market_data_service import MarketDataService

async def test():
    # Test the market data service directly
    print("\n=== Testing Market Data Service ===")
    market_service = MarketDataService()
    symbol = 'AAPL'
    price_data = await market_service.get_stock_price(symbol)
    print(f"Source: {price_data.get('source', 'Unknown')}")
    print(f"Volume: {price_data.get('volume', 0):,}")
    
    # Test the UI formatting directly
    print("\n=== Testing UI Formatting ===")
    formatted_price = TradingBotUI.format_price_data(price_data, symbol)
    print(formatted_price)
    
    # Test format_large_number directly
    print("\n=== Testing format_large_number ===")
    test_numbers = [0, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]
    for num in test_numbers:
        print(f"{num} -> {TradingBotUI.format_large_number(num)}")
    
    # Test with the actual volume from the price data
    volume = price_data.get('volume', 0)
    print(f"\nActual volume: {volume} -> {TradingBotUI.format_large_number(volume)}")

if __name__ == '__main__':
    asyncio.run(test())