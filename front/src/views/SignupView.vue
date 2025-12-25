import { handleApiError } from '@/utils/errorHandler'

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const password1 = ref('')
const password2 = ref('')
const errorMessage = ref('')
const successMessage = ref('')

const signup = async () => {
  // 초기화
  errorMessage.value = ''
  successMessage.value = ''

  // 입력 검증
  if (!username.value.trim()) {
    errorMessage.value = '아이디를 입력해주세요.'
    return
  }

  if (!password1.value) {
    errorMessage.value = '비밀번호를 입력해주세요.'
    return
  }

  if (!password2.value) {
    errorMessage.value = '비밀번호 확인을 입력해주세요.'
    return
  }

  if (password1.value !== password2.value) {
    errorMessage.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  if (password1.value.length < 8) {
    errorMessage.value = '비밀번호는 최소 8자 이상이어야 합니다.'
    return
  }

  try {
    await authStore.signupUser(username.value, password1.value, password2.value)

    successMessage.value = '회원가입에 성공했습니다. 로그인 페이지로 이동합니다.'
    
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err) {
    console.error(err)
    
    if (err.response) {
      const data = err.response.data
      
      // 백엔드 에러 메시지 우선
      if (data.password) {
        errorMessage.value = data.password[0]
      } else if (data.password2) {
        errorMessage.value = data.password2[0]
      } else if (data.username) {
        errorMessage.value = data.username[0]
      } else if (data.detail) {
        errorMessage.value = data.detail
      } else if (err.response.status === 400) {
        errorMessage.value = '이미 가입된 아이디입니다.'
      } else {
        errorMessage.value = '회원가입에 실패했습니다.'
      }
    } else if (err.request) {
      errorMessage.value = '서버에 연결할 수 없습니다.'
    } else {
      errorMessage.value = '회원가입 처리 중 오류가 발생했습니다.'
    }
  }
}
</script>

<template>
  <div class="signup-page">
    <h1>회원가입</h1>

    <!-- 아이디 입력 -->
    <input v-model="username" placeholder="아이디" />
    
    <!-- 비밀번호 입력 -->
    <input v-model="password1" type="password" placeholder="비밀번호" />
    
    <!-- 비밀번호 확인 입력 -->
    <input v-model="password2" type="password" placeholder="비밀번호 확인" />
    
    <!-- 회원가입 버튼 -->
    <button @click="signup">회원가입</button>
    
    <!-- 오류 메시지 -->
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <!-- 성공 메시지 -->
    <p v-if="successMessage" class="success-message">{{ successMessage }}</p> 
  </div>
</template>


<style scoped>
.signup-page {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}
input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 10px 20px;
  background-color: #7b10adff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #7b10adff;
}
.error-message {
  color: red;
  margin-top: 10px;
}

.success-message {
  color: green;
  margin-top: 10px;
  font-weight: bold;
}
</style>