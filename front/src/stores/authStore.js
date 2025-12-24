import { defineStore } from 'pinia'
import apiClient from '@/api/axios'  
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || '')
  const username = ref(localStorage.getItem('username') || '')  // 👈 수정: localStorage에서 복원
  const errorMessage = ref('')
  const isLogin = ref(!!token.value)

  // 로그인 상태에서 사용자 정보 가져오기
  const fetchUser = async () => {
    if (!token.value) return
    try {
      const response = await apiClient.get('/accounts/me/')  
      username.value = response.data.username
      localStorage.setItem('username', response.data.username)  // 👈 추가
      isLogin.value = true
      
      console.log('✅ 사용자 정보 저장:', username.value)  // 👈 추가 (디버깅)
    } catch (error) {
      console.error('사용자 정보 가져오기 실패:', error)
      
      if (error.response?.status === 401) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('username')  // 👈 추가
        token.value = ''
        username.value = ''
        isLogin.value = false
      }
    }
  }

  // 로그인 요청 함수
  const loginUser = async (loginUsername, password) => {  // 👈 수정: 파라미터명 변경
    try {
      const response = await apiClient.post('/accounts/login/', {  
        username: loginUsername,  // 👈 수정
        password,
      })
      token.value = response.data.access
      localStorage.setItem('access_token', token.value)
      isLogin.value = true
      
      // 👇 추가: 로그인 후 사용자 정보 가져오기
      await fetchUser()
      
      console.log('✅ 로그인 성공! 사용자:', username.value)  // 👈 추가 (디버깅)
      
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || '로그인 실패'
      throw new Error('로그인 실패: ' + error.response?.data?.detail || '알 수 없는 오류')
    }
  }

  // 로그아웃 요청 함수
  const logoutUser = async () => {
    try {
      await apiClient.post('/accounts/logout/')  
    } catch (error) {
      console.error('로그아웃 실패', error)
    } finally {
      localStorage.removeItem('access_token')
      localStorage.removeItem('username')  // 👈 추가
      token.value = ''
      username.value = ''
      isLogin.value = false
    }
  }

  // 회원가입 요청 함수
  const signupUser = async (signupUsername, password1, password2) => {  // 👈 수정: 파라미터명 변경
    try {
      if (password1 !== password2) {
        errorMessage.value = '비밀번호가 일치하지 않습니다.'
        throw new Error('비밀번호가 일치하지 않습니다.')
      }

      const response = await apiClient.post('/accounts/signup/', {  
        username: signupUsername,  // 👈 수정
        password: password1,
        password2: password2,
      })
      return response
    } catch (error) {
      console.error("회원가입 실패:", error)

      if (error.response) {
        if (error.response.data.password) {
          errorMessage.value = error.response.data.password[0]
        } else if (error.response.data.password2) {
          errorMessage.value = error.response.data.password2[0]
        } else if (error.response.data.username) {
          errorMessage.value = error.response.data.username[0]
        } else if (error.response.status === 400) {
          errorMessage.value = error.response.data.detail || '회원가입에 실패했습니다.'
        } else {
          errorMessage.value = error.response.data.detail || '회원가입에 실패했습니다.'
        }
      } else {
        errorMessage.value = '회원가입 중 알 수 없는 오류가 발생했습니다.'
      }
      throw new Error('회원가입 실패: ' + (error.response?.data?.detail || errorMessage.value))
    }
  }
  
  // 👇 추가: 앱 초기화 시 사용자 정보 복원
  const initializeAuth = async () => {
    if (token.value && !username.value) {
      console.log('🔄 사용자 정보 복원 중...')
      await fetchUser()
    }
  }

  return {
    token,
    username,
    errorMessage,
    isLogin,
    loginUser,
    logoutUser,
    signupUser,
    fetchUser,
    initializeAuth,  // 👈 추가
  }
})