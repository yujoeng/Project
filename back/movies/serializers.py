from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    """영화 상세 직렬화"""
    
    poster_url = serializers.SerializerMethodField()
    backdrop_url = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id',
            'tmdb_id',
            'title',
            'original_title',
            'overview',
            'poster_path',
            'poster_url',
            'backdrop_path',
            'backdrop_url',
            'release_date',
            'year',
            'runtime',
            'vote_average',
            'vote_count',
            'popularity',
            'genres',
            'original_language',
            'created_at',
        ]
    
    def get_poster_url(self, obj):
        return obj.poster_url
    
    def get_backdrop_url(self, obj):
        return obj.backdrop_url
    
    def get_year(self, obj):
        if obj.release_date:
            return obj.release_date.year
        return None


class MovieListSerializer(serializers.ModelSerializer):
    """영화 목록용 간단한 직렬화"""
    
    poster_url = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id',
            'tmdb_id',
            'title',
            'poster_url',
            'release_date',
            'year',
            'vote_average',
            'popularity',
        ]
    
    def get_poster_url(self, obj):
        return obj.poster_url
    
    def get_year(self, obj):
        if obj.release_date:
            return obj.release_date.year
        return None