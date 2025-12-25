<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { toggleReviewLike, updateReview, deleteReview } from '@/api/community'  
import CommentSection from './CommentSection.vue'
import { getEmotionEmoji, getEmotionLabel } from '@/utils/emotions'

const props = defineProps({
  review: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['refresh'])

const authStore = useAuthStore()

const showComments = ref(false)
const isLiking = ref(false)


const isEditing = ref(false)
const editForm = ref({
  title: props.review.title,
  content: props.review.content,
  rating: props.review.rating,
  emotion_tags: props.review.emotion_tags || []
})

// 로컬 상태로 좋아요 관리
const localLikeCount = ref(props.review.like_count)
const localIsLiked = ref(props.review.is_liked)

// 별점 표시 (5점 만점)
const stars = computed(() => {
  const rating = props.review.rating
  return '⭐'.repeat(Math.round(rating))
})

// 감정 태그가 있는지 확인
const hasEmotions = computed(() => {
  return props.review.emotion_tags && props.review.emotion_tags.length > 0
})

// 수정/삭제 권한 확인
const canEdit = computed(() => {
  return authStore.isLogin && authStore.username === props.review.username
})

const canDelete = computed(() => {
  // 작성자 본인 또는 관리자
  return authStore.isLogin && 
         (authStore.username === props.review.username || authStore.isAdmin)
})

// 좋아요 토글
const handleLike = async () => {
  if (!authStore.isLogin) {
    alert('로그인이 필요합니다.')
    return
  }

  isLiking.value = true
  try {
    const response = await toggleReviewLike(props.review.id)
    localIsLiked.value = response.data.liked
    localLikeCount.value = response.data.like_count
  } catch (error) {
    console.error('좋아요 처리 실패:', error)
    alert('좋아요 처리에 실패했습니다.')
  } finally {
    isLiking.value = false
  }
}

const toggleComments = () => {
  showComments.value = !showComments.value
}

const toggleEdit = () => {
  isEditing.value = !isEditing.value
  if (isEditing.value) {
    editForm.value = {
      title: props.review.title,
      content: props.review.content,
      rating: props.review.rating,
      emotion_tags: props.review.emotion_tags || []
    }
  }
}

const handleUpdate = async () => {
  if (!editForm.value.title.trim()) {
    alert('제목을 입력해주세요.')
    return
  }
  if (!editForm.value.content.trim()) {
    alert('내용을 입력해주세요.')
    return
  }

  try {
    await updateReview(props.review.id, editForm.value)
    alert('리뷰가 수정되었습니다.')
    isEditing.value = false
    emit('refresh')  // 리뷰 목록 새로고침
  } catch (error) {
    console.error('리뷰 수정 실패:', error)
    alert('리뷰 수정에 실패했습니다.')
  }
}

const handleDelete = async () => {
  if (!confirm('정말 이 리뷰를 삭제하시겠습니까?')) {
    return
  }

  try {
    await deleteReview(props.review.id)
    alert('리뷰가 삭제되었습니다.')
    emit('refresh')  // 리뷰 목록 새로고침
  } catch (error) {
    console.error('리뷰 삭제 실패:', error)
    alert('리뷰 삭제에 실패했습니다.')
  }
}
</script>

<template>
  <div class="review-item card">
    <!-- 수정 모드가 아닐 때 -->
    <div v-if="!isEditing">
      <!-- 리뷰 헤더 -->
      <div class="review-header">
        <div class="review-author-info">
          <span class="username">{{ review.username }}</span>
          <span class="rating">{{ stars }}</span>
          <span class="rating-number">({{ review.rating }}점)</span>
        </div>
        <div class="header-right">
          <span class="review-date">{{ new Date(review.created_at).toLocaleDateString('ko-KR') }}</span>
          

          <div v-if="canEdit || canDelete" class="action-buttons">
            <button v-if="canEdit" @click="toggleEdit" class="btn-edit" title="수정">
              ✏️
            </button>
            <button v-if="canDelete" @click="handleDelete" class="btn-delete" title="삭제">
              🗑️
            </button>
          </div>
        </div>
      </div>

      <!-- 감정 뱃지 -->
      <div v-if="hasEmotions" class="emotion-badges">
        <span
          v-for="emotionCode in review.emotion_tags"
          :key="emotionCode"
          class="emotion-badge"
        >
          <span class="badge-emoji">{{ getEmotionEmoji(emotionCode) }}</span>
          <span class="badge-label">{{ getEmotionLabel(emotionCode) }}</span>
        </span>
      </div>

      <h3 class="review-title">{{ review.title }}</h3>

      <!-- 리뷰 내용 -->
      <p class="review-content">{{ review.content }}</p>

      <!-- 리뷰 푸터 (좋아요, 댓글) -->
      <div class="review-footer">
        <button 
          @click="handleLike" 
          :disabled="isLiking"
          class="btn-action btn-like"
          :class="{ liked: localIsLiked }"
        >
          <span class="icon">{{ localIsLiked ? '❤️' : '🤍' }}</span>
          <span class="count">{{ localLikeCount }}</span>
        </button>

        <button 
          @click="toggleComments" 
          class="btn-action btn-comment"
          :class="{ active: showComments }"
        >
          <span class="icon">💬</span>
          <span class="count">{{ review.comment_count }}</span>
        </button>
      </div>
    </div>

    <div v-else class="edit-mode">
      <h3 class="edit-title">리뷰 수정</h3>
      
      <div class="form-group">
        <label>제목</label>
        <input 
          v-model="editForm.title" 
          type="text" 
          class="input-field"
          maxlength="100"
        />
      </div>

      <div class="form-group">
        <label>평점</label>
        <div class="rating-selector">
          <button
            v-for="star in 5"
            :key="star"
            type="button"
            @click="editForm.rating = star"
            class="star-button"
            :class="{ active: star <= editForm.rating }"
          >
            {{ star <= editForm.rating ? '⭐' : '☆' }}
          </button>
          <span class="rating-text">{{ editForm.rating }}점</span>
        </div>
      </div>

      <div class="form-group">
        <label>내용</label>
        <textarea
          v-model="editForm.content"
          class="input-field textarea"
          rows="5"
          maxlength="1000"
        ></textarea>
      </div>

      <div class="form-actions">
        <button @click="toggleEdit" class="btn btn-secondary">
          취소
        </button>
        <button @click="handleUpdate" class="btn btn-primary">
          수정 완료
        </button>
      </div>
    </div>

    <!-- 댓글 섹션 (토글) -->
    <transition name="slide-fade">
      <CommentSection 
        v-if="showComments && !isEditing" 
        :review-id="review.id"
      />
    </transition>
  </div>
</template>

<style scoped>
/* 기존 스타일 유지... */

.review-item {
  margin-bottom: var(--spacing-lg);
  transition: var(--transition-normal);
}

.review-item:hover {
  transform: translateY(-4px);
  border-color: var(--primary-purple);
  box-shadow: var(--shadow-glow);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid rgba(183, 148, 246, 0.1);
}

.review-author-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}


.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.username {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.95rem;
}

.rating {
  font-size: 0.9rem;
}

.rating-number {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.review-date {
  font-size: 0.8rem;
  color: var(--text-muted);
}


.action-buttons {
  display: flex;
  gap: var(--spacing-xs);
}

.btn-edit,
.btn-delete {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: var(--spacing-xs);
  transition: var(--transition-fast);
  opacity: 0.6;
}

.btn-edit:hover {
  opacity: 1;
  transform: scale(1.2);
}

.btn-delete:hover {
  opacity: 1;
  transform: scale(1.2);
}

/* 감정 뱃지 스타일 */
.emotion-badges {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-md);
}

.emotion-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-sm);
  background: linear-gradient(135deg, 
    rgba(183, 148, 246, 0.15), 
    rgba(183, 148, 246, 0.05)
  );
  border: 1px solid rgba(183, 148, 246, 0.3);
  border-radius: 20px;
  font-size: 0.85rem;
  transition: var(--transition-fast);
}

.emotion-badge:hover {
  background: linear-gradient(135deg, 
    rgba(183, 148, 246, 0.25), 
    rgba(183, 148, 246, 0.15)
  );
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(183, 148, 246, 0.2);
}

.badge-emoji {
  font-size: 1.1rem;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.badge-label {
  color: var(--text-secondary);
  font-weight: 500;
}

.review-title {
  margin: 0 0 var(--spacing-md) 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text-primary);
  font-family: var(--font-display);
  letter-spacing: 0.02em;
}

