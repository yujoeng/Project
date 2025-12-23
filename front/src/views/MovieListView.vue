<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getPopularMovies, getMoviesByEmotion } from '@/api/tmdb'
import MovieCard from '../components/MovieCard.vue'

const router = useRouter()
const route = useRoute()

const movies = ref([])
const isLoading = ref(true)
const errorMessage = ref('')

const isEmotionBased = computed(() => !!route.query.emotion)
const emotionName = computed(() => route.query.emotionName || '')
const emotionTagline = computed(() => route.query.emotionTagline || '')  // // 디버깅용 추가
const displayGenres = computed(() => {
  if (route.query.genres) {
    return route.query.genres.replace(/,/g, ' · ')
  }
  return ''
})

// // 디버깅용 감정별 색상 매핑
const emotionColors = {
  joy: { primary: '#F39C12', secondary: '#F1C40F' },
  sadness: { primary: '#3498DB', secondary: '#2C3E50' },
  anger: { primary: '#E74C3C', secondary: '#C0392B' },
  fear: { primary: '#8E44AD', secondary: '#2C3E50' },
  excitement: { primary: '#E67E22', secondary: '#D35400' },
  calm: { primary: '#1ABC9C', secondary: '#16A085' },
  melancholy: { primary: '#34495E', secondary: '#2C3E50' }
}

const currentEmotionColor = computed(() => {
  return emotionColors[route.query.emotion] || { primary: '#7b10ad', secondary: '#d946ef' }
})

const loadMovies = async () => {
  isLoading.value = true
  errorMessage.value = ''

  console.log('🎬 영화 로드 시작')
  console.log('현재 라우트 쿼리:', route.query)

  try {
    if (route.query.genreIds) {
      console.log('// 디버깅용 감정 기반 필터링 모드')
      const genreIds = route.query.genreIds.split(',').map(Number)
      const results = await getMoviesByEmotion(route.query.emotion, genreIds)
      movies.value = results
    } else {
      console.log('// 디버깅용 전체 영화 목록 모드')
      const data = await getPopularMovies()
      movies.value = data.results || []
    }
    
    console.log('// 디버깅용 최종 영화 개수:', movies.value.length)
  } catch (error) {
    console.error('❌ 영화 로딩 실패:', error)
    errorMessage.value = '영화 정보를 가져오는데 실패했습니다.'
  } finally {
    isLoading.value = false
  }
}

const goDetail = (id) => {
  router.push(`/movies/${id}`)
}

watch(() => route.query, () => {
  loadMovies()
}, { deep: true })

onMounted(() => {
  loadMovies()
})
</script>

<template>
  <div class="movie-list-view">
    <!-- 감정 기반 헤더 -->
    <div v-if="isEmotionBased" class="emotion-header">
      <!-- 배경 그라디언트 -->
      <div 
        class="header-gradient" 
        :style="{
          background: `linear-gradient(135deg, ${currentEmotionColor.primary}, ${currentEmotionColor.secondary})`
        }"
      ></div>

      <!-- 헤더 컨텐츠 -->
      <div class="header-content">
        <button @click="$router.push('/emotions')" class="back-button">
          <span>←</span>
          <span>다시 선택하기</span>
        </button>

        <div class="header-main">
          <h1 class="emotion-title">
            {{ emotionName }}에 어울리는 영화
          </h1>
          
          <p v-if="emotionTagline" class="emotion-tagline">
            "{{ emotionTagline }}"
          </p>

          <div v-if="displayGenres" class="genre-badges">
            <span 
              v-for="genre in route.query.genres.split(',')" 
              :key="genre"
              class="genre-badge"
            >
              {{ genre }}
            </span>
          </div>

          <!-- 감정 매치도 (시뮬레이션) -->
          <div class="match-indicator">
            <div class="match-bar">
              <div 
                class="match-fill"
                :style="{
                  width: '85%',
                  background: `linear-gradient(90deg, ${currentEmotionColor.primary}, ${currentEmotionColor.secondary})`
                }"
              ></div>
            </div>
            <p class="match-text">감정 매치도 85%</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 전체 영화 헤더 -->
    <div v-else class="standard-header">
      <h1 class="standard-title">최고 평점 영화 목록 🎬</h1>
      <p class="standard-subtitle">TMDB 기반 인기 영화를 만나보세요</p>
    </div>

    <!-- 로딩 -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">당신의 감정에 맞는 영화를 찾고 있어요...</p>
      <div class="loading-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>

    <!-- 에러 -->
    <div v-else-if="errorMessage" class="error-container">
      <div class="error-icon">😢</div>
      <p class="error-message">{{ errorMessage }}</p>
      <button @click="loadMovies" class="retry-button">다시 시도</button>
    </div>

    <!-- 영화 목록 -->
    <div v-else-if="movies.length > 0" class="movies-section">
      <!-- 추천 이유 (감정 기반일 때) -->
      <div v-if="isEmotionBased" class="recommendation-info">
        <p class="info-text">
          <span class="info-icon">🎯</span>
          당신의 <strong>{{ emotionName }}</strong> 감정을 위해 선별된 {{ movies.length }}편의 영화
        </p>
      </div>

      <!-- 영화 그리드 -->
      <div class="movie-grid">
        <div
          v-for="movie in movies"
          :key="movie.id"
          class="movie-item"
          @click="goDetail(movie.id)"
        >
          <MovieCard :movie="movie" />
        </div>
      </div>
    </div>

    <!-- 결과 없음 -->
    <div v-else class="no-results">
      <div class="no-results-icon">🎬</div>
      <h2 class="no-results-title">조건에 맞는 영화를 찾을 수 없어요</h2>
      <p class="no-results-text">
        다른 감정을 선택하거나 필터 조건을 변경해보세요
      </p>
      <button 
        v-if="isEmotionBased"
        @click="$router.push('/emotions')" 
        class="retry-button"
      >
        다른 감정 선택하기
      </button>
    </div>
  </div>
