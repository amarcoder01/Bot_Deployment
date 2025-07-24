#!/usr/bin/env python3
"""
Test script to check OpenAI API key formatting
"""

import os
from dotenv import load_dotenv
from config import Config

# Load environment variables
load_dotenv()

def test_api_key_format():
    """Test the OpenAI API key format and content"""
    print("🔍 Testing OpenAI API Key Format...\n")
    
    # Direct from environment
    direct_key = os.getenv("OPENAI_API_KEY", "")
    print(f"Direct from env: '{direct_key}'")
    print(f"Length: {len(direct_key)}")
    print(f"Starts with 'sk-': {direct_key.startswith('sk-')}")
    print(f"Has whitespace: {direct_key != direct_key.strip()}")
    
    # From config
    config = Config()
    config_key = config.OPENAI_API_KEY
    print(f"\nFrom config: '{config_key}'")
    print(f"Length: {len(config_key)}")
    print(f"Starts with 'sk-': {config_key.startswith('sk-')}")
    print(f"Has whitespace: {config_key != config_key.strip()}")
    
    # Check if they match
    print(f"\nKeys match: {direct_key == config_key}")
    
    # Check for common issues
    if direct_key != direct_key.strip():
        print("⚠️ WARNING: API key has leading/trailing whitespace!")
        return False
    
    if not direct_key.startswith('sk-'):
        print("⚠️ WARNING: API key doesn't start with 'sk-'!")
        return False
        
    if len(direct_key) < 50:
        print("⚠️ WARNING: API key seems too short!")
        return False
        
    print("✅ API key format appears correct")
    return True

if __name__ == "__main__":
    test_api_key_format()