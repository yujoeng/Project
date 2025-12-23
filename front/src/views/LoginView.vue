<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()

// 입력 값과 에러 메시지 상태 변수 
const username = ref('')
const password = ref('')
const errorMessage = ref('')

// 로그인 처리 함수 
const login = async () => {
  errorMessage.value = '' // 에러 메시지 초기화 

  try {
    // const res = await axios.post('accounts/login/', {
      // username: username.value,
      // password: password.value,
    // })
    await authStore.loginUser(username.value, password.value)

    // // Pinia에 토큰 저장
    // authStore.setToken(res.data.access)

    // 로그인 성공 후 이동
    router.push('/')
  } catch (err) {
    console.error(err)

    // 비밀번호 오류 시 
    if (err.response && err. response.status === 401) {
      errorMessage.value = '가입되지 않은 계정이거나 비밀번호가 틀렸습니다.'
    } else {
      // 그 외 오류 발생 시
      errorMessage.value = authStore.errorMessage || '로그인에 실패했습니다.'
    }
  }
}
</script>

<template>
  <div class="login-page">
    <h1>로그인</h1>

    
    <input v-model="username" placeholder="아이디" />
    <input v-model="password" type="password" placeholder="비밀번호" />

    <button @click="login">로그인</button>

    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<style scoped>
/* 로그인 페이지 스타일링 (선택 사항) */
.login-page {
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
</style>