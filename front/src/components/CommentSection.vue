vue<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { getComments, createComment, updateComment, deleteComment } from '@/api/community'  

const props = defineProps({
  reviewId: {
    type: Number,
    required: true
  }
})

const authStore = useAuthStore()

const comments = ref([])
const newComment = ref('')
const isLoading = ref(false)
const isSubmitting = ref(false)

// 수정 중인 댓글 관리
const editingCommentId = ref(null)
const editingContent = ref('')

// 댓글 목록 조회
const fetchComments = async () => {
  isLoading.value = true
  try {
    const response = await getComments(props.reviewId)
    comments.value = response.data
  } catch (error) {
    console.error('댓글 조회 실패:', error)
  } finally {
    isLoading.value = false
  }
}

// 댓글 작성
const handleSubmit = async () => {
  if (!newComment.value.trim()) {
    alert('댓글 내용을 입력해주세요.')
    return
  }

  isSubmitting.value = true
  try {
    await createComment(props.reviewId, newComment.value)
    newComment.value = ''
    await fetchComments()
  } catch (error) {
    console.error('댓글 작성 실패:', error)
    alert('댓글 작성에 실패했습니다.')
  } finally {
    isSubmitting.value = false
  }
}

// 수정 모드 시작
const startEdit = (comment) => {
  editingCommentId.value = comment.id
  editingContent.value = comment.content
}

// 수정 취소
const cancelEdit = () => {
  editingCommentId.value = null
  editingContent.value = ''
}

// 댓글 수정
const handleUpdate = async (commentId) => {
  if (!editingContent.value.trim()) {
    alert('댓글 내용을 입력해주세요.')
    return
  }

  try {
    await updateComment(commentId, editingContent.value)
    editingCommentId.value = null
    editingContent.value = ''
    await fetchComments()
    alert('댓글이 수정되었습니다.')
  } catch (error) {
    console.error('댓글 수정 실패:', error)
    alert('댓글 수정에 실패했습니다.')
  }
}

// 댓글 삭제
const handleDelete = async (commentId) => {
  if (!confirm('정말 이 댓글을 삭제하시겠습니까?')) {
    return
  }

  try {
    await deleteComment(commentId)
    await fetchComments()
    alert('댓글이 삭제되었습니다.')
  } catch (error) {
    console.error('댓글 삭제 실패:', error)
    alert('댓글 삭제에 실패했습니다.')
  }
}

// 수정/삭제 권한 확인
const canEdit = (comment) => {
  return authStore.isLogin && authStore.username === comment.username
}

const canDelete = (comment) => {
  return authStore.isLogin && 
         (authStore.username === comment.username || authStore.isAdmin)
}

onMounted(() => {
  fetchComments()
})
</script>

<template>
  <div class="comment-section">
    <h4 class="comment-title">
      <span class="icon">💬</span>
      댓글 {{ comments.length }}개
    </h4>

    <!-- 댓글 목록 -->
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner"></div>
      <span>댓글을 불러오는 중...</span>
    </div>

    <div v-else-if="comments.length === 0" class="no-comments">
      <span class="icon">📭</span>
      <p>첫 번째 댓글을 남겨보세요!</p>
    </div>

    <div v-else class="comment-list">
      <div 
        v-for="comment in comments" 
        :key="comment.id" 
        class="comment-item"
      >
        <!-- 수정 모드가 아닐 때 -->
        <div v-if="editingCommentId !== comment.id" class="comment-content">
          <div class="comment-header">
            <span class="comment-author">{{ comment.username }}</span>
            <div class="comment-header-right">
              <span class="comment-date">
                {{ new Date(comment.created_at).toLocaleDateString('ko-KR') }}
              </span>
              

              <div v-if="canEdit(comment) || canDelete(comment)" class="comment-actions">
                <button 
                  v-if="canEdit(comment)" 
                  @click="startEdit(comment)" 
                  class="btn-edit-comment"
                  title="수정"
                >
                  ✏️
                </button>
                <button 
                  v-if="canDelete(comment)" 
                  @click="handleDelete(comment.id)" 
                  class="btn-delete-comment"
                  title="삭제"
                >
                  🗑️
                </button>
              </div>
            </div>
          </div>
          <p class="comment-text">{{ comment.content }}</p>
        </div>

        <div v-else class="comment-edit-mode">
          <textarea
            v-model="editingContent"
            class="edit-textarea"
            rows="3"
            maxlength="500"
          ></textarea>
          <div class="edit-actions">
            <button @click="cancelEdit" class="btn btn-secondary btn-sm">
              취소
            </button>
            <button @click="handleUpdate(comment.id)" class="btn btn-primary btn-sm">
              수정 완료
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 댓글 작성 폼 -->
    <div v-if="authStore.isLogin" class="comment-form">
      <textarea
        v-model="newComment"
        placeholder="댓글을 입력하세요..."
        class="comment-input"
        rows="3"
        maxlength="500"
      ></textarea>
      <div class="form-footer">
        <span class="char-count">{{ newComment.length }} / 500</span>
        <button 
          @click="handleSubmit"
          :disabled="isSubmitting || !newComment.trim()"
          class="btn btn-primary btn-sm"
        >
          {{ isSubmitting ? '작성 중...' : '댓글 작성' }}
        </button>
      </div>
    </div>

    <!-- 로그인 필요 안내 -->
    <div v-else class="login-required-comment">
      <span class="icon">🔒</span>
      <p>
        댓글을 작성하려면 
        <router-link to="/login" class="login-link">로그인</router-link>이 필요합니다.
      </p>
    </div>
  </div>
