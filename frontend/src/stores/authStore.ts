import { defineStore } from 'pinia'
import type { User } from '../types/User'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

export const useAuthStore = defineStore('authStore', {
  state: () => ({
    users: [] as User[],
    currentUser: null as User | null,
    isLoggedIn: false as boolean,
    token: localStorage.getItem('accessToken') as string | null,
  }),
  getters: {
    isAuthenticated: (state): boolean => {
      return state.isLoggedIn && state.currentUser?.username !== null && state.token !== null
    },
    getUsername: (state): string | null => {
      return state.currentUser ? state.currentUser.username : null
    },
  },
  actions: {
    async login(userData: User, accessToken: string) {
      this.currentUser = userData
      this.isLoggedIn = true
      this.token = accessToken
      localStorage.setItem('accessToken', accessToken)
      axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
    },
    logout() {
      this.currentUser = null
      this.isLoggedIn = false
      this.token = null
      localStorage.removeItem('accessToken')
      delete axios.defaults.headers.common['Authorization']
    },
    async initializeAuth() {
      const storedToken = localStorage.getItem('accessToken')
      if (storedToken) {
        this.token = storedToken
        axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`
        try {
          const response = await axios.get(`${API_URL}/api/auth/users/me`)
          this.currentUser = response.data
          this.isLoggedIn = true
          console.log('User initialized from stored token:', response.data)
        } catch (error) {
          console.error('Failed to initialize auth with stored token:', error)
          this.logout()
        }
      } else {
        console.log('No token found in localStorage')
      }
    },
  },
})
