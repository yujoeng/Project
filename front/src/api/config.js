export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

export const API_ENDPOINTS = {
  ACCOUNTS: {
    SIGNUP: `${API_BASE_URL}/accounts/signup/`,
    LOGIN: `${API_BASE_URL}/accounts/login/`,
    LOGOUT: `${API_BASE_URL}/accounts/logout/`,
    ME: `${API_BASE_URL}/accounts/me/`,
  },
  MOVIES: {
    LIST: `${API_BASE_URL}/movies/`,
    DETAIL: (id) => `${API_BASE_URL}/movies/${id}/`,
  }
}