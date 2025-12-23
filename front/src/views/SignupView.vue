import { handleApiError } from '@/utils/errorHandler'

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
const router = useRouter()


const username = ref('')
const password1 = ref('')
const password2 = ref('')
const errorMessage = ref('')
const successMessage = ref('')


const usernameError = ref('')  // 아이디 오류 메시지
const password1Error = ref('') // 비밀번호1 오류 메시지
const password2Error = ref('') // 비밀번호2 오류 메시지

const signup = async () => {
  // 초기화
  usernameError.value = ''
  password1Error.value = ''
  password2Error.value = ''
  errorMessage.value = ''

  // 필드 검증
  let isValid = true;

  // 빈 값 체크
  if (!username.value) {
    usernameError.value = '아이디를 입력해주세요.'
    isValid = false;
  }

  if (!password1.value) {
    password1Error.value = '비밀번호를 입력해주세요.'
    isValid = false;
  }

  if (!password2.value) {
    password2Error.value = '비밀번호 확인을 입력해주세요.'
    isValid = false;
  }

  // 비밀번호 일치 여부 확인 
  if (password1.value !== password2.value) {
    errorMessage.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  if (password1.value.length < 8) {
    errorMessage.value = '비밀번호는 최소 8자 이상이어야 합니다.'
    isValid = false;
  }

  if (!isValid) {
    return; // 유효하지 않으면 계속 진행하지 않음
  }

  try {
    // const res = await axios.post('accounts/signup/', {
    //   username: username.value,
    //   password1: password1.value,
    //   password2: password2.value,
    // })

    // **authStore에서 signupUser 호출**
    await authStore.signupUser(username.value, password1.value, password2.value)

    successMessage.value = '회원가입에 성공했습니다. 로그인 페이지로 이동합니다.'
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err) {
      // ✅ 간결해진 에러 처리
    errorMessage.value = handleApiError(error)
    console.error(error)
    
    // if (err.response && err.response.data.password){
    //   // 백에서 반환된 비밀번호 관련 에러 메시지 출력
    //   errorMessage.value = err.response.data.password[0]    
    // } else if (err.response && err.response.status === 400) {
    //   errorMessage.value = '이미 가입된 아이디입니다.'
    // } else {
    //   errorMessage.value = '회원가입에 실패했습니다. 다시 시도해주세요.'
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
    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>  <!-- 성공 메시지 추가 -->
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