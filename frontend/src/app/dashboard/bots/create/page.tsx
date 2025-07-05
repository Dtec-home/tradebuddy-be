'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import apiService from '@/services/api'
import { ArrowLeft, ArrowRight, Bot, TrendingUp, Settings, CheckCircle, X } from 'lucide-react'

interface BotFormData {
  name: string
  description: string
  exchange: string
  symbols: string[]
  strategy_type: string
  mode: string
}

const AVAILABLE_SYMBOLS = [
  'HYPE/USDT:USDT',
  'NEAR/USDT:USDT',
  'BTC/USDT:USDT',
  'ETH/USDT:USDT',
  'BNB/USDT:USDT',
  'SOL/USDT:USDT',
  'DOGE/USDT:USDT',
  'ADA/USDT:USDT'
]

const STRATEGY_TYPES = [
  {
    id: 'martingale',
    name: 'Martingale Strategy',
    description: 'Our proven strategy with 1.1% drop triggers and 0.56% take profit',
    features: ['Automated position sizing', 'Risk management', 'Real-time monitoring'],
    recommended: true
  },
  {
    id: 'dca',
    name: 'Dollar Cost Average',
    description: 'Regular purchases regardless of price',
    features: ['Consistent buying', 'Lower risk', 'Long-term focused'],
    recommended: false
  },
  {
    id: 'grid',
    name: 'Grid Trading',
    description: 'Buy low, sell high in price ranges',
    features: ['Range-bound markets', 'Multiple orders', 'Profit from volatility'],
    recommended: false
  }
]

