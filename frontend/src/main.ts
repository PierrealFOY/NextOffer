import { createApp } from 'vue'
import { MotionPlugin } from '@vueuse/motion'
import App from './App.vue'
import './index.css'
import { createWebHistory, createRouter } from 'vue-router'
import { createPinia } from 'pinia'
import { useAuthStore } from './stores/authStore'
import { routes } from './routes/routes'

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)

const authStore = useAuthStore()

authStore.initializeAuth().finally(() => {
  app.use(router)
  app.use(MotionPlugin)
  app.mount('#app')
})
