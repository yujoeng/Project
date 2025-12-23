import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny  # 👈 추가
from rest_framework.response import Response
from rest_framework import status  # 👈 추가

TMDB_URL = "https://api.themoviedb.org/3"

# 인기 영화
@api_view(['GET'])
@permission_classes([AllowAny])  # 👈 추가
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
        print(f"❌ 인기 영화 오류: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# 영화 상세 페이지
@api_view(['GET'])
@permission_classes([AllowAny])  # 👈 추가
def movie_detail(request, movie_id):
    url = f"{TMDB_URL}/movie/{movie_id}"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ko-KR",
    }

    try:
        print(f"🎬 영화 ID {movie_id} 조회 중...")  # 👈 디버깅용
        
        res = requests.get(url, params=params)
        res.raise_for_status()
        
        movie_data = res.json()
        
        print(f"// 디버깅용 성공: {movie_data.get('title', 'Unknown')}")  # 👈 디버깅용
        
        return Response(movie_data)

    except requests.exceptions.RequestException as e:
        print(f"❌ TMDB API 오류: {str(e)}")  # 👈 디버깅용
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {str(e)}")  # 👈 디버깅용
        import traceback
        traceback.print_exc()
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# 영화 추천 시스템
@api_view(['POST'])
@permission_classes([AllowAny])  # 👈 추가
def recommend_movies(request):
    emotion = request.data.get("emotion")

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
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )