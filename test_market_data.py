import asyncio
import sys
sys.path.append('C:\\bot_d\\TradeAiCompanion')
from market_data_service import MarketDataService
import logging

# Reduce logging noise
logging.basicConfig(level=logging.WARNING)

async def test_market_data():
    ms = MarketDataService()
    
    print("Testing market data fetching...\n")
    
    # Test SPY
    spy = await ms.get_stock_price('SPY')
    print(f'SPY data: {spy}\n')
    
    # Test QQQ
    qqq = await ms.get_stock_price('QQQ')
    print(f'QQQ data: {qqq}\n')
    
    # Test VIX
    vix = await ms.get_stock_price('^VIX')
    print(f'VIX data: {vix}\n')
    
    # Test what the _get_market_context would return
    print("Market context calculation:")
    spy_performance = spy.get('change_percent', 0) if spy else 0
    qqq_performance = qqq.get('change_percent', 0) if qqq else 0
    vix_level = vix.get('price', 20) if vix and vix.get('price') else 20
    
    print(f"SPY Performance: {spy_performance:.2f}%")
    print(f"QQQ Performance: {qqq_performance:.2f}%")
    print(f"VIX Level: {vix_level:.1f}")
    
    # Check if the issue is with change_percent vs change
    if spy:
        print(f"\nSPY raw data analysis:")
        print(f"  change: {spy.get('change', 'N/A')}")
        print(f"  change_percent: {spy.get('change_percent', 'N/A')}")
        print(f"  price: {spy.get('price', 'N/A')}")
    
    if qqq:
        print(f"\nQQQ raw data analysis:")
        print(f"  change: {qqq.get('change', 'N/A')}")
        print(f"  change_percent: {qqq.get('change_percent', 'N/A')}")
        print(f"  price: {qqq.get('price', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(test_market_data())