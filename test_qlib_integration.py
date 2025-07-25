import unittest
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import warnings
warnings.filterwarnings('ignore')

try:
    import qlib
    from qlib.constant import REG_US
    QLIB_AVAILABLE = True
except ImportError:
    QLIB_AVAILABLE = False

from qlib_ai_portfolio_pipeline import print_section, ensure_dir
from advanced_qlib_strategies import AdvancedQlibStrategies
from logger import logger

class TestQlibIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qlib_data_dir = os.path.join(os.getcwd(), 'qlib_data', 'us_data')
        cls.results_dir = 'test_results'
        ensure_dir(cls.results_dir)
        cls.test_symbols = ['AAPL', 'MSFT', 'GOOGL']
        cls.start_date = '2020-01-01'
        cls.end_date = datetime.now().strftime('%Y-%m-%d')
        
        if QLIB_AVAILABLE:
            try:
                qlib.init(provider_uri=cls.qlib_data_dir, region=REG_US)
                logger.info('Qlib initialized successfully for testing')
            except Exception as e:
                logger.error(f'Failed to initialize Qlib for testing: {e}')
                raise
    
    def setUp(self):
        self.strategies = AdvancedQlibStrategies()
        
    def test_data_availability(self):
        """Test if Qlib data is available and fresh"""
        print_section('Testing Data Availability')
        
        # Check if data directory exists
        self.assertTrue(os.path.exists(self.qlib_data_dir), 
                       f'Qlib data directory not found: {self.qlib_data_dir}')
        
        # Check instruments file
        instruments_file = os.path.join(self.qlib_data_dir, 'instruments', 'all.txt')
        self.assertTrue(os.path.exists(instruments_file), 
                       f'Instruments file not found: {instruments_file}')
        
        # Read and validate instruments
        with open(instruments_file, 'r') as f:
            instruments = [line.strip().split('	')[0] for line in f if line.strip() and not line.startswith('#')]
        
        self.assertGreater(len(instruments), 0, 'No instruments found in data')
        logger.info(f'Found {len(instruments)} instruments in Qlib data')
        
        # Check if test symbols are available
        available_symbols = set(instruments)
        for symbol in self.test_symbols:
            self.assertIn(symbol, available_symbols, f'Test symbol {symbol} not found in data')
    
    def test_data_freshness(self):
        """Test if Qlib data is up to date"""
        print_section('Testing Data Freshness')
        
        if not QLIB_AVAILABLE:
            self.skipTest('Qlib not available')
        
        from qlib.data import D
        
        # Check last update time for each test symbol
        for symbol in self.test_symbols:
            try:
                # Get latest data point
                df = D.features(
                    instruments=[symbol],
                    fields=['$close'],
                    start_time=self.start_date,
                    end_time=self.end_date,
                    freq='day'
                )
                
                if df.empty:
                    self.fail(f'No data found for {symbol}')
                
                latest_date = df.index.get_level_values('datetime')[-1]
                days_old = (pd.Timestamp.now() - latest_date).days
                
                # Data should not be more than 5 business days old
                self.assertLess(days_old, 5, 
                              f'Data for {symbol} is {days_old} days old')
                
                logger.info(f'Latest data for {symbol} is from {latest_date}')
                
            except Exception as e:
                self.fail(f'Error checking data freshness for {symbol}: {e}')
    
    def test_feature_quality(self):
        """Test quality of Qlib features"""
        print_section('Testing Feature Quality')
        
        if not QLIB_AVAILABLE:
            self.skipTest('Qlib not available')
            
        from qlib.data import D
        
        # Core features to check
        features = [
            '$close', '$volume', 
            '$high', '$low', '$open',
            '$vwap'
        ]
        
        for symbol in self.test_symbols:
            try:
                # Fetch feature data
                df = D.features(
                    instruments=[symbol],
                    fields=features,
                    start_time=self.start_date,
                    end_time=self.end_date,
                    freq='day'
                )
                
                self.assertFalse(df.empty, f'No feature data found for {symbol}')
                
                # Check for NaN values
                nan_pct = df.isna().mean() * 100
                for feature, pct in nan_pct.items():
                    self.assertLess(pct, 5, 
                                  f'{feature} has {pct:.2f}% NaN values for {symbol}')
                
                # Check for zero values in volume
                volume_zeros = (df['$volume'] == 0).mean() * 100
                self.assertLess(volume_zeros, 1, 
                              f'{symbol} has {volume_zeros:.2f}% zero volume days')
                
                # Check price consistency
                self.assertTrue((df['$high'] >= df['$low']).all(), 
                              f'High < Low found in {symbol} data')
                self.assertTrue((df['$high'] >= df['$close']).all(), 
                              f'High < Close found in {symbol} data')
                self.assertTrue((df['$close'] >= df['$low']).all(), 
                              f'Close < Low found in {symbol} data')
                
                logger.info(f'All feature quality checks passed for {symbol}')
                
            except Exception as e:
                self.fail(f'Error checking feature quality for {symbol}: {e}')
                
    def test_portfolio_optimization(self):
        """Test portfolio optimization with data validation"""
        print_section('Testing Portfolio Optimization')
        
        # Test different risk tolerances
        risk_levels = ['conservative', 'moderate', 'aggressive']
        
        for risk_tolerance in risk_levels:
            try:
                logger.info(f'Testing {risk_tolerance} portfolio optimization')
                
                # Get portfolio optimization results
                result = self.strategies.portfolio_optimization(
                    symbols=self.test_symbols,
                    risk_tolerance=risk_tolerance
                )
                
                # Basic validation
                self.assertIsInstance(result, dict)
                self.assertIn('weights', result)
                self.assertIn('metrics', result)
                
                weights = result['weights']
                metrics = result['metrics']
                
                # Validate weights
                self.assertEqual(len(weights), len(self.test_symbols))
                self.assertAlmostEqual(sum(weights.values()), 1.0, places=2)
                for weight in weights.values():
                    self.assertGreaterEqual(weight, 0)
                    self.assertLessEqual(weight, 1)
                
                # Validate metrics
                self.assertIn('expected_return', metrics)
                self.assertIn('volatility', metrics)
                self.assertIn('sharpe_ratio', metrics)
                
                # Check metric values are reasonable
                self.assertGreater(metrics['expected_return'], -1)
                self.assertLess(metrics['expected_return'], 2)
                self.assertGreater(metrics['volatility'], 0)
                self.assertLess(metrics['volatility'], 1)
                
                logger.info(f'Portfolio optimization passed for {risk_tolerance} strategy')
                logger.info(f'Weights: {weights}')
                logger.info(f'Metrics: {metrics}')
                
            except Exception as e:
                self.fail(f'Portfolio optimization failed for {risk_tolerance}: {e}')
                
    def test_data_analysis_pipeline(self):
        """Test the complete data analysis pipeline"""
        print_section('Testing Data Analysis Pipeline')
        
        try:
            # 1. Test data fetching
            price_data = self.strategies._fetch_price_data(self.test_symbols)
            self.assertFalse(price_data.empty)
            self.assertEqual(len(price_data.columns), len(self.test_symbols))
            
            # 2. Test returns calculation
            returns = price_data.pct_change().dropna()
            self.assertFalse(returns.empty)
            
            # 3. Test covariance calculation
            from pypfopt import risk_models
            cov_matrix = risk_models.sample_cov(returns)
            self.assertEqual(cov_matrix.shape, (len(self.test_symbols), len(self.test_symbols)))
            
            # 4. Test expected returns calculation
            from pypfopt import expected_returns
            mu = expected_returns.mean_historical_return(price_data)
            self.assertEqual(len(mu), len(self.test_symbols))
            
            # 5. Test optimization constraints
            from pypfopt import EfficientFrontier
            ef = EfficientFrontier(mu, cov_matrix)
            weights = ef.min_volatility()
            cleaned_weights = ef.clean_weights()
            
            self.assertEqual(len(cleaned_weights), len(self.test_symbols))
            self.assertAlmostEqual(sum(cleaned_weights.values()), 1.0, places=2)
            
            logger.info('Complete data analysis pipeline test passed')
            logger.info(f'Final portfolio weights: {cleaned_weights}')
            
        except Exception as e:
            self.fail(f'Data analysis pipeline failed: {e}')

if __name__ == '__main__':
    unittest.main()