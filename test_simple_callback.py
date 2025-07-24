#!/usr/bin/env python3
"""
Simple callback test to debug inline keyboard issues
"""

import asyncio
import logging
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_simple_test():
    """Send a simple test message with inline keyboard"""
    config = Config()
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    
    # Replace with your actual chat ID (you can get this from bot logs when you send /start)
    chat_id = "7902186602"  # Based on the logs, this appears to be your chat ID
    
    try:
        # Create a very simple inline keyboard
        keyboard = [
            [InlineKeyboardButton("✅ Test Button 1", callback_data="test_1")],
            [InlineKeyboardButton("🔥 Test Button 2", callback_data="test_2")],
            [InlineKeyboardButton("📊 Menu Test", callback_data="menu_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = await bot.send_message(
            chat_id=chat_id,
            text="🧪 **SIMPLE CALLBACK TEST**\n\nThis is a basic test to check if inline keyboards work.\n\n**Instructions:**\n1. Click any button below\n2. Check the bot console for debug messages\n3. If you see 'DEBUG: Callback received' in the logs, callbacks are working\n\n**If buttons don't respond:**\n- The issue is with callback handling\n- Check bot logs for errors",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        logger.info(f"✅ Simple test message sent! Message ID: {message.message_id}")
        logger.info("📱 Now click the buttons in Telegram and watch the bot logs!")
        logger.info("🔍 Look for 'DEBUG: Callback received' messages in the bot console")
        
    except Exception as e:
        logger.error(f"❌ Error sending test message: {e}")
        logger.info("💡 Make sure the bot is running and the chat ID is correct")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🧪 SIMPLE CALLBACK TEST")
    print("="*50)
    print("\n📋 This test will:")
    print("   1. Send a message with 3 simple buttons")
    print("   2. Help identify if callbacks are working")
    print("   3. Show debug output in bot logs")
    print("\n🔍 After running this:")
    print("   - Click the buttons in Telegram")
    print("   - Watch the bot console for debug messages")
    print("   - Look for 'DEBUG: Callback received' logs")
    print("\n" + "="*50 + "\n")
    
    asyncio.run(send_simple_test())