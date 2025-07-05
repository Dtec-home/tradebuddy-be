"""
Script to reset the database with new schema
"""
import asyncio
from sqlalchemy import text
from app.db.session import async_engine
from app.db.base import BaseModel
from app import models  # Import all models

async def reset_database():
    """Drop all tables and recreate them"""
    async with async_engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(BaseModel.metadata.drop_all)
        print("Dropped all tables")
        
        # Create all tables with new schema
        await conn.run_sync(BaseModel.metadata.create_all)
        print("Created all tables with new schema")
        print("Database reset complete!")

if __name__ == "__main__":
    asyncio.run(reset_database())