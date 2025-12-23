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