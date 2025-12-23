<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  movie: {
    type: Object,
    required: true
  }
})

const isHovered = ref(false)

// 평점 색상
const ratingColor = computed(() => {
  const rating = props.movie.vote_average
  if (rating >= 8) return '#2ECC71'      // 초록 (좋음)
  if (rating >= 7) return '#F39C12'      // 노랑 (보통 이상)
  if (rating >= 6) return '#E67E22'      // 주황 (괜찮음)
  return '#E74C3C'                        // 빨강 (낮음)
})

// 개봉년도
const releaseYear = computed(() => {
  if (props.movie.release_date) {
    return props.movie.release_date.split('-')[0]
  }
  return 'N/A'
})

// 장르 (TMDB genre_ids로부터)
const genres = computed(() => {
  const genreMap = {
    28: '액션', 12: '모험', 16: '애니', 35: '코미디',
    80: '범죄', 99: '다큐', 18: '드라마', 10751: '가족',
    14: '판타지', 36: '역사', 27: '공포', 10402: '음악',
    9648: '미스터리', 10749: '로맨스', 878: 'SF',
    10770: 'TV', 53: '스릴러', 10752: '전쟁', 37: '서부'
  }
  
  if (props.movie.genre_ids) {
    return props.movie.genre_ids
      .slice(0, 2)  // 최대 2개만
      .map(id => genreMap[id] || '')
      .filter(Boolean)
  }
  return []
})
</script>

<template>
  <div 
    class="movie-card"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <!-- 포스터 컨테이너 -->
    <div class="poster-container">
      <!-- 포스터 이미지 -->
      <img
        v-if="movie.poster_path"
        :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
        :alt="movie.title"
        class="movie-poster"
      />
      <div v-else class="no-poster">
        <span class="poster-icon">🎬</span>
      </div>

      <!-- 호버 오버레이 -->
      <div class="hover-overlay" :class="{ active: isHovered }">
        <!-- 상단: 평점 -->
        <div class="overlay-top">
          <div class="rating-badge" :style="{ background: ratingColor }">
            <span class="rating-icon">⭐</span>
            <span class="rating-value">{{ movie.vote_average?.toFixed(1) || 'N/A' }}</span>
          </div>
        </div>

        <!-- 중앙: 줄거리 -->
        <div class="overlay-center">
          <p class="movie-overview">
            {{ movie.overview ? movie.overview.slice(0, 120) + '...' : '줄거리 정보가 없습니다.' }}
          </p>
        </div>

        <!-- 하단: 버튼 -->
        <div class="overlay-bottom">
          <button class="action-button primary">
            <span>자세히 보기</span>
            <span class="button-arrow">→</span>
          </button>
        </div>
      </div>

      <!-- 평점 뱃지 (호버 아닐 때) -->
      <div v-if="!isHovered" class="rating-corner">
        <span>⭐ {{ movie.vote_average?.toFixed(1) }}</span>
      </div>
    </div>

    <!-- 영화 정보 -->
    <div class="movie-info">
      <!-- 제목 -->
      <h3 class="movie-title">{{ movie.title }}</h3>

      <!-- 메타 정보 -->
      <div class="movie-meta">
        <!-- 개봉년도 -->
        <span class="meta-year">{{ releaseYear }}</span>
        
        <!-- 장르 -->
        <div v-if="genres.length > 0" class="meta-genres">
          <span 
            v-for="genre in genres" 
            :key="genre"
            class="genre-tag"
          >
            {{ genre }}
          </span>
        </div>
      </div>

      <!-- 인기도 표시 -->
      <div class="popularity-bar">
        <div 
          class="popularity-fill"
          :style="{ width: Math.min(movie.popularity / 10, 100) + '%' }"
        ></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.movie-card {
  background: var(--bg-dark-elevated);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(183, 148, 246, 0.1);
  cursor: pointer;
}

.movie-card:hover {
  transform: translateY(-12px);
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(183, 148, 246, 0.3);
}

