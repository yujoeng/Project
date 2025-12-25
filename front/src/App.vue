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

  createShootingStars()
})

const logout = async () => {
  await authStore.logoutUser()
  router.push('/')
}

const createShootingStars = () => {
  const shootingStarsContainer = document.getElementById('shooting-stars')
  
  if (!shootingStarsContainer) return

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
    div.style.setProperty('--left', star.left)
    shootingStarsContainer.appendChild(div)
  })

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
    <div id="shooting-stars"></div>

    <!-- 네비게이션 -->
    <header class="navbar">
      <div class="nav-inner">
        <RouterLink to="/" class="logo">
          <span class="logo-text">
            <span class="logo-cine">CINE</span><span class="logo-motion">motion</span>
          </span>
        </RouterLink>

        <nav class="nav-links">
          <RouterLink to="/" class="nav-link">홈</RouterLink>
          <RouterLink to="/movies" class="nav-link">전체 영화</RouterLink>
          <RouterLink to="/emotions" class="nav-link">감정 카드</RouterLink>
          <RouterLink to="/search" class="nav-link">검색</RouterLink>
          <RouterLink v-if="authStore.isLogin" to="/recommended" class="nav-link">추천 영화</RouterLink>
          <RouterLink v-if="authStore.isLogin" to="/profile" class="nav-link">프로필</RouterLink>

          <template v-if="!authStore.isLogin">
            <RouterLink to="/signup" class="nav-link nav-link-signup">회원가입</RouterLink>
            <RouterLink to="/login" class="btn btn-primary">로그인</RouterLink>
          </template>
          <button v-else @click="logout" class="btn btn-secondary">로그아웃</button>
        </nav>
      </div>
    </header>

    <!-- 메인 컨텐츠 -->
    <main class="main-container">
      <div class="main-inner">
        <RouterView />
      </div>
    </main>

    <!-- 푸터 -->
    <footer class="footer">
      <div class="footer-inner">
        <p>&copy; 2025 CINEmotion. 당신의 감정에 맞는 영화를 찾아드립니다.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.app-container {
  height: 100dvh;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow-x: hidden;
  
  /* 전체 너비 강제 */
  width: 100vw;
  max-width: 100vw;
  margin: 0;
  padding: 0;
  left: 0;
  right: 0;
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
  flex: 0 0 auto;
  margin: 0;
  padding: 0;
}

.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 100%;
  padding: 16px 40px;
  margin: 0 auto;
  box-sizing: border-box;
}

@media (min-width: 1920px) {
  .logo-text {
    font-size: 2rem;
  }
  
  .nav-link {
    font-size: 1rem;
    padding: 12px 20px;
  }
  
  .nav-inner {
    padding: 20px 80px;
  }
}

/* 로고 */
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

.logo-text {
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.logo-cine {
  background: linear-gradient(135deg, #d4af37, #ffffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 8px rgba(212, 175, 55, 0.4));
}

.logo-motion {
  background: linear-gradient(135deg, #b794f6, #7b10ad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 300;
  font-style: italic;
  filter: drop-shadow(0 0 8px rgba(183, 148, 246, 0.4));
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

.nav-link-signup {
  border: 1px solid rgba(183, 148, 246, 0.3);
}

.nav-link-signup:hover {
  border-color: rgba(183, 148, 246, 0.6);
}

/* 메인 컨텐츠 */
.main-container {
  flex: 1 1 auto;
  min-height: 0;
  width: 100%;
  max-width: 100vw;
  position: relative;
  z-index: 10;
  overflow-x: hidden;
  margin: 0;
  padding: 0;
}

.main-inner {
  height: 100%;
  min-height: 0;       
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0;
  width: 100%;
  max-width: 100vw;
  margin: 0;
  box-sizing: border-box;
}

/* 푸터 */
.footer {
  width: 100%;
  background: rgba(15, 10, 26, 0.8);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(183, 148, 246, 0.2);
  flex: 0 0 auto;
  padding: 18px 0;
  position: relative;
  z-index: 10;
}

.footer-inner {
  text-align: center;
  color: var(--text-muted);
  font-size: 1rem;
  width: 100%;
  max-width: 100%;
  padding: 0 40px;
  margin: 0 auto;
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