<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { getReviews, createReview } from '@/api/community'
import ReviewItem from './ReviewItem.vue'
import { EMOTIONS } from '@/utils/emotions'

const props = defineProps({
  movieId: {
    type: Number,
    required: true
  }
})

const authStore = useAuthStore()

const reviews = ref([])
const isLoading = ref(false)

// 리뷰 작성 폼
const newReview = ref({
  title: '',
  content: '',
  rating: 5,
  emotion_tags: []
})
const isSubmitting = ref(false)
const showForm = ref(false)

// 리뷰 목록 조회
const fetchReviews = async () => {
  isLoading.value = true
  try {
    const response = await getReviews(props.movieId)
    reviews.value = response.data
  } catch (error) {
    console.error('리뷰 조회 실패:', error)
  } finally {
    isLoading.value = false
  }
}

// 리뷰 작성 폼 토글
const toggleForm = () => {
  showForm.value = !showForm.value
}

// 감정 선택 토글
const toggleEmotion = (emotionCode) => {
  const index = newReview.value.emotion_tags.indexOf(emotionCode)
  if (index > -1) {
    newReview.value.emotion_tags.splice(index, 1)
  } else {
    newReview.value.emotion_tags.push(emotionCode)
  }
}

// 리뷰 작성
const handleSubmitReview = async () => {
  if (!newReview.value.title.trim()) {
    alert('제목을 입력해주세요.')
    return
  }
  if (!newReview.value.content.trim()) {
    alert('내용을 입력해주세요.')
    return
  }

  isSubmitting.value = true
  try {
    await createReview(props.movieId, newReview.value)
    
    // 폼 초기화
    newReview.value = {
      title: '',
      content: '',
      rating: 5,
      emotion_tags: []
    }
    showForm.value = false
    
    alert('리뷰가 작성되었습니다.')
    
    // 리뷰 목록 새로고침
    await fetchReviews()
    
  } catch (error) {
    console.error('리뷰 작성 실패:', error)
    alert('리뷰 작성에 실패했습니다.')
  } finally {
    isSubmitting.value = false
  }
}


const handleRefresh = async () => {
  await fetchReviews()
}

onMounted(() => {
  fetchReviews()
})
</script>

