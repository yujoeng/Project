<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import apiClient from '@/api/axios'

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

onMounted(() => {
  fetchProfile()
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
  color: #111827;
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
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
}

.profile-section h2 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #374151;
}

.info-row {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.info-row label {
  width: 120px;
  font-weight: 600;
  color: #6b7280;
}

.info-row span {
  color: #111827;
}

.info-row input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}

.preference-group {
  margin-bottom: 24px;
}

.preference-group label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 12px;
}

.preference-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}

.preference-group span {
  color: #6b7280;
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
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
}

.genre-btn:hover,
.country-btn:hover {
  border-color: #7b10adff;
}

.genre-btn.active,
.country-btn.active {
  background: #7b10adff;
  color: white;
  border-color: #7b10adff;
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
  background: #f3f4f6;
  border-radius: 16px;
  font-size: 14px;
  color: #374151;
}

.empty {
  color: #9ca3af;
  font-style: italic;
}

.button-group {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.btn-primary {
  padding: 10px 20px;
  background: #7b10adff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary:hover {
  background: #6a0e96;
}

.btn-secondary {
  padding: 10px 20px;
  background: white;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
}

.btn-secondary:hover {
  background: #f9fafb;
}

.password-change-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.password-change-form input {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}

.danger-zone {
  border-color: #fecaca;
  background: #fef2f2;
}

.danger-zone h2 {
  color: #dc2626;
}

.danger-zone p {
  color: #991b1b;
  margin-bottom: 16px;
}

.btn-danger {
  padding: 10px 20px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.btn-danger:hover {
  background: #b91c1c;
}
</style>