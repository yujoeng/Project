<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

// 컴포넌트 및 API 임포트
import { searchTrailer } from '../api/youtube'
import YoutubeTrailerModal from '../components/YoutubeTrailerModal.vue'
import ReviewSection from '../components/ReviewSection.vue'
import { getMovieDetail as getDjangoMovieDetail } from '@/api/movies'

const route = useRoute()
const router = useRouter()

// 상태 관리
const movie = ref(null)
const credits = ref(null)
const tmdbVideos = ref([])
const similar = ref([])
const isLoading = ref(true)
const errorMessage = ref('')

const isTrailerOpen = ref(false)
const trailerId = ref(null)

const TMDB_API_KEY = import.meta.env.VITE_TMDB_API_KEY
const TMDB_BASE_URL = 'https://api.themoviedb.org/3'

// --- Computed 속성 ---

const releaseYear = computed(() => movie.value?.release_date?.split('-')[0] || 'N/A')
const runtimeFormatted = computed(() => {
  if (!movie.value?.runtime) return 'N/A'
  const h = Math.floor(movie.value.runtime / 60)
  const m = movie.value.runtime % 60
  return `${h}시간 ${m}분`
})

const genreNames = computed(() => movie.value?.genres?.map(g => g.name).join(' · ') || '')

const officialTrailer = computed(() => {
  return tmdbVideos.value.find(v => v.site === 'YouTube' && (v.type === 'Trailer' || v.type === 'Teaser'))
})

const mainCast = computed(() => credits.value?.cast?.slice(0, 6) || [])
const director = computed(() => credits.value?.crew?.find(c => c.job === 'Director')?.name || 'N/A')

// --- 함수 로직 ---

const loadMovieData = async () => {
  isLoading.value = true
  errorMessage.value = ''
  const movieId = route.params.movieId

  try {
    // 1. Django API (DB 정보)와 TMDB 정보를 병렬로 호출 시도
    const [djangoRes, tmdbRes, creditsRes, videosRes, similarRes] = await Promise.all([
      getDjangoMovieDetail(movieId).catch(() => ({ data: null })), // Django 데이터가 없을 경우 대비
      axios.get(`${TMDB_BASE_URL}/movie/${movieId}`, { params: { api_key: TMDB_API_KEY, language: 'ko-KR' } }),
      axios.get(`${TMDB_BASE_URL}/movie/${movieId}/credits`, { params: { api_key: TMDB_API_KEY, language: 'ko-KR' } }),
      axios.get(`${TMDB_BASE_URL}/movie/${movieId}/videos`, { params: { api_key: TMDB_API_KEY, language: 'ko-KR' } }),
      axios.get(`${TMDB_BASE_URL}/movie/${movieId}/similar`, { params: { api_key: TMDB_API_KEY, language: 'ko-KR', page: 1 } })
    ])

    movie.value = tmdbRes.data
    credits.value = creditsRes.data
    tmdbVideos.value = videosRes.data.results
    similar.value = similarRes.data.results.slice(0, 6)
  } catch (error) {
    console.error('데이터 로딩 실패:', error)
    errorMessage.value = '영화 정보를 불러오는 데 실패했습니다.'
  } finally {
    isLoading.value = false
  }
}

const openTrailer = async () => {
  if (officialTrailer.value) {
    trailerId.value = officialTrailer.value.key
    isTrailerOpen.value = true
  } else {
    // TMDB에 없을 경우 유튜브 검색 API 활용
    const videoId = await searchTrailer(movie.value.title)
    if (videoId) {
      trailerId.value = videoId
      isTrailerOpen.value = true
    } else {
      alert('예고편을 찾을 수 없습니다.')
    }
  }
}

const closeTrailer = () => { isTrailerOpen.value = false }

const goToMovie = (id) => {
  router.push(`/movies/${id}`)
  window.scrollTo(0, 0)
}

// 경로 변경 감시 (비슷한 영화 클릭 시 갱신)
watch(() => route.params.movieId, () => loadMovieData())

onMounted(() => loadMovieData())
</script>

