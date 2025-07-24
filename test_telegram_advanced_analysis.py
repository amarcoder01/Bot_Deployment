#!/usr/bin/env python3
"""
Test script to verify the Telegram bot's advanced_analysis command
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_handler import TelegramHandler
from unittest.mock import Mock, AsyncMock

async def test_advanced_analysis_command():
    """
    Test the advanced_analysis_command method directly
    """
    print("🧪 Testing Telegram advanced_analysis_command...")
    
    try:
        # Initialize TelegramHandler
        handler = TelegramHandler()
        
        # Create mock objects for Telegram update and context
        mock_update = Mock()
        mock_update.message = Mock()
        mock_update.message.reply_text = AsyncMock()
        mock_update.message.edit_text = AsyncMock()
        mock_update.message.chat_id = 12345
        mock_update.message.from_user.id = 12345
        mock_update.message.from_user.first_name = "TestUser"
        
        mock_context = Mock()
        mock_context.args = ["AAPL"]  # Test with Apple stock
        mock_context.bot = Mock()
        mock_context.bot.send_chat_action = AsyncMock()
        
        print("\n1. Testing with valid symbol: AAPL")
        
        # Test the command
        await handler.advanced_analysis_command(mock_update, mock_context)
        
        # Check if reply_text was called (indicating success)
        if mock_update.message.reply_text.called:
            print("   ✅ Command executed successfully")
            
            # Get the response content
            call_args = mock_update.message.reply_text.call_args
            if call_args:
                response_text = call_args[0][0] if call_args[0] else "No response text"
                print(f"   📄 Response preview (first 200 chars): {response_text[:200]}...")
            else:
                print("   ⚠️ No response text found")
        else:
            print("   ❌ Command did not call reply_text")
        
        print("\n2. Testing with invalid symbol: INVALID")
        
        # Reset mocks
        mock_update.message.reply_text.reset_mock()
        mock_context.args = ["INVALID"]
        
        # Test with invalid symbol
        await handler.advanced_analysis_command(mock_update, mock_context)
        
        if mock_update.message.reply_text.called:
            call_args = mock_update.message.reply_text.call_args
            if call_args:
                response_text = call_args[0][0] if call_args[0] else "No response text"
                print(f"   📄 Error response: {response_text[:200]}...")
                if "Error" in response_text or "invalid" in response_text.lower():
                    print("   ✅ Proper error handling detected")
                else:
                    print("   ⚠️ Unexpected response for invalid symbol")
        
        print("\n3. Testing with no symbol provided")
        
        # Reset mocks
        mock_update.message.reply_text.reset_mock()
        mock_context.args = []
        
        # Test with no symbol
        await handler.advanced_analysis_command(mock_update, mock_context)
        
        if mock_update.message.reply_text.called:
            call_args = mock_update.message.reply_text.call_args
            if call_args:
                response_text = call_args[0][0] if call_args[0] else "No response text"
                print(f"   📄 Usage response: {response_text[:200]}...")
                if "Usage" in response_text or "provide" in response_text.lower():
                    print("   ✅ Proper usage message detected")
        
        print("\n🏁 Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_advanced_analysis_command())