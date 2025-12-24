// src/api/movies.js
import tmdb from "./tmdb";

/**
 * 인기 영화 목록
 */
export const getPopularMovies = () => {
  return tmdb.get("/movies/popular/");
};

/**
 * 영화 상세 정보
 */
export const getMovieDetail = (movieId) => {
  return tmdb.get(`/movies/${movieId}/`);
};

/**
 * 영화 검색 (TMDB API)
 */
export const searchMovies = async (query) => {
  const TMDB_API_KEY = import.meta.env.VITE_TMDB_API_KEY
  const response = await fetch(
    `https://api.themoviedb.org/3/search/movie?api_key=${TMDB_API_KEY}&language=ko-KR&query=${encodeURIComponent(query)}&page=1`
  )
  return await response.json()
}

/**
 * DB에서 영화 검색 (제목 기반)
 */
export const searchMoviesInDB = (query) => {
  return apiClient.get(`/movies/search/`, {
    params: { q: query }
  })
}