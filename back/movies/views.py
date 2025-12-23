import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

TMDB_URL = "https://api.themoviedb.org/3"

#인기 영화
@api_view(['GET'])
def popular_movies(request):
    url = f"{TMDB_URL}/movie/popular"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ko-KR",
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()

        return Response({
            "results": data.get("results", [])
        })

    except requests.exceptions.RequestException as e:
        return Response(
            {"error": str(e)},
            status=500
        )

#영화 상세 페이지
@api_view(['GET'])
def movie_detail(request, movie_id):
    url = f"{TMDB_URL}/movie/{movie_id}"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ko-KR",
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        return Response(res.json())

    except requests.exceptions.RequestException as e:
        return Response(
            {"error": str(e)},
            status=500
        )

# 영화 추천 시스템
@api_view(['POST'])
def recommend_movies(request):
    emotion = request.data.get("emotion")

    # 임시 로직: 인기 영화 반환
    url = f"{TMDB_URL}/movie/popular"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ko-KR",
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()

        return Response({
            "emotion": emotion,
            "results": data.get("results", [])
        })

    except requests.exceptions.RequestException as e:
        return Response(
            {"error": str(e)},
            status=500
        )