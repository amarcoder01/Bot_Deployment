import asyncio
from telegram_handler import TelegramHandler
from unittest.mock import Mock

async def test_analyze():
    try:
        handler = TelegramHandler()
        
        # Create mock update object
        update = Mock()
        update.message = Mock()
        update.message.text = '/analyze AAPL'
        update.effective_user = Mock()
        update.effective_user.id = 123
        update.effective_chat = Mock()
        update.effective_chat.id = 123
        
        # Mock reply function to capture output
        responses = []
        async def mock_reply(text, **kwargs):
            responses.append(text)
            print(f"Bot reply: {text}")
        update.message.reply_text = mock_reply
        
        context = Mock()
        context.args = ['AAPL']  # Mock the command arguments
        
        print("Testing /analyze AAPL command...")
        await handler.analyze_command(update, context)
        
        print("\nBot responses:")
        for response in responses:
            print(f"Response: {response}")
            
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_analyze())