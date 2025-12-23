from django.urls import path
from . import views 

urlpatterns = [
    # popular, recommend 등
    path('popular/', views.popular_movies),
    path('recommend/', views.recommend_movies),
    path('<int:movie_id>/', views.movie_detail),
]