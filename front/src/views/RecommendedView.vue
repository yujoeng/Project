<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import apiClient from '@/api/axios'

const router = useRouter()

// 프로필 정보
const profile = ref({
  favorite_genres: [],
  favorite_actors: '',
  preferred_countries: []
})

// 추천 영화 목록
const genreMovies = ref([])
const countryMovies = ref([])
const favoriteBasedMovies = ref([])
const isLoading = ref(true)
const errorMessage = ref('')

// 찜한 영화 목록
const favoriteMovies = ref([])

const TMDB_API_KEY = import.meta.env.VITE_TMDB_API_KEY
const TMDB_BASE_URL = 'https://api.themoviedb.org/3'

// 장르 이름 -> TMDB ID 매핑
const genreMap = {
  '액션': 28,
  '코미디': 35,
  '드라마': 18,
  '스릴러': 53,
  '공포': 27,
  'SF': 878,
  '판타지': 14,
  '로맨스': 10749,
  '애니메이션': 16,
  '다큐멘터리': 99
}

// 국가 이름 -> 코드 매핑
const countryMap = {
  '한국': 'KR',
  '미국': 'US',
  '일본': 'JP',
  '중국': 'CN',
  '프랑스': 'FR',
  '영국': 'GB'
}

// 프로필 조회
const fetchProfile = async () => {
  try {
    const response = await apiClient.get('/accounts/profile/')
    profile.value = response.data
    console.log('프로필 정보:', profile.value)
  } catch (error) {
    console.error('프로필 조회 실패:', error)
    errorMessage.value = '프로필을 불러올 수 없습니다. 프로필을 먼저 설정해주세요.'
  }
}

// 장르 기반 영화 추천
const fetchGenreMovies = async () => {
  if (!profile.value.favorite_genres || profile.value.favorite_genres.length === 0) {
    return
  }

  try {
    // 선호 장르 ID로 변환
    const genreIds = profile.value.favorite_genres
      .map(genre => genreMap[genre])
      .filter(id => id !== undefined)
      .join(',')

    if (!genreIds) return

    const response = await axios.get(`${TMDB_BASE_URL}/discover/movie`, {
      params: {
        api_key: TMDB_API_KEY,
        language: 'ko-KR',
        sort_by: 'popularity.desc',
        with_genres: genreIds,
        page: 1
      }
    })

    genreMovies.value = response.data.results.slice(0, 12)
  } catch (error) {
    console.error('장르 기반 영화 로딩 실패:', error)
  }
}

// 국가 기반 영화 추천
const fetchCountryMovies = async () => {
  if (!profile.value.preferred_countries || profile.value.preferred_countries.length === 0) {
    return
  }

  try {
    const allMovies = []

    // 각 국가별로 영화 검색
    for (const country of profile.value.preferred_countries) {
      const countryCode = countryMap[country]
      if (!countryCode) continue

      const response = await axios.get(`${TMDB_BASE_URL}/discover/movie`, {
        params: {
          api_key: TMDB_API_KEY,
          language: 'ko-KR',
          sort_by: 'popularity.desc',
          with_origin_country: countryCode,
          page: 1
        }
      })

      allMovies.push(...response.data.results.slice(0, 6))
    }

    // 중복 제거 및 최대 12개
    const uniqueMovies = Array.from(
      new Map(allMovies.map(movie => [movie.id, movie])).values()
    )
    countryMovies.value = uniqueMovies.slice(0, 12)
  } catch (error) {
    console.error('국가 기반 영화 로딩 실패:', error)
  }
}

// 영화 상세 페이지로 이동
const goToMovie = (movieId) => {
  router.push(`/movies/${movieId}`)
}

// 프로필 설정 페이지로 이동
const goToProfile = () => {
  router.push('/profile')
}

// 찜한 영화 목록 조회
const fetchFavoriteMovies = async () => {
  try {
    const response = await apiClient.get('/accounts/favorite-movies/')
    favoriteMovies.value = response.data.favorite_movies || []
  } catch (error) {
    console.error('찜한 영화 조회 실패:', error)
  }
}

