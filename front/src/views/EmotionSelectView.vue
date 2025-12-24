<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const emotions = [
  {
    id: 'joy',
    name: '기쁨',
    nameEn: 'JOY',
    emoji: '✨',
    icon: '😊',
    color: '#F39C12',
    gradient: 'linear-gradient(135deg, #F39C12, #F1C40F)',
    shadowColor: 'rgba(243, 156, 18, 0.5)',
    genreIds: [35, 10749],
    genres: ['코미디', '로맨스'],
    description: '행복하고 즐거운 기분이 들 때',
    tagline: '웃음꽃이 피어나는 순간들'
  },
  {
    id: 'sadness',
    name: '슬픔',
    nameEn: 'SADNESS',
    emoji: '💧',
    icon: '😢',
    color: '#3498DB',
    gradient: 'linear-gradient(135deg, #3498DB, #2C3E50)',
    shadowColor: 'rgba(52, 152, 219, 0.5)',
    genreIds: [18, 99],
    genres: ['드라마'],
    description: '위로가 필요하고 감성적인 기분일 때',
    tagline: '빗소리와 함께 펑펑 울고 싶다면'
  },
  {
    id: 'anger',
    name: '분노',
    nameEn: 'ANGER',
    emoji: '⚡',
    icon: '😡',
    color: '#E74C3C',
    gradient: 'linear-gradient(135deg, #E74C3C, #C0392B)',
    shadowColor: 'rgba(231, 76, 60, 0.5)',
    genreIds: [28],
    genres: ['액션'],
    description: '답답하고 시원하게 풀고 싶을 때',
    tagline: '복수는 나의 것'
  },
  {
    id: 'fear',
    name: '두려움',
    nameEn: 'FEAR',
    emoji: '🌙',
    icon: '😨',
    color: '#8E44AD',
    gradient: 'linear-gradient(135deg, #8E44AD, #2C3E50)',
    shadowColor: 'rgba(142, 68, 173, 0.5)',
    genreIds: [27, 53],
    genres: ['공포', '스릴러'],
    description: '짜릿한 긴장감을 원할 때',
    tagline: '심장이 두근거리는 전율'
  },
  {
    id: 'excitement',
    name: '흥분',
    nameEn: 'EXCITEMENT',
    emoji: '🔥',
    icon: '🤩',
    color: '#E67E22',
    gradient: 'linear-gradient(135deg, #E67E22, #D35400)',
    shadowColor: 'rgba(230, 126, 34, 0.5)',
    genreIds: [28, 878],
    genres: ['액션', 'SF'],
    description: '박진감 넘치는 영화가 보고 싶을 때',
    tagline: '아드레날린이 폭발하는'
  },
  {
    id: 'calm',
    name: '평온',
    nameEn: 'CALM',
    emoji: '🌿',
    icon: '😌',
    color: '#1ABC9C',
    gradient: 'linear-gradient(135deg, #1ABC9C, #16A085)',
    shadowColor: 'rgba(26, 188, 156, 0.5)',
    genreIds: [16, 10751],
    genres: ['애니메이션', '가족'],
    description: '조용하고 편안한 시간을 원할 때',
    tagline: '마음이 차분해지는'
  },
  {
    id: 'melancholy',
    name: '우울',
    nameEn: 'MELANCHOLY',
    emoji: '🌧️',
    icon: '😔',
    color: '#34495E',
    gradient: 'linear-gradient(135deg, #34495E, #2C3E50)',
    shadowColor: 'rgba(52, 73, 94, 0.5)',
    genreIds: [18, 36],
    genres: ['드라마'],
    description: '감상적이고 깊이 있는 영화가 보고 싶을 때',
    tagline: '혼자만의 시간에 잠기고 싶을 때'
  }
]

const hoveredCard = ref(null)

const selectEmotion = (emotion) => {
  console.log('🎴 카드 클릭됨!')
  console.log('선택된 감정:', emotion)
  
  router.push({
    name: 'movies',
    query: {
      emotion: emotion.id,
      emotionName: emotion.name,
      emotionTagline: emotion.tagline,
      genreIds: emotion.genreIds.join(','),
      genres: emotion.genres.join(',')
    }
  })
}
</script>

