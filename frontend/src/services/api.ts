import { AuthResponse, LoginRequest, RegisterRequest, User, Bot, CreateBotRequest } from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class ApiService {
  private baseUrl: string
  private token: string | null = null

  constructor() {
    this.baseUrl = `${API_BASE_URL}/api/v1`
    // Try to get token from localStorage on client side
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('token')
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }

    // Merge existing headers if they exist and are an object
    if (options.headers && typeof options.headers === 'object' && !Array.isArray(options.headers)) {
      Object.assign(headers, options.headers)
    }

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`
    }

    const response = await fetch(url, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const error = await response.text()
      throw new Error(`API Error: ${response.status} - ${error}`)
    }

    return response.json()
  }

  setToken(token: string) {
    this.token = token
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', token)
    }
  }

  clearToken() {
    this.token = null
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token')
    }
  }

  // Auth endpoints
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    const response = await fetch(`${this.baseUrl}/auth/login`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error('Invalid credentials')
    }

    const data = await response.json()
    this.setToken(data.access_token)
    return data
  }

  async register(userData: RegisterRequest): Promise<User> {
    return this.request<User>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    })
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('/users/me')
  }

  // Bot endpoints
  async getBots(): Promise<Bot[]> {
    return this.request<Bot[]>('/bots')
  }

  async getBot(botId: string): Promise<Bot> {
    return this.request<Bot>(`/bots/${botId}`)
  }

  async createBot(botData: CreateBotRequest): Promise<Bot> {
    return this.request<Bot>('/bots', {
      method: 'POST',
      body: JSON.stringify(botData),
    })
  }

  async startBot(botId: string): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/bots/${botId}/start`, {
      method: 'POST',
    })
  }

  async stopBot(botId: string): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/bots/${botId}/stop`, {
      method: 'POST',
    })
  }

  // Trading endpoints
  async getTradingStatus(): Promise<any> {
    return this.request<any>('/trading/status')
  }

  async getBalance(): Promise<any> {
    return this.request<any>('/trading/balance')
  }

  async getPositions(): Promise<any> {
    return this.request<any>('/trading/positions')
  }
}

export const apiService = new ApiService()
export default apiService