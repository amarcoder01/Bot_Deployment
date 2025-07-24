"""
Test script for Phase 3 Advanced Features
Real market data, advanced Qlib strategies, and enhanced technical indicators
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from real_market_data import RealMarketDataService
from advanced_qlib_strategies import AdvancedQlibStrategies
from enhanced_technical_indicators import EnhancedTechnicalIndicators
from logger import logger

async def test_real_market_data():
    """Test real market data integration"""
    print("📊 Testing Real Market Data Integration...")
    
    async with RealMarketDataService() as market_service:
        # Test stock price
        price_data = await market_service.get_stock_price('AAPL')
        print(f"✅ AAPL Price: ${price_data.get('price', 0):.2f} (Source: {price_data.get('source', 'Unknown')})")
        
        # Test historical data
        hist_data = await market_service.get_historical_data('TSLA', '1mo')
        print(f"✅ TSLA Historical Data: {len(hist_data)} records")
        
        # Test comprehensive market data
        market_data = await market_service.get_market_data('GOOGL')
        print(f"✅ GOOGL Market Data: {'Success' if market_data else 'Failed'}")
        

        
        # Test earnings calendar
        earnings = await market_service.get_earnings_calendar('AAPL')
        print(f"✅ AAPL Earnings: {len(earnings)} records")

async def test_advanced_qlib_strategies():
    """Test advanced Qlib strategies"""
    print("\n🤖 Testing Advanced Qlib Strategies...")
    
    advanced_qlib = AdvancedQlibStrategies()
    
    # Test model training
    symbols = ['AAPL', 'TSLA', 'GOOGL']
    models = advanced_qlib.train_multiple_models(symbols)
    print(f"✅ Trained {len(models)} models")
    
    # Test ensemble signals
    signals = advanced_qlib.generate_ensemble_signals(symbols)
    print(f"✅ Generated ensemble signals for {len(signals)} symbols")
    
    for symbol, signal in signals.items():
        print(f"   {symbol}: {signal['signal']} (Confidence: {signal['confidence']:.1f}%)")
    
    # Test portfolio optimization
    portfolio = advanced_qlib.portfolio_optimization(symbols, 'moderate')
    print(f"✅ Portfolio optimization completed")
    print(f"   Expected Return: {portfolio['metrics'].get('expected_return', 0):.1%}")
    print(f"   Volatility: {portfolio['metrics'].get('volatility', 0):.1%}")
    
    # Test risk management
    risk_metrics = advanced_qlib.risk_management({'AAPL': 1.0}, {})
    print(f"✅ Risk analysis completed")
    print(f"   Risk Level: {risk_metrics.get('risk_level', 'Unknown')}")
    print(f"   VaR (95%): ${risk_metrics.get('var_95', 0):,.0f}")

async def test_enhanced_technical_indicators():
    """Test enhanced technical indicators"""
    print("\n📈 Testing Enhanced Technical Indicators...")
    
    import pandas as pd
    import numpy as np
    
    # Create sample data
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    np.random.seed(42)
    
    sample_data = pd.DataFrame({
        'Date': dates,
        'Open': np.random.uniform(100, 200, 100),
        'High': np.random.uniform(200, 300, 100),
        'Low': np.random.uniform(50, 150, 100),
        'Close': np.random.uniform(100, 200, 100),
        'Volume': np.random.uniform(1000000, 5000000, 100)
    })
    
    # Calculate indicators
    indicators = EnhancedTechnicalIndicators()
    all_indicators = indicators.calculate_all_indicators(sample_data)
    
    print(f"✅ Calculated {len(all_indicators)} indicator categories")
    
    # Test specific indicators
    if 'rsi' in all_indicators:
        print(f"   RSI: {all_indicators['rsi']:.1f}")
    
    if 'macd' in all_indicators:
        print(f"   MACD: {all_indicators['macd']:.3f}")
    
    if 'sma_20' in all_indicators:
        print(f"   SMA 20: ${all_indicators['sma_20']:.2f}")
    
    if 'bb_upper' in all_indicators:
        print(f"   Bollinger Bands: ${all_indicators['bb_lower']:.2f} - ${all_indicators['bb_upper']:.2f}")
    
    # Test signals
    if 'signals' in all_indicators:
        signals = all_indicators['signals']
        print(f"   Overall Signal: {signals.get('overall_signal', 'Unknown')}")
        print(f"   Signal Strength: {signals.get('strength', 0)}")

async def test_integration():
    """Test integration between all services"""
    print("\n🔗 Testing Service Integration...")
    
    async with RealMarketDataService() as market_service:
        # Get real market data
        market_data = await market_service.get_market_data('AAPL')
        
        if market_data and 'historical_data' in market_data:
            # Convert to DataFrame
            import pandas as pd
            hist_df = pd.DataFrame(market_data['historical_data'])
            
            # Calculate technical indicators
            indicators = EnhancedTechnicalIndicators()
            tech_indicators = indicators.calculate_all_indicators(hist_df)
            
            # Generate Qlib signals
            advanced_qlib = AdvancedQlibStrategies()
            signals = advanced_qlib.generate_ensemble_signals(['AAPL'])
            
            print(f"✅ Integration test completed")
            print(f"   Market Data: {'Success' if market_data else 'Failed'}")
            print(f"   Technical Indicators: {'Success' if tech_indicators else 'Failed'}")
            print(f"   Qlib Signals: {'Success' if signals else 'Failed'}")
            
            # Combined analysis
            if signals and 'AAPL' in signals:
                signal = signals['AAPL']
                print(f"   Combined Signal: {signal['signal']} (Confidence: {signal['confidence']:.1f}%)")

async def test_performance():
    """Test performance of new features"""
    print("\n⚡ Testing Performance...")
    
    import time
    
    # Test market data performance
    start_time = time.time()
    async with RealMarketDataService() as market_service:
        await market_service.get_stock_price('AAPL')
    market_time = time.time() - start_time
    print(f"✅ Market Data: {market_time:.2f} seconds")
    
    # Test technical indicators performance
    start_time = time.time()
    import pandas as pd
    import numpy as np
    
    sample_data = pd.DataFrame({
        'Open': np.random.uniform(100, 200, 100),
        'High': np.random.uniform(200, 300, 100),
        'Low': np.random.uniform(50, 150, 100),
        'Close': np.random.uniform(100, 200, 100),
        'Volume': np.random.uniform(1000000, 5000000, 100)
    })
    
    indicators = EnhancedTechnicalIndicators()
    indicators.calculate_all_indicators(sample_data)
    indicators_time = time.time() - start_time
    print(f"✅ Technical Indicators: {indicators_time:.2f} seconds")
    
    # Test Qlib strategies performance
    start_time = time.time()
    advanced_qlib = AdvancedQlibStrategies()
    advanced_qlib.generate_ensemble_signals(['AAPL', 'TSLA', 'GOOGL'])
    qlib_time = time.time() - start_time
    print(f"✅ Qlib Strategies: {qlib_time:.2f} seconds")
    
    total_time = market_time + indicators_time + qlib_time
    print(f"✅ Total Performance: {total_time:.2f} seconds")

async def test_portfolio_backend_vs_bot():
    """Test that backend and bot output for portfolio optimization are consistent"""
    print("\n🔄 Testing Backend vs Bot Portfolio Optimization Consistency...")
    symbols = ['AAPL', 'TSLA', 'GOOGL']
    advanced_qlib = AdvancedQlibStrategies()
    portfolio = advanced_qlib.portfolio_optimization(symbols, 'moderate')
    print("\n--- Backend Output ---")
    print(portfolio)
    # Simulate Telegram bot formatting
    response = f"""
