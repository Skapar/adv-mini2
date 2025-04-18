import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../services/api'
import toast from 'react-hot-toast'
import PageContainer from '../components/PageContainer'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    try {
      const response = await login({ username, password })
      console.log('Login response:', response.data)
      localStorage.setItem('token', response.data.access)
      toast.success('Successfully logged in!')
      navigate('/')
    } catch (error: any) {
      console.error('Login error:', error.response?.data || error.message)
      setError(
        error.response?.data?.detail || 
        error.message || 
        'Failed to login. Please check your credentials and try again.'
      )
    }
  }

  useEffect(() => {
    if (error) {
      toast.error(error)
    }
  }, [error])

  return (
    <PageContainer title="Welcome Back">
      <div className="max-w-md mx-auto">
        <form 
          onSubmit={handleSubmit}
          className="space-y-6"
        >
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Username
            </label>
            <div className="relative">
              <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                placeholder="Enter your username"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
              placeholder="••••••••"
            />
          </div>

          {error && (
            <div className="text-red-600 bg-red-50 p-3 rounded-lg">
              ⚠️ {error}
            </div>
          )}

          <button
            type="submit"
            className="w-full bg-teal-600 hover:bg-teal-700 text-white font-medium py-3 px-4 rounded-lg transition-all"
          >
            Sign In
          </button>
        </form>
      </div>
    </PageContainer>
  )
}