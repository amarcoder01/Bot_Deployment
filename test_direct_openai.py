#!/usr/bin/env python3
"""
Direct OpenAI API test to verify key validity
"""

import asyncio
from openai import AsyncOpenAI
from config import Config

async def test_direct_openai():
    """Test OpenAI API directly"""
    try:
        print("🔍 Testing OpenAI API directly...\n")
        
        config = Config()
        api_key = config.OPENAI_API_KEY
        
        print(f"Using API key: {api_key[:20]}...{api_key[-10:]}")
        
        client = AsyncOpenAI(api_key=api_key)
        
        # Test with a simple completion
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Say hello"}
            ],
            max_tokens=10
        )
        
        print("✅ OpenAI API call successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API call failed: {str(e)}")
        
        # Check for specific error types
        error_str = str(e).lower()
        if "invalid_api_key" in error_str:
            print("\n🔑 The API key appears to be invalid or expired.")
            print("Please check your OpenAI account and generate a new key if needed.")
        elif "quota" in error_str:
            print("\n💳 API quota exceeded. Check your OpenAI billing.")
        elif "rate_limit" in error_str:
            print("\n⏱️ Rate limit exceeded. Try again later.")
        else:
            print(f"\n❓ Unknown error: {str(e)}")
            
        return False

if __name__ == "__main__":
    result = asyncio.run(test_direct_openai())
    if result:
        print("\n🎉 OpenAI integration is working correctly!")
    else:
        print("\n⚠️ OpenAI integration needs attention.")