<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

onMounted(async () => {
  if (authStore.token) {
    await authStore.fetchUser()
  }

  // // 디버깅용 별똥별 생성
  createShootingStars()
})

const logout = async () => {
  await authStore.logoutUser()
  router.push('/')
}

// // 디버깅용 별똥별 생성 함수
const createShootingStars = () => {
  const shootingStarsContainer = document.getElementById('shooting-stars')
  
  if (!shootingStarsContainer) return

  // 별똥별 5개
  const shootingStars = [
    { delay: '0s', duration: '4s', top: '5%', left: '20%' },
    { delay: '3s', duration: '5s', top: '15%', left: '70%' },
    { delay: '6s', duration: '4.5s', top: '10%', left: '45%' },
    { delay: '9s', duration: '5.5s', top: '8%', left: '85%' },
    { delay: '12s', duration: '4s', top: '12%', left: '30%' },
    { delay: '15s', duration: '5s', top: '6%', left: '60%' },
    { delay: '18s', duration: '4.5s', top: '14%', left: '50%' },
    { delay: '21s', duration: '5.5s', top: '9%', left: '75%' }
  ]
  
  shootingStars.forEach(star => {
    const div = document.createElement('div')
    div.className = 'shooting-star'
    div.style.setProperty('--delay', star.delay)
    div.style.setProperty('--duration', star.duration)
    div.style.setProperty('--top', star.top)
    div.style.setProperty('--rigrt', star.right)
    shootingStarsContainer.appendChild(div)
  })

  // 반짝이는 별 20개
  for (let i = 0; i < 50; i++) {
    const div = document.createElement('div')
    div.className = 'twinkle-star'
    div.style.setProperty('--delay', `${Math.random() * 5}s`)
    div.style.setProperty('--duration', `${3 + Math.random() * 2}s`)
    div.style.left = `${Math.random() * 100}%`
    div.style.top = `${Math.random() * 100}%`
    shootingStarsContainer.appendChild(div)
  }
}
</script>

<template>
  <div class="app-container">
    <div id="app-background"></div>
    <!-- 별똥별 컨테이너 -->
    <div id="shooting-stars"></div>

    <!-- 네비게이션 -->
    <header class="navbar">
      <div class="nav-inner">
        <!-- 로고 -->
        <RouterLink to="/" class="logo">
          <span class="logo-icon">🎭</span>
          <span class="logo-text">
            <span class="logo-cine">CINE</span><span class="logo-motion">motion</span>
          </span>
        </RouterLink>

        <!-- 메뉴 -->
        <nav class="nav-links">
          <RouterLink to="/" class="nav-link">
            <span class="nav-icon">🏠</span>
            <span>홈</span>
          </RouterLink>

          <RouterLink to="/movies" class="nav-link">
            <span class="nav-icon">🎬</span>
            <span>영화 목록</span>
          </RouterLink>

          <RouterLink to="/emotions" class="nav-link">
            <span class="nav-icon">🎭</span>
            <span>감정 기반 영화 추천</span>
          </RouterLink>

          <RouterLink to="/review-search" class="nav-link">
            <span class="nav-icon">🔍</span>
            <span>검색</span>
          </RouterLink>

          <RouterLink 
            v-if="authStore.isLogin" 
            to="/recommended" 
            class="nav-link"
          >
            <span class="nav-icon">⭐</span>
            <span>추천 영화</span>
          </RouterLink>

          <RouterLink 
            v-if="authStore.isLogin" 
            to="/profile" 
            class="nav-link"
          >
            <span class="nav-icon">👤</span>
            <span>프로필</span>
          </RouterLink>

          <!-- 로그인/로그아웃 -->
          <template v-if="!authStore.isLogin">
            <RouterLink to="/signup" class="nav-link nav-link-signup">
              회원가입
            </RouterLink>
            <RouterLink to="/login" class="btn btn-primary">
              로그인
            </RouterLink>
          </template>

          <button v-else @click="logout" class="btn btn-secondary">
            로그아웃
          </button>
        </nav>
      </div>
    </header>

    <!-- 메인 컨텐츠 -->
    <main class="main-container">
      <RouterView />
    </main>

    <!-- 푸터 -->
    <footer class="footer">
      <p>&copy; 2024 CINEmotion. 당신의 감정에 맞는 영화를 찾아드립니다.</p>
    </footer>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
}

/* 네비게이션 */
.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
  background: rgba(15, 10, 26, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(183, 148, 246, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.nav-inner {
  max-width: 1920px;
  width: 100%; 
  margin: 0 auto;
  padding: 16px 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

@media (min-width: 1920px) {
  .logo-text {
    font-size: 2rem;  /* 1.75rem → 2rem */
  }
  
  .nav-link {
    font-size: 1rem;  /* 0.95rem → 1rem */
    padding: 12px 20px; /* 10px 16px → 12px 20px */
  }
}

@media (min-width: 1920px) {
  .nav-inner {
    padding: 20px 80px; /* 더 큰 패딩 */
  }
  
  .logo-text {
    font-size: 2.25rem;
  }
  
  .logo-icon {
    font-size: 2.5rem;
  }
}

/* ===== 로고 개선 ===== */
.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 2rem;
  filter: drop-shadow(0 0 10px rgba(183, 148, 246, 0.6));
}

.logo-text {
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

/* // 디버깅용 로고 그라디언트 */
.logo-cine {
  background: linear-gradient(135deg, #ffffff, #b794f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-motion {
  background: linear-gradient(135deg, #d946ef, #7b10ad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 300;
  font-style: italic;
}

/* 네비게이션 링크 */
.nav-links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border-radius: 50px;
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  position: relative;
}

.nav-icon {
  font-size: 1.1rem;
}

.nav-link:hover {
  color: var(--text-primary);
  background: rgba(183, 148, 246, 0.1);
}

.nav-link.router-link-active {
  color: var(--text-primary);
  background: rgba(183, 148, 246, 0.2);
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 2px;
  background: var(--primary-purple);
  border-radius: 2px;
}

/* 회원가입 링크 스타일 */
.nav-link-signup {
  border: 1px solid rgba(183, 148, 246, 0.3);
}

.nav-link-signup:hover {
  border-color: rgba(183, 148, 246, 0.6);
}

/* 메인 컨텐츠 */
.main-container {
  flex: 1;
  width: 100%;
  position: relative;
  z-index: 10;
}

/* 푸터 */
.footer {
  width: 100%;
  background: rgba(15, 10, 26, 0.8);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(183, 148, 246, 0.2);
  padding: 32px 40px;
  text-align: center;
  color: var(--text-muted);
  font-size: 1rem;
  position: relative;
  z-index: 10;
}

/* 반응형 */
@media (max-width: 1024px) {
  .nav-inner {
    padding: 12px 24px;
  }

  .nav-link span:not(.nav-icon) {
    display: none;
  }

  .nav-links {
    gap: 4px;
  }

  .nav-link {
    padding: 10px;
  }

  .nav-link-signup {
    border: none;
  }
}

@media (max-width: 768px) {
  .nav-inner {
    padding: 12px 16px;
  }

  .logo-text {
    font-size: 1.5rem;
  }

  .logo-icon {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .nav-links {
    gap: 2px;
  }

  .nav-link {
    padding: 8px;
  }

  .btn {
    padding: 8px 16px;
    font-size: 0.85rem;
  }
}
</style>