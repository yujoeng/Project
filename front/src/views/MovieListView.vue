<script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router' 
  import { getPopularMovies } from '@/api/movies'
  import MovieCard from '../components/MovieCard.vue'

  const router = useRouter()   

  const movies = ref([])     
  const isLoading = ref(true)
  const errorMessage = ref('')

  const goDetail = (id) => {
  router.push(`/movies/${id}`)
}

  onMounted(async () => {
    try {
      // tmdb.get 대신 getPopularMovies 함수 사용
      const res = await getPopularMovies()
      console.log('인기 영화 결과:', res.data)
      movies.value = res.data.results
    } catch (error) {
      console.error(error)
      errorMessage.value = '영화 정보를 가져오는데 실패했습니다.'
    } finally {
      isLoading.value = false
    }
  })
  </script>

<template>
  <div class="page">
    <h1 class="page-title">최고 평점 영화 목록</h1>

    <p v-if="isLoading">로딩 중...</p>
    <p v-else-if="errorMessage">{{ errorMessage }}</p>

    <div v-else class="movie-list">
      <div
        v-for="movie in movies"
        :key="movie.id"
        class="click-wrapper"
        @click="goDetail(movie.id)"
      >
        <MovieCard :movie="movie" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  
}

.page-title {
  margin: 0 0 20px;
  font-size: 28px;
}
.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.click-wrapper {
  cursor: pointer;
}
.click-wrapper:hover {
  transform: translateY(-4px);
  transition: 0.1s;
}
</style>