</template>

<style scoped>
.movie-list-view {
  min-height: 100vh;
  padding-bottom: 60px;
}

/* ===== 감정 기반 헤더 ===== */
.emotion-header {
  position: relative;
  padding: 80px 40px 60px;
  margin-bottom: 60px;
  overflow: hidden;
}

.header-gradient {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.15;
  z-index: 0;
}

.header-gradient::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100px;
  background: linear-gradient(to bottom, transparent, var(--bg-dark));
}

.header-content {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50px;
  color: var(--text-primary);
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  margin-bottom: 32px;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(-4px);
}

.header-main {
  text-align: center;
}

.emotion-title {
  font-size: 3rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ffffff, #b794f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 16px;
  line-height: 1.2;
}

.emotion-tagline {
  font-size: 1.5rem;
  color: var(--text-secondary);
  font-style: italic;
  margin-bottom: 24px;
  font-weight: 300;
}

.genre-badges {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.genre-badge {
  padding: 8px 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50px;
  color: var(--text-primary);
  font-size: 0.95rem;
  font-weight: 500;
  backdrop-filter: blur(10px);
}

/* ===== 매치도 표시 ===== */
.match-indicator {
  max-width: 500px;
  margin: 0 auto;
}

.match-bar {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 12px;
}

.match-fill {
  height: 100%;
  border-radius: 10px;
  animation: fillBar 1.5s ease-out;
  box-shadow: 0 0 20px currentColor;
}

@keyframes fillBar {
  from { width: 0; }
}

.match-text {
  font-size: 1rem;
  color: var(--text-secondary);
  font-weight: 600;
}

/* ===== 전체 영화 헤더 ===== */
.standard-header {
  text-align: center;
  padding: 80px 40px 60px;
  margin-bottom: 60px;
}

.standard-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.standard-subtitle {
  font-size: 1.125rem;
  color: var(--text-secondary);
}

/* ===== 로딩 ===== */
.loading-container {
  text-align: center;
  padding: 120px 20px;
}

.loading-spinner {
  width: 80px;
  height: 80px;
  border: 6px solid rgba(183, 148, 246, 0.2);
  border-top: 6px solid var(--primary-purple);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 32px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.loading-dots {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.loading-dots span {
  width: 12px;
  height: 12px;
  background: var(--primary-purple);
  border-radius: 50%;
  animation: bounce 1.4s ease-in-out infinite;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* ===== 에러 ===== */
.error-container {
  text-align: center;
  padding: 120px 20px;
}

.error-icon {
  font-size: 5rem;
  margin-bottom: 24px;
}

.error-message {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 32px;
}

.retry-button {
  padding: 14px 32px;
  background: linear-gradient(135deg, var(--primary-purple), #d946ef);
  border: none;
  border-radius: 50px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(123, 16, 173, 0.4);
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(123, 16, 173, 0.6);
}

/* ===== 영화 섹션 ===== */
.movies-section {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 40px;
}

.recommendation-info {
  background: rgba(183, 148, 246, 0.1);
  border: 1px solid rgba(183, 148, 246, 0.2);
  border-radius: 16px;
  padding: 20px 32px;
  margin-bottom: 40px;
  backdrop-filter: blur(10px);
}

.info-text {
  font-size: 1.125rem;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.info-icon {
  font-size: 1.5rem;
}

.info-text strong {
  color: var(--accent-mystic);
  font-weight: 700;
}

/* ===== 영화 그리드 ===== */
.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 24px;
}

.movie-item {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.movie-item:hover {
  transform: translateY(-8px);
}

/* ===== 결과 없음 ===== */
.no-results {
  text-align: center;
  padding: 120px 20px;
}

.no-results-icon {
  font-size: 5rem;
  margin-bottom: 24px;
  opacity: 0.5;
}

.no-results-title {
  font-size: 1.75rem;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.no-results-text {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin-bottom: 32px;
}

/* ===== 반응형 ===== */
@media (max-width: 1200px) {
  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .emotion-header,
  .standard-header {
    padding: 60px 20px 40px;
  }

  .emotion-title,
  .standard-title {
    font-size: 2rem;
  }

  .emotion-tagline {
    font-size: 1.125rem;
  }

  .movies-section {
    padding: 0 20px;
  }

  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 16px;
  }

  .recommendation-info {
    padding: 16px 20px;
  }

  .info-text {
    font-size: 0.95rem;
    flex-direction: column;
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .emotion-title,
  .standard-title {
    font-size: 1.5rem;
  }

  .movie-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
}
</style>
```

---

# 🎨 주요 개선 사항

## 1️⃣ 감정별 색상 적용
- 각 감정마다 고유한 색상 그라디언트
- 헤더 배경, 매치도 바에 반영

## 2️⃣ 태그라인 표시
```
"빗소리와 함께 펑펑 울고 싶다면"
```

## 3️⃣ 감정 매치도
```
████████░░ 85%
```
- 애니메이션으로 채워짐
- 감정별 색상 적용

## 4️⃣ 추천 이유 배너
```
🎯 당신의 슬픔 감정을 위해 선별된 20편의 영화