<template>
  <div class="emotion-select-view">
    <!-- 배경 효과 -->
    <div class="background-effects">
      <div class="star" v-for="n in 50" :key="n" 
           :style="{
             left: Math.random() * 100 + '%',
             top: Math.random() * 100 + '%',
             animationDelay: Math.random() * 3 + 's'
           }">
      </div>
    </div>

    <!-- 헤더 -->
    <div class="header">
      <h1 class="title">오늘 기분이 어때요?</h1>
      <p class="subtitle">카드를 선택하면 당신의 감정에 맞는 영화를 추천해드려요</p>
    </div>

    <!-- 카드 덱 -->
    <div class="card-deck">
      <div
        v-for="(emotion, index) in emotions"
        :key="emotion.id"
        class="emotion-card"
        :class="{ hovered: hoveredCard === emotion.id }"
        :style="{
          '--card-index': index,
          '--total-cards': emotions.length,
          '--card-color': emotion.color,
          '--card-gradient': emotion.gradient,
          '--shadow-color': emotion.shadowColor
        }"
        @mouseenter="hoveredCard = emotion.id"
        @mouseleave="hoveredCard = null"
        @click="selectEmotion(emotion)"
      >
        <!-- 카드 내용 -->
        <div class="card-inner">
          <!-- 필름 텍스처 레이어 -->
          <div class="film-texture"></div>

          <!-- 발광 효과 -->
          <div class="glow-effect"></div>

          <!-- 아이콘 -->
          <div class="card-icon-wrapper">
            <div class="card-emoji">{{ emotion.emoji }}</div>
            <div class="card-icon">{{ emotion.icon }}</div>
          </div>

          <!-- 텍스트 -->
          <div class="card-text">
            <h3 class="name-kr">{{ emotion.name }}</h3>
            <p class="name-en">{{ emotion.nameEn }}</p>
          </div>

          <!-- 태그라인 -->
          <p class="card-tagline">"{{ emotion.tagline }}"</p>

          <!-- 장르 태그 -->
          <div class="card-genres">
            <span 
              v-for="genre in emotion.genres" 
              :key="genre" 
              class="genre-tag"
            >
              {{ genre }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 가이드 텍스트 -->
    <div class="guide-text">
      <p>💡 카드를 클릭하여 감정을 선택하세요</p>
    </div>
  </div>
</template>

<style scoped>
.emotion-select-view {
  min-height: 100vh;
  width: 100%;
  margin: 0;
  padding: 60px 0;
  position: relative;
  overflow: visible;
  box-sizing: border-box;
}

/* ===== 배경 효과 ===== */
.background-effects {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.star {
  position: absolute;
  width: 2px;
  height: 2px;
  background: white;
  border-radius: 50%;
  animation: twinkle 3s ease-in-out infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

/* ===== 헤더 ===== */
.header {
  text-align: center;
  margin-bottom: 80px;
  position: relative;
  z-index: 1;
  padding: 0 20px;
}

.title {
  font-size: 3rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ffffff, #b794f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 16px;
}

.subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
}

/* ===== 카드 덱 ===== */
.card-deck {
  position: relative;
  height: 550px;
  display: flex;
  align-items: center;
  justify-content: center;
  perspective: 1500px;
  max-width: 100vw;
  width: 100%;
  margin: 0 auto;
  overflow: visible;
  padding: 0;
  box-sizing: border-box;
}

.emotion-card {
  position: absolute;
  width: 200px;
  height: 320px;
  cursor: pointer;
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: center bottom;
  
  --base-angle: calc((var(--card-index) - 3) * 15deg);
  --base-x: calc((var(--card-index) - 3) * 60px);
  
  transform: 
    translateX(var(--base-x))
    translateY(220px)
    rotate(var(--base-angle))
    translateY(-250px);
  
  z-index: var(--card-index);
}

.emotion-card.hovered {
  transform: 
    translateX(var(--base-x))
    translateY(180px)
    rotate(var(--base-angle))
    translateY(-290px)
    scale(1.2);
  z-index: 100 !important;
  filter: brightness(1.3);
}

.card-deck:has(.emotion-card.hovered) .emotion-card:not(.hovered) {
  opacity: 0.5;
  filter: brightness(0.5) blur(2px);
}

/* ===== 카드 내부 ===== */
.card-inner {
  width: 100%;
  height: 100%;
  background: var(--card-gradient);
  border-radius: 16px;
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 20px 60px var(--shadow-color),
    0 0 0 1px rgba(255, 255, 255, 0.1) inset;
}

/* ===== 필름 텍스처 ===== */
.film-texture {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 10px,
      rgba(0, 0, 0, 0.05) 10px,
      rgba(0, 0, 0, 0.05) 11px
    );
  opacity: 0.3;
  pointer-events: none;
}

/* ===== 발광 효과 ===== */
.glow-effect {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.3) 0%,
    transparent 70%
  );
  opacity: 0;
  transition: opacity 0.6s ease;
  pointer-events: none;
}

.emotion-card.hovered .glow-effect {
  opacity: 1;
}

/* ===== 아이콘 ===== */
.card-icon-wrapper {
  position: relative;
  margin-bottom: 8px;
}

.card-emoji {
  font-size: 3.5rem;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.3));
}

.card-icon {
  font-size: 2rem;
  position: absolute;
  bottom: -10px;
  right: -10px;
  filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.4));
}

/* ===== 텍스트 ===== */
.card-text {
  text-align: center;
  margin-bottom: 8px;
}

.name-kr {
  font-size: 1.75rem;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  margin-bottom: 4px;
}

.name-en {
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

/* ===== 태그라인 ===== */
.card-tagline {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.9);
  text-align: center;
  font-style: italic;
  line-height: 1.4;
  margin-bottom: 12px;
  min-height: 2.8em;
}

/* ===== 장르 태그 ===== */
.card-genres {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  justify-content: center;
}

.genre-tag {
  font-size: 0.75rem;
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  color: white;
  font-weight: 500;
}

/* ===== 가이드 텍스트 ===== */
.guide-text {
  text-align: center;
  margin-top: 80px;
  padding: 0 20px;
  color: var(--text-muted);
  font-size: 1rem;
}

/* ===== 반응형 ===== */
@media (max-width: 1400px) {
  .emotion-card {
    --base-x: calc((var(--card-index) - 3) * 50px);
  }
}

@media (max-width: 1200px) {
  .card-deck {
    height: 500px;
  }

  .emotion-card {
    width: 180px;
    height: 290px;
    --base-x: calc((var(--card-index) - 3) * 45px);
  }
}

@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .card-deck {
    height: 400px;
  }

  .emotion-card {
    width: 140px;
    height: 240px;
    --base-x: calc((var(--card-index) - 3) * 30px);
  }

  .card-tagline {
    font-size: 0.75rem;
  }
}

@media (max-width: 480px) {
  .card-deck {
    height: 350px;
  }

  .emotion-card {
    width: 110px;
    height: 190px;
    --base-x: calc((var(--card-index) - 3) * 20px);
  }

  .card-tagline,
  .card-genres {
    display: none;
  }
}
</style>