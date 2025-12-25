import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import './assets/main.css'
import App from './App.vue'
import router from './router/index.js'
import { useAuthStore } from './stores/authStore'  

const app = createApp(App)
const pinia = createPinia()
    
app.use(pinia)
app.use(router)


const authStore = useAuthStore()
authStore.initializeAuth().then(() => {
  app.mount('#app')
})
