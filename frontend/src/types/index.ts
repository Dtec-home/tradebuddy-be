export interface User {
  id: number
  email: string
  username: string
  full_name?: string
  is_active: boolean
  is_superuser: boolean
}

export interface Bot {
  id: number
  uuid: string
  name: string
  description?: string
  user_id: number
  status: BotStatus
  mode: TradingMode
  is_active: boolean
  exchange: string
  symbols: string[]
  strategy_type: string
  total_profit_pct: number
  total_trades: number
  winning_trades: number
  created_at: string
  updated_at?: string
  config?: BotConfig
}

export interface BotConfig {
  id: number
  bot_id: number
  leverage: number
  take_profit_pct: number
  martingale_sequence: number[]
  max_positions: number
  martingale_trigger_pct: number
  max_drawdown_pct: number
  daily_loss_limit: number
  position_size_limit: number
  telegram_enabled: boolean
  telegram_chat_id?: string
  discord_enabled: boolean
  discord_webhook?: string
  email_notifications: boolean
}

export interface Position {
  id: number
  bot_id: number
  symbol: string
  side: string
  is_active: boolean
  entry_price: number
  current_price?: number
  contracts: number
  current_step: number
  position_levels: PositionLevel[]
  martingale_trigger_prices: number[]
  unrealized_pnl: number
  realized_pnl: number
}

export interface PositionLevel {
  price: number
  margin: number
  contracts: number
  level: number
}

export interface Trade {
  id: number
  bot_id: number
  symbol: string
  side: string
  price: number
  quantity: number
  exchange_order_id?: string
  order_type: string
  pnl: number
  pnl_pct: number
  commission: number
  created_at: string
}

export enum BotStatus {
  CREATED = "created",
  RUNNING = "running", 
  STOPPED = "stopped",
  ERROR = "error",
  MAINTENANCE = "maintenance"
}

export enum TradingMode {
  LIVE = "live",
  PAPER = "paper", 
  BACKTEST = "backtest"
}

export interface CreateBotRequest {
  name: string
  description?: string
  exchange?: string
  symbols?: string[]
  strategy_type?: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
  full_name?: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export interface WebSocketMessage {
  type: string
  data: any
  timestamp: string
  bot_id?: string
  update_type?: string
}