<template>
  <div class="movie-detail-view">
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>영화 정보를 불러오는 중...</p>
    </div>

    <div v-else-if="errorMessage" class="error-container">
      <span class="error-icon">⚠️</span>
      <p>{{ errorMessage }}</p>
      <button @click="router.push('/movies')" class="btn-back">목록으로 돌아가기</button>
    </div>

    <div v-else-if="movie" class="movie-detail">
      <section class="hero-section">
        <div class="backdrop-image" :style="{ backgroundImage: `url(https://image.tmdb.org/t/p/original${movie.backdrop_path})` }"></div>
        <div class="backdrop-overlay"></div>

        <div class="hero-content">
          <button @click="router.go(-1)" class="btn-back-hero">← 뒤로가기</button>

          <div class="hero-main">
            <div class="poster-large">
              <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" :alt="movie.title" />
            </div>

            <div class="movie-main-info">
              <h1 class="movie-title-large gradient-text">{{ movie.title }}</h1>
              <p class="original-title">{{ movie.original_title }}</p>

              <div class="meta-info">
                <span>{{ releaseYear }}</span>
                <span class="meta-divider">•</span>
                <span>{{ runtimeFormatted }}</span>
                <span class="meta-divider">•</span>
                <span>{{ genreNames }}</span>
              </div>

              <div class="rating-section">
                <div class="rating-badge-large">
                  <span class="rating-value">⭐ {{ movie.vote_average?.toFixed(1) }}</span>
                </div>
                <span class="vote-count">{{ movie.vote_count?.toLocaleString() }}명 참여</span>
              </div>

              <p v-if="movie.tagline" class="tagline">"{{ movie.tagline }}"</p>

              <div class="overview-section">
                <h3>줄거리</h3>
                <p class="overview-text">{{ movie.overview || '줄거리 정보가 없습니다.' }}</p>
              </div>

              <div class="director-info">
                <span class="label">감독:</span> <span class="value">{{ director }}</span>
              </div>

              <div class="action-buttons">
                <button class="btn-trailer" @click="openTrailer">
                  <span>▶ 예고편 보기</span>
                  <span v-if="officialTrailer" class="official-badge">공식</span>
                </button>
                <button class="btn-bookmark">🔖 찜하기</button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section cast-section">
        <h2 class="section-heading">주요 출연진</h2>
        <div class="cast-grid">
          <div v-for="actor in mainCast" :key="actor.id" class="cast-card">
            <div class="cast-photo">
              <img v-if="actor.profile_path" :src="`https://image.tmdb.org/t/p/w185${actor.profile_path}`" alt="" />
              <div v-else class="no-photo">👤</div>
            </div>
            <p class="actor-name">{{ actor.name }}</p>
            <p class="character-name">{{ actor.character }}</p>
          </div>
        </div>
      </section>

      <section class="section review-section">
        <h2 class="section-heading">평점 및 리뷰</h2>
        <ReviewSection :movie-id="Number(route.params.movieId)" />
      </section>

      <section class="section similar-section">
        <h2 class="section-heading">비슷한 영화 추천</h2>
        <div class="similar-grid">
          <div v-for="sim in similar" :key="sim.id" class="similar-card" @click="goToMovie(sim.id)">
            <img :src="`https://image.tmdb.org/t/p/w300${sim.poster_path}`" alt="" />
            <div class="similar-info">
              <p class="similar-title">{{ sim.title }}</p>
              <p class="similar-rating">⭐ {{ sim.vote_average?.toFixed(1) }}</p>
            </div>
          </div>
        </div>
      </section>
    </div>

    <YoutubeTrailerModal v-if="isTrailerOpen" :video-id="trailerId" @close="closeTrailer" />
  </div>
</template>

<style scoped>
/* 변수 및 기본 레이아웃 */
.movie-detail-view { background-color: #0f0a1a; min-height: 100vh; color: white; }

/* 로딩/에러 스타일 */
.loading-container, .error-container { 
  display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 70vh; 
}
.loading-spinner { 
  width: 50px; height: 50px; border: 5px solid rgba(183,148,246,0.2); border-top-color: #b794f6; 
  border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 20px;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* 히어로 섹션 */
.hero-section { position: relative; min-height: 80vh; overflow: hidden; display: flex; align-items: center; }
.backdrop-image { 
  position: absolute; inset: 0; background-size: cover; background-position: center; 
  filter: blur(15px); transform: scale(1.1); opacity: 0.4;
}
.backdrop-overlay { position: absolute; inset: 0; background: linear-gradient(to bottom, transparent, #0f0a1a); }

.hero-content { position: relative; z-index: 2; max-width: 1300px; margin: 0 auto; padding: 60px 20px; width: 100%; }
.hero-main { display: flex; gap: 50px; align-items: flex-start; }

.poster-large { width: 350px; flex-shrink: 0; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }
.poster-large img { width: 100%; display: block; }

.movie-title-large { font-size: 3.5rem; font-weight: 800; margin-bottom: 10px; }
.meta-info { display: flex; gap: 15px; color: rgba(255,255,255,0.7); margin-bottom: 20px; }
.tagline { font-style: italic; color: #b794f6; margin-bottom: 25px; font-size: 1.2rem; }
.overview-text { line-height: 1.8; color: rgba(255,255,255,0.9); margin-bottom: 20px; max-width: 800px; }

/* 버튼 스타일 */
.action-buttons { display: flex; gap: 15px; margin-top: 30px; }
.btn-trailer { 
  background: #e74c3c; color: white; border: none; padding: 12px 25px; border-radius: 30px; 
  font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 10px;
}
.official-badge { font-size: 0.7rem; background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px; }
.btn-bookmark { background: rgba(255,255,255,0.1); color: white; border: 1px solid rgba(255,255,255,0.3); padding: 12px 25px; border-radius: 30px; cursor: pointer; }

/* 섹션 공통 스타일 */
.section { max-width: 1300px; margin: 80px auto; padding: 0 20px; }
.section-heading { font-size: 1.8rem; margin-bottom: 30px; border-left: 5px solid #b794f6; padding-left: 15px; }

/* 출연진 그리드 */
.cast-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 20px; }
.cast-card { text-align: center; }
.cast-photo { width: 100%; aspect-ratio: 2/3; border-radius: 12px; overflow: hidden; background: #222; margin-bottom: 10px; }
.cast-photo img { width: 100%; height: 100%; object-fit: cover; }
.actor-name { font-weight: 600; font-size: 0.95rem; }
.character-name { font-size: 0.8rem; color: #888; }

/* 비슷한 영화 그리드 */
.similar-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; }
.similar-card { cursor: pointer; transition: transform 0.3s; }
.similar-card:hover { transform: translateY(-10px); }
.similar-card img { width: 100%; border-radius: 10px; }
.similar-title { font-size: 0.9rem; margin-top: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* 반응형 */
@media (max-width: 1024px) {
  .hero-main { flex-direction: column; align-items: center; text-align: center; }
  .poster-large { width: 250px; }
  .movie-title-large { font-size: 2.5rem; }
  .meta-info { justify-content: center; }
  .action-buttons { justify-content: center; }
}
</style>