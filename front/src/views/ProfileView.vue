<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import apiClient from '@/api/axios'
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()

// 프로필 데이터
const profile = ref({
  username: '',
  nickname: '',
  favorite_genres: [],
  favorite_actors: '',
  preferred_countries: [],
  created_at: '',
})

// 비밀번호 변경 데이터
const passwordData = ref({
  old_password: '',
  new_password: '',
  new_password2: '',
})

// 상태 관리
const isEditing = ref(false)
const showPasswordChange = ref(false)
const message = ref('')
const errorMessage = ref('')

// 내 활동 데이터
const myReviews = ref([])
const myComments = ref([])
const isLoadingActivity = ref(false)

// 찜한 영화 데이터
const favoriteMovies = ref([])
const favoriteMoviesDetails = ref([])
const isLoadingFavorites = ref(false)

const TMDB_API_KEY = import.meta.env.VITE_TMDB_API_KEY
const TMDB_BASE_URL = 'https://api.themoviedb.org/3'

// 장르 목록
const genreOptions = [
  '액션', '코미디', '드라마', '스릴러', '공포',
  'SF', '판타지', '로맨스', '애니메이션', '다큐멘터리'
]

// 국가 목록
const countryOptions = [
  '한국', '미국', '일본', '중국', '프랑스', '영국'
]

// 프로필 조회
const fetchProfile = async () => {
  try {
    const response = await apiClient.get('/accounts/profile/')
    profile.value = response.data
  } catch (error) {
    console.error('프로필 조회 실패:', error)
    errorMessage.value = '프로필을 불러올 수 없습니다.'
  }
}

// 프로필 수정
const updateProfile = async () => {
  try {
    message.value = ''
    errorMessage.value = ''

    const response = await apiClient.patch('/accounts/profile/', {
      nickname: profile.value.nickname,
      favorite_genres: profile.value.favorite_genres,
      favorite_actors: profile.value.favorite_actors,
      preferred_countries: profile.value.preferred_countries,
    })

    profile.value = response.data
    message.value = '프로필이 수정되었습니다.'
    isEditing.value = false
  } catch (error) {
    console.error('프로필 수정 실패:', error)
    errorMessage.value = '프로필 수정에 실패했습니다.'
  }
}

// 비밀번호 변경
const changePassword = async () => {
  try {
    message.value = ''
    errorMessage.value = ''

    // 입력 검증
    if (!passwordData.value.old_password) {
      errorMessage.value = '기존 비밀번호를 입력해주세요.'
      return
    }

    if (!passwordData.value.new_password) {
      errorMessage.value = '새 비밀번호를 입력해주세요.'
      return
    }

    if (passwordData.value.new_password !== passwordData.value.new_password2) {
      errorMessage.value = '새 비밀번호가 일치하지 않습니다.'
      return
    }

    if (passwordData.value.new_password.length < 8) {
      errorMessage.value = '비밀번호는 최소 8자 이상이어야 합니다.'
      return
    }

    await apiClient.post('/accounts/change-password/', passwordData.value)

    message.value = '비밀번호가 변경되었습니다.'
    
    // 초기화
    passwordData.value = {
      old_password: '',
      new_password: '',
      new_password2: '',
    }
    showPasswordChange.value = false
  } catch (error) {
    console.error('비밀번호 변경 실패:', error)
    
    if (error.response?.data) {
      const data = error.response.data
      if (data.old_password) {
        errorMessage.value = data.old_password[0]
      } else if (data.new_password) {
        errorMessage.value = data.new_password[0]
      } else if (data.new_password2) {
        errorMessage.value = data.new_password2[0]
      } else {
        errorMessage.value = '비밀번호 변경에 실패했습니다.'
      }
    } else {
      errorMessage.value = '서버에 연결할 수 없습니다.'
    }
  }
}

