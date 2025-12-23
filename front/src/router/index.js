// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/authStore'

import HomeView from '../views/HomeView.vue'
import MovieListView from '../views/MovieListView.vue'
import MovieDetailView from '../views/MovieDetailView.vue'
import ReviewSearchView from '../views/ReviewSearchView.vue'
import RecommendedView from '../views/RecommendedView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import ProfileView from '../views/ProfileView.vue'
import EmotionSelectView from '../views/EmotionSelectView.vue'

//로그인이 필요한 경우에는 뒤에 meta:{ requiresAuth: true },  추가하기
const routes = [
  { path: '/', name: 'home', component: HomeView },
    { path: '/emotions', name: 'emotions', component: EmotionSelectView },
  { path: '/movies', name: 'movies', component: MovieListView },
  { path: '/movies/:movieId', name: 'movie-detail', component: MovieDetailView },
  { path: '/review-search', name: 'review-search', component: ReviewSearchView },
  { path: '/recommended', name: 'recommended', component: RecommendedView, meta: { requiresAuth: true }, },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/signup', name: 'signup', component: SignupView },
  { path: '/profile', name: 'profile', component: ProfileView, meta: { requiresAuth: true } },
]


const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isLogin) {
    alert('로그인이 필요합니다.')
    next({
      name: 'login',
      query: { redirect: to.fullPath },
    })
  } else {
    next()
  }
})

export default router