<template>
  <div class="review-section">
    <!-- 섹션 헤더 -->
    <div class="section-header">
      <h2 class="section-title gradient-text">
        <span class="icon">🎬</span>
        리뷰
      </h2>
      <div class="review-count">{{ reviews.length }}개의 리뷰</div>
    </div>

    <!-- 리뷰 작성 버튼 -->
    <div v-if="authStore.isLogin" class="write-review-container">
      <button 
        @click="toggleForm" 
        class="btn btn-primary btn-write"
        :class="{ active: showForm }"
      >
        <span class="icon">✍️</span>
        {{ showForm ? '작성 취소' : '리뷰 작성하기' }}
      </button>
    </div>

    <!-- 리뷰 작성 폼 -->
    <transition name="slide-down">
      <div v-if="authStore.isLogin && showForm" class="review-form card">
        <h3 class="form-title">
          <span class="icon">✨</span>
          이 영화에 대한 당신의 생각을 들려주세요
        </h3>
        
        <div class="form-group">
          <label for="review-title">제목</label>
          <input 
            id="review-title"
            v-model="newReview.title" 
            type="text" 
            placeholder="리뷰 제목을 입력하세요"
            class="input-field"
            maxlength="100"
          />
        </div>

        <div class="form-group">
          <label for="review-rating">평점</label>
          <div class="rating-selector">
            <button
              v-for="star in 5"
              :key="star"
              type="button"
              @click="newReview.rating = star"
              class="star-button"
              :class="{ active: star <= newReview.rating }"
            >
              {{ star <= newReview.rating ? '⭐' : '☆' }}
            </button>
            <span class="rating-text">{{ newReview.rating }}점</span>
          </div>
        </div>

        <!-- 감정 선택 UI -->
        <div class="form-group">
          <label>이 영화를 보며 느낀 감정 (복수 선택 가능)</label>
          <div class="emotion-selector">
            <button
              v-for="emotion in EMOTIONS"
              :key="emotion.code"
              type="button"
              @click="toggleEmotion(emotion.code)"
              class="emotion-button"
              :class="{ selected: newReview.emotion_tags.includes(emotion.code) }"
              :style="{ '--emotion-color': emotion.color }"
            >
              <span class="emotion-emoji">{{ emotion.emoji }}</span>
              <span class="emotion-label">{{ emotion.label }}</span>
            </button>
          </div>
          <p class="emotion-hint">
            선택한 감정: 
            <span v-if="newReview.emotion_tags.length === 0" class="text-muted">없음</span>
            <span v-else>{{ newReview.emotion_tags.length }}개</span>
          </p>
        </div>

        <div class="form-group">
          <label for="review-content">내용</label>
          <textarea
            id="review-content"
            v-model="newReview.content"
            placeholder="이 영화에 대한 당신의 생각을 자유롭게 작성해주세요."
            class="input-field textarea"
            rows="6"
            maxlength="1000"
          ></textarea>
          <div class="char-count">{{ newReview.content.length }} / 1000</div>
        </div>

        <div class="form-actions">
          <button 
            @click="toggleForm"
            class="btn btn-secondary"
          >
            취소
          </button>
          <button 
            @click="handleSubmitReview"
            :disabled="isSubmitting"
            class="btn btn-primary"
          >
            {{ isSubmitting ? '작성 중...' : '리뷰 등록' }}
          </button>
        </div>
      </div>
    </transition>

    <!-- 로그인 필요 안내 -->
    <div v-if="!authStore.isLogin" class="login-required card">
      <span class="icon">🔒</span>
      <p>리뷰를 작성하려면 <router-link to="/login" class="login-link">로그인</router-link>이 필요합니다.</p>
    </div>

    <!-- 리뷰 목록 -->
    <div class="review-list">
      <!-- 로딩 상태 -->
      <div v-if="isLoading" class="loading-state">
        <div class="loading-spinner"></div>
        <span>리뷰를 불러오는 중...</span>
      </div>
      
      <!-- 리뷰 없음 -->
      <div v-else-if="reviews.length === 0" class="no-reviews card">
        <span class="icon">📝</span>
        <h3>아직 작성된 리뷰가 없습니다</h3>
        <p>이 영화의 첫 번째 리뷰를 남겨보세요!</p>
      </div>

      <!-- 리뷰 목록 -->
      <ReviewItem 
        v-else
        v-for="review in reviews" 
        :key="review.id" 
        :review="review"
        @refresh="handleRefresh"
      />
    </div>
  </div>
</template>

<style scoped>
/* 기존 스타일 유지 */
.review-section {
  margin-top: var(--spacing-2xl);
  padding: var(--spacing-2xl) 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-lg);
  border-bottom: 2px solid rgba(183, 148, 246, 0.2);
}

.section-title {
  font-size: 2rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-family: var(--font-display);
}

.section-title .icon {
  font-size: 2.2rem;
  filter: drop-shadow(0 0 10px var(--accent-mystic));
}

.review-count {
  font-size: 0.95rem;
  color: var(--text-secondary);
  background: var(--bg-dark-elevated);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 20px;
  border: 1px solid rgba(183, 148, 246, 0.2);
}

.write-review-container {
  margin-bottom: var(--spacing-lg);
}

.btn-write {
  width: 100%;
  justify-content: center;
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: 1rem;
}

.btn-write .icon {
  font-size: 1.2rem;
}

.btn-write.active {
  background: var(--bg-dark-elevated);
  border: 1px solid var(--primary-purple);
}

.review-form {
  margin-bottom: var(--spacing-xl);
  background: linear-gradient(135deg, var(--bg-dark-elevated) 0%, var(--bg-dark-secondary) 100%);
  border: 1px solid rgba(183, 148, 246, 0.3);
}

.form-title {
  margin: 0 0 var(--spacing-lg) 0;
  font-size: 1.3rem;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-family: var(--font-display);
}

.form-title .icon {
  font-size: 1.5rem;
  filter: drop-shadow(0 0 8px var(--accent-mystic));
}

.form-group {
  margin-bottom: var(--spacing-lg);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-sm);
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.95rem;
}

.input-field {
  width: 100%;
  padding: var(--spacing-md);
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: var(--font-body);
}

.input-field.textarea {
  resize: vertical;
  min-height: 120px;
  line-height: 1.6;
}

