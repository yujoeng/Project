export const EMOTIONS = [
  { code: 'joy', label: '기쁨', emoji: '😊', color: '#FFD93D' },
  { code: 'sadness', label: '슬픔', emoji: '😢', color: '#6BCB77' },
  { code: 'anger', label: '분노', emoji: '😠', color: '#FF6B6B' },
  { code: 'fear', label: '두려움', emoji: '😰', color: '#A78BFA' },
  { code: 'excitement', label: '흥분', emoji: '🤩', color: '#FF8E53' },
  { code: 'calm', label: '평온', emoji: '😌', color: '#4ECDC4' },
  { code: 'depression', label: '우울', emoji: '😔', color: '#95A5A6' },
]

// 감정 코드로 정보 가져오기
export const getEmotionByCode = (code) => {
  return EMOTIONS.find(e => e.code === code)
}

// 감정 코드로 이모지 가져오기
export const getEmotionEmoji = (code) => {
  return getEmotionByCode(code)?.emoji || '❓'
}

// 감정 코드로 라벨 가져오기
export const getEmotionLabel = (code) => {
  return getEmotionByCode(code)?.label || code
}