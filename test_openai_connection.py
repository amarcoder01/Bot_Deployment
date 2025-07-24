import asyncio
from openai_service import OpenAIService
from config import Config

async def test_connection():
    try:
        service = OpenAIService()
        result = await service.test_connection()
        print(f'Connection test result: {result}')
        
        # Also test a simple response
        if result:
            response = await service.generate_response("Hello", 12345)
            print(f'Test response: {response}')
        
    except Exception as e:
        print(f'Error during test: {e}')

if __name__ == "__main__":
    asyncio.run(test_connection())