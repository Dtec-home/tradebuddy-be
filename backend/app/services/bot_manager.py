import asyncio
import logging
from typing import Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models import Bot, ExchangeApiKey, BotStatus
from app.trading.bot_engine import TradingBot
from app.core.websocket import websocket_manager

logger = logging.getLogger(__name__)


class BotManager:
    """Manages active trading bot instances"""
    
    def __init__(self):
        self.running_bots: Dict[str, TradingBot] = {}
        self.bot_tasks: Dict[str, asyncio.Task] = {}
    
    async def start_bot(self, db: AsyncSession, bot: Bot) -> bool:
        """Start a trading bot"""
        try:
            # Check if bot is already running
            if str(bot.uuid) in self.running_bots:
                logger.warning(f"Bot {bot.uuid} is already running")
                return False
            
            # Get user's API key for this exchange
            api_key_query = select(ExchangeApiKey).where(
                and_(
                    ExchangeApiKey.user_id == bot.user_id,
                    ExchangeApiKey.exchange == bot.exchange,
                    ExchangeApiKey.is_active == True,
                    ExchangeApiKey.is_verified == True
                )
            )
            result = await db.execute(api_key_query)
            api_key = result.scalar_one_or_none()
            
            if not api_key:
                logger.error(f"No verified API key found for user {bot.user_id} on {bot.exchange}")
                raise ValueError(f"No verified API key found for {bot.exchange}")
            
            # Get decrypted credentials
            credentials = api_key.get_credentials()
            
            # Add sandbox flag
            credentials['sandbox'] = api_key.is_sandbox
            
            # Create bot instance
            bot_instance = TradingBot(bot, bot.config, credentials)
            
            # Start bot in background task
            task = asyncio.create_task(self._run_bot(bot_instance, db))
            
            # Store references
            self.running_bots[str(bot.uuid)] = bot_instance
            self.bot_tasks[str(bot.uuid)] = task
            
            # Update bot status
            bot.status = BotStatus.RUNNING
            bot.is_active = True
            await db.commit()
            
            # Send WebSocket notification
            await websocket_manager.broadcast_bot_update(
                str(bot.user_id),
                str(bot.uuid),
                "started",
                {"status": bot.status.value}
            )
            
            logger.info(f"Bot {bot.uuid} started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start bot {bot.uuid}: {str(e)}")
            bot.status = BotStatus.ERROR
            await db.commit()
            
            # Send error notification
            await websocket_manager.broadcast_bot_update(
                str(bot.user_id),
                str(bot.uuid),
                "error",
                {"status": bot.status.value, "error": str(e)}
            )
            
            return False
    
    async def stop_bot(self, db: AsyncSession, bot: Bot) -> bool:
        """Stop a trading bot"""
        try:
            bot_uuid_str = str(bot.uuid)
            
            # Check if bot is running
            if bot_uuid_str not in self.running_bots:
                logger.warning(f"Bot {bot.uuid} is not running")
                # Update status anyway
                bot.status = BotStatus.STOPPED
                bot.is_active = False
                await db.commit()
                return True
            
            # Stop the bot instance
            bot_instance = self.running_bots[bot_uuid_str]
            await bot_instance.stop()
            
            # Cancel the task
            if bot_uuid_str in self.bot_tasks:
                task = self.bot_tasks[bot_uuid_str]
                if not task.done():
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
                del self.bot_tasks[bot_uuid_str]
            
            # Remove from running bots
            del self.running_bots[bot_uuid_str]
            
            # Update bot status
            bot.status = BotStatus.STOPPED
            bot.is_active = False
            await db.commit()
            
            # Send WebSocket notification
            await websocket_manager.broadcast_bot_update(
                str(bot.user_id),
                str(bot.uuid),
                "stopped",
                {"status": bot.status.value}
            )
            
            logger.info(f"Bot {bot.uuid} stopped successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop bot {bot.uuid}: {str(e)}")
            return False
    
    async def _run_bot(self, bot_instance: TradingBot, db: AsyncSession):
        """Run bot instance in background"""
        try:
            await bot_instance.start()
            
            # Keep running until stopped
            while bot_instance.is_running:
                await asyncio.sleep(1)  # Bot handles its own timing
                
        except asyncio.CancelledError:
            logger.info(f"Bot {bot_instance.bot.uuid} task cancelled")
            await bot_instance.stop()
        except Exception as e:
            logger.error(f"Bot {bot_instance.bot.uuid} crashed: {str(e)}")
            
            # Update bot status to error
            bot_instance.bot.status = BotStatus.ERROR
            await db.commit()
            
            # Send error notification
            await websocket_manager.broadcast_bot_update(
                str(bot_instance.bot.user_id),
                str(bot_instance.bot.uuid),
                "error",
                {"status": BotStatus.ERROR.value, "error": str(e)}
            )
            
            # Remove from running bots
            bot_uuid_str = str(bot_instance.bot.uuid)
            if bot_uuid_str in self.running_bots:
                del self.running_bots[bot_uuid_str]
            if bot_uuid_str in self.bot_tasks:
                del self.bot_tasks[bot_uuid_str]
    
    def get_running_bot(self, bot_uuid: str) -> Optional[TradingBot]:
        """Get running bot instance"""
        return self.running_bots.get(bot_uuid)
    
    def is_bot_running(self, bot_uuid: str) -> bool:
        """Check if bot is running"""
        return bot_uuid in self.running_bots
    
    async def stop_all_bots(self):
        """Stop all running bots (for shutdown)"""
        tasks = []
        for bot_instance in self.running_bots.values():
            tasks.append(bot_instance.stop())
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        # Cancel all tasks
        for task in self.bot_tasks.values():
            if not task.done():
                task.cancel()
        
        if self.bot_tasks:
            await asyncio.gather(*self.bot_tasks.values(), return_exceptions=True)
        
        self.running_bots.clear()
        self.bot_tasks.clear()


# Global bot manager instance
bot_manager = BotManager()