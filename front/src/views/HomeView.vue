<template>
  <div class="home">
    <div class="hero">
      <h1 class="title">🎬 Movie </h1>
      <p class="subtitle">
        최고 평점 영화 조회, 영화 상세 정보, 예고편 & 리뷰 영상 검색까지  
        한 곳에서 경험해보세요.
      </p>

      <div class="buttons">
        <RouterLink to="/movies" class="button-primary">영화 보러가기</RouterLink>
        <RouterLink to="/review-search" class="button-outline">리뷰 검색하기</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  justify-content: center;
  text-align: center;
  padding: 80px 20px;
}

.title {
  font-size: 42px;
  font-weight: 800;
  margin-bottom: 20px;
}

.subtitle {
  font-size: 18px;
  color: #555;
  margin-bottom: 32px;
  line-height: 1.6;
}

.buttons a {
  color: #111827;       
  text-decoration: none; 
}

.buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.button-primary,
.button-outline {
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 16px;
}
</style>
