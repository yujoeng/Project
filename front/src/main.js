import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import './assets/main.css'
import App from './App.vue'
import router from './router/index.js'
import { useAuthStore } from './stores/authStore'  // 👈 추가

const app = createApp(App)
const pinia = createPinia()
    
app.use(pinia)
app.use(router)

// 👇 추가: 앱 시작 전 인증 상태 초기화
const authStore = useAuthStore()
authStore.initializeAuth().then(() => {
  app.mount('#app')
})
