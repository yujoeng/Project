from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # 기본 필드: username, password는 AbstractUser가 제공
    
    # 영화 취향 필드
    nickname = models.CharField(max_length=50, blank=True, null=True)
    favorite_genres = models.JSONField(default=list, blank=True)  # ['액션', '코미디', '스릴러']
    favorite_actors = models.TextField(blank=True, null=True)  # 쉼표로 구분
    preferred_countries = models.JSONField(default=list, blank=True)  # ['한국', '미국']

    # 찜한 영화 (TMDB movie_id 목록)
    favorite_movies = models.JSONField(default=list, blank=True)  # [123, 456, 789]

    # 프로필 이미지 (선택사항)
    profile_image = models.URLField(blank=True, null=True)
    
    # 자동 생성 필드
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username