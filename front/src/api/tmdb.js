// src/api/tmdb.js
import axios from "axios"
import { useAuthStore } from "@/stores/authStore"

const tmdb = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
})

tmdb.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  const token = authStore.token

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

tmdb.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default tmdb