// 회원탈퇴
const deleteAccount = async () => {
  if (!confirm('정말로 탈퇴하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) {
    return
  }

  try {
    await apiClient.post('/accounts/delete/')
    
    alert('회원 탈퇴가 완료되었습니다.')
    
    // 로그아웃 처리
    await authStore.logoutUser()
    router.push('/')
  } catch (error) {
    console.error('회원탈퇴 실패:', error)
    errorMessage.value = '회원 탈퇴에 실패했습니다.'
  }
}

// 장르 토글
const toggleGenre = (genre) => {
  const index = profile.value.favorite_genres.indexOf(genre)
  if (index > -1) {
    profile.value.favorite_genres.splice(index, 1)
  } else {
    profile.value.favorite_genres.push(genre)
  }
}

// 국가 토글
const toggleCountry = (country) => {
  const index = profile.value.preferred_countries.indexOf(country)
  if (index > -1) {
    profile.value.preferred_countries.splice(index, 1)
  } else {
    profile.value.preferred_countries.push(country)
  }
}

// 내가 작성한 리뷰 조회
const fetchMyReviews = async () => {
  try {
    isLoadingActivity.value = true
    const response = await apiClient.get('/accounts/my-reviews/')
    myReviews.value = response.data
  } catch (error) {
    console.error('리뷰 조회 실패:', error)
  } finally {
    isLoadingActivity.value = false
  }
}

// 내가 작성한 댓글 조회
const fetchMyComments = async () => {
  try {
    const response = await apiClient.get('/accounts/my-comments/')
    myComments.value = response.data
  } catch (error) {
    console.error('댓글 조회 실패:', error)
  }
}

// 영화 상세 페이지로 이동
const goToMovie = (movieId) => {
  router.push(`/movies/${movieId}`)
}

// 찜한 영화 목록 조회
const fetchFavoriteMovies = async () => {
  try {
    isLoadingFavorites.value = true
    const response = await apiClient.get('/accounts/favorite-movies/')
    favoriteMovies.value = response.data.favorite_movies || []

    // 찜한 영화가 있으면 TMDB에서 상세 정보 가져오기
    if (favoriteMovies.value.length > 0) {
      await fetchFavoriteMoviesDetails()
    }
  } catch (error) {
    console.error('찜한 영화 조회 실패:', error)
  } finally {
    isLoadingFavorites.value = false
  }
}

// 찜한 영화 상세 정보 가져오기 (TMDB)
const fetchFavoriteMoviesDetails = async () => {
  try {
    const promises = favoriteMovies.value.map(async (movieId) => {
      try {
        const response = await axios.get(`${TMDB_BASE_URL}/movie/${movieId}`, {
          params: {
            api_key: TMDB_API_KEY,
            language: 'ko-KR'
          }
        })
        return response.data
      } catch (error) {
        console.error(`영화 ${movieId} 정보 조회 실패:`, error)
        return null
      }
    })

    const results = await Promise.all(promises)
    favoriteMoviesDetails.value = results.filter(movie => movie !== null)
  } catch (error) {
    console.error('찜한 영화 상세 정보 조회 실패:', error)
  }
}

onMounted(async () => {
  await fetchProfile()
  await Promise.all([fetchMyReviews(), fetchMyComments(), fetchFavoriteMovies()])
})
</script>

<template>
  <div class="profile-page">
    <h1>내 프로필</h1>

    <!-- 성공/에러 메시지 -->
    <p v-if="message" class="success-message">{{ message }}</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <!-- 기본 정보 -->
    <div class="profile-section">
      <h2>기본 정보</h2>
      
      <div class="info-row">
        <label>아이디</label>
        <span>{{ profile.username }}</span>
      </div>

      <div class="info-row">
        <label>가입일</label>
        <span>{{ new Date(profile.created_at).toLocaleDateString() }}</span>
      </div>

      <div class="info-row">
        <label>닉네임</label>
        <input 
          v-if="isEditing"
          v-model="profile.nickname" 
          placeholder="닉네임을 입력하세요"
        />
        <span v-else>{{ profile.nickname || '미설정' }}</span>
      </div>
    </div>

    <!-- 영화 취향 -->
    <div class="profile-section">
      <h2>영화 취향</h2>

      <!-- 선호 장르 -->
      <div class="preference-group">
        <label>선호 장르</label>
        <div v-if="isEditing" class="genre-grid">
          <button
            v-for="genre in genreOptions"
            :key="genre"
            :class="['genre-btn', { active: profile.favorite_genres.includes(genre) }]"
            @click="toggleGenre(genre)"
          >
            {{ genre }}
          </button>
        </div>
        <div v-else class="genre-tags">
          <span 
            v-for="genre in profile.favorite_genres" 
            :key="genre"
            class="tag"
          >
            {{ genre }}
          </span>
          <span v-if="profile.favorite_genres.length === 0" class="empty">미설정</span>
        </div>
      </div>

      <!-- 좋아하는 배우 -->
      <div class="preference-group">
        <label>좋아하는 배우</label>
        <input 
          v-if="isEditing"
          v-model="profile.favorite_actors"
          placeholder="예: 송강호, 마동석, 톰 크루즈"
        />
        <span v-else>{{ profile.favorite_actors || '미설정' }}</span>
      </div>

      <!-- 관심 국가 -->
      <div class="preference-group">
        <label>관심 국가 영화</label>
        <div v-if="isEditing" class="country-grid">
          <button
            v-for="country in countryOptions"
            :key="country"
            :class="['country-btn', { active: profile.preferred_countries.includes(country) }]"
            @click="toggleCountry(country)"
          >
            {{ country }}
          </button>
        </div>
        <div v-else class="country-tags">
          <span 
            v-for="country in profile.preferred_countries" 
            :key="country"
            class="tag"
          >
            {{ country }}
          </span>
          <span v-if="profile.preferred_countries.length === 0" class="empty">미설정</span>
        </div>
      </div>

      <!-- 수정/저장 버튼 -->
      <div class="button-group">
        <button v-if="!isEditing" @click="isEditing = true" class="btn-primary">
          프로필 수정
        </button>
        <template v-else>
          <button @click="updateProfile" class="btn-primary">저장</button>
          <button @click="isEditing = false; fetchProfile()" class="btn-secondary">취소</button>
        </template>
      </div>
    </div>

    <!-- 찜한 영화 -->
    <div class="profile-section">
      <h2>찜한 영화 ({{ favoriteMoviesDetails.length }})</h2>

      <!-- 로딩 -->
      <div v-if="isLoadingFavorites" class="activity-loading">
        <div class="loading-spinner"></div>
        <p>찜한 영화를 불러오는 중...</p>
      </div>

      <!-- 빈 상태 -->
      <div v-else-if="favoriteMoviesDetails.length === 0" class="empty-activity">
        <p>아직 찜한 영화가 없습니다.</p>
        <button @click="router.push('/movies')" class="btn-secondary" style="margin-top: 16px;">
          영화 둘러보기
        </button>
      </div>

      <!-- 찜한 영화 그리드 -->
      <div v-else class="favorite-movies-grid">
        <div
          v-for="movie in favoriteMoviesDetails"
          :key="movie.id"
          class="favorite-movie-card"
          @click="goToMovie(movie.id)"
        >
          <div class="favorite-movie-poster">
            <img
              v-if="movie.poster_path"
              :src="`https://image.tmdb.org/t/p/w300${movie.poster_path}`"
              :alt="movie.title"
            />
            <div v-else class="no-poster">🎬</div>
          </div>
          <div class="favorite-movie-info">
            <h4 class="favorite-movie-title">{{ movie.title }}</h4>
            <div class="favorite-movie-meta">
              <span class="favorite-rating">⭐ {{ movie.vote_average?.toFixed(1) }}</span>
              <span class="favorite-year">{{ movie.release_date?.split('-')[0] }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 내 활동 -->
    <div class="profile-section">
      <h2>내 활동</h2>

      <!-- 로딩 -->
      <div v-if="isLoadingActivity" class="activity-loading">
        <div class="loading-spinner"></div>
        <p>활동 내역을 불러오는 중...</p>
      </div>

      <div v-else class="activity-container">
        <!-- 내가 작성한 리뷰 -->
        <div class="activity-section">
          <h3 class="activity-title">
            <span class="activity-icon">✍️</span>
            작성한 리뷰 ({{ myReviews.length }})
          </h3>

          <div v-if="myReviews.length === 0" class="empty-activity">
            <p>아직 작성한 리뷰가 없습니다.</p>
          </div>

          <div v-else class="activity-list">
            <div
              v-for="review in myReviews.slice(0, 5)"
              :key="review.id"
              class="activity-item"
              @click="goToMovie(review.movie_id)"
            >
              <div class="activity-header">
                <h4 class="activity-item-title">{{ review.title }}</h4>
                <span class="activity-rating">⭐ {{ review.rating }}</span>
              </div>
              <p class="activity-content">{{ review.content }}</p>
              <div class="activity-meta">
                <span class="activity-date">{{ new Date(review.created_at).toLocaleDateString() }}</span>
                <div class="activity-stats">
                  <span>❤️ {{ review.like_count }}</span>
                  <span>💬 {{ review.comment_count }}</span>
                </div>
              </div>
            </div>
          </div>

          <button
            v-if="myReviews.length > 5"
            class="btn-show-more"
            @click="router.push('/review-search')"
          >
            모든 리뷰 보기 ({{ myReviews.length }}개)
          </button>
        </div>

        <!-- 내가 작성한 댓글 -->
        <div class="activity-section">
          <h3 class="activity-title">
            <span class="activity-icon">💬</span>
            작성한 댓글 ({{ myComments.length }})
          </h3>

          <div v-if="myComments.length === 0" class="empty-activity">
            <p>아직 작성한 댓글이 없습니다.</p>
          </div>

          <div v-else class="activity-list">
            <div
              v-for="comment in myComments.slice(0, 5)"
              :key="comment.id"
              class="activity-item comment-item"
            >
              <p class="activity-content">{{ comment.content }}</p>
              <div class="activity-meta">
                <span class="activity-date">{{ new Date(comment.created_at).toLocaleDateString() }}</span>
              </div>
            </div>
          </div>

          <button
            v-if="myComments.length > 5"
            class="btn-show-more"
            @click="router.push('/review-search')"
          >
            모든 댓글 보기 ({{ myComments.length }}개)
          </button>
        </div>
      </div>
    </div>

    <!-- 비밀번호 변경 -->
    <div class="profile-section">
      <h2>비밀번호 변경</h2>
      
      <button 
        v-if="!showPasswordChange"
        @click="showPasswordChange = true"
        class="btn-secondary"
      >
        비밀번호 변경하기
      </button>

      <div v-else class="password-change-form">
        <input 
          v-model="passwordData.old_password"
          type="password"
          placeholder="기존 비밀번호"
        />
        <input 
          v-model="passwordData.new_password"
          type="password"
          placeholder="새 비밀번호 (최소 8자)"
        />
        <input 
          v-model="passwordData.new_password2"
          type="password"
          placeholder="새 비밀번호 확인"
        />
        
        <div class="button-group">
          <button @click="changePassword" class="btn-primary">변경</button>
          <button @click="showPasswordChange = false" class="btn-secondary">취소</button>
        </div>
      </div>
    </div>

    <!-- 회원 탈퇴 -->
    <div class="profile-section danger-zone">
      <h2>회원 탈퇴</h2>
      <p>탈퇴 시 모든 데이터가 삭제되며 복구할 수 없습니다.</p>
      <button @click="deleteAccount" class="btn-danger">회원 탈퇴</button>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 30px;
  color: rgba(255, 255, 255, 0.95);
  text-shadow: 0 2px 10px rgba(183, 148, 246, 0.3);
}

.success-message {
  color: green;
  background: #d1fae5;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.error-message {
  color: #dc2626;
  background: #fee2e2;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.profile-section {
  background: linear-gradient(135deg, #8b5fc7 0%, #6b4a8f 50%, #4a2d5e 100%);
  border: 2px solid rgba(212, 175, 55, 0.3);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(123, 16, 173, 0.2);
}

.profile-section h2 {
  font-size: 18px;
  margin-bottom: 20px;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 600;
}

.info-row {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.info-row label {
  width: 120px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
}

.info-row span {
  color: rgba(255, 255, 255, 0.95);
}

.info-row input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.95);
}

.info-row input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.preference-group {
  margin-bottom: 24px;
}

.preference-group label {
  display: block;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 12px;
}

.preference-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.95);
}

