#!/usr/bin/env python3
"""Comprehensive test to verify portfolio optimization fixes"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
from unittest.mock import AsyncMock, MagicMock
from telegram_handler import TelegramHandler
from portfolio_optimizer import ModernPortfolioOptimizer
from advanced_qlib_strategies import AdvancedQlibStrategies
from logger import logger
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def test_modern_portfolio_optimizer():
    """Test ModernPortfolioOptimizer directly"""
    print("\n=== Testing ModernPortfolioOptimizer ===")
    
    optimizer = ModernPortfolioOptimizer()
    symbols = ['AAPL', 'MSFT', 'GOOGL']
    
    result = optimizer.optimize_portfolio(symbols, risk_tolerance='moderate')
    
    print(f"Strategy: {result.get('strategy', 'Unknown')}")
    print(f"Optimizer: {result.get('optimizer', 'Unknown')}")
    print(f"Weights: {result.get('weights', {})}")
    print(f"Expected Return: {result.get('metrics', {}).get('expected_return', 0):.4f}")
    print(f"Volatility: {result.get('metrics', {}).get('volatility', 0):.4f}")
    print(f"Sharpe Ratio: {result.get('metrics', {}).get('sharpe_ratio', 0):.4f}")
    print(f"Data Period: {result.get('data_period_days', 0)} days")
    
    if 'warning' in result:
        print(f"⚠️ Warning: {result['warning']}")
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
    
    return result

def test_advanced_qlib_strategies():
    """Test AdvancedQlibStrategies portfolio optimization"""
    print("\n=== Testing AdvancedQlibStrategies ===")
    
    strategies = AdvancedQlibStrategies()
    symbols = ['AAPL', 'MSFT']
    
    result = strategies.portfolio_optimization(symbols, risk_tolerance='moderate')
    
    print(f"Strategy: {result.get('strategy', 'Unknown')}")
    print(f"Optimizer: {result.get('optimizer', 'Unknown')}")
    print(f"Weights: {result.get('weights', {})}")
    print(f"Expected Return: {result.get('metrics', {}).get('expected_return', 0):.4f}")
    print(f"Volatility: {result.get('metrics', {}).get('volatility', 0):.4f}")
    print(f"Sharpe Ratio: {result.get('metrics', {}).get('sharpe_ratio', 0):.4f}")
    print(f"Data Period: {result.get('data_period_days', 0)} days")
    
    if 'warning' in result:
        print(f"⚠️ Warning: {result['warning']}")
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
    
    return result

def test_solver_robustness():
    """Test CVXPY solver robustness with different scenarios"""
    print("\n=== Testing Solver Robustness ===")
    
    optimizer = ModernPortfolioOptimizer()
    
    # Test different symbol combinations
    test_cases = [
        (['AAPL', 'MSFT'], 'Two tech stocks'),
        (['AAPL', 'TSLA', 'GOOGL'], 'Three growth stocks'),
        (['AAPL', 'JNJ', 'PG'], 'Mixed sectors'),
    ]
    
    for symbols, description in test_cases:
        print(f"\nTesting: {description} - {symbols}")
        try:
            result = optimizer.optimize_portfolio(symbols, risk_tolerance='moderate')
            optimizer_used = result.get('optimizer', 'unknown')
            strategy = result.get('strategy', 'unknown')
            print(f"  Result: {optimizer_used} - {strategy}")
            
            if optimizer_used in ['cvxpy', 'riskfolio']:
                print("  ✅ Advanced optimization successful")
            else:
                print("  ⚠️ Fallback optimization used")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:100]}...")

def test_library_availability():
    """Test if required libraries are available"""
    print("\n=== Testing Library Availability ===")
    
    try:
        import riskfolio as rp
        print("✅ Riskfolio-Lib available")
    except ImportError:
        print("❌ Riskfolio-Lib NOT available")
    
    try:
        import cvxpy as cp
        print("✅ CVXPY available")
        print(f"Available solvers: {cp.installed_solvers()}")
    except ImportError:
        print("❌ CVXPY NOT available")
    
    try:
        import yfinance as yf
        print("✅ yfinance available")
    except ImportError:
        print("❌ yfinance NOT available")

def main():
    """Run all tests"""
    print("Portfolio Optimization Fixes - Comprehensive Test")
    print("=" * 50)
    
    # Test library availability
    test_library_availability()
    
    # Test ModernPortfolioOptimizer
    modern_result = test_modern_portfolio_optimizer()
    
    # Test AdvancedQlibStrategies
    qlib_result = test_advanced_qlib_strategies()
    
    # Test solver robustness
    test_solver_robustness()
    
    # Summary
    print("\n=== Test Summary ===")
    
    modern_success = modern_result.get('optimizer') not in ['fallback', 'error_fallback']
    qlib_success = qlib_result.get('optimizer') not in ['fallback', 'error_fallback']
    
    print(f"ModernPortfolioOptimizer: {'✅ PASS' if modern_success else '⚠️ FALLBACK'}")
    print(f"AdvancedQlibStrategies: {'✅ PASS' if qlib_success else '⚠️ FALLBACK'}")
    
    if modern_success and qlib_success:
        print("\n🎉 All tests passed! Portfolio optimization is working correctly.")
    elif modern_success or qlib_success:
        print("\n⚠️ Partial success. Some optimizers are working.")
    else:
        print("\n❌ Tests failed. Portfolio optimization needs more work.")

if __name__ == '__main__':
    main()