// 찜한 영화 기반 추천
const fetchFavoriteBasedMovies = async () => {
  if (!favoriteMovies.value || favoriteMovies.value.length === 0) {
    return
  }

  try {
    const allSimilarMovies = []

    // 찜한 영화 중 최대 5개만 사용 (API 호출 제한)
    const moviesToCheck = favoriteMovies.value.slice(0, 5)

    for (const movieId of moviesToCheck) {
      try {
        const response = await axios.get(`${TMDB_BASE_URL}/movie/${movieId}/similar`, {
          params: {
            api_key: TMDB_API_KEY,
            language: 'ko-KR',
            page: 1
          }
        })

        allSimilarMovies.push(...response.data.results.slice(0, 4))
      } catch (error) {
        console.error(`영화 ${movieId}의 비슷한 영화 로딩 실패:`, error)
      }
    }

    // 중복 제거 및 찜한 영화 제외
    const uniqueMovies = Array.from(
      new Map(allSimilarMovies.map(movie => [movie.id, movie])).values()
    ).filter(movie => !favoriteMovies.value.includes(movie.id))

    favoriteBasedMovies.value = uniqueMovies.slice(0, 12)
  } catch (error) {
    console.error('찜한 영화 기반 추천 로딩 실패:', error)
  }
}

onMounted(async () => {
  isLoading.value = true
  await fetchProfile()
  await fetchFavoriteMovies()

  // 추천 영화 로딩
  await Promise.all([
    fetchGenreMovies(),
    fetchCountryMovies(),
    fetchFavoriteBasedMovies()
  ])

  isLoading.value = false
})

// 추천 영화가 있는지 확인
const hasRecommendations = computed(() => {
  return genreMovies.value.length > 0 || countryMovies.value.length > 0 || favoriteBasedMovies.value.length > 0
})
</script>