.preference-group input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.preference-group span {
  color: rgba(255, 255, 255, 0.8);
}

.genre-grid,
.country-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
}

.genre-btn,
.country-btn {
  padding: 8px 16px;
  border: 2px solid rgba(212, 175, 55, 0.4);
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.genre-btn:hover,
.country-btn:hover {
  border-color: #d4af37;
  background: rgba(212, 175, 55, 0.2);
}

.genre-btn.active,
.country-btn.active {
  background: linear-gradient(135deg, #d4af37, #f4d03f);
  color: #1a0d2e;
  border-color: #d4af37;
  font-weight: 600;
}

.genre-tags,
.country-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  display: inline-block;
  padding: 6px 12px;
  background: rgba(212, 175, 55, 0.2);
  border: 1px solid rgba(212, 175, 55, 0.4);
  border-radius: 16px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
}

.empty {
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
}

.button-group {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.btn-primary {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.95);
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-primary:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.6);
  transform: translateY(-2px);
}

.btn-secondary {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
}

.password-change-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.password-change-form input {
  padding: 10px 12px;
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.95);
}

.password-change-form input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.danger-zone {
  border-color: rgba(220, 38, 38, 0.3);
  background: linear-gradient(135deg, #4a2d5e 0%, #2d1b3d 100%);
  padding: 16px;
  margin-top: 40px;
}

.danger-zone h2 {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  margin-bottom: 8px;
}

.danger-zone p {
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 12px;
  font-size: 12px;
}

.btn-danger {
  padding: 6px 16px;
  background: rgba(220, 38, 38, 0.2);
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(220, 38, 38, 0.4);
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  font-size: 13px;
  transition: all 0.3s;
}

.btn-danger:hover {
  background: rgba(220, 38, 38, 0.3);
  border-color: rgba(220, 38, 38, 0.6);
  color: rgba(255, 255, 255, 0.95);
}

/* 내 활동 섹션 */
.activity-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  gap: 16px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(183, 148, 246, 0.2);
  border-top-color: #b794f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.activity-loading p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.activity-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.activity-section {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 20px;
}

