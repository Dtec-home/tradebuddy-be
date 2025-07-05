"""
Clear the entire database and recreate with new schema
"""
import asyncio
from sqlalchemy import text
from app.db.session import engine
from app.db.base import BaseModel
from app import models  # Import all models to register them

async def clear_and_init_database():
    """Drop all tables and recreate them with OAuth fields"""
    
    async with engine.begin() as conn:
        print("🗑️  Dropping all existing tables...")
        
        # Drop all tables
        await conn.run_sync(BaseModel.metadata.drop_all)
        print("✅ All tables dropped successfully")
        
        print("🏗️  Creating tables with new schema (including OAuth fields)...")
        
        # Create all tables with new schema
        await conn.run_sync(BaseModel.metadata.create_all)
        print("✅ All tables created with OAuth support")
        
        print("🎉 Database reset complete!")
        print("📋 Tables created:")
        
        # Show created tables
        result = await conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
        
        tables = result.fetchall()
        for table in tables:
            print(f"   - {table[0]}")
            
        print("\n✨ Your database is ready with OAuth support!")

if __name__ == "__main__":
    asyncio.run(clear_and_init_database())