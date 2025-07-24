#!/usr/bin/env python3
"""
Test script to check if database schema has the required columns
"""

import asyncio
from db import AsyncSessionLocal
from sqlalchemy import text

async def test_schema():
    """Test if the required columns exist in the database"""
    async with AsyncSessionLocal() as session:
        try:
            # Test users.access_level column
            result = await session.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'access_level'"
            ))
            access_level_exists = bool(result.fetchone())
            print(f"users.access_level column exists: {access_level_exists}")
            
            # Test alerts.created_from_ip column
            result = await session.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'alerts' AND column_name = 'created_from_ip'"
            ))
            created_from_ip_exists = bool(result.fetchone())
            print(f"alerts.created_from_ip column exists: {created_from_ip_exists}")
            
            # Test security_logs table
            result = await session.execute(text(
                "SELECT table_name FROM information_schema.tables WHERE table_name = 'security_logs'"
            ))
            security_logs_exists = bool(result.fetchone())
            print(f"security_logs table exists: {security_logs_exists}")
            
            if access_level_exists and created_from_ip_exists and security_logs_exists:
                print("\n✅ Database schema migration successful!")
                return True
            else:
                print("\n❌ Database schema migration incomplete!")
                return False
                
        except Exception as e:
            print(f"Error testing schema: {e}")
            return False

if __name__ == "__main__":
    asyncio.run(test_schema())