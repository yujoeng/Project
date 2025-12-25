<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import apiClient from '@/api/axios'

// 컴포넌트 및 API 임포트
import { searchTrailer } from '../api/youtube'
import YoutubeTrailerModal from '../components/YoutubeTrailerModal.vue'
import OttProviderModal from '../components/OttProviderModal.vue'
import ReviewSection from '../components/ReviewSection.vue'
import { getMovieDetail as getDjangoMovieDetail } from '@/api/movies'
import { nextTick } from 'vue'
import YoutubeRelatedModal from '../components/YoutubeRelatedModal.vue'

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

const isOttModalOpen = ref(false)
const ottProviders = ref(null)

// 찜하기 관련 상태
const favoriteMovies = ref([])
const isFavorite = ref(false)
const isFavoriteLoading = ref(false)

// 관련 영상 모달 상태
const isRelatedVideosOpen = ref(false)

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

  // 페이지 시작 시 스크롤을 맨 위로 이동
  window.scrollTo(0, 0)

  try {
    // 1. Django API (DB 정보)와 TMDB 정보를 병렬로 호출 시도
    const [djangoRes, tmdbRes, creditsRes, videosRes, similarRes, watchProvidersRes] = await Promise.all([
      getDjangoMovieDetail(movieId).catch(() => ({ data: null })), // Django 데이터가 없을 경우 대비
      axios.get(`${TMDB_BASE_URL}/movie/${movieId}`, { params: { api_key: TMDB_API_KEY, language: 'ko-KR' } }),
      axios.get(`${TMDB_BASE_URL}/movie/${movieId}/credits`, { params: { api_key: TMDB_API_KEY, language: 'ko-KR' } }),
      axios.get(`${TMDB_BASE_URL}/movie/${movieId}/videos`, { params: { api_key: TMDB_API_KEY, language: 'ko-KR' } }),
      axios.get(`${TMDB_BASE_URL}/movie/${movieId}/similar`, { params: { api_key: TMDB_API_KEY, language: 'ko-KR', page: 1 } }),
      axios.get(`${TMDB_BASE_URL}/movie/${movieId}/watch/providers`, { params: { api_key: TMDB_API_KEY } })
        .catch((err) => {
          console.warn('OTT 정보 로딩 실패:', err)
          return { data: { results: {} } }
        })
    ])

    movie.value = tmdbRes.data
    credits.value = creditsRes.data
    tmdbVideos.value = videosRes.data.results
    similar.value = similarRes.data.results.slice(0, 6)
    // KR(한국) 지역의 OTT 정보 저장
    ottProviders.value = watchProvidersRes.data.results?.KR || null
    console.log('OTT 정보 로딩 완료:', ottProviders.value)
  } catch (error) {
    console.error('데이터 로딩 실패:', error)
    errorMessage.value = '영화 정보를 불러오는 데 실패했습니다.'
  } finally {
    isLoading.value = false
    // 데이터 로딩 완료 후 다시 한 번 스크롤을 맨 위로 이동
    await nextTick()
    window.scrollTo({ top: 0, behavior: 'instant' })
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

const openOttModal = () => {
  try {
    console.log('OTT 모달 열기 시도:', ottProviders.value)
    isOttModalOpen.value = true
  } catch (error) {
    console.error('OTT 모달 열기 오류:', error)
  }
}

const closeOttModal = () => {
  try {
    isOttModalOpen.value = false
  } catch (error) {
    console.error('OTT 모달 닫기 오류:', error)
  }
}

const goToMovie = async (id) => {
  await router.push(`/movies/${id}`)
  // 라우터 이동 후 스크롤 최상단으로 이동
  await nextTick()
  window.scrollTo({ top: 0, behavior: 'instant' })
}

// 찜한 영화 목록 가져오기
const fetchFavoriteMovies = async () => {
  try {
    const response = await apiClient.get('/accounts/favorite-movies/')
    favoriteMovies.value = response.data.favorite_movies || []

    // 현재 영화가 찜 목록에 있는지 확인
    const currentMovieId = Number(route.params.movieId)
    isFavorite.value = favoriteMovies.value.includes(currentMovieId)
  } catch (error) {
    console.error('찜한 영화 목록 조회 실패:', error)
    // 인증 오류 시 무시 (로그인 안 된 상태)
    if (error.response?.status !== 401) {
      console.error('찜한 영화 목록 조회 중 오류 발생')
    }
  }
}

// 관련 영상 모달 열기
const openRelatedVideos = () => {
  isRelatedVideosOpen.value = true
}

// 관련 영상 모달 닫기
const closeRelatedVideos = () => {
  isRelatedVideosOpen.value = false
}

// 찜하기 토글
const toggleFavorite = async () => {
  if (isFavoriteLoading.value) return

  try {
    isFavoriteLoading.value = true
    const movieId = Number(route.params.movieId)

    const response = await apiClient.post('/accounts/favorite-movies/toggle/', {
      movie_id: movieId
    })

    // 상태 업데이트
    isFavorite.value = response.data.is_favorite
    favoriteMovies.value = response.data.favorite_movies

    // 사용자 피드백
    const message = response.data.message || (isFavorite.value ? '찜하기에 추가되었습니다.' : '찜하기가 취소되었습니다.')
    console.log(message)
  } catch (error) {
    console.error('찜하기 토글 실패:', error)

    if (error.response?.status === 401) {
      alert('로그인이 필요합니다.')
      router.push('/login')
    } else {
      alert('찜하기 처리 중 오류가 발생했습니다.')
    }
  } finally {
    isFavoriteLoading.value = false
  }
}

// 경로 변경 감시 (비슷한 영화 클릭 시 갱신)
watch(() => route.params.movieId, () => {
  loadMovieData()
  fetchFavoriteMovies()
})

onMounted(() => {
  loadMovieData()
  fetchFavoriteMovies()
})
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

          <div class="hero-main">
            <div class="poster-large">
              <button @click="router.go(-1)" class="btn-back-hero">← 뒤로가기</button>
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
                <button class="btn-watch-now" @click="openOttModal">
                  🎬 보러가기
                </button>
                <button
                  class="btn-bookmark"
                  :class="{ 'is-favorite': isFavorite }"
                  @click="toggleFavorite"
                  :disabled="isFavoriteLoading"
                >
                  {{ isFavorite ? '❤️' : '🤍' }} {{ isFavorite ? '찜 완료' : '찜하기' }}
                </button>

                <button class="btn-related-videos" @click="openRelatedVideos">
                  📺 관련 영상 보기
                </button>

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
    <OttProviderModal v-if="isOttModalOpen" :providers="ottProviders" :movie-title="movie?.title" @close="closeOttModal" />
    <YoutubeRelatedModal v-if="isRelatedVideosOpen" :movie-title="movie?.title" @close="closeRelatedVideos" />
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

.poster-large { position: relative; width: 350px; flex-shrink: 0; border-radius: 20px; overflow: visible; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }
.poster-large img { width: 100%; display: block; border-radius: 20px; }

.movie-title-large { font-size: 3.5rem; font-weight: 800; margin-bottom: 10px; }
.meta-info { display: flex; gap: 15px; color: rgba(255,255,255,0.7); margin-bottom: 20px; }
.tagline { font-style: italic; color: #b794f6; margin-bottom: 25px; font-size: 1.2rem; }
.overview-text { line-height: 1.8; color: rgba(255,255,255,0.9); margin-bottom: 20px; max-width: 800px; }

/* 버튼 스타일 */
.action-buttons { display: flex; gap: 15px; margin-top: 30px; flex-wrap: wrap; }
.btn-trailer {
  background: #e74c3c; color: white; border: none; padding: 12px 25px; border-radius: 30px;
  font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 10px;
  transition: all 0.3s;
}
.btn-trailer:hover {
  background: #c0392b;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4);
}
.official-badge { font-size: 0.7rem; background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px; }
.btn-watch-now {
  background: linear-gradient(135deg, #b794f6, #9b59b6);
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 30px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}
.btn-watch-now:hover {
  background: linear-gradient(135deg, #9b59b6, #8e44ad);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(183, 148, 246, 0.4);
}
.btn-bookmark {
  background: rgba(255,255,255,0.1);
  color: white;
  border: 1px solid rgba(255,255,255,0.3);
  padding: 12px 25px;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
}
.btn-bookmark:hover {
  background: rgba(255,255,255,0.2);
  border-color: rgba(255,255,255,0.5);
  transform: translateY(-2px);
}
.btn-bookmark.is-favorite {
  background: linear-gradient(135deg, #ff4757, #ff6348);
  border-color: #ff4757;
  color: white;
}
.btn-bookmark.is-favorite:hover {
  background: linear-gradient(135deg, #ee5a6f, #ff7979);
  border-color: #ff6348;
}
.btn-bookmark:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

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

/* 뒤로가기 버튼 - 왼쪽 상단 고정 */
.btn-back-hero {
  position: absolute;  /*  fixed에서 absolute로 변경 */
  top: -60px;  
  left: 0;
  z-index: 10; 
  
  background: rgba(15, 10, 26, 0.9);
  backdrop-filter: blur(10px);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 12px 24px;
  border-radius: 30px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s;
  
  display: flex;
  align-items: center;
  gap: 8px;
  
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.btn-back-hero:hover {
  background: rgba(183, 148, 246, 0.4);
  border-color: rgba(183, 148, 246, 0.6);
  transform: translateX(-5px);
  box-shadow: 0 6px 16px rgba(183, 148, 246, 0.4);
}

.btn-related-videos {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 30px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-related-videos:hover {
  background: linear-gradient(135deg, #c0392b, #a93226);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4);
}



/* 반응형 */
@media (max-width: 1024px) {
  .btn-back-hero {
    top: -50px;
  }
}

@media (max-width: 768px) {
  .btn-back-hero {
    top: -45px;
    padding: 10px 18px;
    font-size: 0.9rem;
  }
}
</style>