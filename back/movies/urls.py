from django.urls import path
from . import views 

urlpatterns = [
    # 기존 엔드포인트 (그대로 유지)
    path('popular/', views.popular_movies),
    path('recommend/', views.recommend_movies),
    path('<int:movie_id>/', views.movie_detail),

    # 새로 추가: DB 사용 엔드포인트
    path('db/popular/', views.popular_movies_db),
    path('db/<int:movie_id>/', views.movie_detail_db),

    # 감정별 영화 정렬
    path('emotion-sorted/', views.movies_by_emotion_count),
]