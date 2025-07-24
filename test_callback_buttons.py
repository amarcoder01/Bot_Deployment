#!/usr/bin/env python3
"""
Test script to verify callback button functionality
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import Config
from ui_components import TradingBotUI
from callback_handler import ModernCallbackHandler

class CallbackTester:
    def __init__(self):
        self.config = Config()
        self.ui = TradingBotUI()
        
    async def test_menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Test command that shows a menu with buttons"""
        message = f"""
{TradingBotUI.EMOJIS['rocket']} **Button Test Menu**

{TradingBotUI.EMOJIS['info']} Click any button below to test callback functionality:
        """
        
        keyboard = [
            [
                InlineKeyboardButton(f"{TradingBotUI.EMOJIS['price']} Test Price", callback_data="test_price"),
                InlineKeyboardButton(f"{TradingBotUI.EMOJIS['chart']} Test Chart", callback_data="test_chart")
            ],
            [
                InlineKeyboardButton(f"{TradingBotUI.EMOJIS['analysis']} Test Analysis", callback_data="test_analysis"),
                InlineKeyboardButton(f"{TradingBotUI.EMOJIS['alert']} Test Alert", callback_data="test_alert")
            ],
            [
                InlineKeyboardButton(f"{TradingBotUI.EMOJIS['back']} Back to Main", callback_data="main_menu")
            ]
        ]
        
        await update.message.reply_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def test_callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Test callback handler"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        user_id = update.effective_user.id
        
        print(f"[TEST] Callback received from user {user_id}: {callback_data}")
        
        if callback_data.startswith("test_"):
            test_type = callback_data.replace("test_", "")
            await query.edit_message_text(
                f"{TradingBotUI.EMOJIS['success']} **Button Test Successful!**\n\n"
                f"Button clicked: {test_type.title()}\n"
                f"Callback data: `{callback_data}`\n"
                f"User ID: `{user_id}`\n\n"
                f"{TradingBotUI.EMOJIS['info']} The callback system is working correctly!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(f"{TradingBotUI.EMOJIS['back']} Test Again", callback_data="test_menu")
                ]]),
                parse_mode='Markdown'
            )
        elif callback_data == "test_menu":
            await self.show_test_menu(query)
        elif callback_data == "main_menu":
            await query.edit_message_text(
                f"{TradingBotUI.EMOJIS['success']} **Test Complete!**\n\n"
                f"The callback button system is working properly.\n\n"
                f"Use `/testmenu` to run this test again.",
                parse_mode='Markdown'
            )
    
    async def show_test_menu(self, query):
        """Show the test menu"""
        message = f"""
{TradingBotUI.EMOJIS['rocket']} **Button Test Menu**

{TradingBotUI.EMOJIS['info']} Click any button below to test callback functionality:
        """
        
        keyboard = [
            [
                InlineKeyboardButton(f"{TradingBotUI.EMOJIS['price']} Test Price", callback_data="test_price"),
                InlineKeyboardButton(f"{TradingBotUI.EMOJIS['chart']} Test Chart", callback_data="test_chart")
            ],
            [
                InlineKeyboardButton(f"{TradingBotUI.EMOJIS['analysis']} Test Analysis", callback_data="test_analysis"),
                InlineKeyboardButton(f"{TradingBotUI.EMOJIS['alert']} Test Alert", callback_data="test_alert")
            ],
            [
                InlineKeyboardButton(f"{TradingBotUI.EMOJIS['back']} Back to Main", callback_data="main_menu")
            ]
        ]
        
        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

async def main():
    """Run the test bot"""
    tester = CallbackTester()
    
    # Create application
    application = Application.builder().token(tester.config.TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("testmenu", tester.test_menu_command))
    application.add_handler(CallbackQueryHandler(tester.test_callback_handler))
    
    print("[TEST] Starting callback button test...")
    print("[TEST] Use /testmenu command in Telegram to test buttons")
    print("[TEST] Press Ctrl+C to stop")
    
    # Start the bot
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())