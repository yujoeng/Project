import apiClient from './axios'

/**
 * 영화별 리뷰 목록 조회
 */
export const getReviews = (movieId) => {
  return apiClient.get(`/community/reviews/${movieId}/`)
}

/**
 * 리뷰 작성
 */
export const createReview = (movieId, reviewData) => {
  return apiClient.post(`/community/reviews/${movieId}/create/`, reviewData)
}

/**
 * 리뷰 수정
 */
export const updateReview = (reviewId, reviewData) => {
  return apiClient.put(`/community/reviews/${reviewId}/update/`, reviewData)
}

/**
 * 리뷰 삭제
 */
export const deleteReview = (reviewId) => {
  return apiClient.delete(`/community/reviews/${reviewId}/delete/`)
}

/**
 * 리뷰 좋아요 토글
 */
export const toggleReviewLike = (reviewId) => {
  return apiClient.post(`/community/reviews/${reviewId}/like/`)
}

/**
 * 댓글 목록 조회
 */
export const getComments = (reviewId) => {
  return apiClient.get(`/community/reviews/${reviewId}/comments/`)
}

/**
 * 댓글 작성
 */
export const createComment = (reviewId, content) => {
  return apiClient.post(`/community/reviews/${reviewId}/comments/create/`, { content })
}

/**
 * 댓글 수정
 */
export const updateComment = (commentId, content) => {
  return apiClient.put(`/community/comments/${commentId}/update/`, { content })
}

/**
 * 댓글 삭제
 */
export const deleteComment = (commentId) => {
  return apiClient.delete(`/community/comments/${commentId}/delete/`)
}