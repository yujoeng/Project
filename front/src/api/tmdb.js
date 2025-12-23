import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const TMDB_API_KEY = import.meta.env.VITE_TMDB_API_KEY
const TMDB_BASE_URL = 'https://api.themoviedb.org/3'

//  API 키 확인 로그
console.log('🔑 TMDB API KEY:', TMDB_API_KEY ? '설정됨 ' : '설정 안됨 ')

const djangoAPI = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
})

djangoAPI.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  const token = authStore.token

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

djangoAPI.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logoutUser()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// 감정 기반 영화 추천
export async function getMoviesByEmotion(emotionId, genreIds) {
  console.log('🎯 TMDB API 호출 시작')
  console.log('감정 ID:', emotionId)
  console.log('장르 IDs:', genreIds)

  if (!TMDB_API_KEY) {
    console.error(' TMDB API 키가 설정되지 않았습니다!')
    return []
  }

  console.log(' API 키 확인됨')

  try {
    const genreQuery = genreIds.join(',')
    console.log('장르 쿼리 문자열:', genreQuery)
    
    const params = {
      api_key: TMDB_API_KEY,
      language: 'ko-KR',
      sort_by: 'popularity.desc',
      with_genres: genreQuery,
      'vote_average.gte': 5.0,
      'vote_count.gte': 50,
      page: 1
    }
    
    console.log('API 요청 파라미터:', params)
    
    const url = `${TMDB_BASE_URL}/discover/movie`
    console.log('요청 URL:', url)
    
    const response = await axios.get(url, { params })
    
    console.log(' API 응답 성공')
    console.log('응답 데이터:', response.data)
    console.log('총 결과 수:', response.data.total_results)
    console.log('현재 페이지 결과 수:', response.data.results.length)

    if (response.data.results.length === 0 && genreIds.length > 1) {
      console.log('결과 없음. 첫 번째 장르만으로 재시도:', genreIds[0])
      
      const fallbackResponse = await axios.get(url, {
        params: {
          ...params,
          with_genres: genreIds[0]  // 첫 번째 장르만
        }
      })
      
      console.log('대체 검색 결과:', fallbackResponse.data.results.length)
      return fallbackResponse.data.results
    }

    return response.data.results
  } catch (error) {
    console.error(' TMDB API 에러:', error)
    console.error('에러 응답:', error.response?.data)
    console.error('에러 상태:', error.response?.status)
    return []
  }
}

// 인기 영화 가져오기
export async function getPopularMovies(page = 1) {
  try {
    const response = await axios.get(`${TMDB_BASE_URL}/movie/popular`, {
      params: {
        api_key: TMDB_API_KEY,
        language: 'ko-KR',
        page: page
      }
    })

    return response.data
  } catch (error) {
    console.error(' TMDB API 에러:', error)
    return { results: [] }
  }
}

export default djangoAPI