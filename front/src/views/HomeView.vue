<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const curtainOpen = ref(false)
const contentVisible = ref(false)

onMounted(() => {
  // 0.5초 후 커튼 열기 시작
  setTimeout(() => {
    curtainOpen.value = true
  }, 500)

  // 2초 후 컨텐츠 페이드인
  setTimeout(() => {
    contentVisible.value = true
  }, 2000)
})

const navigateToEmotionCards = () => {
  router.push('/emotions')
}

const navigateToMovies = () => {
  router.push('/movies')
}
</script>

<template>
  <div class="home-view">
    <!-- 커튼 오버레이 (네비게이션도 가림) -->
    <div class="curtain-overlay" :class="{ open: curtainOpen }">
      <div class="curtain-container">
        <!-- 왼쪽 커튼 -->
        <div class="curtain curtain-left"></div>
        
        <!-- 오른쪽 커튼 -->
        <div class="curtain curtain-right"></div>
        
        <!-- 금색 테두리 -->
        <div class="curtain-border curtain-border-left"></div>
        <div class="curtain-border curtain-border-right"></div>
        
        <!-- 커튼 술 장식 -->
        <div class="curtain-tassel curtain-tassel-left"></div>
        <div class="curtain-tassel curtain-tassel-right"></div>
      </div>
    </div>

    <!-- 배경 효과 -->
    <div class="background-effects">
      <!-- 보라색 그라디언트 오브 -->
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="content-wrapper" :class="{ visible: contentVisible }">
      <!-- 히어로 섹션 -->
      <div class="hero-section">
        <!-- 로고 -->
        <div class="logo-container">
          <h1 class="logo">
            <span class="logo-cine">CINE</span><span class="logo-motion">motion</span>
          </h1>
          <div class="logo-underline"></div>
        </div>

        <!-- 태그라인 -->
        <p class="tagline">
          당신의 감정이 영화를 선택합니다
        </p>

        <!-- 설명 -->
        <p class="description">
          오늘 기분에 맞는 완벽한 영화를<br>
          AI가 추천해드립니다
        </p>

        <!-- CTA 버튼 -->
        <div class="cta-buttons">
          <button @click="navigateToEmotionCards" class="btn-primary-glow">
            <span class="btn-icon">✨</span>
            <span class="btn-text">감정으로 영화 찾기</span>
            <span class="btn-arrow">→</span>
          </button>

          <button @click="navigateToMovies" class="btn-secondary-outline">
            <span class="btn-icon">🎬</span>
            <span class="btn-text">전체 영화 둘러보기</span>
          </button>
        </div>
      </div>

      <!-- 특징 카드 -->
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🎭</div>
          <h3 class="feature-title">7가지 감정 분석</h3>
          <p class="feature-description">
            지금 당신의 기분에 딱 맞는 영화
          </p>
          <div class="feature-shine"></div>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🎬</div>
          <h3 class="feature-title">최신 영화 정보</h3>
          <p class="feature-description">
            TMDB 기반 실시간 업데이트
          </p>
          <div class="feature-shine"></div>
        </div>

        <div class="feature-card">
          <div class="feature-icon">⭐</div>
          <h3 class="feature-title">개인화 추천</h3>
          <p class="feature-description">
            취향에 맞는 맞춤 추천
          </p>
          <div class="feature-shine"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #0a0612 0%, #1a0b2e 50%, #0a0612 100%);
}

/* ===== 커튼 오버레이 (전체 화면) ===== */
.curtain-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 10000;
  pointer-events: all;
  transition: opacity 0.8s ease 1.5s, visibility 0s 2.3s;
}

.curtain-overlay.open {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
}

/* 커튼 컨테이너 */
.curtain-container {
  position: relative;
  width: 100%;
  height: 100%;
}

/* 커튼 (보라색 벨벳) */
.curtain {
  position: absolute;
  top: 0;
  width: 50%;
  height: 100%;
  background: linear-gradient(
    90deg,
    #2d1b3d 0%,
    #4a2d5e 15%,
    #6b4a8f 30%,
    #8b5fc7 45%,
    #6b4a8f 60%,
    #4a2d5e 75%,
    #2d1b3d 100%
  );
  transition: transform 1.5s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    inset 0 0 80px rgba(139, 95, 199, 0.3),
    inset 0 0 50px rgba(0, 0, 0, 0.5);
}

/* 펄 효과 (벨벳 질감) */
.curtain::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: repeating-linear-gradient(
    90deg,
    transparent,
    transparent 8px,
    rgba(255, 255, 255, 0.05) 8px,
    rgba(255, 255, 255, 0.05) 10px,
    transparent 10px,
    transparent 18px,
    rgba(139, 95, 199, 0.1) 18px,
    rgba(139, 95, 199, 0.1) 20px
  );
  opacity: 0.6;
}

