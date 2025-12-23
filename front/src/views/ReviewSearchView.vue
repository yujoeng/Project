<script setup>
import { ref } from 'vue'
import { searchReviewVideos } from '../api/youtube'
import YoutubeTrailerModal from '../components/YoutubeTrailerModal.vue'

const query = ref('')
const videos = ref([])
const isLoading = ref(false)
const errorMessage = ref('')

const isModalOpen = ref(false)
const currentVideoId = ref(null)

const search = async () => {
  if (!query.value.trim()) return

  isLoading.value = true
  errorMessage.value = ''
  videos.value = []

  try {
    const items = await searchReviewVideos(query.value)
    videos.value = items
  } catch (error) {
    console.error(error)
    if (error.response?.status === 401) {  
      errorMessage.value = '로그인 후 이용 가능합니다.'
    } else {
      errorMessage.value = '영상 검색에 실패했습니다.'
    }
  } finally {
    isLoading.value = false
  }
}

const openVideo = (videoId) => {
  currentVideoId.value = videoId
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}
</script>

<template>
  <div class="page">
    <h1 class="page-title">영화 리뷰 영상 검색</h1>

    <form class="search-bar" @submit.prevent="search">
      <input
        v-model="query"
        type="text"
        placeholder="영화 제목 또는 키워드를 입력하세요"
      />
      <button class="button-primary">검색</button>

    </form>

    <p v-if="isLoading">검색 중...</p>
    <p v-else-if="errorMessage">{{ errorMessage }}</p>

    <div v-else class="video-list">
      <div
        v-for="item in videos"
        :key="item.id.videoId"
        class="video-card"
        @click="openVideo(item.id.videoId)"
      >
        <img
          :src="item.snippet.thumbnails.medium.url"
          :alt="item.snippet.title"
        />
        <h3>{{ item.snippet.title }}</h3>
        <p class="channel">{{ item.snippet.channelTitle }}</p>
      </div>
    </div>

    <YoutubeTrailerModal
      v-if="isModalOpen"
      :video-id="currentVideoId"
      @close="closeModal"
    />
  </div>
</template>

<style scoped>
.page {
  padding: 24px;
}

.search-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.search-bar input {
  flex: 1;
  padding: 8px;
}

.search-bar button {
  padding: 8px 16px;
}

.video-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.video-card {
  width: 260px;
  cursor: pointer;
}

.video-card img {
  width: 100%;
  border-radius: 8px;
}

.video-card h3 {
  margin-top: 8px;
  font-size: 14px;
}

.channel {
  font-size: 12px;
  color: #777;
}
</style>
