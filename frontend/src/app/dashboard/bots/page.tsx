'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Bot, BotStatus } from '@/types'
import apiService from '@/services/api'
import { formatPercentage, formatDate } from '@/lib/utils'
import { Plus, Play, Square, Settings, TrendingUp, TrendingDown, Bot as BotIcon, MoreVertical } from 'lucide-react'

export default function BotsPage() {
  const [bots, setBots] = useState<Bot[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadBots()
  }, [])

  const loadBots = async () => {
    try {
      const data = await apiService.getBots()
      setBots(data)
    } catch (error) {
      console.error('Error loading bots:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleStartBot = async (botId: string) => {
    try {
      await apiService.startBot(botId)
      loadBots() // Refresh data
    } catch (error) {
      console.error('Error starting bot:', error)
    }
  }

  const handleStopBot = async (botId: string) => {
    try {
      await apiService.stopBot(botId)
      loadBots() // Refresh data
    } catch (error) {
      console.error('Error stopping bot:', error)
    }
  }

  const getBotStatusBadge = (status: BotStatus) => {
    switch (status) {
      case BotStatus.RUNNING:
        return <Badge variant="success">Running</Badge>
      case BotStatus.STOPPED:
        return <Badge variant="secondary">Stopped</Badge>
      case BotStatus.ERROR:
        return <Badge variant="destructive">Error</Badge>
      default:
        return <Badge variant="outline">{status}</Badge>
    }
  }

  const getStrategyDisplay = (strategy: string) => {
    switch (strategy) {
      case 'martingale':
        return 'Martingale Strategy'
      case 'dca':
        return 'Dollar Cost Average'
      case 'grid':
        return 'Grid Trading'
      default:
        return strategy
    }
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">My Bots</h1>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Create Bot
          </Button>
        </div>
        <div className="flex items-center justify-center h-64">
          <div className="text-lg">Loading bots...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">My Bots</h1>
          <p className="text-muted-foreground">
            Manage and monitor your trading bots
          </p>
        </div>
        <Link href="/dashboard/bots/create">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Create Bot
          </Button>
        </Link>
      </div>

      {/* Bots Grid */}
      {bots.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-16">
            <BotIcon className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">No bots yet</h3>
            <p className="text-muted-foreground mb-4 text-center">
              Create your first trading bot to start automated trading
            </p>
            <Link href="/dashboard/bots/create">
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                Create Your First Bot
              </Button>
            </Link>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {bots.map((bot) => (
            <Card key={bot.uuid} className="relative">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <CardTitle className="text-lg">{bot.name}</CardTitle>
                    <div className="flex items-center space-x-2">
                      {getBotStatusBadge(bot.status)}
                      <Badge variant="outline" className="text-xs">
                        {bot.mode}
                      </Badge>
                    </div>
                  </div>
                  <Button variant="ghost" size="icon">
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </div>
                
                <CardDescription>
                  {bot.description || getStrategyDisplay(bot.strategy_type)}
                </CardDescription>
              </CardHeader>
              
              <CardContent className="space-y-4">
                {/* Performance Metrics */}
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <div className="text-muted-foreground">Total Profit</div>
                    <div className={`font-semibold flex items-center ${
                      bot.total_profit_pct >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {bot.total_profit_pct >= 0 ? (
                        <TrendingUp className="h-3 w-3 mr-1" />
                      ) : (
                        <TrendingDown className="h-3 w-3 mr-1" />
                      )}
                      {formatPercentage(bot.total_profit_pct)}
                    </div>
                  </div>
                  
                  <div>
                    <div className="text-muted-foreground">Total Trades</div>
                    <div className="font-semibold">{bot.total_trades}</div>
                  </div>
                  
                  <div>
                    <div className="text-muted-foreground">Win Rate</div>
                    <div className="font-semibold">
                      {bot.total_trades > 0 
                        ? formatPercentage((bot.winning_trades / bot.total_trades) * 100)
                        : '0%'
                      }
                    </div>
                  </div>
                  
                  <div>
                    <div className="text-muted-foreground">Exchange</div>
                    <div className="font-semibold capitalize">{bot.exchange}</div>
                  </div>
                </div>

                {/* Trading Pairs */}
                <div>
                  <div className="text-sm text-muted-foreground mb-2">Trading Pairs</div>
                  <div className="flex flex-wrap gap-1">
                    {bot.symbols.slice(0, 3).map((symbol) => (
                      <Badge key={symbol} variant="outline" className="text-xs">
                        {symbol.split('/')[0]}
                      </Badge>
                    ))}
                    {bot.symbols.length > 3 && (
                      <Badge variant="outline" className="text-xs">
                        +{bot.symbols.length - 3} more
                      </Badge>
                    )}
                  </div>
                </div>

                {/* Creation Date */}
                <div className="text-xs text-muted-foreground">
                  Created {formatDate(bot.created_at)}
                </div>

                {/* Action Buttons */}
                <div className="flex gap-2 pt-2">
                  {bot.status === BotStatus.RUNNING ? (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleStopBot(bot.uuid)}
                      className="flex-1"
                    >
                      <Square className="mr-2 h-3 w-3" />
                      Stop
                    </Button>
                  ) : (
                    <Button
                      size="sm"
                      onClick={() => handleStartBot(bot.uuid)}
                      className="flex-1"
                    >
                      <Play className="mr-2 h-3 w-3" />
                      Start
                    </Button>
                  )}
                  
                  <Link href={`/dashboard/bots/${bot.uuid}`}>
                    <Button variant="outline" size="sm">
                      View
                    </Button>
                  </Link>
                  
                  <Button variant="outline" size="sm">
                    <Settings className="h-3 w-3" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}