<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchMovies } from '@/api/movies'

const route = useRoute()
const router = useRouter()

const searchQuery = ref('')
const movies = ref([])
const isLoading = ref(false)
const errorMessage = ref('')
const showSearchForm = ref(false)

const performSearch = async () => {
  const query = route.query.q

  if (!query) {
    showSearchForm.value = true
    return
  }

  showSearchForm.value = false
  searchQuery.value = query
  isLoading.value = true
  errorMessage.value = ''

  try {
    const data = await searchMovies(query)
    movies.value = data.results || []
    
    if (movies.value.length === 0) {
      errorMessage.value = '검색 결과가 없습니다.'
    }
  } catch (error) {
    console.error('검색 실패:', error)
    errorMessage.value = '검색 중 오류가 발생했습니다.'
  } finally {
    isLoading.value = false
  }
}

const goToMovie = (movieId) => {
  router.push(`/movies/${movieId}`)
}

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      name: 'movie-search',
      query: { q: searchQuery.value.trim() }
    })
  }
}

watch(() => route.query.q, () => {
  performSearch()
})

onMounted(() => {
  performSearch()
})

</script>

<template>
   <div class="search-result-view">
    <!-- 👇 추가: 검색 폼 -->
    <div v-if="showSearchForm" class="search-form-container">
      <h1>영화 검색</h1>
      <form @submit.prevent="handleSearch" class="search-form">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="영화 제목을 입력하세요..."
          class="search-input"
          autofocus
        />
        <button type="submit" class="search-button">
          🔍 검색
        </button>
      </form>
      <p class="search-hint">영화 제목으로 검색해보세요</p>
    </div>

    <!-- 👇 기존: 검색 결과 -->
    <div v-else>
      <!-- 검색어 다시 입력 -->
      <div class="search-header">
        <h1>"{{ searchQuery }}" 검색 결과</h1>
        <p v-if="!isLoading && !errorMessage">{{ movies.length }}개의 영화를 찾았습니다</p>
        
        <!-- 👇 추가: 다시 검색하기 -->
        <form @submit.prevent="handleSearch" class="search-form-inline">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="다른 영화 검색..."
            class="search-input-small"
          />
          <button type="submit" class="search-button-small">🔍</button>
        </form>
      </div>

      <div v-if="isLoading" class="loading">
        <div class="spinner"></div>
        <p>검색 중...</p>
      </div>

      <div v-else-if="errorMessage" class="no-results">
        <p>😢 {{ errorMessage }}</p>
        <p>다른 검색어를 시도해보세요</p>
        <button @click="router.push('/movies')" class="btn-back">전체 영화 보기</button>
      </div>

      <div v-else class="movie-grid">
        <div 
          v-for="movie in movies" 
          :key="movie.id" 
          class="movie-card"
          @click="goToMovie(movie.id)"
        >
          <div class="poster-wrapper">
            <img 
              v-if="movie.poster_path"
              :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" 
              :alt="movie.title"
            />
            <div v-else class="no-poster">
              <span>🎬</span>
              <p>포스터 없음</p>
            </div>
          </div>
          <div class="movie-info">
            <h3>{{ movie.title }}</h3>
            <div class="meta">
              <span class="rating">⭐ {{ movie.vote_average?.toFixed(1) || 'N/A' }}</span>
              <span class="year">{{ movie.release_date?.split('-')[0] || '' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.search-result-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0a1a 0%, #1a1a2e 100%);
  padding: 100px 40px 60px;
  color: white;
}

/* 👇 추가: 검색 폼 스타일 */
.search-form-container {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  padding: 80px 20px;
}

.search-form-container h1 {
  font-size: 3rem;
  margin-bottom: 40px;
  background: linear-gradient(135deg, #b794f6, #9b59b6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
}

.search-form {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 18px 24px;
  border: 2px solid rgba(183, 148, 246, 0.3);
  border-radius: 50px;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 1.1rem;
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: rgba(183, 148, 246, 0.6);
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 20px rgba(183, 148, 246, 0.3);
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-button {
  padding: 18px 40px;
  background: linear-gradient(135deg, #b794f6, #9b59b6);
  border: none;
  border-radius: 50px;
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.search-button:hover {
  background: linear-gradient(135deg, #9b59b6, #8e44ad);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(183, 148, 246, 0.4);
}

.search-hint {
  color: rgba(255, 255, 255, 0.5);
  font-size: 1rem;
}

/* 검색 헤더 */
.search-header {
  max-width: 1400px;
  margin: 0 auto 40px;
}

.search-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  background: linear-gradient(135deg, #b794f6, #9b59b6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
}

.search-header p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
  margin-bottom: 20px;
}

/* 👇 추가: 인라인 검색 폼 */
.search-form-inline {
  display: flex;
  gap: 8px;
  max-width: 500px;
  margin-top: 20px;
}

.search-input-small {
  flex: 1;
  padding: 12px 20px;
  border: 1px solid rgba(183, 148, 246, 0.3);
  border-radius: 30px;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 0.95rem;
  transition: all 0.3s;
}

.search-input-small:focus {
  outline: none;
  border-color: rgba(183, 148, 246, 0.6);
  background: rgba(255, 255, 255, 0.1);
}

.search-input-small::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-button-small {
  padding: 12px 20px;
  background: rgba(183, 148, 246, 0.2);
  border: 1px solid rgba(183, 148, 246, 0.4);
  border-radius: 30px;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s;
}

.search-button-small:hover {
  background: rgba(183, 148, 246, 0.3);
  border-color: rgba(183, 148, 246, 0.6);
}

.loading {
  text-align: center;
  padding: 100px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(183, 148, 246, 0.2);
  border-top-color: #b794f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.movie-grid {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 30px;
  justify-items: center;
}

.movie-card {
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  border-radius: 12px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid transparent;
  width: 100%;  /* 👈 추가 */
  max-width: 250px; 
}

.movie-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 30px rgba(183, 148, 246, 0.4);
  border-color: rgba(183, 148, 246, 0.5);
}

.poster-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 2/3;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.3);
}

.poster-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-poster {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #2a2a3e, #1a1a2e);
  color: rgba(255, 255, 255, 0.5);
}

.no-poster span {
  font-size: 3rem;
  margin-bottom: 10px;
}

.movie-info {
  padding: 15px;
}

.movie-info h3 {
  font-size: 1rem;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
  min-height: 2.8em;
}

.meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.rating {
  color: #ffd700;
}

.year {
  color: rgba(255, 255, 255, 0.6);
}

.no-results {
  text-align: center;
  padding: 100px 20px;
  color: rgba(255, 255, 255, 0.6);
}

.no-results p {
  font-size: 1.3rem;
  margin-bottom: 15px;
}

.btn-back {
  margin-top: 30px;
  padding: 12px 30px;
  background: linear-gradient(135deg, #b794f6, #9b59b6);
  color: white;
  border: none;
  border-radius: 30px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-back:hover {
  background: linear-gradient(135deg, #9b59b6, #8e44ad);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(183, 148, 246, 0.4);
}

/* 반응형 */
@media (max-width: 1024px) {
  .search-result-view {
    padding: 80px 24px 40px;
  }

  .search-form-container h1 {
    font-size: 2.5rem;
  }

  .search-header h1 {
    font-size: 2rem;
  }

  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .search-form {
    flex-direction: column;
  }

  .search-button {
    width: 100%;
  }

  .search-form-container h1 {
    font-size: 2rem;
  }

  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 15px;
  }

  .search-header h1 {
    font-size: 1.5rem;
  }
}
</style>