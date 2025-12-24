<script setup>
import { ref, onMounted } from 'vue'
import { searchReviewVideos } from '@/api/youtube'

const props = defineProps({
  movieTitle: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close'])

const videos = ref([])
const isLoading = ref(false)
const errorMessage = ref('')
const currentVideoId = ref(null)
const isPlayerOpen = ref(false)

const loadRelatedVideos = async () => {
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    const searchQuery = `${props.movieTitle} 리뷰 해설`
    const items = await searchReviewVideos(searchQuery)
    videos.value = items
    
    if (items.length === 0) {
      errorMessage.value = '관련 영상을 찾을 수 없습니다.'
    }
  } catch (error) {
    console.error('YouTube 검색 실패:', error)
    errorMessage.value = '영상을 불러오는 데 실패했습니다.'
  } finally {
    isLoading.value = false
  }
}

const openVideo = (videoId) => {
  currentVideoId.value = videoId
  isPlayerOpen.value = true
}

const closePlayer = () => {
  isPlayerOpen.value = false
  currentVideoId.value = null
}

onMounted(() => {
  loadRelatedVideos()
})
</script>

<template>
  <div class="modal-overlay" @click="emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>{{ movieTitle }} - 관련 영상</h2>
        <button @click="emit('close')" class="btn-close">✕</button>
      </div>

      <div v-if="isLoading" class="loading">
        <div class="spinner"></div>
        <p>관련 영상을 찾는 중...</p>
      </div>

      <div v-else-if="errorMessage" class="error-message">
        <p>{{ errorMessage }}</p>
      </div>

      <div v-else class="video-grid">
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
          <div class="video-info">
            <h3>{{ item.snippet.title }}</h3>
            <p class="channel">{{ item.snippet.channelTitle }}</p>
          </div>
        </div>
      </div>

      <!-- 영상 플레이어 -->
      <div v-if="isPlayerOpen" class="player-overlay" @click="closePlayer">
        <div class="player-container" @click.stop>
          <button @click="closePlayer" class="player-close">✕</button>
          <iframe
            :src="`https://www.youtube.com/embed/${currentVideoId}?autoplay=1`"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 20px;
  max-width: 1200px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 30px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
  border: 1px solid rgba(183, 148, 246, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid rgba(183, 148, 246, 0.3);
}

.modal-header h2 {
  font-size: 1.8rem;
  background: linear-gradient(135deg, #b794f6, #9b59b6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.btn-close {
  background: none;
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
  transition: all 0.3s;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.btn-close:hover {
  background: rgba(183, 148, 246, 0.2);
  color: #b794f6;
  transform: rotate(90deg);
}

.loading {
  text-align: center;
  padding: 60px 20px;
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

.error-message {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.6);
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.video-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid transparent;
}

.video-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(183, 148, 246, 0.4);
  border-color: rgba(183, 148, 246, 0.5);
}

.video-card img {
  width: 100%;
  aspect-ratio: 16/9;
  object-fit: cover;
}

.video-info {
  padding: 15px;
}

.video-info h3 {
  font-size: 0.95rem;
  line-height: 1.4;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  color: white;
}

.channel {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
}

/* 영상 플레이어 */
.player-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
  animation: fadeIn 0.3s ease;
}

.player-container {
  position: relative;
  width: 90%;
  max-width: 1200px;
  aspect-ratio: 16/9;
}

.player-close {
  position: absolute;
  top: -50px;
  right: 0;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
}

.player-close:hover {
  background: rgba(183, 148, 246, 0.3);
  border-color: #b794f6;
}

.player-container iframe {
  width: 100%;
  height: 100%;
  border-radius: 12px;
}

/* 반응형 */
@media (max-width: 768px) {
  .modal-content {
    padding: 20px;
  }

  .modal-header h2 {
    font-size: 1.3rem;
  }

  .video-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
  }

  .player-container {
    width: 95%;
  }
}
</style>