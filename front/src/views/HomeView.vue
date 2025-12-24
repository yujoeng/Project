<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const curtainOpen = ref(false)
const contentVisible = ref(false)
const cardsSpread = ref(false)
const popularMovies = ref([])

const TMDB_API_KEY = import.meta.env.VITE_TMDB_API_KEY
const TMDB_BASE_URL = 'https://api.themoviedb.org/3'

onMounted(async () => {
  // 인기 영화 먼저 가져오기
  await fetchPopularMovies()

  // 커튼 애니메이션
  setTimeout(() => {
    curtainOpen.value = true
  }, 500)

  setTimeout(() => {
    contentVisible.value = true
  }, 2000)

  // 카드 펼쳐지는 애니메이션
  setTimeout(() => {
    cardsSpread.value = true
  }, 2500)
})

const fetchPopularMovies = async () => {
  try {
    // 페이지 1, 2를 모두 가져와서 더 많은 영화 표시
    const [page1, page2] = await Promise.all([
      axios.get(`${TMDB_BASE_URL}/movie/popular`, {
        params: { api_key: TMDB_API_KEY, language: 'ko-KR', page: 1 }
      }),
      axios.get(`${TMDB_BASE_URL}/movie/popular`, {
        params: { api_key: TMDB_API_KEY, language: 'ko-KR', page: 2 }
      })
    ])

    // 총 40개 중 상위 20개 영화 선택
    const allMovies = [...page1.data.results, ...page2.data.results]
    popularMovies.value = allMovies.slice(0, 20)
  } catch (error) {
    console.error('인기 영화 로딩 실패:', error)
  }
}

const navigateToMovie = (movieId) => {
  router.push(`/movies/${movieId}`)
}
</script>

<template>
  <div class="home-view">
    <!-- 커튼 오버레이 -->
    <div class="curtain-overlay" :class="{ open: curtainOpen }">
      <div class="curtain-container">
        <div class="curtain curtain-left"></div>
        <div class="curtain curtain-right"></div>
        <div class="curtain-border curtain-border-left"></div>
        <div class="curtain-border curtain-border-right"></div>
        <div class="curtain-tassel curtain-tassel-left"></div>
        <div class="curtain-tassel curtain-tassel-right"></div>
      </div>
    </div>

    <!-- 배경 효과 -->
    <div class="background-effects">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="content-wrapper" :class="{ visible: contentVisible }">
      <!-- 히어로 섹션 -->
      <div class="hero-section">
        <div class="logo-container">
          <h1 class="logo">
            <span class="logo-cine">CINE</span><span class="logo-motion">motion</span>
          </h1>
          <div class="logo-underline"></div>
        </div>

        <p class="tagline">당신의 감정이 영화를 선택합니다</p>
        <p class="description">
          오늘 기분에 맞는 완벽한 영화를<br>
          AI가 추천해드립니다
        </p>
      </div>

      <!-- 타로 카드 섹션 -->
      <div class="tarot-section">
        <h2 class="section-title"> 영화 카드를 선택하세요</h2>

        <div class="cards-container" :class="{ spread: cardsSpread }">
          <!-- 영화 포스터 카드들 -->
          <div
            v-for="(movie, index) in popularMovies"
            :key="movie.id"
            class="tarot-card movie-card"
            :style="{
              '--card-index': index,
              '--total-cards': popularMovies.length
            }"
            @click="navigateToMovie(movie.id)"
          >
            <div class="card-inner">
              <!-- 카드 뒷면 (기본적으로 보임) -->
              <div class="card-back">
                <div class="card-back-border-outer"></div>
                <div class="card-back-content">
                  <div class="card-back-pattern"></div>
                  <div class="card-back-stars"></div>
                </div>
              </div>
              <!-- 카드 앞면 (hover 시 보임) -->
              <div class="card-front movie-poster">
                <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" :alt="movie.title" />
                <div class="movie-overlay">
                  <h4 class="movie-title">{{ movie.title }}</h4>
                  <div class="movie-rating">⭐ {{ movie.vote_average.toFixed(1) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-view {
  width: 100%;
  height: 100%;
  min-height: 100%;
  display: flex;
  align-items: stretch;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #0a0612 0%, #1a0b2e 50%, #0a0612 100%);
}

/* ===== 커튼 오버레이 ===== */
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

.curtain-container {
  position: relative;
  width: 100%;
  height: 100%;
}

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
    rgba(255, 255, 255, 0.05) 10px
  );
  opacity: 0.6;
}

.curtain-left {
  left: 0;
}

.curtain-right {
  right: 0;
}

.curtain-overlay.open .curtain-left {
  transform: translateX(-100%);
}