/* 빛 반사 효과 */
.curtain::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(
      ellipse at 30% 20%,
      rgba(255, 255, 255, 0.15) 0%,
      transparent 50%
    ),
    radial-gradient(
      ellipse at 70% 80%,
      rgba(139, 95, 199, 0.2) 0%,
      transparent 50%
    ),
    linear-gradient(
      180deg,
      rgba(255, 255, 255, 0.1) 0%,
      transparent 30%,
      transparent 70%,
      rgba(0, 0, 0, 0.3) 100%
    );
}

.curtain-left {
  left: 0;
  transform-origin: left center;
}

.curtain-right {
  right: 0;
  transform-origin: right center;
}

/* 커튼 열림 */
.curtain-overlay.open .curtain-left {
  transform: translateX(-100%);
}

.curtain-overlay.open .curtain-right {
  transform: translateX(100%);
}

/* 금색 테두리 */
.curtain-border {
  position: absolute;
  top: 0;
  width: 3px;
  height: 100%;
  background: linear-gradient(
    180deg,
    transparent 0%,
    rgba(212, 175, 55, 0.8) 20%,
    rgba(212, 175, 55, 1) 50%,
    rgba(212, 175, 55, 0.8) 80%,
    transparent 100%
  );
  box-shadow: 
    0 0 20px rgba(212, 175, 55, 0.6),
    0 0 40px rgba(212, 175, 55, 0.3);
  transition: transform 1.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.curtain-border-left {
  left: 50%;
  margin-left: -1.5px;
}

.curtain-border-right {
  right: 50%;
  margin-right: -1.5px;
}

.curtain-overlay.open .curtain-border-left {
  transform: translateX(-200%);
}

.curtain-overlay.open .curtain-border-right {
  transform: translateX(200%);
}

/* 커튼 술 장식 (금색) */
.curtain-tassel {
  position: absolute;
  top: 50%;
  width: 30px;
  height: 180px;
  background: linear-gradient(
    to bottom,
    rgba(212, 175, 55, 0.9),
    rgba(212, 175, 55, 0.7),
    rgba(212, 175, 55, 0.3),
    transparent
  );
  border-radius: 15px;
  transform: translateY(-50%);
  box-shadow: 
    0 0 20px rgba(212, 175, 55, 0.6),
    inset 0 0 20px rgba(212, 175, 55, 0.3);
  transition: transform 1.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.curtain-tassel::before {
  content: '';
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 10px;
  height: 60px;
  background: linear-gradient(180deg, rgba(212, 175, 55, 1), rgba(212, 175, 55, 0.8));
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(212, 175, 55, 0.8);
}

.curtain-tassel-left {
  left: 50%;
  margin-left: -80px;
}

.curtain-tassel-right {
  right: 50%;
  margin-right: -80px;
}

.curtain-overlay.open .curtain-tassel-left {
  transform: translateY(-50%) translateX(-250%);
}

.curtain-overlay.open .curtain-tassel-right {
  transform: translateY(-50%) translateX(250%);
}

/* ===== 배경 효과 ===== */
.background-effects {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.15;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #7b10ad, #d946ef);
  top: -300px;
  left: -300px;
  animation-delay: 0s;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  bottom: -250px;
  right: -250px;
  animation-delay: 5s;
}

.orb-3 {
  width: 700px;
  height: 700px;
  background: linear-gradient(135deg, #d946ef, #ec4899);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(50px, -50px) scale(1.1); }
  66% { transform: translate(-30px, 30px) scale(0.9); }
}

/* ===== 컨텐츠 ===== */
.content-wrapper {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1600px;
  padding: 80px 40px;
  opacity: 0;
  transform: translateY(30px);
  transition: all 1s cubic-bezier(0.4, 0, 0.2, 1);
}



.content-wrapper.visible {
  opacity: 1;
  transform: translateY(0);
}

/* ===== 히어로 섹션 ===== */
.hero-section {
  text-align: center;
  margin-bottom: 80px;
}

/* 로고 */
.logo-container {
  margin-bottom: 32px;
}

.logo {
  font-size: 5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin: 0 0 16px 0;
  line-height: 1;
}

.logo-cine {
  background: linear-gradient(135deg, #ffffff, #d4af37);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 40px rgba(212, 175, 55, 0.3);
}

.logo-motion {
  background: linear-gradient(135deg, #d946ef, #7b10ad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 300;
  font-style: italic;
}

.logo-underline {
  width: 200px;
  height: 4px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(212, 175, 55, 0.8),
    transparent
  );
  margin: 0 auto;
  border-radius: 2px;
  box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
}

/* 태그라인 */
.tagline {
  font-size: 1.75rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 16px;
  letter-spacing: -0.01em;
}

.description {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 48px;
  line-height: 1.8;
}

/* CTA 버튼 */
.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 80px;
}

.btn-primary-glow {
  position: relative;
  padding: 18px 40px;
  font-size: 1.125rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #7b10ad, #d946ef);
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 
    0 8px 32px rgba(123, 16, 173, 0.4),
    0 0 0 2px rgba(212, 175, 55, 0.2);
  overflow: hidden;
}

.btn-primary-glow::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.btn-primary-glow:hover::before {
  left: 100%;
}

.btn-primary-glow:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 48px rgba(123, 16, 173, 0.6),
    0 0 0 3px rgba(212, 175, 55, 0.4);
}

.btn-secondary-outline {
  padding: 18px 40px;
  font-size: 1.125rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  background: transparent;
  border: 2px solid rgba(212, 175, 55, 0.4);
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 12px;
  backdrop-filter: blur(10px);
}

.btn-secondary-outline:hover {
  border-color: rgba(212, 175, 55, 0.8);
  background: rgba(212, 175, 55, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(212, 175, 55, 0.3);
}

/* ===== 특징 그리드 ===== */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
}

.feature-card {
  position: relative;
  background: linear-gradient(135deg, rgba(45, 27, 61, 0.6), rgba(15, 10, 26, 0.8));
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 20px;
  padding: 40px 32px;
  text-align: center;
  transition: all 0.4s ease;
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(183, 148, 246, 0.1) 0%,
    transparent 50%,
    rgba(212, 175, 55, 0.1) 100%
  );
  opacity: 0;
  transition: opacity 0.4s ease;
}

.feature-card:hover::before {
  opacity: 1;
}

.feature-card:hover {
  transform: translateY(-8px);
  border-color: rgba(212, 175, 55, 0.5);
  box-shadow: 
    0 20px 60px rgba(123, 16, 173, 0.4),
    0 0 40px rgba(212, 175, 55, 0.2);
}

.feature-icon {
  font-size: 3.5rem;
  margin-bottom: 20px;
  filter: drop-shadow(0 0 20px rgba(183, 148, 246, 0.6));
}

.feature-title {
  font-size: 1.375rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 12px;
  background: linear-gradient(135deg, #ffffff, rgba(212, 175, 55, 0.8));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.feature-description {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.6;
}

/* 카드 반짝임 효과 */
.feature-shine {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent,
    rgba(212, 175, 55, 0.1),
    transparent
  );
  transform: rotate(45deg);
  transition: all 0.8s ease;
  opacity: 0;
}

.feature-card:hover .feature-shine {
  opacity: 1;
  transform: rotate(45deg) translate(50%, 50%);
}

/* ===== 반응형 ===== */
@media (max-width: 1024px) {
  .logo {
    font-size: 4rem;
  }

  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }

  .btn-primary-glow,
  .btn-secondary-outline {
    width: 100%;
    max-width: 400px;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 60px 20px;
  }

  .logo {
    font-size: 3rem;
  }

  .tagline {
    font-size: 1.375rem;
  }

  .description {
    font-size: 1rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}

@media (max-width: 480px) {
  .logo {
    font-size: 2.5rem;
  }

  .tagline {
    font-size: 1.125rem;
  }

  .btn-primary-glow,
  .btn-secondary-outline {
    padding: 14px 32px;
    font-size: 1rem;
  }

  .feature-card {
    padding: 32px 24px;
  }
}

@media (min-width: 1600px) {
  .logo {
    font-size: 6rem;  /* ✅ 추가 */
  }
  
  .tagline {
    font-size: 2rem;
  }
  
  .description {
    font-size: 1.25rem;
  }
  
  .btn-primary-glow,
  .btn-secondary-outline {
    padding: 20px 48px;
    font-size: 1.25rem;
  }
  
  .feature-card {
    padding: 48px 40px;
  }
  
  .feature-icon {
    font-size: 4rem;
  }
  
  .feature-title {
    font-size: 1.5rem;
  }
  
  .feature-description {
    font-size: 1.125rem;
  }
}

@media (min-width: 1920px) {
  .content-wrapper {
    max-width: 1800px;
    padding: 100px 80px;
  }
  
  .logo {
    font-size: 7rem;
  }
  
  .tagline {
    font-size: 2.25rem;
  }
  
  .features-grid {
    gap: 48px;
  }
}

@media (min-width: 2560px) {
  .content-wrapper {
    max-width: 2200px;
    padding: 120px 120px;
  }
  
  .logo {
    font-size: 8rem;
  }
}
</style>