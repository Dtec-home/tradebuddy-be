'use client'

import { useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Card, CardContent } from '@/components/ui/card'
import { Loader2 } from 'lucide-react'
import apiService from '@/services/api'

export default function AuthCallbackPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  
  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code')
      
      if (!code) {
        console.error('No authorization code found')
        router.push('/login?error=no_code')
        return
      }
      
      try {
        // Send code to backend
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/api/v1/auth/google/callback`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ code }),
        })
        
        if (!response.ok) {
          throw new Error('Failed to authenticate with Google')
        }
        
        const data = await response.json()
        
        // Store token and user data
        apiService.setToken(data.access_token)
        if (data.user) {
          localStorage.setItem('user', JSON.stringify(data.user))
        }
        
        // Redirect to dashboard
        router.push('/dashboard')
      } catch (error) {
        console.error('OAuth callback error:', error)
        router.push('/login?error=auth_failed')
      }
    }
    
    handleCallback()
  }, [searchParams, router])
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <Card className="w-full max-w-md">
        <CardContent className="pt-6">
          <div className="flex flex-col items-center space-y-4">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
            <h2 className="text-xl font-semibold">Authenticating...</h2>
            <p className="text-sm text-muted-foreground text-center">
              Please wait while we complete your sign in with Google
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}