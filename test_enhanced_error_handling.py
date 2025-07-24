#!/usr/bin/env python3
"""
Test script for enhanced error handling in TradeMaster AI bot
Tests typo suggestions, invalid format handling, and helpful error messages
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_error_handler import EnhancedErrorHandler

def test_enhanced_error_handling():
    """Test various error handling scenarios"""
    print("🧪 Testing Enhanced Error Handling\n")
    
    error_handler = EnhancedErrorHandler()
    
    # Test 1: Invalid stock symbol with typo suggestions
    print("📊 Test 1: Invalid Stock Symbol with Typo Suggestions")
    print("=" * 50)
    
    test_symbols = ["APPL", "TSLA1", "GOOGL1", "MSFT123", "NVDA_", "AMAZN"]
    
    for symbol in test_symbols:
        error_msg = error_handler.format_error_message(
            "invalid_symbol",
            context={"invalid_symbol": symbol}
        )
        print(f"Input: {symbol}")
        print(f"Response: {error_msg}\n")
    
    # Test 2: Command typo suggestions
    print("⌨️ Test 2: Command Typo Suggestions")
    print("=" * 50)
    
    test_commands = ["/pric", "/chart", "/analyz", "/hep", "/manu", "/prise"]
    
    for command in test_commands:
        error_msg = error_handler.handle_command_error(command)
        print(f"Input: {command}")
        print(f"Response: {error_msg}\n")
    
    # Test 3: Invalid format examples
    print("📝 Test 3: Invalid Format Examples")
    print("=" * 50)
    
    test_formats = [
        ("/price", "missing_symbol"),
        ("/chart", "missing_symbol"),
        ("/analyze", "missing_symbol")
    ]
    
    for command, format_type in test_formats:
        error_msg = error_handler.handle_command_error(command)
        print(f"Input: {command} (missing symbol)")
        print(f"Response: {error_msg}\n")
    
    # Test 4: API and data errors
    print("🔌 Test 4: API and Data Errors")
    print("=" * 50)
    
    api_error_msg = error_handler.format_error_message("api_error")
    print(f"API Error Response: {api_error_msg}\n")
    
    data_error_msg = error_handler.format_error_message("data_error")
    print(f"Data Error Response: {data_error_msg}\n")
    
    # Test 5: Direct function tests
    print("🔍 Test 5: Direct Function Tests")
    print("=" * 50)
    
    # Test symbol suggestions
    suggestion = error_handler.suggest_similar_symbol("APPL")
    print(f"Symbol suggestion for 'APPL': {suggestion}")
    
    # Test command corrections
    correction = error_handler.suggest_command_correction("/pric")
    print(f"Command correction for '/pric': {correction}")
    
    # Test format validation
    is_valid = error_handler.validate_command_format("/price AAPL")
    print(f"Format validation for '/price AAPL': {is_valid}")
    
    is_invalid = error_handler.validate_command_format("/price")
    print(f"Format validation for '/price': {is_invalid}")
    
    print("\n✅ Enhanced Error Handling Tests Completed!")

if __name__ == "__main__":
    test_enhanced_error_handling()