.curtain-overlay.open .curtain-right {
  transform: translateX(100%);
}

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
  height: 100%;
  max-width: 100%;
  padding: clamp(20px, 6vh, 80px) 0 32px 0;
  opacity: 0;
  transform: translateY(30px);
  transition: all 1s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  margin: 0;
  box-sizing: border-box;
}

.content-wrapper.visible {
  opacity: 1;
  transform: translateY(0);
}

/* ===== 히어로 섹션 ===== */
.hero-section {
  text-align: center;
  margin-top: clamp(10px, 6vh, 90px);
  margin-bottom: clamp(18px, 4vh, 40px);
  flex-shrink: 0;
  padding: 0 40px;
}

.logo-container {
  margin-bottom: 30px;
}

.logo {
  font-size: clamp(2.6rem, 6vw, 6rem);
  font-weight: 600;
  letter-spacing: -0.02em;
  margin: 0 0 12px 0;
  line-height: 1;
}

.logo-cine {
  background: linear-gradient(135deg, #d4af37, #ffffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-motion {
  background: linear-gradient(135deg, #b794f6, #7b10ad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 300;
  font-style: italic;
}

.logo-underline {
  width: 150px;
  height: 3px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(212, 175, 55, 0.8),
    transparent
  );
  margin: 0 auto;
  border-radius: 2px;
  box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
}

.tagline {
  font-size: clamp(1rem, 1.4vw, 1.4rem);
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 8px;
}

.description {
  font-size: clamp(0.85rem, 1.1vw, 1.05rem);
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 0;
  line-height: 1.6;
}

/* ===== 타로 카드 섹션 ===== */
.tarot-section {
  text-align: center;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 0 40px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 30px;
  background: linear-gradient(135deg, #d4af37, #b794f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.cards-container {
  perspective: 2000px;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  flex: 1;
  position: relative;
  padding-bottom: 20px;
  overflow: visible;
  width: 100%;
  max-width: 100vw;
  margin: 0 auto;
}

/* ===== 타로 카드 스타일 ===== */
.tarot-card {
  width: 280px;
  height: 450px;
  position: absolute;
  cursor: pointer;
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  transition-delay: calc(var(--card-index) * 0.05s);
  transform-style: preserve-3d;

  /* 하단 일자 겹침 배치 */
  --card-spacing: 65px;
  --total-width: calc((var(--total-cards) - 1) * var(--card-spacing));
  --start-position: calc(-1 * var(--total-width) / 2);
  --offset-x: calc(var(--start-position) + (var(--card-index) * var(--card-spacing)));

  bottom: 0;
  left: 50%;

  /* 초기 상태: 모두 중앙에 겹쳐져 있음 */
  transform: translateX(-50%) translateY(0) rotate(0deg);
  z-index: var(--card-index);
  opacity: 0;
}

/* 카드 펼쳐진 상태 */
.cards-container.spread .tarot-card {
  left: calc(50% + var(--offset-x));
  transform: translateX(-50%) translateY(0) rotate(0deg);
  opacity: 1;
  animation: cardFloat 3s ease-in-out infinite;
  animation-delay: calc(var(--card-index) * 0.1s + 0.8s);
}

@keyframes cardFloat {
  0%, 100% {
    transform: translateX(-50%) translateY(0);
  }
  50% {
    transform: translateX(-50%) translateY(-10px);
  }
}

.cards-container.spread .tarot-card:hover {
  transform: translateX(-50%) translateY(-60px) scale(1.1);
  z-index: 1000;
  animation: none;
}

.card-inner {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  border-radius: 16px;
  box-shadow:
    0 10px 40px rgba(0, 0, 0, 0.5),
    0 0 30px rgba(212, 175, 55, 0.2);
  transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

/* hover 시 카드 뒤집기 */
.cards-container.spread .tarot-card:hover .card-inner {
  transform: rotateY(180deg);
}

/* 카드 뒷면 */
.card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #0a0612 0%, #1a0d2e 50%, #2d1b3d 100%);
  border-radius: 16px;
  backface-visibility: hidden;
  transform: rotateY(0deg);
  overflow: hidden;
}

/* 금색 외곽 테두리 */
.card-back-border-outer {
  position: absolute;
  inset: 0;
  border: 3px solid #d4af37;
  border-radius: 16px;
  box-shadow:
    inset 0 0 20px rgba(212, 175, 55, 0.3),
    0 0 20px rgba(212, 175, 55, 0.4);
}

/* 카드 뒷면 컨텐츠 */
.card-back-content {
  position: absolute;
  inset: 12px;
  border: 2px solid rgba(212, 175, 55, 0.4);
  border-radius: 12px;
  overflow: hidden;
}

/* 기하학적 무늬 */
.card-back-pattern {
  position: absolute;
  inset: 0;
  background-image:
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 20px,
      rgba(183, 148, 246, 0.08) 20px,
      rgba(183, 148, 246, 0.08) 21px
    ),
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 20px,
      rgba(183, 148, 246, 0.08) 20px,
      rgba(183, 148, 246, 0.08) 21px
    ),
    repeating-linear-gradient(
      45deg,
      transparent,
      transparent 28px,
      rgba(212, 175, 55, 0.05) 28px,
      rgba(212, 175, 55, 0.05) 30px
    ),
    repeating-linear-gradient(
      -45deg,
      transparent,
      transparent 28px,
      rgba(212, 175, 55, 0.05) 28px,
      rgba(212, 175, 55, 0.05) 30px
    );
}

