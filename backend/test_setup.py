#!/usr/bin/env python3
"""
Simple test script to verify the backend setup is working correctly.
Run this after setting up the development environment.
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

async def test_imports():
    """Test that all imports work correctly"""
    try:
        from app.main import app
        from app.core.config import settings
        from app.db.session import AsyncSessionLocal
        from app import models
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

async def test_database_connection():
    """Test database connection"""
    try:
        from app.db.session import AsyncSessionLocal
        from sqlalchemy import text
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        print("   Make sure PostgreSQL is running and database exists")
        return False

async def test_config():
    """Test configuration"""
    try:
        from app.core.config import settings
        print(f"✅ Configuration loaded - Project: {settings.PROJECT_NAME}")
        print(f"   Database URL: {settings.DATABASE_URL}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

async def main():
    print("🧪 Testing TradeBuddy Backend Setup\n")
    
    tests = [
        ("Configuration", test_config()),
        ("Imports", test_imports()),
        ("Database Connection", test_database_connection()),
    ]
    
    results = []
    for name, test_coro in tests:
        print(f"Testing {name}...")
        result = await test_coro
        results.append(result)
        print()
    
    if all(results):
        print("🎉 All tests passed! Backend is ready for development.")
        print("\nNext steps:")
        print("1. Run: uvicorn app.main:app --reload")
        print("2. Open: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())