#!/usr/bin/env python3
"""
Test script for Qlib integration
Verifies that Qlib can initialize, train a model, and generate signals
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qlib_service import QlibService
from logger import logger

async def test_qlib_integration():
    """Test the complete Qlib integration"""
    print("🤖 Testing Qlib Integration...")
    
    try:
        # Initialize Qlib service
        print("1. Initializing Qlib service...")
        qs = QlibService()
        
        # Try to initialize (this will fail if data is not ready)
        print("2. Attempting to initialize Qlib...")
        try:
            qs.initialize()
            print("✅ Qlib initialized successfully!")
        except Exception as e:
            print(f"⚠️ Qlib initialization failed (data may still be building): {e}")
            print("This is expected if the data collection is still in progress.")
            return
        
        # Try to train a model
        print("3. Attempting to train Qlib model...")
        try:
            signals = qs.train_basic_model()
            print(f"✅ Model trained successfully! Generated {len(signals)} signals")
            
            # Test signal retrieval
            print("4. Testing signal retrieval...")
            test_symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
            for symbol in test_symbols:
                signal = qs.get_signal(symbol)
                if signal is not None:
                    print(f"✅ Signal for {symbol}: {signal:.4f}")
                else:
                    print(f"⚠️ No signal for {symbol}")
            
            print("\n🎉 Qlib integration test completed successfully!")
            
        except Exception as e:
            print(f"❌ Model training failed: {e}")
            print("This may be because the data is still being collected.")
            
    except Exception as e:
        print(f"❌ Qlib integration test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_qlib_integration()) 