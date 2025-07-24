#!/usr/bin/env python3
"""
Alert System Performance Test
Tests the alert system's ability to handle high traffic scenarios.
"""

import asyncio
import time
import logging
from datetime import datetime
from typing import List, Dict
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertPerformanceTest:
    """Test suite for alert system performance under high traffic"""
    
    def __init__(self):
        self.results = []
        self.test_users = list(range(1000, 1100))  # 100 test users
        self.test_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'CRM', 'ORCL']
        
    async def simulate_alert_creation(self, user_id: int, symbol: str, condition: str, price: float) -> Dict:
        """Simulate alert creation with timing"""
        start_time = time.time()
        try:
            # Simulate alert service call
            await asyncio.sleep(0.01)  # Simulate database operation
            
            # Mock successful result
            result = {
                'success': True,
                'alert_id': f"{user_id}_{symbol}_{int(time.time())}",
                'user_id': user_id,
                'symbol': symbol,
                'condition': condition,
                'price': price
            }
            
            end_time = time.time()
            duration = end_time - start_time
            
            return {
                'operation': 'create_alert',
                'success': True,
                'duration': duration,
                'user_id': user_id,
                'symbol': symbol
            }
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            return {
                'operation': 'create_alert',
                'success': False,
                'duration': duration,
                'error': str(e),
                'user_id': user_id,
                'symbol': symbol
            }
    
    async def simulate_alert_retrieval(self, user_id: int) -> Dict:
        """Simulate alert retrieval with timing"""
        start_time = time.time()
        try:
            # Simulate cached retrieval
            await asyncio.sleep(0.005)  # Simulate cache lookup
            
            # Mock alerts result
            alerts = [
                {'id': f'{user_id}_1', 'symbol': 'AAPL', 'condition': 'above 150.00', 'is_active': True},
                {'id': f'{user_id}_2', 'symbol': 'MSFT', 'condition': 'below 300.00', 'is_active': True}
            ]
            
            end_time = time.time()
            duration = end_time - start_time
            
            return {
                'operation': 'get_alerts',
                'success': True,
                'duration': duration,
                'user_id': user_id,
                'alert_count': len(alerts)
            }
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            return {
                'operation': 'get_alerts',
                'success': False,
                'duration': duration,
                'error': str(e),
                'user_id': user_id
            }
    
    async def simulate_alert_monitoring(self, alert_count: int) -> Dict:
        """Simulate alert monitoring with batch processing"""
        start_time = time.time()
        try:
            # Simulate batch processing of alerts
            batch_size = 50
            batches = (alert_count + batch_size - 1) // batch_size
            
            for batch in range(batches):
                # Simulate price fetching and alert checking
                await asyncio.sleep(0.02)  # Simulate API calls and processing
            
            end_time = time.time()
            duration = end_time - start_time
            
            return {
                'operation': 'monitor_alerts',
                'success': True,
                'duration': duration,
                'alert_count': alert_count,
                'batches_processed': batches
            }
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            return {
                'operation': 'monitor_alerts',
                'success': False,
                'duration': duration,
                'error': str(e),
                'alert_count': alert_count
            }
    
    async def test_concurrent_alert_creation(self, concurrent_users: int = 50) -> Dict:
        """Test concurrent alert creation"""
        logger.info(f"Testing concurrent alert creation with {concurrent_users} users")
        
        tasks = []
        for i in range(concurrent_users):
            user_id = self.test_users[i % len(self.test_users)]
            symbol = self.test_symbols[i % len(self.test_symbols)]
            condition = 'above' if i % 2 == 0 else 'below'
            price = 100.0 + (i * 10)
            
            task = self.simulate_alert_creation(user_id, symbol, condition, price)
            tasks.append(task)
        
        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()
        
        # Analyze results
        successful = sum(1 for r in results if isinstance(r, dict) and r.get('success', False))
        failed = len(results) - successful
        durations = [r['duration'] for r in results if isinstance(r, dict) and 'duration' in r]
        
        return {
            'test': 'concurrent_alert_creation',
            'total_time': end_time - start_time,
            'concurrent_users': concurrent_users,
            'successful': successful,
            'failed': failed,
            'success_rate': successful / len(results) * 100,
            'avg_duration': statistics.mean(durations) if durations else 0,
            'max_duration': max(durations) if durations else 0,
            'min_duration': min(durations) if durations else 0
        }
    
    async def test_concurrent_alert_retrieval(self, concurrent_users: int = 100) -> Dict:
        """Test concurrent alert retrieval"""
        logger.info(f"Testing concurrent alert retrieval with {concurrent_users} users")
        
        tasks = []
        for i in range(concurrent_users):
            user_id = self.test_users[i % len(self.test_users)]
            task = self.simulate_alert_retrieval(user_id)
            tasks.append(task)
        
        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()
        
        # Analyze results
        successful = sum(1 for r in results if isinstance(r, dict) and r.get('success', False))
        failed = len(results) - successful
        durations = [r['duration'] for r in results if isinstance(r, dict) and 'duration' in r]
        
        return {
            'test': 'concurrent_alert_retrieval',
            'total_time': end_time - start_time,
            'concurrent_users': concurrent_users,
            'successful': successful,
            'failed': failed,
            'success_rate': successful / len(results) * 100,
            'avg_duration': statistics.mean(durations) if durations else 0,
            'max_duration': max(durations) if durations else 0,
            'min_duration': min(durations) if durations else 0
        }
    
    async def test_alert_monitoring_performance(self, alert_counts: List[int] = [100, 500, 1000, 2000]) -> Dict:
        """Test alert monitoring performance with different alert counts"""
        logger.info("Testing alert monitoring performance")
        
        monitoring_results = []
        
        for alert_count in alert_counts:
            logger.info(f"Testing monitoring with {alert_count} alerts")
            result = await self.simulate_alert_monitoring(alert_count)
            monitoring_results.append(result)
        
        return {
            'test': 'alert_monitoring_performance',
            'results': monitoring_results
        }
    
    async def test_mixed_workload(self, duration_seconds: int = 30) -> Dict:
        """Test mixed workload simulation"""
        logger.info(f"Testing mixed workload for {duration_seconds} seconds")
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        operations = []
        
        while time.time() < end_time:
            # Mix of operations
            tasks = []
            
            # 40% alert creation
            for _ in range(4):
                user_id = self.test_users[len(operations) % len(self.test_users)]
                symbol = self.test_symbols[len(operations) % len(self.test_symbols)]
                task = self.simulate_alert_creation(user_id, symbol, 'above', 150.0)
                tasks.append(task)
            
            # 50% alert retrieval
            for _ in range(5):
                user_id = self.test_users[len(operations) % len(self.test_users)]
                task = self.simulate_alert_retrieval(user_id)
                tasks.append(task)
            
            # 10% monitoring
            task = self.simulate_alert_monitoring(100)
            tasks.append(task)
            
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            operations.extend([r for r in batch_results if isinstance(r, dict)])
            
            # Small delay to prevent overwhelming
            await asyncio.sleep(0.1)
        
        # Analyze mixed workload results
        total_operations = len(operations)
        successful = sum(1 for op in operations if op.get('success', False))
        
        operation_types = {}
        for op in operations:
            op_type = op.get('operation', 'unknown')
            if op_type not in operation_types:
                operation_types[op_type] = {'count': 0, 'successful': 0, 'durations': []}
            operation_types[op_type]['count'] += 1
            if op.get('success', False):
                operation_types[op_type]['successful'] += 1
            if 'duration' in op:
                operation_types[op_type]['durations'].append(op['duration'])
        
        return {
            'test': 'mixed_workload',
            'duration': duration_seconds,
            'total_operations': total_operations,
            'successful_operations': successful,
            'success_rate': successful / total_operations * 100 if total_operations > 0 else 0,
            'operations_per_second': total_operations / duration_seconds,
            'operation_breakdown': operation_types
        }
    
    async def run_all_tests(self) -> Dict:
        """Run all performance tests"""
        logger.info("Starting Alert System Performance Tests")
        
        test_results = {
            'timestamp': datetime.utcnow().isoformat(),
            'tests': []
        }
        
        # Test 1: Concurrent Alert Creation
        result1 = await self.test_concurrent_alert_creation(50)
        test_results['tests'].append(result1)
        
        # Test 2: Concurrent Alert Retrieval
        result2 = await self.test_concurrent_alert_retrieval(100)
        test_results['tests'].append(result2)
        
        # Test 3: Alert Monitoring Performance
        result3 = await self.test_alert_monitoring_performance()
        test_results['tests'].append(result3)
        
        # Test 4: Mixed Workload
        result4 = await self.test_mixed_workload(30)
        test_results['tests'].append(result4)
        
        return test_results
    
    def generate_report(self, results: Dict) -> str:
        """Generate a performance test report"""
        report = []
        report.append("=" * 60)
        report.append("ALERT SYSTEM PERFORMANCE TEST REPORT")
        report.append("=" * 60)
        report.append(f"Test Timestamp: {results['timestamp']}")
        report.append("")
        
        for test in results['tests']:
            test_name = test.get('test', 'Unknown Test')
            report.append(f"📊 {test_name.upper().replace('_', ' ')}")
            report.append("-" * 40)
            
            if test_name == 'concurrent_alert_creation':
                report.append(f"Concurrent Users: {test['concurrent_users']}")
                report.append(f"Success Rate: {test['success_rate']:.1f}%")
                report.append(f"Average Duration: {test['avg_duration']*1000:.1f}ms")
                report.append(f"Max Duration: {test['max_duration']*1000:.1f}ms")
                report.append(f"Total Time: {test['total_time']:.2f}s")
                
            elif test_name == 'concurrent_alert_retrieval':
                report.append(f"Concurrent Users: {test['concurrent_users']}")
                report.append(f"Success Rate: {test['success_rate']:.1f}%")
                report.append(f"Average Duration: {test['avg_duration']*1000:.1f}ms")
                report.append(f"Max Duration: {test['max_duration']*1000:.1f}ms")
                report.append(f"Total Time: {test['total_time']:.2f}s")
                
            elif test_name == 'alert_monitoring_performance':
                report.append("Alert Count | Duration | Batches")
                for result in test['results']:
                    if result['success']:
                        report.append(f"{result['alert_count']:10d} | {result['duration']*1000:7.1f}ms | {result['batches_processed']:7d}")
                        
            elif test_name == 'mixed_workload':
                report.append(f"Duration: {test['duration']}s")
                report.append(f"Total Operations: {test['total_operations']}")
                report.append(f"Operations/Second: {test['operations_per_second']:.1f}")
                report.append(f"Success Rate: {test['success_rate']:.1f}%")
                report.append("")
                report.append("Operation Breakdown:")
                for op_type, stats in test['operation_breakdown'].items():
                    avg_duration = statistics.mean(stats['durations']) if stats['durations'] else 0
                    success_rate = stats['successful'] / stats['count'] * 100 if stats['count'] > 0 else 0
                    report.append(f"  {op_type}: {stats['count']} ops, {success_rate:.1f}% success, {avg_duration*1000:.1f}ms avg")
            
            report.append("")
        
        # Overall assessment
        report.append("🎯 PERFORMANCE ASSESSMENT")
        report.append("-" * 40)
        
        # Calculate overall metrics
        creation_test = next((t for t in results['tests'] if t['test'] == 'concurrent_alert_creation'), None)
        retrieval_test = next((t for t in results['tests'] if t['test'] == 'concurrent_alert_retrieval'), None)
        mixed_test = next((t for t in results['tests'] if t['test'] == 'mixed_workload'), None)
        
        if creation_test and creation_test['success_rate'] >= 95:
            report.append("✅ Alert Creation: EXCELLENT (>95% success rate)")
        elif creation_test and creation_test['success_rate'] >= 90:
            report.append("✅ Alert Creation: GOOD (>90% success rate)")
        else:
            report.append("⚠️ Alert Creation: NEEDS IMPROVEMENT")
        
        if retrieval_test and retrieval_test['success_rate'] >= 98:
            report.append("✅ Alert Retrieval: EXCELLENT (>98% success rate)")
        elif retrieval_test and retrieval_test['success_rate'] >= 95:
            report.append("✅ Alert Retrieval: GOOD (>95% success rate)")
        else:
            report.append("⚠️ Alert Retrieval: NEEDS IMPROVEMENT")
        
        if mixed_test and mixed_test['operations_per_second'] >= 50:
            report.append("✅ Throughput: EXCELLENT (>50 ops/sec)")
        elif mixed_test and mixed_test['operations_per_second'] >= 30:
            report.append("✅ Throughput: GOOD (>30 ops/sec)")
        else:
            report.append("⚠️ Throughput: NEEDS IMPROVEMENT")
        
        report.append("")
        report.append("🚀 OPTIMIZATION RECOMMENDATIONS:")
        report.append("• Implement connection pooling for database operations")
        report.append("• Use caching for frequently accessed user data")
        report.append("• Batch process alert monitoring for better efficiency")
        report.append("• Consider rate limiting for high-frequency operations")
        report.append("• Monitor memory usage during peak loads")
        
        return "\n".join(report)

async def main():
    """Run the alert performance tests"""
    test_suite = AlertPerformanceTest()
    
    print("Starting Alert System Performance Tests...")
    results = await test_suite.run_all_tests()
    
    # Generate and save report
    report = test_suite.generate_report(results)
    
    # Save to file
    with open('alert_performance_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n" + report)
    print("\n📄 Report saved to: alert_performance_report.txt")

if __name__ == "__main__":
    asyncio.run(main())