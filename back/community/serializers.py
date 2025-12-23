from rest_framework import serializers
from .models import Review, Comment

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    emotion_tags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )  # 👈 감정 태그 필드 추가
    emotion_display = serializers.SerializerMethodField()  # 👈 한글 표시용

    class Meta:
        model = Review
        fields = [
            'id',
            'movie_id',
            'title',
            'content',
            'rating',
            'username',
            'like_count',
            'is_liked',
            'comment_count',
            'emotion_tags',
            'emotion_display',
            'created_at',
        ]
        read_only_fields = ['id', 'movie_id', 'username', 'like_count', 'is_liked', 'comment_count', 'emotion_display', 'created_at']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False
    
    def get_emotion_display(self, obj):
        """감정 코드를 한글로 변환"""
        emotion_map = {
            'joy': '기쁨',
            'sadness': '슬픔',
            'anger': '분노',
            'fear': '두려움',
            'excitement': '흥분',
            'calm': '평온',
            'depression': '우울',
        }
        return [emotion_map.get(tag, tag) for tag in obj.emotion_tags]


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'review',
            'username',
            'content',
            'created_at',
        ]
        read_only_fields = ['id', 'review', 'username', 'created_at']