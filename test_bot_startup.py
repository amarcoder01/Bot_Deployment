#!/usr/bin/env python3
"""
Test bot startup with detailed error logging
"""

import sys
import os
import asyncio
import traceback

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from telegram_handler import TelegramHandler
    print("✅ TelegramHandler imported successfully")
except Exception as e:
    print(f"❌ Failed to import TelegramHandler: {e}")
    traceback.print_exc()
    sys.exit(1)

async def test_bot():
    """Test bot startup"""
    try:
        print("🚀 Creating TelegramHandler...")
        handler = TelegramHandler()
        print("✅ TelegramHandler created successfully")
        
        print("🚀 Starting bot...")
        await handler.run()
        
    except Exception as e:
        print(f"❌ Error during bot startup: {e}")
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    try:
        print("🤖 Testing bot startup...")
        result = asyncio.run(test_bot())
        if result:
            print("✅ Bot started successfully")
        else:
            print("❌ Bot startup failed")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        traceback.print_exc()