import axios from 'axios'
import { API_BASE_URL } from './config'

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
    // 401 에러 시 자동 로그아웃
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient