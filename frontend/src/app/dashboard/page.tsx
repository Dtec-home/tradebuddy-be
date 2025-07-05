'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Bot, BotStatus } from '@/types'
import apiService from '@/services/api'
import { formatCurrency, formatPercentage } from '@/lib/utils'
import { Plus, Play, Square, TrendingUp, TrendingDown, DollarSign, Bot as BotIcon } from 'lucide-react'

export default function DashboardPage() {
  const [bots, setBots] = useState<Bot[]>([])
  const [stats, setStats] = useState({
    totalBots: 0,
    activeBots: 0,
    totalProfit: 0,
    totalTrades: 0
  })
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const [botsData, balance] = await Promise.all([
        apiService.getBots(),
        apiService.getBalance().catch(() => ({ balance: 0 }))
      ])
      
      setBots(botsData)
      
      // Calculate stats
      const totalProfit = botsData.reduce((sum, bot) => sum + bot.total_profit_pct, 0)
      const totalTrades = botsData.reduce((sum, bot) => sum + bot.total_trades, 0)
      const activeBots = botsData.filter(bot => bot.status === BotStatus.RUNNING).length
      
      setStats({
        totalBots: botsData.length,
        activeBots,
        totalProfit,
        totalTrades
      })
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleStartBot = async (botId: string) => {
    try {
      await apiService.startBot(botId)
      loadDashboardData() // Refresh data
    } catch (error) {
      console.error('Error starting bot:', error)
    }
  }

  const handleStopBot = async (botId: string) => {
    try {
      await apiService.stopBot(botId)
      loadDashboardData() // Refresh data
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

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Loading dashboard...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">
            Manage your trading bots and monitor performance
          </p>
        </div>
        <Link href="/dashboard/bots/create">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Create Bot
          </Button>
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Bots</CardTitle>
            <BotIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalBots}</div>
            <p className="text-xs text-muted-foreground">
              {stats.activeBots} active
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Profit</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatPercentage(stats.totalProfit)}
            </div>
            <p className="text-xs text-muted-foreground">
              Across all bots
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Trades</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalTrades}</div>
            <p className="text-xs text-muted-foreground">
              Executed trades
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Win Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {stats.totalTrades > 0 
                ? formatPercentage(
                    (bots.reduce((sum, bot) => sum + bot.winning_trades, 0) / stats.totalTrades) * 100
                  )
                : '0%'
              }
            </div>
            <p className="text-xs text-muted-foreground">
              Success rate
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Bots List */}
      <div>
        <h2 className="text-2xl font-bold tracking-tight mb-4">Your Bots</h2>
        
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
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {bots.map((bot) => (
              <Card key={bot.uuid}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{bot.name}</CardTitle>
                    {getBotStatusBadge(bot.status)}
                  </div>
                  <CardDescription>
                    {bot.description || `${bot.strategy_type} strategy`}
                  </CardDescription>
                </CardHeader>
                
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Symbols:</span>
                      <span className="font-mono">{bot.symbols.join(', ')}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Profit:</span>
                      <span className={`font-semibold ${
                        bot.total_profit_pct >= 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {formatPercentage(bot.total_profit_pct)}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Trades:</span>
                      <span>{bot.total_trades}</span>
                    </div>
                  </div>
                  
                  <div className="flex gap-2 mt-4">
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
                    <Button variant="outline" size="sm">
                      View
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}