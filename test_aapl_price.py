import asyncio
from market_data_service import MarketDataService
from logger import logger

async def test_aapl_price():
    """Test AAPL price fetching with detailed debugging"""
    print("Testing AAPL price fetching...")
    
    service = MarketDataService()
    
    # Test with user_id to enable OpenAI fallback
    result = await service.get_stock_price('AAPL', user_id=12345)
    
    if result:
        print(f"✅ SUCCESS: Got AAPL price data")
        print(f"Price: ${result.get('price', 'N/A')}")
        print(f"Source: {result.get('source', 'N/A')}")
        print(f"Company: {result.get('company_name', 'N/A')}")
        print(f"Change: {result.get('change_percent', 'N/A')}%")
    else:
        print("❌ FAILED: Could not get AAPL price data")
        print("Check the logs above for detailed error information")

if __name__ == "__main__":
    asyncio.run(test_aapl_price())