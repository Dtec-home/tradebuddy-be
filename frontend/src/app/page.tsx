'use client'

import React from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ArrowRight, Bot, TrendingUp, Shield, Zap, Users, BarChart3, Sparkles } from 'lucide-react'
import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center space-x-2">
            <Bot className="h-6 w-6 text-primary" />
            <span className="text-xl font-bold">TradeBuddy</span>
          </div>
          
          <div className="flex items-center space-x-4">
            <Link href="/login">
              <Button variant="ghost">Sign In</Button>
            </Link>
            <Link href="/register">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden py-24 lg:py-32 bg-gradient-to-br from-purple-50 via-white to-blue-50">
        {/* Animated background patterns */}
        <div className="absolute inset-0 overflow-hidden">
          {/* Grid pattern */}
          <svg className="absolute inset-0 h-full w-full stroke-gray-200/50 [mask-image:radial-gradient(100%_100%_at_top_right,white,transparent)]" aria-hidden="true">
            <defs>
              <pattern id="grid-pattern" width="60" height="60" x="50%" y="-1" patternUnits="userSpaceOnUse">
                <path d="M.5 60V.5H60" fill="none" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" strokeWidth="0" fill="url(#grid-pattern)" />
          </svg>
          
          {/* Floating shapes */}
          <div className="absolute -top-40 -right-32 h-80 w-80 rounded-full bg-purple-300 opacity-20 blur-3xl animate-float"></div>
          <div className="absolute -bottom-40 -left-32 h-80 w-80 rounded-full bg-blue-300 opacity-20 blur-3xl animate-float" style={{animationDelay: '2s'} as React.CSSProperties}></div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-96 w-96 rounded-full bg-indigo-300 opacity-10 blur-3xl animate-glow"></div>
          
          {/* Trading symbols floating */}
          <div className="absolute top-20 left-20 text-purple-300/30 animate-float" style={{animationDelay: '1s'} as React.CSSProperties}>
            <svg className="h-8 w-8" fill="currentColor" viewBox="0 0 20 20">
              <path d="M4 4a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2H4zm12 2v4l-3-2-3 2V6h6z"/>
            </svg>
          </div>
          <div className="absolute top-32 right-32 text-blue-300/30 animate-float" style={{animationDelay: '3s'} as React.CSSProperties}>
            <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/>
            </svg>
          </div>
          <div className="absolute bottom-32 left-1/3 text-green-300/30 animate-float" style={{animationDelay: '4s'} as React.CSSProperties}>
            <svg className="h-7 w-7" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z"/>
            </svg>
          </div>
          
          {/* Animated dots */}
          <svg className="absolute inset-0 h-full w-full" aria-hidden="true">
            <defs>
              <pattern id="dots-pattern" width="20" height="20" patternUnits="userSpaceOnUse">
                <circle cx="2" cy="2" r="1" fill="currentColor" className="text-purple-300/40" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#dots-pattern)" />
          </svg>
        </div>
        <div className="container relative">
          <div className="mx-auto max-w-4xl text-center">
            <div className="mb-6 inline-flex items-center rounded-full border border-gray-200 bg-white px-3 py-1 text-sm">
              <Sparkles className="mr-2 h-3 w-3 text-purple-600" />
              Powered by Advanced AI Trading
            </div>
            
            <h1 className="text-5xl font-bold leading-tight tracking-tighter text-gray-900 sm:text-6xl md:text-7xl">
              Trading Bots
              <br />
              <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                as a Service
              </span>
            </h1>
            
            <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground">
              Create, deploy, and manage automated cryptocurrency trading bots with our powerful platform. 
              No coding required. Start with our proven martingale strategy.
            </p>
            
            <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:justify-center">
              <button 
                onClick={() => {
                  window.location.href = 'http://localhost:8000/api/v1/auth/google/login'
                }}
                className="inline-flex items-center justify-center px-8 py-4 text-base font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors shadow-lg"
              >
                <svg className="w-5 h-5 mr-3" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Get Started with Google
              </button>
              <Link href="/login">
                <button className="inline-flex items-center justify-center px-8 py-4 text-base font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                  Sign in with Email
                </button>
              </Link>
            </div>
            
            <div className="mt-8 flex items-center justify-center space-x-6 text-sm text-muted-foreground">
              <div className="flex items-center space-x-2">
                <Shield className="h-4 w-4 text-green-500" />
                <span>Bank-level Security</span>
              </div>
              <div className="flex items-center space-x-2">
                <Zap className="h-4 w-4 text-yellow-500" />
                <span>Lightning Fast</span>
              </div>
              <div className="flex items-center space-x-2">
                <Users className="h-4 w-4 text-blue-500" />
                <span>10k+ Users</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="relative border-t py-24 bg-white">
        {/* Subtle background pattern */}
        <div className="absolute inset-0 opacity-5">
          <svg className="h-full w-full" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern id="feature-pattern" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M0 20L20 0L40 20L20 40Z" stroke="currentColor" strokeWidth="1" fill="none" className="text-gray-400"/>
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#feature-pattern)" />
          </svg>
        </div>
        
        <div className="container relative">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Why Choose TradeBuddy?
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Everything you need to succeed in automated cryptocurrency trading
            </p>
          </div>
          
          <div className="mx-auto mt-16 grid max-w-6xl grid-cols-1 gap-8 md:grid-cols-3">
            <Card className="relative overflow-hidden border-2 transition-all hover:shadow-lg hover:shadow-purple-500/10 group">
              {/* Card background glow */}
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500/5 to-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <CardHeader className="relative">
                <div className="flex h-16 w-16 items-center justify-center rounded-xl bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg">
                  <svg className="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                  </svg>
                </div>
                <CardTitle className="text-xl">Automated Trading</CardTitle>
                <CardDescription>
                  Deploy sophisticated trading strategies including our proven martingale system with 99.2% uptime
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center">
                    <div className="mr-2 h-1 w-1 rounded-full bg-primary" />
                    Martingale Strategy (Recommended)
                  </li>
                  <li className="flex items-center">
                    <div className="mr-2 h-1 w-1 rounded-full bg-primary" />
                    DCA & Grid Trading
                  </li>
                  <li className="flex items-center">
                    <div className="mr-2 h-1 w-1 rounded-full bg-primary" />
                    Custom Strategy Builder
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="relative overflow-hidden border-2 transition-all hover:shadow-lg hover:shadow-green-500/10 group">
              <div className="absolute inset-0 bg-gradient-to-r from-green-500/5 to-emerald-500/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <CardHeader className="relative">
                <div className="flex h-16 w-16 items-center justify-center rounded-xl bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-lg">
                  <svg className="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/>
                  </svg>
                </div>
                <CardTitle className="text-xl">Real-time Analytics</CardTitle>
                <CardDescription>
                  Monitor your bot performance with live P&L tracking, detailed analytics, and performance insights
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center">
                    <div className="mr-2 h-1 w-1 rounded-full bg-primary" />
                    Live P&L Dashboard
                  </li>
                  <li className="flex items-center">
                    <div className="mr-2 h-1 w-1 rounded-full bg-primary" />
                    Performance Charts
                  </li>
                  <li className="flex items-center">
                    <div className="mr-2 h-1 w-1 rounded-full bg-primary" />
                    Risk Management Tools
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="relative overflow-hidden border-2 transition-all hover:shadow-lg hover:shadow-orange-500/10 group">
              <div className="absolute inset-0 bg-gradient-to-r from-orange-500/5 to-red-500/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <CardHeader className="relative">
                <div className="flex h-16 w-16 items-center justify-center rounded-xl bg-gradient-to-r from-orange-500 to-red-500 text-white shadow-lg">
                  <svg className="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                  </svg>
                </div>
                <CardTitle className="text-xl">Secure & Reliable</CardTitle>
                <CardDescription>
                  Enterprise-grade security with encrypted API keys, isolated bot instances, and 24/7 monitoring
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center">
                    <div className="mr-2 h-1 w-1 rounded-full bg-primary" />
                    Bank-level Encryption
                  </li>
                  <li className="flex items-center">
                    <div className="mr-2 h-1 w-1 rounded-full bg-primary" />
                    Isolated Bot Instances
                  </li>
                  <li className="flex items-center">
                    <div className="mr-2 h-1 w-1 rounded-full bg-primary" />
                    24/7 System Monitoring
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="relative border-t bg-gradient-to-r from-gray-900 to-gray-800 py-24 text-white overflow-hidden">
        {/* Animated background */}
        <div className="absolute inset-0 opacity-10">
          <svg className="h-full w-full" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern id="stats-pattern" width="100" height="100" patternUnits="userSpaceOnUse">
                <circle cx="50" cy="50" r="2" fill="currentColor" />
                <circle cx="10" cy="10" r="1" fill="currentColor" />
                <circle cx="90" cy="20" r="1.5" fill="currentColor" />
                <circle cx="20" cy="90" r="1" fill="currentColor" />
                <circle cx="80" cy="80" r="1.5" fill="currentColor" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#stats-pattern)" />
          </svg>
        </div>
        
        {/* Gradient overlays */}
        <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 to-blue-600/20"></div>
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        
        <div className="container relative">
          <div className="mx-auto grid max-w-6xl grid-cols-2 gap-8 md:grid-cols-4">
            <div className="text-center group">
              <div className="text-4xl font-bold text-white group-hover:text-purple-300 transition-colors">10,000+</div>
              <div className="text-sm text-gray-300">Active Users</div>
            </div>
            <div className="text-center group">
              <div className="text-4xl font-bold text-white group-hover:text-green-300 transition-colors">$2.5M+</div>
              <div className="text-sm text-gray-300">Trading Volume</div>
            </div>
            <div className="text-center group">
              <div className="text-4xl font-bold text-white group-hover:text-blue-300 transition-colors">99.2%</div>
              <div className="text-sm text-gray-300">Uptime</div>
            </div>
            <div className="text-center group">
              <div className="text-4xl font-bold text-white group-hover:text-orange-300 transition-colors">24/7</div>
              <div className="text-sm text-gray-300">Support</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="border-t py-24">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Ready to Start Trading?
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Join thousands of traders who trust TradeBuddy for automated cryptocurrency trading
            </p>
            <div className="mt-8">
              <button 
                onClick={() => {
                  window.location.href = 'http://localhost:8000/api/v1/auth/google/login'
                }}
                className="inline-flex items-center justify-center px-8 py-4 text-lg font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors shadow-lg"
              >
                <svg className="w-5 h-5 mr-3" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Get Started Free with Google
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-12">
        <div className="container">
          <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
            <div className="flex items-center space-x-2">
              <Bot className="h-5 w-5 text-primary" />
              <span className="font-semibold">TradeBuddy</span>
            </div>
            <p className="text-center text-sm text-muted-foreground">
              © 2024 TradeBuddy. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </main>
  )
}