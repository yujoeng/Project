import { defineStore } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || '')
  const username = ref('')
  const errorMessage = ref('')
  const isLogin = ref(!!token.value)

  // 로그인 상태에서 사용자 정보 가져오기
  const fetchUser = async () => {
    if (!token.value) return
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/accounts/me/', {
        headers: { Authorization: `Bearer ${token.value}` }
      })
      username.value = response.data.username
      isLogin.value = true
    } catch (error) {
      console.error('사용자 정보 가져오기 실패:', error)
      isLogin.value = false
    }
  }

  // 로그인 요청 함수
  const loginUser = async (username, password) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/accounts/login/', {
        username,
        password,
      })
      token.value = response.data.access
      localStorage.setItem('access_token', token.value)
      isLogin.value = true
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || '로그인 실패'
      throw new Error('로그인 실패: ' + error.response?.data?.detail || '알 수 없는 오류')
    }
  }

  // 로그아웃 요청 함수
const logoutUser = async () => {
  try {
    // 백엔드 로그아웃 API 호출 (선택사항)
    await axios.post('http://127.0.0.1:8000/api/accounts/logout/', {}, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
  } catch (error) {
    console.error('로그아웃 API 호출 실패:', error)
    // API 실패해도 계속 진행
  } finally {
    // 클라이언트 측 로그아웃 처리 (필수)
    localStorage.removeItem('access_token')
    token.value = ''
    username.value = ''
    isLogin.value = false
  }
}

  // 회원가입 요청 함수
  const signupUser = async (username, password1, password2) => {
    try {
      if (password1 !== password2) {
        errorMessage.value = '비밀번호가 일치하지 않습니다.'
        throw new Error('비밀번호가 일치하지 않습니다.')
      }

      const response = await axios.post('http://127.0.0.1:8000/api/accounts/signup/', {
        username,
        password: password1,
        password2: password2,
      })
      return response
    } catch (error) {
      console.error("회원가입 실패:", error)

      // **서버에서 받은 응답 에러 처리**
      if (error.response) {
        if (error.response.data.password) {
          errorMessage.value = error.response.data.password[0]  // 비밀번호 관련 에러
        } else if (error.response.status === 400) {
          errorMessage.value = error.response.data.detail || '이미 가입된 아이디입니다.'
        } else {
          errorMessage.value = error.response.data.detail || '회원가입에 실패했습니다.'
        }
      } else {
        errorMessage.value = '회원가입 중 알 수 없는 오류가 발생했습니다.'
      }
      throw new Error('회원가입 실패: ' + error.response?.data?.detail || '알 수 없는 오류')
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
    fetchUser, // fetchUser 함수 추가
  }
})