<template>
  <div class="recommended-page">
    <div class="page-header">
      <h1>나를 위한 추천 영화</h1>
      <p class="subtitle">프로필 설정을 바탕으로 맞춤 영화를 추천해드립니다</p>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>추천 영화를 찾는 중...</p>
    </div>

    <!-- 에러 메시지 -->
    <div v-else-if="errorMessage" class="error-container">
      <p class="error-text">{{ errorMessage }}</p>
      <button @click="goToProfile" class="btn-profile">프로필 설정하러 가기</button>
    </div>

    <!-- 프로필 미설정 -->
    <div v-else-if="!hasRecommendations" class="empty-container">
      <div class="empty-icon">🎬</div>
      <h2>아직 설정된 선호 정보가 없습니다</h2>
      <p>프로필에서 선호 장르와 관심 국가를 설정하면<br>맞춤 영화를 추천해드립니다!</p>
      <button @click="goToProfile" class="btn-profile">프로필 설정하러 가기</button>
    </div>

    <!-- 추천 영화 목록 -->
    <div v-else class="recommendations-container">
      <!-- 찜한 영화 기반 추천 -->
      <section v-if="favoriteBasedMovies.length > 0" class="recommendation-section">
        <h2 class="section-title">
          <span class="title-icon">❤️</span>
          내가 찜한 영화와 비슷한 작품
        </h2>
        <div class="movies-grid">
          <div
            v-for="movie in favoriteBasedMovies"
            :key="movie.id"
            class="movie-card"
            @click="goToMovie(movie.id)"
          >
            <div class="movie-poster">
              <img
                v-if="movie.poster_path"
                :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
                :alt="movie.title"
              />
              <div v-else class="no-poster">🎬</div>
            </div>
            <div class="movie-info">
              <h3 class="movie-title">{{ movie.title }}</h3>
              <div class="movie-meta">
                <span class="rating">⭐ {{ movie.vote_average.toFixed(1) }}</span>
                <span class="year">{{ movie.release_date?.split('-')[0] }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 선호 장르 기반 추천 -->
      <section v-if="genreMovies.length > 0" class="recommendation-section">
        <h2 class="section-title">
          <span class="title-icon">🎭</span>
          {{ profile.favorite_genres.join(', ') }} 장르 영화
        </h2>
        <div class="movies-grid">
          <div
            v-for="movie in genreMovies"
            :key="movie.id"
            class="movie-card"
            @click="goToMovie(movie.id)"
          >
            <div class="movie-poster">
              <img
                v-if="movie.poster_path"
                :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
                :alt="movie.title"
              />
              <div v-else class="no-poster">🎬</div>
            </div>
            <div class="movie-info">
              <h3 class="movie-title">{{ movie.title }}</h3>
              <div class="movie-meta">
                <span class="rating">⭐ {{ movie.vote_average.toFixed(1) }}</span>
                <span class="year">{{ movie.release_date?.split('-')[0] }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 관심 국가 기반 추천 -->
      <section v-if="countryMovies.length > 0" class="recommendation-section">
        <h2 class="section-title">
          <span class="title-icon">🌍</span>
          {{ profile.preferred_countries.join(', ') }} 영화
        </h2>
        <div class="movies-grid">
          <div
            v-for="movie in countryMovies"
            :key="movie.id"
            class="movie-card"
            @click="goToMovie(movie.id)"
          >
            <div class="movie-poster">
              <img
                v-if="movie.poster_path"
                :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
                :alt="movie.title"
              />
              <div v-else class="no-poster">🎬</div>
            </div>
            <div class="movie-info">
              <h3 class="movie-title">{{ movie.title }}</h3>
              <div class="movie-meta">
                <span class="rating">⭐ {{ movie.vote_average.toFixed(1) }}</span>
                <span class="year">{{ movie.release_date?.split('-')[0] }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.recommended-page {
  min-height: 100vh;
  padding: 40px 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 50px;
}

.page-header h1 {
  font-size: 2.5rem;
  margin-bottom: 15px;
  background: linear-gradient(135deg, #b794f6, #7b10ad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.7);
}

/* 로딩 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  gap: 20px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(183, 148, 246, 0.2);
  border-top-color: #b794f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-container p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
}

/* 에러/빈 상태 */
.error-container,
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  text-align: center;
  padding: 40px;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-container h2 {
  font-size: 1.8rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 15px;
}

.empty-container p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.6;
  margin-bottom: 30px;
}

.error-text {
  color: #ef4444;
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.btn-profile {
  padding: 12px 30px;
  background: rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.95);
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-profile:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.6);
  transform: translateY(-2px);
}

/* 추천 영화 섹션 */
.recommendations-container {
  display: flex;
  flex-direction: column;
  gap: 60px;
}

.recommendation-section {
  width: 100%;
}

.section-title {
  font-size: 1.8rem;
  margin-bottom: 30px;
  color: rgba(255, 255, 255, 0.95);
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 15px;
  border-bottom: 2px solid rgba(183, 148, 246, 0.3);
}

.title-icon {
  font-size: 1.5rem;
}

/* 영화 그리드 */
.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 25px;
}

.movie-card {
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  border-radius: 12px;
  overflow: hidden;
  background: linear-gradient(135deg, #8b5fc7 0%, #6b4a8f 50%, #4a2d5e 100%);
  border: 2px solid rgba(183, 148, 246, 0.3);
}

.movie-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 30px rgba(183, 148, 246, 0.3);
  border-color: rgba(183, 148, 246, 0.6);
}

.movie-poster {
  width: 100%;
  aspect-ratio: 2/3;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.3);
}

.movie-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.movie-card:hover .movie-poster img {
  transform: scale(1.05);
}

.no-poster {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  background: rgba(0, 0, 0, 0.2);
}

.movie-info {
  padding: 15px;
}

.movie-title {
  font-size: 1rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 8px;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.movie-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.rating {
  color: #fbbf24;
  font-weight: 600;
}

.year {
  color: rgba(255, 255, 255, 0.6);
}

/* 반응형 */
@media (max-width: 1024px) {
  .movies-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 2rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .movies-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 15px;
  }
}

@media (max-width: 480px) {
  .recommended-page {
    padding: 20px 10px;
  }

  .movies-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
