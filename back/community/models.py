from django.db import models
from django.conf import settings

# Create your models here.
class Review(models.Model):
    # 감정 선택지 정의
    EMOTION_CHOICES = [
        ('joy', '기쁨'),
        ('sadness', '슬픔'),
        ('anger', '분노'),
        ('fear', '두려움'),
        ('excitement', '흥분'),
        ('calm', '평온'),
        ('depression', '우울'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    movie_id = models.IntegerField()
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_reviews',
        blank=True
    )
    
    # 👇 감정 태그 필드 추가!
    emotion_tags = models.JSONField(default=list, blank=True)  # ['joy', 'excitement']

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review.title}"

class EmotionDiary(models.Model):
    EMOTION_CHOICES = [
        ('joy', '기쁨'),
        ('sadness', '슬픔'),
        ('anger', '분노'),
        ('fear', '두려움'),
        ('excitement', '흥분'),
        ('calm', '평온'),
        ('depression', '우울'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='emotion_diaries'
    )
    emotion = models.CharField(
        max_length=20,
        choices=EMOTION_CHOICES
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    movie_id = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.get_emotion_display()} ({self.created_at.date()})"