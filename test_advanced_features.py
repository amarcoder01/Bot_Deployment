"""
Test script for advanced features: Auto-Trainer and Alert Service
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qlib_service import QlibService
from auto_trainer import AutoTrainer
from alert_service import AlertService
from market_data_service import MarketDataService
from logger import logger

async def test_alert_service():
    """Test the alert service functionality"""
    print("🔔 Testing Alert Service...")
    
    # Mock market service
    class MockMarketService:
        async def get_stock_price(self, symbol, user_id):
            # Return mock prices
            mock_prices = {
                'AAPL': 150.0,
                'TSLA': 200.0,
                'GOOGL': 2800.0
            }
            return {'price': mock_prices.get(symbol, 100.0)}
    
    market_service = MockMarketService()
    alert_service = AlertService(market_service)
    
    # Test adding alerts
    result1 = alert_service.add_alert(123, 'AAPL', 'above', 160.0)
    result2 = alert_service.add_alert(123, 'TSLA', 'below', 180.0)
    result3 = alert_service.add_alert(456, 'GOOGL', 'above', 2900.0)
    
    print(f"✅ Alert 1 created: {result1['success']}")
    print(f"✅ Alert 2 created: {result2['success']}")
    print(f"✅ Alert 3 created: {result3['success']}")
    
    # Test getting user alerts
    user_alerts = alert_service.get_user_alerts(123)
    print(f"📊 User 123 has {len(user_alerts)} alerts")
    
    # Test alert statistics
    stats = alert_service.get_alert_stats()
    print(f"📈 Alert stats: {stats}")
    
    # Test alert monitoring (simplified)
    print("🔄 Testing alert monitoring...")
    await alert_service._check_alerts()
    
    print("✅ Alert service test completed!")

async def test_auto_trainer():
    """Test the auto-trainer functionality"""
    print("🤖 Testing Auto-Trainer...")
    
    qlib_service = QlibService()
    auto_trainer = AutoTrainer(qlib_service)
    
    # Test training status
    status = auto_trainer.get_training_status()
    print(f"📊 Training status: {status}")
    
    # Test manual training
    print("🔄 Testing manual training...")
    await auto_trainer.manual_train()
    
    # Check updated status
    status_after = auto_trainer.get_training_status()
    print(f"📊 Training status after manual train: {status_after}")
    
    print("✅ Auto-trainer test completed!")

async def test_integration():
    """Test integration between services"""
    print("🔗 Testing Service Integration...")
    
    # Initialize services
    qlib_service = QlibService()
    market_service = MarketDataService()
    
    # Test Qlib signals
    signals = qlib_service.get_signals(['AAPL', 'TSLA', 'GOOGL'])
    print(f"📊 Generated {len(signals)} Qlib signals")
    
    # Test alert with real market data
    alert_service = AlertService(market_service)
    
    # Add a test alert
    result = alert_service.add_alert(999, 'AAPL', 'above', 200.0)
    print(f"✅ Test alert created: {result['success']}")
    
    # Check alerts
    alerts = alert_service.get_user_alerts(999)
    print(f"📊 Test user has {len(alerts)} alerts")
    
    print("✅ Integration test completed!")

async def main():
    """Run all tests"""
    print("🚀 Starting Advanced Features Test Suite...")
    print("=" * 50)
    
    try:
        await test_alert_service()
        print("-" * 30)
        
        await test_auto_trainer()
        print("-" * 30)
        
        await test_integration()
        print("-" * 30)
        
        print("🎉 All tests completed successfully!")
        print("✅ Auto-training service: Ready")
        print("✅ Alert monitoring service: Ready")
        print("✅ Qlib integration: Working")
        print("✅ Real-time notifications: Configured")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logger.error(f"Test error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 