</template>

<style scoped>
.comment-section {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-xl);
  border-top: 2px solid rgba(183, 148, 246, 0.1);
}

.comment-title {
  margin: 0 0 var(--spacing-lg) 0;
  font-size: 1.1rem;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-family: var(--font-display);
}

.comment-title .icon {
  font-size: 1.3rem;
  filter: drop-shadow(0 0 8px var(--accent-mystic));
}

/* 로딩 상태 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xl);
  color: var(--text-secondary);
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--bg-dark-elevated);
  border-top-color: var(--primary-purple);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 댓글 없음 */
.no-comments {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--text-secondary);
}

.no-comments .icon {
  display: block;
  font-size: 3rem;
  margin-bottom: var(--spacing-sm);
  opacity: 0.5;
}

.no-comments p {
  margin: 0;
  font-size: 0.95rem;
}

/* 댓글 목록 */
.comment-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.comment-item {
  padding: var(--spacing-md);
  background: var(--bg-dark-secondary);
  border-radius: 8px;
  border: 1px solid rgba(183, 148, 246, 0.1);
  transition: var(--transition-fast);
}

.comment-item:hover {
  border-color: rgba(183, 148, 246, 0.3);
  background: var(--bg-dark-elevated);
}

.comment-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 👇 헤더 오른쪽 영역 */
.comment-header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.comment-author {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.comment-date {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.comment-actions {
  display: flex;
  gap: var(--spacing-xs);
}

.btn-edit-comment,
.btn-delete-comment {
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  padding: 2px;
  transition: var(--transition-fast);
  opacity: 0.5;
}

.btn-edit-comment:hover {
  opacity: 1;
  transform: scale(1.15);
}

.btn-delete-comment:hover {
  opacity: 1;
  transform: scale(1.15);
}

.comment-text {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.comment-edit-mode {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.edit-textarea {
  width: 100%;
  padding: var(--spacing-sm);
  border-radius: 6px;
  font-size: 0.9rem;
  font-family: var(--font-body);
  line-height: 1.6;
  resize: vertical;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-xs);
}

/* 댓글 작성 폼 */
.comment-form {
  padding: var(--spacing-md);
  background: var(--bg-dark-secondary);
  border-radius: 8px;
  border: 1px solid rgba(183, 148, 246, 0.2);
}

.comment-input {
  width: 100%;
  padding: var(--spacing-sm);
  border-radius: 6px;
  font-size: 0.9rem;
  font-family: var(--font-body);
  line-height: 1.6;
  resize: vertical;
  margin-bottom: var(--spacing-sm);
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.char-count {
  font-size: 0.75rem;
  color: var(--text-muted);
}

/* 로그인 필요 안내 */
.login-required-comment {
  text-align: center;
  padding: var(--spacing-lg);
  background: var(--bg-dark-secondary);
  border-radius: 8px;
  border: 1px solid rgba(183, 148, 246, 0.2);
}

.login-required-comment .icon {
  display: block;
  font-size: 2rem;
  margin-bottom: var(--spacing-sm);
  filter: drop-shadow(0 0 8px var(--accent-mystic));
}

.login-required-comment p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
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

/* 버튼 스타일 */
.btn-sm {
  padding: var(--spacing-xs) var(--spacing-md);
  font-size: 0.85rem;
  min-width: 80px;
}

/* 반응형 */
@media (max-width: 768px) {
  .comment-section {
    padding-top: var(--spacing-md);
    margin-top: var(--spacing-md);
  }

  .comment-title {
    font-size: 1rem;
  }

  .comment-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
  }

  .comment-header-right {
    width: 100%;
    justify-content: space-between;
  }

  .comment-text {
    font-size: 0.85rem;
  }

  .edit-actions {
    flex-direction: column;
  }

  .edit-actions button {
    width: 100%;
  }

  .form-footer {
    flex-direction: column;
    gap: var(--spacing-sm);
    align-items: flex-end;
  }
}
</style>