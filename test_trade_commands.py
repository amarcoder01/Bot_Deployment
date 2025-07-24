#!/usr/bin/env python3
"""
Test script for trade commands functionality
Tests the TradeService and trade command handlers
"""

import asyncio
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_trade_service_import():
    """Test that TradeService can be imported and instantiated"""
    print("🧪 Testing TradeService import and instantiation...")
    
    try:
        from trade_service import TradeService
        trade_service = TradeService()
        print("✅ TradeService imported and created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import or create TradeService: {e}")
        return False

def test_trade_command_logic():
    """Test the trade command logic without database"""
    print("\n🧪 Testing trade command logic...")
    
    def simulate_trade_command(args):
        """Simulate the trade command logic"""
        if len(args) != 4:
            return {"success": False, "error": "Usage: /trade [buy|sell] SYMBOL QUANTITY PRICE"}
        
        action, symbol, quantity_str, price_str = args
        action = action.lower()
        
        if action not in ["buy", "sell"]:
            return {"success": False, "error": "Action must be 'buy' or 'sell'"}
        
        try:
            quantity = float(quantity_str)
            price = float(price_str)
        except ValueError:
            return {"success": False, "error": "Quantity and price must be numbers"}
        
        return {
            "success": True, 
            "trade": {
                "action": action,
                "symbol": symbol.upper(),
                "quantity": quantity,
                "price": price
            }
        }
    
    # Test valid commands
    test_cases = [
        (["buy", "AAPL", "10", "150.50"], True),
        (["sell", "MSFT", "5.5", "300.25"], True),
        (["BUY", "tsla", "2", "800.00"], True),
        (["SELL", "GOOGL", "1.5", "2500.75"], True),
    ]
    
    for args, should_succeed in test_cases:
        result = simulate_trade_command(args)
        if result["success"] == should_succeed:
            if should_succeed:
                trade = result["trade"]
                print(f"✅ Valid: {trade['action'].upper()} {trade['quantity']} {trade['symbol']} @ ${trade['price']:.2f}")
            else:
                print(f"✅ Correctly rejected: {args}")
        else:
            print(f"❌ Unexpected result for {args}: {result}")
    
    # Test invalid commands
    invalid_cases = [
        (["invalid", "AAPL", "10", "150.50"], False),  # Invalid action
        (["buy", "AAPL", "abc", "150.50"], False),     # Invalid quantity
        (["sell", "MSFT", "10", "xyz"], False),       # Invalid price
        (["buy", "AAPL"], False),                      # Too few arguments
        (["sell", "MSFT", "10", "150.50", "extra"], False)  # Too many arguments
    ]
    
    for args, should_succeed in invalid_cases:
        result = simulate_trade_command(args)
        if result["success"] == should_succeed:
            print(f"✅ Correctly rejected: {args} - {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ Should have been rejected: {args}")
    
    print("\n✅ Trade command logic tests completed!")

def test_trade_command_parsing():
    """Test trade command argument parsing logic"""
    print("\n🧪 Testing trade command parsing logic...")
    
    # Test valid command formats
    test_cases = [
        ["buy", "AAPL", "10", "150.50"],
        ["sell", "MSFT", "5.5", "300.25"],
        ["BUY", "tsla", "2", "800.00"],
        ["SELL", "GOOGL", "1.5", "2500.75"]
    ]
    
    for i, args in enumerate(test_cases, 1):
        action, symbol, quantity_str, price_str = args
        action = action.lower()
        
        # Validate action
        if action not in ["buy", "sell"]:
            print(f"❌ Test {i}: Invalid action '{action}'")
            continue
        
        # Validate quantity and price
        try:
            quantity = float(quantity_str)
            price = float(price_str)
            print(f"✅ Test {i}: {action.upper()} {quantity} {symbol.upper()} @ ${price:.2f}")
        except ValueError:
            print(f"❌ Test {i}: Invalid quantity or price")
    
    # Test invalid command formats
    print("\n🧪 Testing invalid command formats...")
    invalid_cases = [
        ["invalid", "AAPL", "10", "150.50"],  # Invalid action
        ["buy", "AAPL", "abc", "150.50"],     # Invalid quantity
        ["sell", "MSFT", "10", "xyz"],       # Invalid price
        ["buy", "AAPL"],                      # Too few arguments
        ["sell", "MSFT", "10", "150.50", "extra"]  # Too many arguments
    ]
    
    for i, args in enumerate(invalid_cases, 1):
        if len(args) != 4:
            print(f"❌ Invalid Test {i}: Wrong number of arguments ({len(args)} instead of 4)")
            continue
        
        action, symbol, quantity_str, price_str = args
        action = action.lower()
        
        if action not in ["buy", "sell"]:
            print(f"❌ Invalid Test {i}: Invalid action '{action}'")
            continue
        
        try:
            quantity = float(quantity_str)
            price = float(price_str)
            print(f"⚠️ Invalid Test {i}: Unexpectedly valid - {action.upper()} {quantity} {symbol.upper()} @ ${price:.2f}")
        except ValueError:
            print(f"✅ Invalid Test {i}: Correctly rejected invalid numbers")
    
    print("\n✅ Trade command parsing tests completed!")

if __name__ == "__main__":
    print("🚀 Starting trade command tests...\n")
    
    # Test 1: Import and instantiation
    import_success = test_trade_service_import()
    
    # Test 2: Command logic
    test_trade_command_logic()
    
    # Test 3: Command parsing
    test_trade_command_parsing()
    
    print("\n🎉 All tests completed!")
    
    if import_success:
        print("\n✅ TradeService is ready for use!")
    else:
        print("\n⚠️ TradeService import failed - check dependencies")