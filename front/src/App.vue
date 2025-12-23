<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

// 사용자 정보 가져오기 
onMounted(async () => {
  if (authStore.token) {
    // ✅ 토큰이 있을 때만 호출
    await authStore.fetchUser()
  }
})


const logout = async () => {
  await authStore.logoutUser()
  router.push('/')
}
</script>

<template>
  <div>
    <header class="navbar">
      <div class="nav-inner">
        <h1 class="logo">🎬CINEmotion</h1>

        <nav class="nav-links">
          <RouterLink to="/">홈</RouterLink>
          <RouterLink to="/movies">영화 목록</RouterLink>
          <RouterLink to="/review-search">리뷰 검색</RouterLink>

          <!-- 로그인한 경우만 -->
          <RouterLink
            v-if="authStore.isLogin"
            to="/recommended"
          >
            추천 영화
          </RouterLink>

          <!-- 로그인 안 된 상태 -->
          <RouterLink
            v-if="!authStore.isLogin"
            to="/signup"
          >
            회원가입
          </RouterLink>

          <!-- 로그인 안 된 상태 -->
          <RouterLink
            v-if="!authStore.isLogin"
            to="/login"
          >
            로그인
          </RouterLink>

          <!-- 로그인 된 상태 -->
          <button
            v-else
            class="button-outline"
            @click="logout"
          >
            로그아웃
          </button>
        </nav>
      </div>
    </header>

    <main class="main-container">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;
}

.nav-inner {
  max-width: 1080px;
  margin: 0 auto;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 20px;
  margin: 0;
}

.nav-links {
  display: flex;
  gap: 16px;
  font-size: 14px;
}

.nav-links a {
  padding: 4px 12px;
  border-radius: 999px;
  text-decoration: none;
  color: #111827;       
  font-weight: 700;      
}

/* 활성화된 링크 강조 */
.nav-links a.router-link-active {
  background-color: #020202;  
  color: #ffffff;
}

.main-container {
  max-width: 1080px;
  margin: 0 auto;
  padding: 24px 20px 40px;
}

.button-primary {
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  background-color: #ef4444; /* 빨간색 */
  color: white;
  cursor: pointer;
  font-size: 14px;
  transition: 0.15s ease;
}

.button-primary:hover {
  background-color: #dc2626; /* 좀 더 진한 빨강 */
}

/* 회색 아웃라인 버튼 (← 목록으로 등에 사용) */
.button-outline {
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid #9ca3af;
  background-color: white;
  color: #374151;
  cursor: pointer;
  font-size: 14px;
  transition: 0.15s ease;
}

.button-outline:hover {
  background-color: #f3f4f6;
}
</style>
