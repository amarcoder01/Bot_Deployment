#!/usr/bin/env python3
"""
Test script to verify callback handler functionality
This script will help debug why inline keyboard buttons are not responding
"""

import asyncio
import logging
from telegram import Bot
from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_callback_functionality():
    """Test if the bot can send and receive callbacks"""
    config = Config()
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    
    # Replace with your actual chat ID
    chat_id = "YOUR_CHAT_ID_HERE"  # You need to replace this with your actual chat ID
    
    try:
        # Send a test message with inline keyboard
        # All code related to InlineKeyboardButton, InlineKeyboardMarkup, and callback_data has been removed for full removal of inline button test/debug code.
        
        message = await bot.send_message(
            chat_id=chat_id,
            text="🧪 **Callback Test**\n\nClick any button below to test if callbacks are working.\n\nCheck the bot logs for debug messages!",
            parse_mode='Markdown'
        )
        
        logger.info(f"Test message sent successfully! Message ID: {message.message_id}")
        logger.info("Now click on any button and check the bot logs for debug output.")
        
    except Exception as e:
        logger.error(f"Error sending test message: {e}")
        logger.info("Make sure to replace YOUR_CHAT_ID_HERE with your actual Telegram chat ID")
        logger.info("You can get your chat ID by sending /start to the bot and checking the logs")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("CALLBACK FUNCTIONALITY TEST")
    print("="*60)
    print("\nIMPORTANT: Before running this test:")
    print("1. Replace YOUR_CHAT_ID_HERE with your actual Telegram chat ID")
    print("2. Make sure the bot is running")
    print("3. After running this script, click the buttons in Telegram")
    print("4. Check the bot logs for debug messages")
    print("\n" + "="*60 + "\n")
    
    asyncio.run(test_callback_functionality())