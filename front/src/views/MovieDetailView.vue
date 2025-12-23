<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import tmdb from '../api/tmdb'
import { searchTrailer } from '../api/youtube'
import YoutubeTrailerModal from '../components/YoutubeTrailerModal.vue'
import { getMovieDetail } from '@/api/movies'

const route = useRoute()
const router = useRouter()

const movieId = route.params.movieId

const movie = ref(null)
const isLoading = ref(true)
const errorMessage = ref('')

const isTrailerOpen = ref(false)
const trailerId = ref(null)

const openTrailer = async () => {
  if (!movie.value) return

  console.log('예고편 버튼 클릭!')  

  const videoId = await searchTrailer(movie.value.title)
  console.log('찾은 videoId:', videoId)

  trailerId.value = videoId
  isTrailerOpen.value = true
}

const closeTrailer = () => {
  isTrailerOpen.value = false
}

onMounted(async () => {
  try {
    // const res = await tmdb.get(`/movie/${movieId}`)
    const res = await getMovieDetail(movieId)
    movie.value = res.data
    console.log('상세 정보:', res.data)
    movie.value = res.data
  } catch (error) {
    console.error(error)
    errorMessage.value = '영화 상세 정보를 가져오는데 실패했습니다.'
  } finally {
    isLoading.value = false
  }
})

const goBackToList = () => {
  router.push('/movies')
}
</script>

<template>
  <div class="page">
    <button class="button-outline" @click="goBackToList">
      ← 목록으로
    </button>

    <h1 class="page-title">영화 상세 정보</h1>

    <p v-if="isLoading">로딩 중...</p>
    <p v-else-if="errorMessage">{{ errorMessage }}</p>

    <div v-else-if="movie" class="detail">
      <img
        class="poster"
        :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
        :alt="movie.title"
      />

      <div class="info">
        <h1>{{ movie.title }}</h1>
        <p class="original-title">원제: {{ movie.original_title }}</p>
        <p>개봉일: {{ movie.release_date }}</p>
        <p>평점: ⭐ {{ movie.vote_average }} ({{ movie.vote_count }}명)</p>

        <p class="genres">
          장르:
          <span v-for="g in movie.genres" :key="g.id">
            {{ g.name }}
          </span>
        </p>

        <p class="overview">
          {{ movie.overview || '줄거리 정보가 없습니다.' }}
        </p>

        <button class="button-primary" @click="openTrailer">
          공식 예고편 보기
        </button>
      </div>
    </div>
    
    <YoutubeTrailerModal
      v-if="isTrailerOpen"
      :video-id="trailerId"
      @close="closeTrailer"
    />


  </div>
</template>

<style scoped>
.page {
  padding: 24px;
}

.back-btn {
  margin-bottom: 16px;
}

.detail {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.poster {
  width: 300px;
  border-radius: 8px;
}

.info {
  max-width: 600px;
}

.original-title {
  font-size: 14px;
  color: #666;
}

.genres span + span::before {
  content: ' / ';
}

.overview {
  margin-top: 16px;
  line-height: 1.5;
}


</style>
