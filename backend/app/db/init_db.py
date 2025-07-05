import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.db.base import Base
from app.db.session import engine
from app import models

logger = logging.getLogger(__name__)


async def init_db() -> None:
    """Initialize database tables"""
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


async def create_initial_data() -> None:
    """Create initial data like superuser"""
    async with AsyncSessionLocal() as session:
        # TODO: Create initial superuser
        pass