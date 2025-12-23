export function handleApiError(error) {
  if (error.response) {
    // 서버 응답 있음
    const status = error.response.status
    const data = error.response.data

    switch (status) {
      case 400:
        return data.detail || '잘못된 요청입니다.'
      case 401:
        return '로그인이 필요합니다.'
      case 404:
        return '요청한 리소스를 찾을 수 없습니다.'
      case 500:
        return '서버 오류가 발생했습니다.'
      default:
        return '알 수 없는 오류가 발생했습니다.'
    }
  } else if (error.request) {
    // 요청은 했지만 응답 없음
    return '서버에 연결할 수 없습니다.'
  } else {
    // 요청 설정 중 오류
    return error.message
  }
}