.review-content {
  margin: 0 0 var(--spacing-lg) 0;
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.7;
  white-space: pre-wrap;
}

.review-footer {
  display: flex;
  gap: var(--spacing-sm);
  padding-top: var(--spacing-md);
  border-top: 1px solid rgba(183, 148, 246, 0.1);
}

.btn-action {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid rgba(183, 148, 246, 0.2);
  border-radius: 8px;
  background: var(--bg-dark-secondary);
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition-fast);
  font-size: 0.9rem;
}

.btn-action:hover:not(:disabled) {
  background: var(--bg-dark-elevated);
  border-color: var(--primary-purple);
  transform: translateY(-2px);
}

.btn-action .icon {
  font-size: 1.1rem;
}

.btn-action .count {
  font-weight: 500;
}

.btn-like.liked {
  background: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
  color: #ef4444;
}

.btn-like.liked:hover {
  background: rgba(239, 68, 68, 0.2);
}

.btn-comment.active {
  background: rgba(183, 148, 246, 0.1);
  border-color: var(--accent-mystic);
  color: var(--accent-mystic);
}

.btn-action:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}


.edit-mode {
  padding: var(--spacing-md);
  background: var(--bg-dark-secondary);
  border-radius: 8px;
}

.edit-title {
  margin: 0 0 var(--spacing-lg) 0;
  font-size: 1.2rem;
  color: var(--text-primary);
}

.form-group {
  margin-bottom: var(--spacing-md);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-xs);
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.input-field {
  width: 100%;
  padding: var(--spacing-sm);
  border-radius: 6px;
  font-size: 0.9rem;
}

.input-field.textarea {
  resize: vertical;
  min-height: 100px;
  line-height: 1.6;
}

.rating-selector {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.star-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  transition: var(--transition-fast);
  padding: var(--spacing-xs);
}

.star-button:hover {
  transform: scale(1.2);
}

.star-button.active {
  filter: drop-shadow(0 0 8px var(--accent-gold));
}

.rating-text {
  margin-left: var(--spacing-sm);
  font-weight: 600;
  color: var(--accent-gold);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
}

/* 애니메이션 */
.slide-fade-enter-active {
  transition: all 0.3s ease;
}

.slide-fade-leave-active {
  transition: all 0.2s ease;
}

.slide-fade-enter-from {
  transform: translateY(-10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-5px);
  opacity: 0;
}

/* 반응형 */
@media (max-width: 768px) {
  .review-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
  }

  .header-right {
    width: 100%;
    justify-content: space-between;
  }

  .review-title {
    font-size: 1.1rem;
  }

  .review-content {
    font-size: 0.9rem;
  }

  .btn-action {
    font-size: 0.85rem;
    padding: var(--spacing-xs) var(--spacing-sm);
  }

  .emotion-badges {
    gap: 6px;
  }

  .emotion-badge {
    font-size: 0.75rem;
    padding: 4px 8px;
  }

  .badge-emoji {
    font-size: 1rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions button {
    width: 100%;
  }
}
</style>