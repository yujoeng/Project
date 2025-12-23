<script setup>
const props = defineProps({
  movie: {
    type: Object,
    required: true,
  },
})


</script>

<template>
  <div class="movie-card">
    <img
      class="poster"
      :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
      :alt="movie.title"
    />
    <h2 class="title">{{ movie.title }}</h2>
    <p class="rating">⭐ {{ movie.vote_average }}</p>
    <p class="overview">
      {{ movie.overview ? movie.overview.slice(0, 80) + '...' : '줄거리 없음' }}
    </p>
  </div>
</template>

<style scoped>
.movie-card {
  width: 250px;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background-color: #ffffff;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
  transition: transform 0.1s ease, box-shadow 0.1s ease;
}

.movie-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 10px rgba(15, 23, 42, 0.12);
}

.poster {
  width: 100%;
  border-radius: 4px;
}

.title {
  font-size: 18px;
  margin: 8px 0 4px;
}

.rating {
  font-size: 14px;
  margin-bottom: 4px;
}

.overview {
  font-size: 13px;
  color: #555;
}
</style>
