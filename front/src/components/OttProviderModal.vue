<script setup>
const props = defineProps({
  providers: {
    type: Object,
    default: () => null,
  },
  movieTitle: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}

// OTT 플랫폼 우선순위 (한국에서 인기있는 순서)
const priorityOrder = ['Netflix', 'Disney Plus', 'Watcha', 'wavve', 'Amazon Prime Video', 'Apple TV', 'Apple TV Plus']

// 각 OTT 플랫폼의 직접 URL 매핑
const getProviderUrl = (providerName, movieTitle) => {
  const encodedTitle = encodeURIComponent(movieTitle)

  const urlMap = {
    'Netflix': 'https://www.netflix.com/search?q=' + encodedTitle,
    'Disney Plus': 'https://www.disneyplus.com/search?q=' + encodedTitle,
    'Watcha': 'https://watcha.com/search?query=' + encodedTitle,
    'wavve': 'https://www.wavve.com/search/total?searchWord=' + encodedTitle,
    'Amazon Prime Video': 'https://www.primevideo.com/search?phrase=' + encodedTitle,
    'Apple TV': 'https://tv.apple.com/search?q=' + encodedTitle,
    'Apple TV Plus': 'https://tv.apple.com/search?q=' + encodedTitle,
    'Google Play Movies': 'https://play.google.com/store/search?q=' + encodedTitle + '&c=movies',
    'YouTube': 'https://www.youtube.com/results?search_query=' + encodedTitle + ' 영화',
    'Naver Store': 'https://serieson.naver.com/v2/search/integration?query=' + encodedTitle,
  }

  return urlMap[providerName] || `https://www.google.com/search?q=${encodedTitle}+영화+VOD`
}

// 플랫폼을 우선순위에 따라 정렬
const sortedProviders = (providerList) => {
  if (!providerList) return []
  return [...providerList].sort((a, b) => {
    const aIndex = priorityOrder.indexOf(a.provider_name)
    const bIndex = priorityOrder.indexOf(b.provider_name)
    if (aIndex === -1) return 1
    if (bIndex === -1) return -1
    return aIndex - bIndex
  })
}

// 링크로 이동 - 각 플랫폼의 직접 링크 사용
const goToProvider = (provider) => {
  const url = getProviderUrl(provider.provider_name, props.movieTitle)
  window.open(url, '_blank')
}
</script>

<template>
  <div class="backdrop" @click.self="close">
    <div class="modal">
      <div class="modal-header">
        <h2>{{ movieTitle }} 보러가기</h2>
        <button class="close-btn" @click="close">✕</button>
      </div>

      <div class="modal-body">
        <!-- 스트리밍 (구독형) -->
        <div v-if="providers?.flatrate && providers.flatrate.length > 0" class="provider-section">
          <h3 class="section-title">스트리밍 (구독형)</h3>
          <div class="provider-grid">
            <div
              v-for="provider in sortedProviders(providers.flatrate)"
              :key="provider.provider_id"
              class="provider-card"
              @click="goToProvider(provider)"
            >
              <img
                :src="`https://image.tmdb.org/t/p/original${provider.logo_path}`"
                :alt="provider.provider_name"
                class="provider-logo"
              />
              <p class="provider-name">{{ provider.provider_name }}</p>
            </div>
          </div>
        </div>

        <!-- 대여 -->
        <div v-if="providers?.rent && providers.rent.length > 0" class="provider-section">
          <h3 class="section-title">대여</h3>
          <div class="provider-grid">
            <div
              v-for="provider in sortedProviders(providers.rent)"
              :key="provider.provider_id"
              class="provider-card"
              @click="goToProvider(provider)"
            >
              <img
                :src="`https://image.tmdb.org/t/p/original${provider.logo_path}`"
                :alt="provider.provider_name"
                class="provider-logo"
              />
              <p class="provider-name">{{ provider.provider_name }}</p>
            </div>
          </div>
        </div>

        <!-- 구매 -->
        <div v-if="providers?.buy && providers.buy.length > 0" class="provider-section">
          <h3 class="section-title">구매</h3>
          <div class="provider-grid">
            <div
              v-for="provider in sortedProviders(providers.buy)"
              :key="provider.provider_id"
              class="provider-card"
              @click="goToProvider(provider)"
            >
              <img
                :src="`https://image.tmdb.org/t/p/original${provider.logo_path}`"
                :alt="provider.provider_name"
                class="provider-logo"
              />
              <p class="provider-name">{{ provider.provider_name }}</p>
            </div>
          </div>
        </div>

        <!-- 플랫폼 정보가 없을 경우 -->
        <div v-if="!providers?.flatrate && !providers?.rent && !providers?.buy" class="no-providers">
          <p>😔 한국에서 현재 스트리밍 가능한 플랫폼 정보가 없습니다.</p>
          <p class="hint">나중에 다시 확인해보세요!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 30px;
  border-radius: 20px;
  width: 700px;
  max-width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid rgba(183, 148, 246, 0.3);
}

.modal-header h2 {
  color: #fff;
  font-size: 1.6rem;
  font-weight: 700;
}

.close-btn {
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 24px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(231, 76, 60, 0.8);
  transform: rotate(90deg);
}

.modal-body {
  color: white;
}

.provider-section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 1.2rem;
  margin-bottom: 15px;
  color: #b794f6;
  font-weight: 600;
  border-left: 4px solid #b794f6;
  padding-left: 10px;
}

.provider-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 15px;
}

.provider-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 15px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.provider-card:hover {
  background: rgba(183, 148, 246, 0.2);
  border-color: #b794f6;
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(183, 148, 246, 0.3);
}

.provider-logo {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  margin-bottom: 10px;
  object-fit: cover;
}

.provider-name {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.no-providers {
  text-align: center;
  padding: 50px 20px;
  color: rgba(255, 255, 255, 0.7);
}

.no-providers p {
  font-size: 1.1rem;
  margin-bottom: 10px;
}

.hint {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
}

/* 스크롤바 스타일 */
.modal::-webkit-scrollbar {
  width: 8px;
}

.modal::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.modal::-webkit-scrollbar-thumb {
  background: rgba(183, 148, 246, 0.5);
  border-radius: 10px;
}

.modal::-webkit-scrollbar-thumb:hover {
  background: rgba(183, 148, 246, 0.8);
}
</style>
