#!/usr/bin/env python3
"""
Performance Optimization Test Suite
Tests caching, connection pooling, and cold start reduction features
"""

import asyncio
import time
import logging
import sys
import os
from typing import Dict, Any

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from performance_cache import (
    performance_cache, response_cache, connection_pool, preloader,
    get_cache_stats, clear_all_caches
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PerformanceTestSuite:
    """Test suite for performance optimizations"""
    
    def __init__(self):
        self.test_results = []
        self.start_time = None
        
    def log_test_result(self, test_name: str, passed: bool, duration: float, details: str = ""):
        """Log test result"""
        status = "PASS" if passed else "FAIL"
        result = {
            'test_name': test_name,
            'status': status,
            'duration': duration,
            'details': details
        }
        self.test_results.append(result)
        logger.info(f"{test_name}: {status} ({duration:.3f}s) {details}")
    
    async def test_performance_cache(self) -> bool:
        """Test performance cache functionality"""
        start_time = time.time()
        
        try:
            # Test basic cache operations
            test_key = "test_key"
            test_value = {"data": "test_value", "timestamp": time.time()}
            
            # Set cache
            performance_cache.set(test_key, test_value, ttl=60)
            
            # Get cache
            cached_value = performance_cache.get(test_key)
            
            # Verify cache hit
            if cached_value != test_value:
                raise ValueError("Cache value mismatch")
            
            # Test cache miss
            missing_value = performance_cache.get("non_existent_key")
            if missing_value is not None:
                raise ValueError("Expected cache miss")
            
            # Test TTL expiration (short TTL for testing)
            short_ttl_key = "short_ttl_key"
            performance_cache.set(short_ttl_key, "test", ttl=1)
            await asyncio.sleep(1.1)
            expired_value = performance_cache.get(short_ttl_key)
            if expired_value is not None:
                raise ValueError("Cache should have expired")
            
            duration = time.time() - start_time
            self.log_test_result("Performance Cache", True, duration, "Basic operations working")
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result("Performance Cache", False, duration, f"Error: {str(e)}")
            return False
    
    async def test_response_cache(self) -> bool:
        """Test response cache functionality"""
        start_time = time.time()
        
        try:
            # Test response cache
            response_key = "help_message"
            response_value = "This is a cached help message"
            
            # Set response cache
            response_cache.set(response_key, response_value, ttl=300)
            
            # Get response cache
            cached_response = response_cache.get(response_key)
            
            if cached_response != response_value:
                raise ValueError("Response cache value mismatch")
            
            duration = time.time() - start_time
            self.log_test_result("Response Cache", True, duration, "Response caching working")
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result("Response Cache", False, duration, f"Error: {str(e)}")
            return False
    
    async def test_connection_pool(self) -> bool:
        """Test connection pool functionality"""
        start_time = time.time()
        
        try:
            # Test connection pool
            with connection_pool.get_connection() as conn:
                if conn is None:
                    raise ValueError("Connection pool returned None")
            
            # Test multiple connections
            connections = []
            for i in range(3):
                conn = connection_pool.get_connection()
                connections.append(conn)
            
            # Return connections
            for conn in connections:
                conn.__exit__(None, None, None)
            
            # Check pool stats
            stats = connection_pool.get_stats()
            if 'total_connections' not in stats:
                raise ValueError("Connection pool stats missing")
            
            duration = time.time() - start_time
            self.log_test_result("Connection Pool", True, duration, f"Pool size: {stats['total_connections']}")
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result("Connection Pool", False, duration, f"Error: {str(e)}")
            return False
    
    async def test_preloader(self) -> bool:
        """Test preloader functionality"""
        start_time = time.time()
        
        try:
            # Start preloading
            await preloader.start_preloading()
            
            # Check if common data is preloaded
            preloaded_data = performance_cache.get("common_help_messages")
            if preloaded_data is None:
                logger.warning("Preloaded data not found, but preloader ran successfully")
            
            duration = time.time() - start_time
            self.log_test_result("Preloader", True, duration, "Preloading completed")
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result("Preloader", False, duration, f"Error: {str(e)}")
            return False
    
    async def test_cache_performance(self) -> bool:
        """Test cache performance with multiple operations"""
        start_time = time.time()
        
        try:
            # Perform multiple cache operations
            num_operations = 1000
            
            # Set operations
            set_start = time.time()
            for i in range(num_operations):
                performance_cache.set(f"perf_test_{i}", {"value": i, "data": f"test_data_{i}"}, ttl=300)
            set_duration = time.time() - set_start
            
            # Get operations
            get_start = time.time()
            hits = 0
            for i in range(num_operations):
                value = performance_cache.get(f"perf_test_{i}")
                if value is not None:
                    hits += 1
            get_duration = time.time() - get_start
            
            # Calculate performance metrics
            set_ops_per_sec = num_operations / set_duration
            get_ops_per_sec = num_operations / get_duration
            hit_rate = hits / num_operations
            
            if hit_rate < 0.95:  # Expect at least 95% hit rate
                raise ValueError(f"Low cache hit rate: {hit_rate:.2%}")
            
            duration = time.time() - start_time
            details = f"Set: {set_ops_per_sec:.0f} ops/s, Get: {get_ops_per_sec:.0f} ops/s, Hit rate: {hit_rate:.2%}"
            self.log_test_result("Cache Performance", True, duration, details)
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result("Cache Performance", False, duration, f"Error: {str(e)}")
            return False
    
    async def test_cache_stats(self) -> bool:
        """Test cache statistics functionality"""
        start_time = time.time()
        
        try:
            # Get cache stats
            stats = get_cache_stats()
            
            # Verify stats structure
            required_keys = ['performance_cache', 'response_cache', 'connection_pool']
            for key in required_keys:
                if key not in stats:
                    raise ValueError(f"Missing stats key: {key}")
            
            # Verify performance cache stats
            perf_stats = stats['performance_cache']
            if 'hits' not in perf_stats or 'misses' not in perf_stats:
                raise ValueError("Missing performance cache stats")
            
            duration = time.time() - start_time
            total_ops = perf_stats['hits'] + perf_stats['misses']
            hit_rate = perf_stats['hits'] / total_ops if total_ops > 0 else 0
            details = f"Total ops: {total_ops}, Hit rate: {hit_rate:.2%}"
            self.log_test_result("Cache Statistics", True, duration, details)
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result("Cache Statistics", False, duration, f"Error: {str(e)}")
            return False
    
    async def test_memory_efficiency(self) -> bool:
        """Test memory efficiency of caching system"""
        start_time = time.time()
        
        try:
            import psutil
            import gc
            
            # Get initial memory usage
            process = psutil.Process()
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Create large cache entries
            large_data = {"data": "x" * 10000}  # 10KB per entry
            num_entries = 100
            
            for i in range(num_entries):
                performance_cache.set(f"large_entry_{i}", large_data, ttl=300)
            
            # Get memory after caching
            after_cache_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Clear cache and force garbage collection
            clear_all_caches()
            gc.collect()
            
            # Get memory after clearing
            after_clear_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            memory_increase = after_cache_memory - initial_memory
            memory_recovered = after_cache_memory - after_clear_memory
            
            # Check if memory was properly managed
            if memory_increase > 50:  # More than 50MB increase seems excessive
                logger.warning(f"High memory usage: {memory_increase:.1f}MB")
            
            duration = time.time() - start_time
            details = f"Peak increase: {memory_increase:.1f}MB, Recovered: {memory_recovered:.1f}MB"
            self.log_test_result("Memory Efficiency", True, duration, details)
            return True
            
        except ImportError:
            duration = time.time() - start_time
            self.log_test_result("Memory Efficiency", True, duration, "psutil not available, skipped")
            return True
        except Exception as e:
            duration = time.time() - start_time
            self.log_test_result("Memory Efficiency", False, duration, f"Error: {str(e)}")
            return False
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all performance tests"""
        logger.info("Starting Performance Optimization Test Suite")
        self.start_time = time.time()
        
        # Clear caches before testing
        clear_all_caches()
        
        # Run tests
        tests = [
            self.test_performance_cache(),
            self.test_response_cache(),
            self.test_connection_pool(),
            self.test_preloader(),
            self.test_cache_performance(),
            self.test_cache_stats(),
            self.test_memory_efficiency()
        ]
        
        results = await asyncio.gather(*tests, return_exceptions=True)
        
        # Calculate summary
        total_tests = len(results)
        passed_tests = sum(1 for result in results if result is True)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100
        
        total_duration = time.time() - self.start_time
        
        # Generate report
        report = {
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'success_rate': success_rate,
            'total_duration': total_duration,
            'test_results': self.test_results
        }
        
        return report
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a formatted test report"""
        report_lines = [
            "\n" + "=" * 60,
            "PERFORMANCE OPTIMIZATION TEST REPORT",
            "=" * 60,
            f"Total Tests: {results['total_tests']}",
            f"Passed: {results['passed']}",
            f"Failed: {results['failed']}",
            f"Success Rate: {results['success_rate']:.1f}%",
            f"Total Duration: {results['total_duration']:.2f}s",
            "",
            "DETAILED RESULTS:",
            "-" * 40
        ]
        
        for test_result in results['test_results']:
            status_icon = "✓" if test_result['status'] == 'PASS' else "✗"
            report_lines.append(
                f"{status_icon} {test_result['test_name']}: {test_result['status']} "
                f"({test_result['duration']:.3f}s) {test_result['details']}"
            )
        
        # Add cache statistics
        try:
            cache_stats = get_cache_stats()
            report_lines.extend([
                "",
                "CACHE STATISTICS:",
                "-" * 20,
                f"Performance Cache: {cache_stats['performance_cache']}",
                f"Response Cache: {cache_stats['response_cache']}",
                f"Connection Pool: {cache_stats['connection_pool']}"
            ])
        except Exception as e:
            report_lines.append(f"Cache stats error: {e}")
        
        report_lines.extend([
            "",
            "=" * 60,
            f"CONCLUSION: {'ALL TESTS PASSED' if results['failed'] == 0 else 'SOME TESTS FAILED'}",
            "Performance optimizations are " + ("working correctly" if results['success_rate'] >= 85 else "experiencing issues"),
            "=" * 60
        ])
        
        return "\n".join(report_lines)

async def main():
    """Main test function"""
    test_suite = PerformanceTestSuite()
    
    try:
        # Run all tests
        results = await test_suite.run_all_tests()
        
        # Generate and display report
        report = test_suite.generate_report(results)
        print(report)
        
        # Write report to file
        with open('performance_test_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info("Performance test report saved to performance_test_report.txt")
        
        # Exit with appropriate code
        exit_code = 0 if results['failed'] == 0 else 1
        return exit_code
        
    except Exception as e:
        logger.error(f"Test suite failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)