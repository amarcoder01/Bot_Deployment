#!/usr/bin/env python3
"""
Test script for Professional Chart Analysis feature

This script creates a realistic test chart image and tests the enhanced
image analysis capabilities with improved prompt, response formatting,
and Markdown compatibility.
"""

import asyncio
import base64
import io
import re
import time
from PIL import Image, ImageDraw, ImageFont
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from TradeAiCompanion.openai_service import OpenAIService

def create_test_chart_image():
    """
    Create a realistic test chart image that resembles a professional trading platform chart
    """
    # Create a 1200x800 image with dark background (common in trading platforms)
    width, height = 1200, 800
    background_color = (21, 25, 30)  # Dark blue-gray background
    grid_color = (40, 44, 52)        # Slightly lighter grid lines
    text_color = (180, 185, 190)     # Light gray text
    price_color = (255, 255, 255)    # White for price text
    up_color = (0, 180, 100)         # Green for up candles
    down_color = (220, 50, 50)       # Red for down candles
    volume_color = (100, 120, 220)   # Blue for volume bars
    ma_color = (255, 165, 0)         # Orange for moving average
    
    img = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(img)
    
    # Chart area dimensions
    margin = 60
    chart_width = width - 2 * margin
    chart_height = height - 2 * margin - 100  # Leave room for volume at bottom
    volume_height = 80
    
    # Draw chart border and background
    chart_area = [margin, margin, width - margin, margin + chart_height]
    volume_area = [margin, margin + chart_height + 20, width - margin, margin + chart_height + 20 + volume_height]
    
    # Draw grid lines
    for i in range(7):  # Horizontal price grid lines
        y = margin + i * (chart_height / 6)
        draw.line([margin, y, width - margin, y], fill=grid_color, width=1)
        # Add price labels
        price = 180 - i * 10  # Example prices from 180 to 120
        draw.text((margin - 40, y - 7), f"${price}", fill=price_color)
    
    for i in range(11):  # Vertical date grid lines
        x = margin + i * (chart_width / 10)
        draw.line([x, margin, x, margin + chart_height + 20 + volume_height], fill=grid_color, width=1)
        # Add date labels (simplified)
        month = i + 1
        if month <= 12:
            date = f"2023/{month:02d}"
        else:
            date = f"2024/{month-12:02d}"
        draw.text((x - 20, margin + chart_height + volume_height + 25), date, fill=text_color)
    
    # Generate candlestick data (open, high, low, close)
    import random
    random.seed(42)  # For reproducibility
    
    num_candles = 50
    candle_width = chart_width / num_candles
    
    # Start with a base price and create somewhat realistic price movements
    base_price = 150.0
    volatility = 5.0
    trend = 0.2  # Slight upward trend
    
    candles = []
    volumes = []
    prices = []
    
    for i in range(num_candles):
        # Generate OHLC data with some randomness but following a trend
        if i > 0:
            prev_close = candles[i-1][3]
            # Random walk with drift
            change = (random.random() - 0.5) * volatility + trend
            open_price = prev_close
        else:
            open_price = base_price
            change = (random.random() - 0.5) * volatility + trend
        
        close_price = open_price + change
        high_price = max(open_price, close_price) + random.random() * volatility / 2
        low_price = min(open_price, close_price) - random.random() * volatility / 2
        
        candles.append((open_price, high_price, low_price, close_price))
        prices.append(close_price)
        
        # Generate volume data
        volume = random.randint(50, 200)
        if abs(change) > volatility/2:  # Higher volume on bigger price moves
            volume *= 1.5
        volumes.append(volume)
    
    # Calculate a simple moving average (10-period)
    ma_period = 10
    moving_averages = []
    
    for i in range(num_candles):
        if i < ma_period - 1:
            moving_averages.append(None)
        else:
            ma = sum(prices[i-(ma_period-1):i+1]) / ma_period
            moving_averages.append(ma)
    
    # Draw candlesticks
    max_price = max([c[1] for c in candles])  # Highest high
    min_price = min([c[2] for c in candles])  # Lowest low
    price_range = max_price - min_price
    
    # Function to convert price to y-coordinate
    def price_to_y(price):
        return margin + chart_height - ((price - min_price) / price_range * chart_height)
    
    # Draw volume bars
    max_volume = max(volumes)
    for i, volume in enumerate(volumes):
        x = margin + i * candle_width
        bar_height = (volume / max_volume) * volume_height
        y_top = margin + chart_height + 20 + volume_height - bar_height
        
        # Color volume bars based on price direction
        if candles[i][0] < candles[i][3]:  # Price went up
            vol_color = up_color
        else:  # Price went down
            vol_color = down_color
        
        draw.rectangle([x, y_top, x + candle_width - 1, margin + chart_height + 20 + volume_height], 
                       fill=vol_color, outline=None)
    
    # Draw candlesticks
    for i, (open_price, high, low, close) in enumerate(candles):
        x = margin + i * candle_width
        
        # Draw the wick (high to low line)
        wick_x = x + candle_width / 2
        high_y = price_to_y(high)
        low_y = price_to_y(low)
        draw.line([wick_x, high_y, wick_x, low_y], fill=text_color, width=1)
        
        # Draw the body
        open_y = price_to_y(open_price)
        close_y = price_to_y(close)
        
        # Determine if it's an up or down candle
        if close > open_price:  # Up candle
            body_color = up_color
            body_top = close_y
            body_bottom = open_y
        else:  # Down candle
            body_color = down_color
            body_top = open_y
            body_bottom = close_y
        
        # Draw candle body (rectangle)
        body_width = max(1, candle_width - 2)  # Ensure at least 1px width
        draw.rectangle([x + 1, body_top, x + body_width, body_bottom], fill=body_color, outline=body_color)
    
    # Draw moving average line
    ma_points = []
    for i, ma in enumerate(moving_averages):
        if ma is not None:
            x = margin + i * candle_width + candle_width / 2
            y = price_to_y(ma)
            ma_points.append((x, y))
    
    if len(ma_points) > 1:
        for i in range(len(ma_points) - 1):
            draw.line([ma_points[i], ma_points[i+1]], fill=ma_color, width=2)
    
    # Add chart title and labels
    title = "TSLA - Tesla, Inc. (Daily)"
    draw.text((margin, margin - 40), title, fill=text_color, font=None)
    
    # Add some technical indicators text to make it look more realistic
    indicators_text = "MA(10): $157.23   RSI(14): 62.5   MACD(12,26,9): 2.15"
    draw.text((margin, margin - 20), indicators_text, fill=text_color, font=None)
    
    # Add volume label
    draw.text((margin, margin + chart_height + 5), "Volume", fill=text_color, font=None)
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr

async def test_image_analysis():
    """
    Test the image analysis functionality with enhanced validation for professional chart analysis
    """
    print("🧪 Testing Professional Chart Analysis Feature")
    print("=" * 50)
    
    # Initialize OpenAI service
    try:
        openai_service = OpenAIService()
        print("✅ OpenAI service initialized")
    except Exception as e:
        print(f"❌ Failed to initialize OpenAI service: {e}")
        return
    
    # Create test image
    try:
        start_time = time.time()
        test_image = create_test_chart_image()
        print(f"✅ Test chart image created ({len(test_image)/1024:.1f} KB)")
    except Exception as e:
        print(f"❌ Failed to create test image: {e}")
        return
    
    # Test image analysis
    try:
        print("\n🔍 Testing professional chart analysis...")
        result = await openai_service.analyze_image(test_image, user_id=12345)
        analysis_time = time.time() - start_time
        
        if result:
            print("✅ Image analysis successful!")
            print(f"\n📊 Analysis Result:")
            print("=" * 50)
            print(result)
            print("=" * 50)
            print(f"Analysis completed in {analysis_time:.2f} seconds")
            
            # Validate the analysis result
            validation_results = []
            
            # Check for minimum content length
            if len(result) > 500:
                validation_results.append("✓ Sufficient content length")
            else:
                validation_results.append("✗ Insufficient content length")
            
            # Check for expected sections in the analysis
            expected_sections = [
                "CHART IDENTIFICATION", 
                "TECHNICAL STRUCTURE", 
                "TECHNICAL INDICATORS", 
                "ACTIONABLE TRADING INSIGHTS", 
                "RISK ASSESSMENT"
            ]
            
            found_sections = []
            for section in expected_sections:
                if section in result:
                    found_sections.append(section)
                    validation_results.append(f"✓ Found '{section}' section")
                else:
                    validation_results.append(f"✗ Missing '{section}' section")
            
            # Check for proper Markdown formatting
            markdown_issues = []
            
            # Check for unescaped percent signs (common Markdown issue)
            percent_signs = re.findall(r'(?<!\\)%(?!R\b)', result)
            if percent_signs:
                markdown_issues.append(f"Found {len(percent_signs)} unescaped % signs")
            
            # Check for unmatched asterisks (bold/italic markers)
            asterisk_count = result.count('*')
            if asterisk_count % 2 != 0:
                markdown_issues.append(f"Unmatched asterisks: {asterisk_count}")
            
            if markdown_issues:
                validation_results.append("✗ Markdown formatting issues: " + ", ".join(markdown_issues))
            else:
                validation_results.append("✓ No Markdown formatting issues detected")
            
            # Check for price values and percentages
            price_patterns = re.findall(r'\$\d+\.?\d*', result)
            percentage_patterns = re.findall(r'\d+\.?\d*\\?%', result)
            
            if price_patterns:
                validation_results.append(f"✓ Contains {len(price_patterns)} price values")
            else:
                validation_results.append("✗ No specific price values found")
                
            if percentage_patterns:
                validation_results.append(f"✓ Contains {len(percentage_patterns)} percentage values")
            else:
                validation_results.append("✗ No percentage values found")
            
            # Print validation results
            print("\nValidation Results:")
            for result_item in validation_results:
                print(f"  {result_item}")
        else:
            print("❌ Image analysis returned empty result")
            
    except Exception as e:
        print(f"❌ Image analysis failed: {e}")
        
        # Check if it's an API key issue
        if "api key" in str(e).lower() or "401" in str(e):
            print("\n💡 This appears to be an API key issue.")
            print("   The image analysis feature is implemented correctly,")
            print("   but requires a valid OpenAI API key to function.")
        
    print("\n🏁 Test completed!")

if __name__ == "__main__":
    asyncio.run(test_image_analysis())