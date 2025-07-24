#!/usr/bin/env python3
"""Test script to check data fetching issues in portfolio optimization"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from advanced_qlib_strategies import AdvancedQlibStrategies
from portfolio_optimizer import ModernPortfolioOptimizer
from logger import logger
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def test_data_fetching():
    """Test data fetching capabilities"""
    print("\n" + "="*60)
    print("TESTING DATA FETCHING FOR PORTFOLIO OPTIMIZATION")
    print("="*60)
    
    symbols = ['AAPL', 'TSLA']
    
    # Test 1: Advanced Qlib Strategies data fetching
    print("\n1. Testing AdvancedQlibStrategies data fetching...")
    try:
        strategies = AdvancedQlibStrategies()
        price_data = strategies._fetch_price_data(symbols)
        print(f"   Data shape: {price_data.shape}")
        print(f"   Columns: {list(price_data.columns)}")
        print(f"   Date range: {price_data.index.min()} to {price_data.index.max()}")
        print(f"   Missing values: {price_data.isnull().sum().sum()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: ModernPortfolioOptimizer data fetching
    print("\n2. Testing ModernPortfolioOptimizer data fetching...")
    try:
        optimizer = ModernPortfolioOptimizer()
        price_data = optimizer._fetch_price_data(symbols, 252)
        print(f"   Data shape: {price_data.shape}")
        print(f"   Columns: {list(price_data.columns)}")
        print(f"   Date range: {price_data.index.min()} to {price_data.index.max()}")
        print(f"   Missing values: {price_data.isnull().sum().sum()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Check library availability
    print("\n3. Testing library availability...")
    try:
        import riskfolio as rp
        print("   ✅ Riskfolio-Lib available")
    except ImportError:
        print("   ❌ Riskfolio-Lib NOT available")
    
    try:
        import cvxpy as cp
        print("   ✅ CVXPY available")
    except ImportError:
        print("   ❌ CVXPY NOT available")
    
    # Test 4: Direct portfolio optimization
    print("\n4. Testing direct portfolio optimization...")
    try:
        optimizer = ModernPortfolioOptimizer()
        result = optimizer.optimize_portfolio(symbols, 'moderate')
        print(f"   Strategy: {result.get('strategy', 'Unknown')}")
        print(f"   Optimizer: {result.get('optimizer', 'Unknown')}")
        print(f"   Weights: {result.get('weights', {})}")
        if 'warning' in result:
            print(f"   ⚠️ Warning: {result['warning']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_data_fetching()