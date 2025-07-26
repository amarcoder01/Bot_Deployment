#!/usr/bin/env python3
"""
WSGI wrapper for Render deployment
This file provides a WSGI-compatible entry point for gunicorn
while maintaining the aiohttp application functionality
"""

import os
import sys
import asyncio
import threading
import time
from wsgiref.simple_server import make_server
from wsgiref.util import setup_testing_defaults

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main application
from main import create_app, TradingBot
from logger import logger
from telegram_handler import TelegramHandler

# Global variables
bot_instance = None
aiohttp_app = None
bot_thread = None

def start_bot_in_background():
    """Start the bot in a background thread"""
    global bot_instance
    try:
        bot_instance = TradingBot()
        bot_instance.start_time = time.time()
        
        if bot_instance.validate_environment():
            # Initialize Telegram handler
            bot_instance.telegram_handler = TelegramHandler()
            bot_instance.is_ready = True
            
            # Start the telegram bot
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(bot_instance.telegram_handler.run())
        else:
            logger.error("Bot environment validation failed")
    except Exception as e:
        logger.error(f"Bot startup failed: {e}")

def wsgi_application(environ, start_response):
    """WSGI application entry point"""
    setup_testing_defaults(environ)
    
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    # Simple routing for health checks
    if path == '/health':
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [b'OK']
    
    elif path == '/ready':
        if bot_instance and bot_instance.is_ready:
            status = '200 OK'
            response = b'Ready'
        else:
            status = '503 Service Unavailable'
            response = b'Not Ready'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [response]
    
    elif path == '/':
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [b'TradeAI Companion Bot is running!']
    
    else:
        status = '404 Not Found'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [b'Not Found']

# Initialize the bot when the module is imported
def initialize_bot():
    """Initialize the bot in a separate thread"""
    global bot_thread
    if bot_thread is None:
        bot_thread = threading.Thread(target=start_bot_in_background, daemon=True)
        bot_thread.start()
        logger.info("Bot initialization thread started")

# Start bot initialization
initialize_bot()

# WSGI application object for gunicorn
app = wsgi_application

if __name__ == "__main__":
    # For local testing
    with make_server('', 8000, wsgi_application) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()