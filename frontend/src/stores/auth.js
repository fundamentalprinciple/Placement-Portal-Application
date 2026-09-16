import { defineStore } from 'pinia'
import { API_BASE_URL } from '@/config/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('Authentication-Token') || '',
    username: localStorage.getItem('username') || '',
    isAuthenticated: !!localStorage.getItem('Authentication-Token'),
    role: '',
    name: '',
  }),
  actions: {
    async authenticate() {
      this.token = localStorage.getItem('Authentication-Token') || ''
      this.username = localStorage.getItem('username') || ''
      if (this.username && this.token) {
        try {
          const response = await fetch(`${API_BASE_URL}/api/authenticate`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authentication-Token': this.token
            },
            body: JSON.stringify({ username: this.username })
          })
          if (!response.ok) throw new Error()
          const authData = await response.json()
          this.name = authData.name
          this.role = authData.role
          this.isAuthenticated = true
        } catch (err) {
          this.isAuthenticated = false
          this.role = ''
          this.name = ''
        }
      } else {
        this.isAuthenticated = false
      }
    },
    login({ token, username }) {
      this.token = token
      this.username = username
      this.isAuthenticated = true
      localStorage.setItem('Authentication-Token', token)
      localStorage.setItem('username', username)
    },
    logout() {
      this.token = ''
      this.username = ''
      this.role = ''
      this.name = ''
      this.isAuthenticated = false
      localStorage.removeItem('Authentication-Token')
      localStorage.removeItem('username')
    }
  }
})
