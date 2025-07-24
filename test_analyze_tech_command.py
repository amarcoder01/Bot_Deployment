#!/usr/bin/env python3
"""
Test script to verify the /analyze tech command functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
from unittest.mock import AsyncMock, MagicMock
from telegram_handler import TelegramHandler

async def test_analyze_tech_command_with_handler(telegram_handler):
    """
    Test the /analyze tech command to ensure it provides comprehensive tech sector analysis
    """
    print("🧪 Testing /analyze tech command...")
    
    try:
        
        # Create mock update and context for 'tech' analysis
        mock_update = MagicMock()
        mock_update.effective_user.id = 12345
        mock_update.effective_chat.id = 67890
        mock_update.message.reply_text = AsyncMock()
        
        # Mock the status message for editing
        mock_status_msg = MagicMock()
        mock_status_msg.edit_text = AsyncMock()
        mock_update.message.reply_text.return_value = mock_status_msg
        
        mock_context = MagicMock()
        mock_context.args = ['tech']  # Test with 'tech' argument
        mock_context.bot.send_chat_action = AsyncMock()
        
        print("📊 Testing tech sector analysis...")
        
        # Test the analyze command with 'tech' argument
        await telegram_handler.analyze_command(mock_update, mock_context)
        print("✅ analyze_command completed")
        
        # Verify that reply_text was called (initial status message)
        if not mock_update.message.reply_text.called:
            print("❌ Initial status message was not sent")
            return False
        print("✅ Initial status message sent")
        
        # Verify that edit_text was called (final analysis message)
        if not mock_status_msg.edit_text.called:
            print("❌ Analysis message was not edited")
            return False
        print("✅ Analysis message edited")
        
        # Get the final analysis content
        edit_call_args = mock_status_msg.edit_text.call_args
        if edit_call_args and edit_call_args[0]:
            analysis_content = edit_call_args[0][0]
            print(f"✅ Tech sector analysis generated successfully!")
            print(f"📏 Analysis length: {len(analysis_content)} characters")
            
            # Check for key sections in the analysis
            required_sections = [
                "TECHNOLOGY SECTOR ANALYSIS",
                "Sector Overview:",
                "Sector Sentiment:",
                "Key Metrics:",
                "Top Tech Performers:",
                "Market Insights:"
            ]
            
            sections_found = []
            for section in required_sections:
                if section in analysis_content:
                    sections_found.append(section)
                    print(f"   ✅ Found section: {section}")
                else:
                    print(f"   ❌ Missing section: {section}")
            
            print(f"\n📈 Sections found: {len(sections_found)}/{len(required_sections)}")
            
            # Check for tech stock symbols
            tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX']
            stocks_mentioned = []
            for stock in tech_stocks:
                if stock in analysis_content:
                    stocks_mentioned.append(stock)
            
            print(f"💻 Tech stocks mentioned: {len(stocks_mentioned)} ({', '.join(stocks_mentioned)})")
            
            # Check for sentiment indicators
            sentiment_indicators = ['BULLISH', 'BEARISH', 'NEUTRAL']
            sentiment_found = any(indicator in analysis_content for indicator in sentiment_indicators)
            print(f"🎯 Sentiment analysis: {'✅ Found' if sentiment_found else '❌ Missing'}")
            
            # Check for performance metrics
            metrics_indicators = ['%', 'Average Change', 'Positive Stocks']
            metrics_found = sum(1 for indicator in metrics_indicators if indicator in analysis_content)
            print(f"📊 Performance metrics: {metrics_found}/{len(metrics_indicators)} found")
            
            # Overall assessment
            success = (len(sections_found) >= 5 and 
                      len(stocks_mentioned) >= 5 and 
                      sentiment_found and 
                      metrics_found >= 2)
            
            if success:
                print("\n🎉 SUCCESS: /analyze tech command provides comprehensive sector analysis!")
            else:
                print("\n⚠️ WARNING: Tech sector analysis may be incomplete")
                print(f"   Sections: {len(sections_found)}/6 (need ≥5)")
                print(f"   Stocks: {len(stocks_mentioned)}/8 (need ≥5)")
                print(f"   Sentiment: {sentiment_found} (need True)")
                print(f"   Metrics: {metrics_found}/3 (need ≥2)")
            
            return success
        else:
            print("❌ No analysis content found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing /analyze tech command: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_analyze_technology_alias(telegram_handler):
    """
    Test that 'technology' also works as an alias for tech sector analysis
    """
    print("\n🧪 Testing /analyze technology command...")
    
    try:
        # Create mock update and context for 'technology' analysis
        mock_update = MagicMock()
        mock_update.effective_user.id = 12345
        mock_update.effective_chat.id = 67890
        mock_update.message.reply_text = AsyncMock()
        
        mock_status_msg = MagicMock()
        mock_status_msg.edit_text = AsyncMock()
        mock_update.message.reply_text.return_value = mock_status_msg
        
        mock_context = MagicMock()
        mock_context.args = ['technology']  # Test with 'technology' argument
        mock_context.bot.send_chat_action = AsyncMock()
        
        # Test the analyze command with 'technology' argument
        await telegram_handler.analyze_command(mock_update, mock_context)
        
        # Verify that the command was processed
        if mock_update.message.reply_text.called and mock_status_msg.edit_text.called:
            print("✅ 'technology' alias works correctly!")
            return True
        else:
            print("❌ 'technology' alias failed")
            return False
        
    except Exception as e:
        print(f"❌ Error testing technology alias: {e}")
        return False

async def main():
    """
    Run all tests for the tech sector analysis feature
    """
    print("🚀 Starting /analyze tech command tests...\n")
    
    # Initialize telegram handler once for both tests
    telegram_handler = TelegramHandler()
    print("✅ TelegramHandler initialized for tests")
    
    # Test main functionality
    test1_result = await test_analyze_tech_command_with_handler(telegram_handler)
    
    # Test alias functionality
    test2_result = await test_analyze_technology_alias(telegram_handler)
    
    # Summary
    print("\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)
    print(f"✅ Tech sector analysis: {'PASS' if test1_result else 'FAIL'}")
    print(f"✅ Technology alias: {'PASS' if test2_result else 'FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 ALL TESTS PASSED! The /analyze tech command is working correctly.")
        print("\n💡 Users can now use:")
        print("   • /analyze tech - for technology sector analysis")
        print("   • /analyze technology - alternative command")
        print("   • /analyze AAPL - for individual stock analysis")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    asyncio.run(main())