.activity-section:first-child {
  border-top: none;
  padding-top: 0;
}

.activity-title {
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.activity-icon {
  font-size: 18px;
}

.empty-activity {
  text-align: center;
  padding: 30px 20px;
  color: rgba(255, 255, 255, 0.5);
  font-size: 14px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.activity-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.activity-item:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(183, 148, 246, 0.4);
  transform: translateX(4px);
}

.comment-item {
  cursor: default;
}

.comment-item:hover {
  transform: none;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
  gap: 12px;
}

.activity-item-title {
  font-size: 15px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  flex: 1;
  margin: 0;
}

.activity-rating {
  color: #fbbf24;
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
}

.activity-content {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.activity-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}

.activity-date {
  color: rgba(255, 255, 255, 0.5);
}

.activity-stats {
  display: flex;
  gap: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.activity-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.btn-show-more {
  padding: 8px 16px;
  background: rgba(183, 148, 246, 0.15);
  color: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(183, 148, 246, 0.3);
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s;
  width: 100%;
}

.btn-show-more:hover {
  background: rgba(183, 148, 246, 0.25);
  border-color: rgba(183, 148, 246, 0.5);
}

/* 찜한 영화 그리드 */
.favorite-movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 16px;
}

.favorite-movie-card {
  cursor: pointer;
  border-radius: 12px;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s;
}

.favorite-movie-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px rgba(183, 148, 246, 0.3);
  border-color: rgba(183, 148, 246, 0.5);
}

.favorite-movie-poster {
  width: 100%;
  aspect-ratio: 2/3;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.3);
}

.favorite-movie-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.favorite-movie-card:hover .favorite-movie-poster img {
  transform: scale(1.05);
}

.no-poster {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  background: rgba(0, 0, 0, 0.2);
}

.favorite-movie-info {
  padding: 12px;
}

.favorite-movie-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.3;
}

.favorite-movie-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
}

.favorite-rating {
  color: #fbbf24;
  font-weight: 600;
}

.favorite-year {
  color: rgba(255, 255, 255, 0.6);
}

@media (max-width: 768px) {
  .favorite-movies-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 12px;
  }

  .favorite-movie-title {
    font-size: 0.8rem;
  }
}
</style>