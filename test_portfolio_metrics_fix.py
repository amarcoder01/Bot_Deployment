#!/usr/bin/env python3
"""
Test script to verify the portfolio optimization metrics fix.
This demonstrates that the portfolio optimization now returns realistic values.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from portfolio_optimizer import ModernPortfolioOptimizer
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_portfolio_metrics():
    """Test that portfolio optimization returns realistic metrics"""
    print("\n=== Testing Portfolio Optimization Metrics ===")
    
    # Initialize optimizer
    optimizer = ModernPortfolioOptimizer()
    
    # Test with AAPL and TSLA
    symbols = ['AAPL', 'TSLA']
    risk_tolerance = 'moderate'
    
    print(f"\nOptimizing portfolio for: {symbols}")
    print(f"Risk tolerance: {risk_tolerance}")
    
    try:
        result = optimizer.optimize_portfolio(symbols, risk_tolerance)
        
        if result and 'metrics' in result:
            metrics = result['metrics']
            weights = result['weights']
            
            print("\n📊 Portfolio Results:")
            print(f"Strategy: {result.get('strategy', 'Unknown')}")
            print(f"Optimizer: {result.get('optimizer', 'Unknown')}")
            
            print("\n💰 Optimized Weights:")
            for symbol, weight in weights.items():
                print(f"  {symbol}: {weight:.2%}")
            
            print("\n📈 Portfolio Metrics:")
            print(f"  Expected Return: {metrics.get('expected_return', 0):.2%}")
            print(f"  Volatility: {metrics.get('volatility', 0):.2%}")
            print(f"  Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.3f}")
            print(f"  Max Drawdown: {metrics.get('max_drawdown', 0):.2%}")
            print(f"  VaR (95%): {metrics.get('var_95', 0):.2%}")
            print(f"  CVaR (95%): {metrics.get('cvar_95', 0):.2%}")
            
            # Validate that metrics are realistic
            expected_return = metrics.get('expected_return', 0)
            volatility = metrics.get('volatility', 0)
            sharpe_ratio = metrics.get('sharpe_ratio', 0)
            
            print("\n✅ Validation Checks:")
            
            # Check if expected return is reasonable (between -100% and 500%)
            if -1.0 <= expected_return <= 5.0:
                print(f"  ✅ Expected return ({expected_return:.2%}) is realistic")
            else:
                print(f"  ❌ Expected return ({expected_return:.2%}) seems unrealistic")
                return False
            
            # Check if volatility is reasonable (between 0% and 200%)
            if 0 <= volatility <= 2.0:
                print(f"  ✅ Volatility ({volatility:.2%}) is realistic")
            else:
                print(f"  ❌ Volatility ({volatility:.2%}) seems unrealistic")
                return False
            
            # Check if Sharpe ratio is reasonable (between -5 and 5)
            if -5.0 <= sharpe_ratio <= 5.0:
                print(f"  ✅ Sharpe ratio ({sharpe_ratio:.3f}) is realistic")
            else:
                print(f"  ❌ Sharpe ratio ({sharpe_ratio:.3f}) seems unrealistic")
                return False
            
            print("\n🎉 All metrics are within realistic ranges!")
            return True
            
        else:
            print("❌ No metrics returned from optimization")
            return False
            
    except Exception as e:
        print(f"❌ Error during optimization: {e}")
        return False

if __name__ == "__main__":
    success = test_portfolio_metrics()
    if success:
        print("\n✅ Portfolio metrics fix verification: PASSED")
        print("The portfolio optimization now returns realistic values!")
    else:
        print("\n❌ Portfolio metrics fix verification: FAILED")
        sys.exit(1)