/* 발광하는 흰색 점들과 금색 별빛 */
.card-back-stars {
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.8) 1px, transparent 1px),
    radial-gradient(circle at 80% 30%, rgba(212, 175, 55, 0.6) 2px, transparent 2px),
    radial-gradient(circle at 35% 50%, rgba(255, 255, 255, 0.6) 1px, transparent 1px),
    radial-gradient(circle at 70% 60%, rgba(212, 175, 55, 0.7) 1.5px, transparent 1.5px),
    radial-gradient(circle at 15% 75%, rgba(255, 255, 255, 0.7) 1px, transparent 1px),
    radial-gradient(circle at 85% 80%, rgba(212, 175, 55, 0.5) 2px, transparent 2px),
    radial-gradient(circle at 50% 15%, rgba(255, 255, 255, 0.9) 1.5px, transparent 1.5px),
    radial-gradient(circle at 60% 85%, rgba(212, 175, 55, 0.8) 1px, transparent 1px);
  background-size: 100% 100%;
  animation: twinkleStars 3s ease-in-out infinite;
}

@keyframes twinkleStars {
  0%, 100% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
}

/* 카드 앞면 */
.card-front {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 16px;
  overflow: hidden;
  backface-visibility: hidden;
  transform: rotateY(180deg);
}

/* 영화 포스터 카드 */
.movie-poster {
  position: relative;
  border: 3px solid rgba(212, 175, 55, 0.5);
}

.movie-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.movie-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px;
  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.95) 0%,
    rgba(0, 0, 0, 0.7) 60%,
    transparent 100%
  );
  transform: translateY(100%);
  transition: transform 0.3s ease;
}

.cards-container.spread .tarot-card:hover .movie-overlay {
  transform: translateY(0);
}

.movie-title {
  font-size: 1rem;
  font-weight: 600;
  color: white;
  margin-bottom: 8px;
  line-height: 1.3;
}

.movie-rating {
  font-size: 0.9rem;
  color: #d4af37;
  font-weight: 600;
}

/* ===== 반응형 ===== */
@media (max-width: 1400px) {
  .tarot-card {
    width: 240px;
    height: 380px;
    --card-spacing: 55px;
  }
}

@media (max-width: 1200px) {
  .content-wrapper {
    padding: 40px 0 30px 0;
  }

  .hero-section,
  .tarot-section {
    padding: 0 30px;
  }

  .logo {
    font-size: 2.5rem;
  }

  .tarot-card {
    width: 200px;
    height: 320px;
    --card-spacing: 45px;
  }
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 30px 0 20px 0;
  }

  .hero-section,
  .tarot-section {
    padding: 0 20px;
  }

  .logo {
    font-size: 2rem;
  }

  .tagline {
    font-size: 1rem;
  }

  .description {
    font-size: 0.85rem;
  }

  .section-title {
    font-size: 1.2rem;
    margin-bottom: 20px;
  }

  .tarot-card {
    width: 140px;
    height: 230px;
    --card-spacing: 32px;
  }

  .movie-title {
    font-size: 0.85rem;
  }

  .movie-rating {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .hero-section,
  .tarot-section {
    padding: 0 16px;
  }

  .logo {
    font-size: 1.8rem;
  }

  .tagline {
    font-size: 0.9rem;
  }

  .description {
    font-size: 0.75rem;
  }

  .section-title {
    font-size: 1rem;
  }

  .tarot-card {
    width: 100px;
    height: 160px;
    --card-spacing: 22px;
  }

  .cards-container.spread .tarot-card:hover {
    transform: translateX(calc(-50% + var(--offset-x))) translateY(-30px) scale(1.05);
  }

  .movie-title {
    font-size: 0.7rem;
  }

  .movie-rating {
    font-size: 0.65rem;
  }

  .movie-overlay {
    padding: 10px;
  }
}
</style>