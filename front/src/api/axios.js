import axios from 'axios'
import { useRouter } from 'vue-router'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
})

// 요청 인터셉터
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    //  로그인/회원가입 API는 401 처리 제외
    const isAuthEndpoint = 
      error.config?.url?.includes('/login/') || 
      error.config?.url?.includes('/signup/')
    
    if (error.response?.status === 401 && !isAuthEndpoint) {
      // 토큰 만료 등의 경우에만 자동 로그아웃
      localStorage.removeItem('access_token')
      
      // 현재 경로가 로그인/회원가입이 아닐 때만 리다이렉트
      if (!window.location.pathname.includes('/login') && 
          !window.location.pathname.includes('/signup')) {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient