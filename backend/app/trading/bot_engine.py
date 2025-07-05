import ccxt
import asyncio
import logging
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime

from app.models import Bot, BotConfig, BotPosition
from app.core.websocket import websocket_manager


class TradingBot:
    """Trading bot engine based on original martingale strategy"""
    
    def __init__(self, bot: Bot, config: BotConfig, exchange_credentials: dict):
        self.bot = bot
        self.config = config
        self.logger = logging.getLogger(f"Bot-{bot.uuid}")
        
        # Initialize exchange
        self.exchange = self._init_exchange(exchange_credentials)
        
        # Trading state
        self.trades = {}
        for symbol in bot.symbols:
            self.trades[symbol] = {
                'current_step': 0,
                'entry_price': None,
                'position_side': None,
                'is_active': False,
                'position_levels': [],
                'martingale_trigger_prices': [],
                'trade_in_progress': False,
            }
        
        self.is_running = False
        
    def _init_exchange(self, credentials: dict):
        """Initialize exchange connection"""
        return ccxt.bitget({
            'apiKey': credentials.get('api_key'),
            'secret': credentials.get('secret'),
            'password': credentials.get('passphrase'),
            'sandbox': credentials.get('sandbox', True),
            'enableRateLimit': True,
        })
        
    async def start(self):
        """Start the trading bot"""
        self.is_running = True
        self.logger.info(f"Starting bot {self.bot.uuid}")
        
        while self.is_running:
            try:
                # Check balance
                balance = await self.get_balance()
                if balance < 15.0:  # Minimum required
                    await self.send_notification("error", "Insufficient balance")
                    break
                
                # Monitor active positions
                for symbol in self.bot.symbols:
                    trade = self.trades[symbol]
                    
                    if trade['is_active']:
                        # Check take profit
                        if await self.check_take_profit(symbol):
                            await self.close_position(symbol)
                            continue
                        
                        # Check martingale
                        if await self.should_add_to_position(symbol):
                            current_price = await self.get_current_price(symbol)
                            if current_price:
                                await self.add_martingale_level(symbol, current_price)
                    
                # Start new trades if slots available
                active_count = sum(1 for t in self.trades.values() if t['is_active'])
                if active_count < self.config.max_positions:
                    available_symbol = self.get_available_symbol()
                    if available_symbol:
                        await self.start_new_cycle(available_symbol)
                
                await asyncio.sleep(5)
                
            except Exception as e:
                self.logger.error(f"Error in bot loop: {e}")
                await self.send_notification("error", str(e))
                await asyncio.sleep(10)
                
    async def stop(self):
        """Stop the trading bot"""
        self.is_running = False
        self.logger.info(f"Stopping bot {self.bot.uuid}")
        
    async def get_balance(self) -> float:
        """Get USDT balance"""
        try:
            balance = self.exchange.fetch_balance({'type': 'swap'})
            return balance['USDT']['free']
        except Exception as e:
            self.logger.error(f"Error fetching balance: {e}")
            return 0
            
    async def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for symbol"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker['last']
        except Exception as e:
            self.logger.error(f"Error fetching price for {symbol}: {e}")
            return None
            
    async def check_take_profit(self, symbol: str) -> bool:
        """Check if take profit should trigger"""
        trade = self.trades[symbol]
        if not trade['is_active']:
            return False
            
        weighted_avg = self.calculate_weighted_average_entry(symbol)
        current_price = await self.get_current_price(symbol)
        
        if not weighted_avg or not current_price:
            return False
            
        profit_pct = (current_price - weighted_avg) / weighted_avg * 100
        return profit_pct >= self.config.take_profit_pct
        
    async def should_add_to_position(self, symbol: str) -> bool:
        """Check if should add martingale level"""
        trade = self.trades[symbol]
        current_price = await self.get_current_price(symbol)
        
        if not current_price:
            return False
            
        if trade['current_step'] == 0:
            reference_price = trade['entry_price']
        else:
            if trade['martingale_trigger_prices']:
                reference_price = trade['martingale_trigger_prices'][-1]
            else:
                reference_price = trade['entry_price']
        
        if not reference_price:
            return False
            
        drop_pct = (reference_price - current_price) / reference_price * 100
        return drop_pct >= self.config.martingale_trigger_pct
        
    async def start_new_cycle(self, symbol: str):
        """Start new trading cycle"""
        trade = self.trades[symbol]
        
        if trade['trade_in_progress'] or trade['is_active']:
            return False
            
        trade['trade_in_progress'] = True
        
        try:
            # Set leverage
            self.exchange.set_leverage(self.config.leverage, symbol)
            
            price = await self.get_current_price(symbol)
            if not price:
                trade['trade_in_progress'] = False
                return False
                
            amount = self.calculate_position_size(0, price)
            
            # Place order
            order = self.exchange.create_market_order(
                symbol=symbol,
                side='buy',
                amount=amount,
                params={'marginMode': 'cross', 'reduceOnly': False}
            )
            
            if order:
                trade['current_step'] = 0
                trade['entry_price'] = price
                trade['position_side'] = 'buy'
                trade['is_active'] = True
                trade['position_levels'] = [{
                    'price': price,
                    'margin': self.config.martingale_sequence[0],
                    'contracts': amount,
                    'level': 1
                }]
                trade['martingale_trigger_prices'] = []
                
                await self.send_notification("trade_opened", {
                    "symbol": symbol,
                    "price": price,
                    "amount": amount
                })
                
                trade['trade_in_progress'] = False
                return True
                
        except Exception as e:
            self.logger.error(f"Error starting new cycle: {e}")
            trade['trade_in_progress'] = False
            return False
            
    async def add_martingale_level(self, symbol: str, current_price: float):
        """Add martingale level"""
        trade = self.trades[symbol]
        
        if trade['current_step'] >= len(self.config.martingale_sequence) - 1:
            return False
            
        trade['current_step'] += 1
        amount = self.calculate_position_size(trade['current_step'], current_price)
        
        try:
            order = self.exchange.create_market_order(
                symbol=symbol,
                side='buy',
                amount=amount,
                params={'marginMode': 'cross', 'reduceOnly': False}
            )
            
            if order:
                trade['martingale_trigger_prices'].append(current_price)
                trade['position_levels'].append({
                    'price': current_price,
                    'margin': self.config.martingale_sequence[trade['current_step']],
                    'contracts': amount,
                    'level': trade['current_step'] + 1
                })
                
                await self.send_notification("martingale_added", {
                    "symbol": symbol,
                    "level": trade['current_step'] + 1,
                    "price": current_price,
                    "amount": amount
                })
                
                return True
                
        except Exception as e:
            self.logger.error(f"Error adding martingale: {e}")
            trade['current_step'] -= 1
            return False
            
    async def close_position(self, symbol: str):
        """Close position"""
        trade = self.trades[symbol]
        
        if not trade['position_levels']:
            return False
            
        total_contracts = sum(level['contracts'] for level in trade['position_levels'])
        current_price = await self.get_current_price(symbol)
        
        try:
            order = self.exchange.create_market_order(
                symbol=symbol,
                side='sell',
                amount=total_contracts,
                params={'marginMode': 'cross', 'reduceOnly': True}
            )
            
            if order:
                weighted_avg = self.calculate_weighted_average_entry(symbol)
                profit_pct = (current_price - weighted_avg) / weighted_avg * 100
                margin_return = profit_pct * self.config.leverage
                
                await self.send_notification("position_closed", {
                    "symbol": symbol,
                    "profit_pct": profit_pct,
                    "margin_return": margin_return,
                    "exit_price": current_price
                })
                
                # Reset trade
                trade['is_active'] = False
                trade['entry_price'] = None
                trade['current_step'] = 0
                trade['position_levels'] = []
                trade['martingale_trigger_prices'] = []
                
                return True
                
        except Exception as e:
            self.logger.error(f"Error closing position: {e}")
            return False
            
    def calculate_weighted_average_entry(self, symbol: str) -> float:
        """Calculate weighted average entry price"""
        trade = self.trades[symbol]
        if not trade['position_levels']:
            return trade['entry_price']
            
        total_contracts = sum(level['contracts'] for level in trade['position_levels'])
        weighted_sum = sum(level['price'] * level['contracts'] for level in trade['position_levels'])
        
        return weighted_sum / total_contracts if total_contracts > 0 else trade['entry_price']
        
    def calculate_position_size(self, step: int, price: float) -> float:
        """Calculate position size"""
        margin_amount = self.config.martingale_sequence[step]
        position_value = margin_amount * self.config.leverage
        position_size = position_value / price
        return round(position_size, 4)
        
    def get_available_symbol(self) -> Optional[str]:
        """Get available symbol for new trade"""
        for symbol in self.bot.symbols:
            if not self.trades[symbol]['is_active'] and not self.trades[symbol]['trade_in_progress']:
                return symbol
        return None
        
    async def send_notification(self, event_type: str, data: dict):
        """Send notification via WebSocket"""
        await websocket_manager.broadcast_bot_update(
            str(self.bot.user_id),
            str(self.bot.uuid),
            event_type,
            data
        )