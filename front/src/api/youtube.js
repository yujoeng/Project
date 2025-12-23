import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const YOUTUBE_API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

export async function searchTrailer(videoQuery) {
  const res = await axios.get('https://www.googleapis.com/youtube/v3/search', {
    params: {
      key: YOUTUBE_API_KEY,
      part: 'snippet',
      type: 'video',
      maxResults: 1,
      q: `${videoQuery} official trailer`, // 검색어
    },
  })

  const item = res.data.items[0]
  if (!item) return null

  return item.id.videoId
}

export async function searchReviewVideos(query) {
  const authStore = useAuthStore()
  const token = authStore.token || localStorage.getItem('access_token')


  const headers = token ? { Authorization: `Bearer ${token}` } : {}

  const res = await axios.get('https://www.googleapis.com/youtube/v3/search', {
    params: {
      key: YOUTUBE_API_KEY,
      part: 'snippet',
      type: 'video',
      maxResults: 8,
      q: query, 
    },

  })

  return res.data.items   
}
