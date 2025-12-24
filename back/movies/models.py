from django.db import models

class Movie(models.Model):
    
    # TMDB 고유 ID
    tmdb_id = models.IntegerField(unique=True, db_index=True)
    
    # 기본 정보
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200)
    overview = models.TextField(blank=True)
    
    # 미디어
    poster_path = models.CharField(max_length=200, blank=True, null=True)
    backdrop_path = models.CharField(max_length=200, blank=True, null=True)
    
    # 날짜/시간
    release_date = models.DateField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    
    # 평점
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    popularity = models.FloatField(default=0)
    
    # 장르 (JSON)
    genres = models.JSONField(default=list, blank=True)
    
    # 언어
    original_language = models.CharField(max_length=10, blank=True)
    
    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-popularity']
        
    def __str__(self):
        return f"{self.title} ({self.release_date.year if self.release_date else 'N/A'})"
    
    @property
    def poster_url(self):
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None
    
    @property
    def backdrop_url(self):
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/original{self.backdrop_path}"
        return None