.char-count {
  text-align: right;
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: var(--spacing-xs);
}

.rating-selector {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.star-button {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  transition: var(--transition-fast);
  padding: var(--spacing-xs);
}

.star-button:hover {
  transform: scale(1.2);
  filter: drop-shadow(0 0 8px var(--accent-gold));
}

.star-button.active {
  filter: drop-shadow(0 0 12px var(--accent-gold));
}

.rating-text {
  margin-left: var(--spacing-sm);
  font-weight: 600;
  color: var(--accent-gold);
  font-size: 1.1rem;
}

/* 감정 선택 UI */
.emotion-selector {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: var(--spacing-md);
  margin-top: var(--spacing-md);
  padding: var(--spacing-md) 0;
}

.emotion-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--bg-dark-elevated);
  border: 2px solid rgba(183, 148, 246, 0.2);
  border-radius: 12px;
  cursor: pointer;
  transition: var(--transition-fast);
  min-width: 100px;
}

.emotion-button:hover {
  transform: translateY(-4px);
  border-color: var(--emotion-color);
  box-shadow: 0 8px 16px rgba(183, 148, 246, 0.3);
}

.emotion-button.selected {
  background: linear-gradient(135deg, 
    rgba(183, 148, 246, 0.2), 
    rgba(183, 148, 246, 0.1)
  );
  border-color: var(--emotion-color);
  box-shadow: 0 0 24px var(--emotion-color);
  transform: translateY(-2px);
}

.emotion-emoji {
  font-size: 2.5rem;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.emotion-label {
  font-size: 0.9rem;
  color: var(--text-secondary);
  font-weight: 500;
  text-align: center;
}

.emotion-button.selected .emotion-label {
  color: var(--text-primary);
  font-weight: 600;
}

.emotion-hint {
  margin-top: var(--spacing-md);
  text-align: center;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-xl);
}

.form-actions .btn {
  min-width: 120px;
}

.login-required {
  text-align: center;
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
  background: linear-gradient(135deg, var(--bg-dark-elevated) 0%, var(--bg-dark-secondary) 100%);
  border: 1px solid rgba(183, 148, 246, 0.2);
}

.login-required .icon {
  display: block;
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
  filter: drop-shadow(0 0 10px var(--accent-mystic));
}

.login-required p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 1rem;
}

.login-link {
  color: var(--accent-mystic);
  font-weight: 600;
  text-decoration: underline;
  transition: var(--transition-fast);
}

.login-link:hover {
  color: var(--primary-purple-light);
  text-shadow: 0 0 8px var(--accent-mystic);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2xl);
  gap: var(--spacing-md);
  color: var(--text-secondary);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--bg-dark-elevated);
  border-top-color: var(--primary-purple);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.no-reviews {
  text-align: center;
  padding: var(--spacing-2xl);
  background: linear-gradient(135deg, var(--bg-dark-elevated) 0%, var(--bg-dark-secondary) 100%);
}

.no-reviews .icon {
  display: block;
  font-size: 4rem;
  margin-bottom: var(--spacing-md);
  filter: drop-shadow(0 0 15px var(--accent-mystic));
}

.no-reviews h3 {
  margin: 0 0 var(--spacing-sm) 0;
  color: var(--text-primary);
  font-family: var(--font-display);
}

.no-reviews p {
  margin: 0;
  color: var(--text-secondary);
}

.review-list {
  margin-top: var(--spacing-xl);
}

.slide-down-enter-active {
  transition: all 0.4s ease;
}

.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from {
  transform: translateY(-20px);
  opacity: 0;
}

.slide-down-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

@media (max-width: 768px) {
  .review-section {
    padding: var(--spacing-xl) 0;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }

  .section-title {
    font-size: 1.5rem;
  }

  .review-count {
    align-self: flex-start;
  }

  .form-title {
    font-size: 1.1rem;
  }

  .star-button {
    font-size: 1.5rem;
  }

  .emotion-selector {
    gap: var(--spacing-sm);
  }
  
  .emotion-button {
    min-width: 80px;
    padding: var(--spacing-sm) var(--spacing-md);
  }
  
  .emotion-emoji {
    font-size: 2rem;
  }
  
  .emotion-label {
    font-size: 0.8rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions .btn {
    width: 100%;
  }
}
</style>