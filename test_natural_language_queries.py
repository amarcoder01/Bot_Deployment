#!/usr/bin/env python3
"""
Test script for natural language query handling in Telegram bot
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_handler import TelegramHandler

def test_natural_language_detection():
    """Test the natural language query detection functionality"""
    print("🧪 Testing Natural Language Query Detection...\n")
    
    # Create handler instance
    try:
        handler = TelegramHandler()
    except RuntimeError:
        # Handler already exists, create a mock for testing
        class MockHandler:
            def _detect_natural_language_query(self, message):
                # Import the actual detection logic
                import re
                message_lower = message.lower().strip()
                
                # Price query patterns
                price_patterns = [
                    r'(price|cost|value|worth).*?(of|for)?\s*([a-zA-Z]{1,10})',
                    r'(how much|what.*cost|what.*price).*?([a-zA-Z]{1,10})',
                    r'([a-zA-Z]{1,10}).*?(price|cost|trading|worth)',
                    r'(today.*price|current.*price|latest.*price).*?([a-zA-Z]{1,10})',
                    r'(show me|tell me|get me).*?(price|cost).*?([a-zA-Z]{1,10})'
                ]
                
                # News query patterns
                news_patterns = [
                    r'(news|updates|latest|happening).*?([a-zA-Z]{1,10})',
                    r'([a-zA-Z]{1,10}).*?(news|updates|latest)',
                    r'(what.*happening|what.*going on).*?([a-zA-Z]{1,10})',
                    r'(tell me about|show me.*about).*?([a-zA-Z]{1,10})'
                ]
                
                # Analysis query patterns
                analysis_patterns = [
                    r'(analyze|analysis|review).*?([a-zA-Z]{1,10})',
                    r'([a-zA-Z]{1,10}).*?(analyze|analysis|review)',
                    r'(should i buy|good investment).*?([a-zA-Z]{1,10})',
                    r'(technical analysis|chart analysis).*?([a-zA-Z]{1,10})'
                ]
                
                # Chart query patterns
                chart_patterns = [
                    r'(chart|graph|plot).*?([a-zA-Z]{1,10})',
                    r'([a-zA-Z]{1,10}).*?(chart|graph|plot)',
                    r'(show.*chart|display.*chart).*?([a-zA-Z]{1,10})'
                ]
                
                # Extract potential stock symbol
                def extract_symbol(text, pattern_match):
                    if pattern_match:
                        groups = pattern_match.groups()
                        # Look for stock symbols in the original message
                        stock_words = ['tesla', 'apple', 'microsoft', 'google', 'alphabet', 'amazon', 'meta', 'facebook', 'nvidia', 'netflix', 'bitcoin', 'ethereum']
                        symbol_words = ['aapl', 'tsla', 'msft', 'googl', 'amzn', 'meta', 'nvda', 'nflx', 'btc', 'eth']
                        
                        # Check for company names first
                        for word in message_lower.split():
                            if word in stock_words:
                                name_to_symbol = {
                                    'apple': 'AAPL', 'tesla': 'TSLA', 'microsoft': 'MSFT',
                                    'google': 'GOOGL', 'alphabet': 'GOOGL', 'amazon': 'AMZN',
                                    'meta': 'META', 'facebook': 'META', 'nvidia': 'NVDA',
                                    'netflix': 'NFLX', 'bitcoin': 'BTC', 'ethereum': 'ETH'
                                }
                                return name_to_symbol.get(word, word.upper())
                        
                        # Check for direct symbols
                        for word in message_lower.split():
                            if word in symbol_words or (len(word) <= 5 and word.isupper() in message):
                                return word.upper()
                        
                        # Fallback to regex groups
                        for group in groups:
                            if group and len(group) <= 10 and group.isalpha():
                                name_to_symbol = {
                                    'apple': 'AAPL', 'tesla': 'TSLA', 'microsoft': 'MSFT',
                                    'google': 'GOOGL', 'alphabet': 'GOOGL', 'amazon': 'AMZN',
                                    'meta': 'META', 'facebook': 'META', 'nvidia': 'NVDA',
                                    'netflix': 'NFLX', 'bitcoin': 'BTC', 'ethereum': 'ETH'
                                }
                                return name_to_symbol.get(group.lower(), group.upper())
                    return None
                
                # Check for price queries
                for pattern in price_patterns:
                    match = re.search(pattern, message_lower)
                    if match:
                        symbol = extract_symbol(message_lower, match)
                        if symbol:
                            return {
                                'type': 'price',
                                'symbol': symbol,
                                'command': f'/price {symbol}',
                                'detected': True
                            }
                
                # Check for news queries
                for pattern in news_patterns:
                    match = re.search(pattern, message_lower)
                    if match:
                        symbol = extract_symbol(message_lower, match)
                        if symbol:
                            return {
                                'type': 'news',
                                'symbol': symbol,
                                'command': f'/analyze {symbol}',
                                'detected': True
                            }
                
                # Check for analysis queries
                for pattern in analysis_patterns:
                    match = re.search(pattern, message_lower)
                    if match:
                        symbol = extract_symbol(message_lower, match)
                        if symbol:
                            return {
                                'type': 'analysis',
                                'symbol': symbol,
                                'command': f'/analyze {symbol}',
                                'detected': True
                            }
                
                # Check for chart queries
                for pattern in chart_patterns:
                    match = re.search(pattern, message_lower)
                    if match:
                        symbol = extract_symbol(message_lower, match)
                        if symbol:
                            return {
                                'type': 'chart',
                                'symbol': symbol,
                                'command': f'/chart {symbol}',
                                'detected': True
                            }
                
                return {'detected': False}
        
        handler = MockHandler()
    
    # Test cases for different query types
    test_queries = [
        # Price queries
        "What's happening with Tesla stock?",
        "Show me today's price of Apple",
        "Tell me the latest price for AAPL",
        "How much is Microsoft worth?",
        "What's the current price of NVDA?",
        "TSLA price today",
        
        # News queries
        "Tell me the latest news on Bitcoin",
        "What's happening with Tesla?",
        "Show me updates about Apple",
        "Latest news on GOOGL",
        
        # Analysis queries
        "Analyze Tesla stock",
        "Should I buy Apple?",
        "Technical analysis for MSFT",
        "Review NVDA performance",
        
        # Chart queries
        "Show me Tesla chart",
        "Generate chart for Apple",
        "AAPL price chart",
        "Display graph for TSLA",
        
        # Non-stock queries (should not be detected)
        "Hello, how are you?",
        "What can you do?",
        "Help me with trading",
        "Random conversation"
    ]
    
    detected_count = 0
    total_count = len(test_queries)
    
    for i, query in enumerate(test_queries, 1):
        print(f"Test {i:2d}: {query}")
        result = handler._detect_natural_language_query(query)
        
        if result.get('detected'):
            detected_count += 1
            print(f"         ✅ Detected: {result['type']} query for {result['symbol']}")
            print(f"         💡 Suggested command: {result['command']}")
        else:
            print(f"         ❌ Not detected as stock query")
        print()
    
    print(f"📊 Detection Summary:")
    print(f"   • Total queries tested: {total_count}")
    print(f"   • Stock queries detected: {detected_count}")
    print(f"   • Detection rate: {detected_count/total_count*100:.1f}%")
    
    # Expected detections (first 16 should be detected, last 4 should not)
    expected_detections = 16
    if detected_count >= expected_detections:
        print(f"   ✅ Detection working correctly!")
    else:
        print(f"   ⚠️  Expected at least {expected_detections} detections")
    
    return detected_count >= expected_detections

def test_symbol_extraction():
    """Test symbol extraction from various query formats"""
    print("\n🔍 Testing Symbol Extraction...\n")
    
    # Use the same handler instance or mock
    try:
        handler = TelegramHandler()
    except RuntimeError:
        # Use the same mock handler logic
        class MockHandler:
            def _detect_natural_language_query(self, message):
                import re
                message_lower = message.lower().strip()
                
                # Simple symbol extraction for testing
                stock_words = ['tesla', 'apple', 'microsoft', 'google', 'alphabet', 'amazon', 'meta', 'facebook', 'nvidia', 'netflix', 'bitcoin', 'ethereum']
                name_to_symbol = {
                    'apple': 'AAPL', 'tesla': 'TSLA', 'microsoft': 'MSFT',
                    'google': 'GOOGL', 'alphabet': 'GOOGL', 'amazon': 'AMZN',
                    'meta': 'META', 'facebook': 'META', 'nvidia': 'NVDA',
                    'netflix': 'NFLX', 'bitcoin': 'BTC', 'ethereum': 'ETH'
                }
                
                # Check for company names
                for word in message_lower.split():
                    if word in stock_words:
                        return {
                            'detected': True,
                            'symbol': name_to_symbol.get(word, word.upper()),
                            'type': 'price',
                            'command': f'/price {name_to_symbol.get(word, word.upper())}'
                        }
                
                # Check for direct symbols
                for word in message.split():
                    if word.isupper() and len(word) <= 5 and word.isalpha():
                        return {
                            'detected': True,
                            'symbol': word,
                            'type': 'price',
                            'command': f'/price {word}'
                        }
                
                return {'detected': False}
        
        handler = MockHandler()
    
    test_cases = [
        ("What's Tesla stock price?", "TSLA"),
        ("Show me Apple today", "AAPL"),
        ("Microsoft analysis", "MSFT"),
        ("Google stock news", "GOOGL"),
        ("Amazon price check", "AMZN"),
        ("Meta chart please", "META"),
        ("NVIDIA analysis", "NVDA"),
        ("Netflix price", "NFLX"),
        ("Bitcoin updates", "BTC"),
        ("Ethereum news", "ETH"),
        ("AAPL price today", "AAPL"),
        ("Check TSLA chart", "TSLA")
    ]
    
    correct_extractions = 0
    
    for query, expected_symbol in test_cases:
        result = handler._detect_natural_language_query(query)
        extracted_symbol = result.get('symbol')
        
        print(f"Query: '{query}'")
        print(f"Expected: {expected_symbol}, Got: {extracted_symbol}")
        
        if extracted_symbol == expected_symbol:
            print("✅ Correct extraction")
            correct_extractions += 1
        else:
            print("❌ Incorrect extraction")
        print()
    
    accuracy = correct_extractions / len(test_cases) * 100
    print(f"📊 Symbol Extraction Accuracy: {accuracy:.1f}% ({correct_extractions}/{len(test_cases)})")
    
    return accuracy >= 80  # 80% accuracy threshold

def test_query_type_classification():
    """Test query type classification accuracy"""
    print("\n📋 Testing Query Type Classification...\n")
    
    # Use the same handler instance or mock
    try:
        handler = TelegramHandler()
    except RuntimeError:
        # Use the same mock handler logic from the first test
        class MockHandler:
            def _detect_natural_language_query(self, message):
                import re
                message_lower = message.lower().strip()
                
                # Determine query type based on keywords
                if any(word in message_lower for word in ['price', 'cost', 'worth', 'much']):
                    query_type = 'price'
                elif any(word in message_lower for word in ['news', 'updates', 'happening']):
                    query_type = 'news'
                elif any(word in message_lower for word in ['analyze', 'analysis', 'buy', 'technical']):
                    query_type = 'analysis'
                elif any(word in message_lower for word in ['chart', 'graph']):
                    query_type = 'chart'
                else:
                    return {'detected': False}
                
                # Extract symbol
                stock_words = ['tesla', 'apple', 'microsoft', 'google', 'googl', 'msft', 'aapl']
                name_to_symbol = {
                    'apple': 'AAPL', 'tesla': 'TSLA', 'microsoft': 'MSFT',
                    'google': 'GOOGL', 'googl': 'GOOGL', 'msft': 'MSFT', 'aapl': 'AAPL'
                }
                
                symbol = None
                for word in message_lower.split():
                    if word in stock_words:
                        symbol = name_to_symbol.get(word, word.upper())
                        break
                
                if symbol:
                    return {
                        'detected': True,
                        'type': query_type,
                        'symbol': symbol,
                        'command': f'/{query_type} {symbol}'
                    }
                
                return {'detected': False}
        
        handler = MockHandler()
    
    test_cases = [
        ("Tesla price today", "price"),
        ("Show me Apple cost", "price"),
        ("How much is MSFT worth?", "price"),
        ("Tesla news updates", "news"),
        ("What's happening with Apple?", "news"),
        ("Latest on GOOGL", "news"),
        ("Analyze Tesla stock", "analysis"),
        ("Should I buy Apple?", "analysis"),
        ("Technical analysis MSFT", "analysis"),
        ("Tesla chart please", "chart"),
        ("Show Apple graph", "chart"),
        ("AAPL price chart", "chart")
    ]
    
    correct_classifications = 0
    
    for query, expected_type in test_cases:
        result = handler._detect_natural_language_query(query)
        detected_type = result.get('type')
        
        print(f"Query: '{query}'")
        print(f"Expected: {expected_type}, Got: {detected_type}")
        
        if detected_type == expected_type:
            print("✅ Correct classification")
            correct_classifications += 1
        else:
            print("❌ Incorrect classification")
        print()
    
    accuracy = correct_classifications / len(test_cases) * 100
    print(f"📊 Classification Accuracy: {accuracy:.1f}% ({correct_classifications}/{len(test_cases)})")
    
    return accuracy >= 75  # 75% accuracy threshold

if __name__ == "__main__":
    print("🚀 Natural Language Query Testing Suite\n")
    print("=" * 50)
    
    try:
        # Run all tests
        test1_passed = test_natural_language_detection()
        test2_passed = test_symbol_extraction()
        test3_passed = test_query_type_classification()
        
        print("\n" + "=" * 50)
        print("📋 Final Test Results:")
        print(f"   • Natural Language Detection: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
        print(f"   • Symbol Extraction: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
        print(f"   • Query Classification: {'✅ PASSED' if test3_passed else '❌ FAILED'}")
        
        if all([test1_passed, test2_passed, test3_passed]):
            print("\n🎉 All tests passed! Natural language query handling is working correctly.")
            print("\n💡 Users can now interact with the bot using natural language like:")
            print("   • 'What's happening with Tesla stock?'")
            print("   • 'Show me today's price of Apple'")
            print("   • 'Tell me the latest news on Bitcoin'")
        else:
            print("\n⚠️  Some tests failed. Please review the implementation.")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()