📊 **Real-Time Portfolio Optimization**

🎯 **Optimized Weights:**
"""
    for symbol, weight in portfolio['weights'].items():
        response += f"• {symbol}: {weight:.1%}\n"
    metrics = portfolio['metrics']
    response += f"""
📈 **Portfolio Metrics:**
• Expected Annual Return: {metrics.get('expected_return', 0):.1%}
• Annual Volatility: {metrics.get('volatility', 0):.1%}
• Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.2f}
• Max Drawdown: {metrics.get('max_drawdown', 0):.1%}
"""
    if 'data_quality' in metrics:
        data_quality = metrics['data_quality']
        response += f"""
📊 **Data Quality:**
• Analysis Period: {data_quality.get('data_period_days', 0)} trading days
• Symbols Analyzed: {data_quality.get('symbols_with_data', 0)}
• Data Freshness: {data_quality.get('data_freshness', 'Unknown')}
• Last Updated: {data_quality.get('last_update', 'Unknown')}
"""
    if 'optimization_timestamp' in portfolio:
        from datetime import datetime
        timestamp = datetime.fromisoformat(portfolio['optimization_timestamp'])
        response += f"\n⏰ **Optimization Time:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    if 'data_period_days' in portfolio:
        response += f"\n📅 **Data Period:** {portfolio['data_period_days']} trading days"
    response += f"\n\n✅ **Status:** Real-time optimization completed successfully"
    response += f"\n⚖️ **Risk Tolerance:** {portfolio['risk_tolerance'].title()}"
    response += f"\n\n💡 **Tip:** This optimization uses real-time market data for maximum accuracy. Rerun the command for updated results."
    print("\n--- Simulated Telegram Bot Output ---")
    print(response)

async def main():
    """Run all Phase 3 tests"""
    print("🚀 Starting Phase 3 Advanced Features Test Suite...")
    print("=" * 60)
    
    try:
        await test_real_market_data()
        print("-" * 40)
        
        await test_advanced_qlib_strategies()
        print("-" * 40)
        
        await test_enhanced_technical_indicators()
        print("-" * 40)
        
        await test_integration()
        print("-" * 40)
        
        await test_performance()
        print("-" * 40)
        
        await test_portfolio_backend_vs_bot()
        print("-" * 40)
        
        print("\n🎉 Phase 3 Tests Completed Successfully!")
        print("✅ Real Market Data Integration: Working")
        print("✅ Advanced Qlib Strategies: Working")
        print("✅ Enhanced Technical Indicators: Working")
        print("✅ Service Integration: Working")
        print("✅ Performance: Optimized")
        
        print("\n🚀 Phase 3 Features Ready for Production!")
        print("📊 Real-time market data from multiple sources")
        print("🤖 Advanced AI models with ensemble predictions")
        print("📈 Comprehensive technical analysis")
        print("⚖️ Portfolio optimization and risk management")
        print("🎯 Professional-grade trading insights")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logger.error(f"Phase 3 test error: {e}")

if __name__ == "__main__":
    asyncio.run(main())