/* ===== 포스터 컨테이너 ===== */
.poster-container {
  position: relative;
  aspect-ratio: 2/3;
  overflow: hidden;
  background: linear-gradient(135deg, #1a0b2e, #0f0a1a);
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}

.movie-card:hover .movie-poster {
  transform: scale(1.1);
}

/* 포스터 없을 때 */
.no-poster {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(123, 16, 173, 0.2), rgba(15, 10, 26, 0.8));
}

.poster-icon {
  font-size: 4rem;
  opacity: 0.3;
}

/* ===== 평점 코너 (기본) ===== */
.rating-corner {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 6px 12px;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #FFD700;
  z-index: 2;
  transition: opacity 0.3s ease;
}

.movie-card:hover .rating-corner {
  opacity: 0;
}

/* ===== 호버 오버레이 ===== */
.hover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.3) 0%,
    rgba(0, 0, 0, 0.7) 50%,
    rgba(0, 0, 0, 0.9) 100%
  );
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 16px;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 3;
}

.hover-overlay.active {
  opacity: 1;
}

/* 오버레이 상단 */
.overlay-top {
  display: flex;
  justify-content: flex-end;
}

.rating-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 700;
  color: white;
  font-size: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  animation: slideDown 0.4s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.rating-icon {
  font-size: 1.25rem;
}

.rating-value {
  font-size: 1.125rem;
}

/* 오버레이 중앙 */
.overlay-center {
  flex: 1;
  display: flex;
  align-items: center;
  animation: fadeIn 0.5s ease 0.1s both;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.movie-overview {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.875rem;
  line-height: 1.6;
  text-align: left;
}

/* 오버레이 하단 */
.overlay-bottom {
  animation: slideUp 0.4s ease 0.2s both;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.action-button {
  width: 100%;
  padding: 12px 20px;
  background: linear-gradient(135deg, var(--primary-purple), #d946ef);
  border: none;
  border-radius: 50px;
  color: white;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(123, 16, 173, 0.4);
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(123, 16, 173, 0.6);
}

.button-arrow {
  transition: transform 0.3s ease;
}

.action-button:hover .button-arrow {
  transform: translateX(4px);
}

/* ===== 영화 정보 ===== */
.movie-info {
  padding: 16px;
}

.movie-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.4;
  min-height: 2.8em;
}

/* 메타 정보 */
.movie-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.meta-year {
  font-size: 0.875rem;
  color: var(--text-muted);
  font-weight: 500;
}

.meta-genres {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.genre-tag {
  font-size: 0.75rem;
  padding: 3px 10px;
  background: rgba(183, 148, 246, 0.15);
  border: 1px solid rgba(183, 148, 246, 0.3);
  border-radius: 20px;
  color: var(--accent-mystic);
  font-weight: 500;
}

/* 인기도 바 */
.popularity-bar {
  width: 100%;
  height: 4px;
  background: rgba(183, 148, 246, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

.popularity-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-purple), var(--accent-mystic));
  border-radius: 2px;
  transition: width 0.8s ease;
}

/* ===== 반응형 ===== */
@media (max-width: 768px) {
  .movie-info {
    padding: 12px;
  }

  .movie-title {
    font-size: 0.95rem;
  }

  .movie-overview {
    font-size: 0.8rem;
  }

  .action-button {
    padding: 10px 16px;
    font-size: 0.875rem;
  }
}

@media (max-width: 480px) {
  .movie-title {
    font-size: 0.875rem;
    -webkit-line-clamp: 1;
    min-height: 1.4em;
  }

  .movie-overview {
    display: none;
  }

  .rating-badge {
    padding: 6px 12px;
    font-size: 0.875rem;
  }

  .action-button {
    padding: 8px 14px;
    font-size: 0.8rem;
  }

  .genre-tag {
    font-size: 0.7rem;
    padding: 2px 8px;
  }
}
</style>