'use client'

import { useState, useEffect, createContext, useContext } from 'react'
import { User, LoginRequest, RegisterRequest } from '@/types'
import apiService from '@/services/api'
import websocketService from '@/services/websocket'

interface AuthContextType {
  user: User | null
  isLoading: boolean
  login: (credentials: LoginRequest) => Promise<void>
  register: (userData: RegisterRequest) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export function useAuthState() {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('token')
        if (token) {
          apiService.setToken(token)
          const currentUser = await apiService.getCurrentUser()
          setUser(currentUser)
          
          // Connect to WebSocket
          websocketService.connect(token)
        }
      } catch (error) {
        console.error('Auth check failed:', error)
        apiService.clearToken()
      } finally {
        setIsLoading(false)
      }
    }

    checkAuth()
  }, [])

  const login = async (credentials: LoginRequest) => {
    setIsLoading(true)
    try {
      const authResponse = await apiService.login(credentials)
      const currentUser = await apiService.getCurrentUser()
      setUser(currentUser)
      
      // Connect to WebSocket
      websocketService.connect(authResponse.access_token)
    } finally {
      setIsLoading(false)
    }
  }

  const register = async (userData: RegisterRequest) => {
    setIsLoading(true)
    try {
      await apiService.register(userData)
      // After registration, user needs to login
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    setUser(null)
    apiService.clearToken()
    websocketService.disconnect()
  }

  return {
    user,
    isLoading,
    login,
    register,
    logout,
    isAuthenticated: !!user
  }
}