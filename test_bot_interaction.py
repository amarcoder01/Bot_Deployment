#!/usr/bin/env python3
"""
Test Bot Interaction Script
Tests the inline keyboard functionality by sending commands to the bot
"""

import asyncio
import logging
from telegram import Bot
from telegram.error import TelegramError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_bot_interaction():
    """Test bot interaction and menu functionality"""
    try:
        # Get bot token from environment
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
            return
        
        # Initialize bot
        bot = Bot(token=bot_token)
        
        # Get bot info
        bot_info = await bot.get_me()
        logger.info(f"Connected to bot: {bot_info.username}")
        
        # Test chat ID (replace with your actual chat ID for testing)
        # You can get this by sending a message to the bot and checking the logs
        test_chat_id = "YOUR_CHAT_ID_HERE"  # Replace with actual chat ID
        
        if test_chat_id == "YOUR_CHAT_ID_HERE":
            logger.warning("Please replace YOUR_CHAT_ID_HERE with your actual Telegram chat ID")
            logger.info("To get your chat ID, send a message to the bot and check the logs")
            return
        
        # Send test message
        await bot.send_message(
            chat_id=test_chat_id,
            text="🧪 Testing bot interaction...\n\nPlease try the /menu command to test inline keyboards."
        )
        
        logger.info("Test message sent successfully!")
        logger.info("Now try clicking the buttons in the bot to see if they respond.")
        
    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(test_bot_interaction())