export default function CreateBotPage() {
  const [currentStep, setCurrentStep] = useState(1)
  const [formData, setFormData] = useState<BotFormData>({
    name: '',
    description: '',
    exchange: 'bitget',
    symbols: ['HYPE/USDT:USDT', 'NEAR/USDT:USDT'],
    strategy_type: 'martingale',
    mode: 'paper'
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const router = useRouter()

  const handleNext = () => {
    if (currentStep < 4) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleSymbolToggle = (symbol: string) => {
    setFormData(prev => ({
      ...prev,
      symbols: prev.symbols.includes(symbol)
        ? prev.symbols.filter(s => s !== symbol)
        : [...prev.symbols, symbol]
    }))
  }

  const handleSubmit = async () => {
    setIsLoading(true)
    setError('')

    try {
      const bot = await apiService.createBot({
        name: formData.name,
        description: formData.description,
        exchange: formData.exchange,
        symbols: formData.symbols,
        strategy_type: formData.strategy_type
      })

      router.push(`/dashboard/bots/${bot.uuid}`)
    } catch (err) {
      setError('Failed to create bot. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const isStepValid = () => {
    switch (currentStep) {
      case 1:
        return formData.name.trim().length > 0
      case 2:
        return formData.strategy_type.length > 0
      case 3:
        return formData.symbols.length > 0 && formData.symbols.length <= 5
      case 4:
        return true
      default:
        return false
    }
  }

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <Bot className="mx-auto h-12 w-12 text-primary mb-4" />
              <h2 className="text-2xl font-bold">Bot Details</h2>
              <p className="text-muted-foreground">Give your trading bot a name and description</p>
            </div>

            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Bot Name *</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="e.g., My Martingale Bot"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">Description (Optional)</Label>
                <Input
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  placeholder="Brief description of your bot's purpose"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="mode">Trading Mode</Label>
                <Select
                  value={formData.mode}
                  onValueChange={(value) => setFormData(prev => ({ ...prev, mode: value }))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="paper">
                      <div className="flex items-center space-x-2">
                        <span>📄 Paper Trading</span>
                        <Badge variant="secondary">Recommended</Badge>
                      </div>
                    </SelectItem>
                    <SelectItem value="live">
                      <div className="flex items-center space-x-2">
                        <span>💰 Live Trading</span>
                        <Badge variant="outline">Real Money</Badge>
                      </div>
                    </SelectItem>
                  </SelectContent>
                </Select>
                <p className="text-sm text-muted-foreground">
                  Start with paper trading to test your strategy risk-free
                </p>
              </div>
            </div>
          </div>
        )

      case 2:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <TrendingUp className="mx-auto h-12 w-12 text-primary mb-4" />
              <h2 className="text-2xl font-bold">Choose Strategy</h2>
              <p className="text-muted-foreground">Select the trading strategy for your bot</p>
            </div>

            <div className="space-y-4">
              {STRATEGY_TYPES.map((strategy) => (
                <Card
                  key={strategy.id}
                  className={`cursor-pointer transition-all ${
                    formData.strategy_type === strategy.id
                      ? 'ring-2 ring-primary border-primary'
                      : 'hover:border-primary/50'
                  }`}
                  onClick={() => setFormData(prev => ({ ...prev, strategy_type: strategy.id }))}
                >
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="flex items-center space-x-2">
                        <span>{strategy.name}</span>
                        {strategy.recommended && (
                          <Badge variant="success">Recommended</Badge>
                        )}
                      </CardTitle>
                      {formData.strategy_type === strategy.id && (
                        <CheckCircle className="h-5 w-5 text-primary" />
                      )}
                    </div>
                    <CardDescription>{strategy.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {strategy.features.map((feature, index) => (
                        <div key={index} className="flex items-center text-sm text-muted-foreground">
                          <CheckCircle className="h-3 w-3 mr-2 text-green-500" />
                          {feature}
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )

      case 3:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <Settings className="mx-auto h-12 w-12 text-primary mb-4" />
              <h2 className="text-2xl font-bold">Select Trading Pairs</h2>
              <p className="text-muted-foreground">Choose up to 5 cryptocurrency pairs to trade</p>
            </div>

            <div className="space-y-4">
              <div className="text-sm text-muted-foreground">
                Selected: {formData.symbols.length}/5 pairs
              </div>

              <div className="grid grid-cols-2 gap-3">
                {AVAILABLE_SYMBOLS.map((symbol) => {
                  const isSelected = formData.symbols.includes(symbol)
                  const isDisabled = !isSelected && formData.symbols.length >= 5
                  
                  return (
                    <Card
                      key={symbol}
                      className={`cursor-pointer transition-all ${
                        isSelected
                          ? 'ring-2 ring-primary border-primary bg-primary/5'
                          : isDisabled
                          ? 'opacity-50 cursor-not-allowed'
                          : 'hover:border-primary/50'
                      }`}
                      onClick={() => !isDisabled && handleSymbolToggle(symbol)}
                    >
                      <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                          <span className="font-medium">{symbol.split('/')[0]}</span>
                          {isSelected && (
                            <CheckCircle className="h-4 w-4 text-primary" />
                          )}
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {symbol}
                        </div>
                      </CardContent>
                    </Card>
                  )
                })}
              </div>

              {formData.symbols.length > 0 && (
                <div className="p-4 bg-muted rounded-lg">
                  <h4 className="font-medium mb-2">Selected pairs:</h4>
                  <div className="flex flex-wrap gap-2">
                    {formData.symbols.map((symbol) => (
                      <Badge key={symbol} variant="secondary" className="flex items-center space-x-1">
                        <span>{symbol}</span>
                        <X
                          className="h-3 w-3 cursor-pointer"
                          onClick={(e) => {
                            e.stopPropagation()
                            handleSymbolToggle(symbol)
                          }}
                        />
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )

      case 4:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <CheckCircle className="mx-auto h-12 w-12 text-green-500 mb-4" />
              <h2 className="text-2xl font-bold">Review & Create</h2>
              <p className="text-muted-foreground">Review your bot configuration before creating</p>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Bot Configuration</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className="text-sm font-medium">Name</Label>
                    <p className="text-sm text-muted-foreground">{formData.name}</p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium">Mode</Label>
                    <p className="text-sm text-muted-foreground">
                      {formData.mode === 'paper' ? 'Paper Trading' : 'Live Trading'}
                    </p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium">Strategy</Label>
                    <p className="text-sm text-muted-foreground">
                      {STRATEGY_TYPES.find(s => s.id === formData.strategy_type)?.name}
                    </p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium">Exchange</Label>
                    <p className="text-sm text-muted-foreground">Bitget</p>
                  </div>
                </div>

                <div>
                  <Label className="text-sm font-medium">Trading Pairs</Label>
                  <div className="flex flex-wrap gap-2 mt-1">
                    {formData.symbols.map((symbol) => (
                      <Badge key={symbol} variant="outline">{symbol}</Badge>
                    ))}
                  </div>
                </div>

                {formData.description && (
                  <div>
                    <Label className="text-sm font-medium">Description</Label>
                    <p className="text-sm text-muted-foreground">{formData.description}</p>
                  </div>
                )}
              </CardContent>
            </Card>

            {error && (
              <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md">
                {error}
              </div>
            )}
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <Button
          variant="ghost"
          onClick={() => router.back()}
          className="flex items-center space-x-2"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back</span>
        </Button>
        <div>
          <h1 className="text-2xl font-bold">Create Trading Bot</h1>
          <p className="text-muted-foreground">Step {currentStep} of 4</p>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-muted rounded-full h-2">
        <div
          className="bg-primary h-2 rounded-full transition-all duration-300"
          style={{ width: `${(currentStep / 4) * 100}%` }}
        />
      </div>

      {/* Step Content */}
      <Card>
        <CardContent className="p-8">
          {renderStepContent()}
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex justify-between">
        <Button
          variant="outline"
          onClick={handlePrevious}
          disabled={currentStep === 1}
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Previous
        </Button>

        {currentStep === 4 ? (
          <Button onClick={handleSubmit} disabled={isLoading}>
            {isLoading ? 'Creating Bot...' : 'Create Bot'}
          </Button>
        ) : (
          <Button onClick={handleNext} disabled={!isStepValid()}>
            Next
            <ArrowRight className="h-4 w-4 ml-2" />
          </Button>
        )}
      </div>
    </div>
  )
}