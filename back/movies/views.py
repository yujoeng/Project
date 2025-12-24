import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q

# Community 앱에서 Review 모델 import
try:
    from community.models import Review
except ImportError:
    Review = None

# Movies 앱 모델 및 시리얼라이저
try:
    from .models import Movie
    from .serializers import MovieSerializer, MovieListSerializer
except ImportError:
    Movie = None
    MovieSerializer = None
    MovieListSerializer = None

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

# 이 아래부터는 db로 영화 데이터를 불러온 이후 추가되는 부분 정상 작동하지 않으면 다시 이전으로 revert

# 감정별 영화 정렬 API
@api_view(['GET'])
@permission_classes([AllowAny])
def movies_by_emotion_count(request):
    """
    각 영화별 특정 감정의 리뷰 수를 집계하여 정렬된 영화 목록 반환

    Query Parameters:
    - emotion: 감정 (joy, sadness, anger, fear, excitement, calm, depression)
    - order: 정렬 순서 (desc: 내림차순, asc: 오름차순), 기본값: desc
    - limit: 반환할 영화 수 (기본: 20)
    """
    try:
        # Review 모델이 없으면 에러 반환
        if Review is None:
            return Response(
                {"error": "Review 모델을 불러올 수 없습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        emotion = request.GET.get('emotion')
        order = request.GET.get('order', 'desc')
        limit = int(request.GET.get('limit', 20))

        if not emotion:
            return Response(
                {"error": "emotion 파라미터가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 유효한 감정인지 확인
        valid_emotions = ['joy', 'sadness', 'anger', 'fear', 'excitement', 'calm', 'depression']
        if emotion not in valid_emotions:
            return Response(
                {"error": f"유효하지 않은 감정입니다. 가능한 값: {', '.join(valid_emotions)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        print(f"🔍 감정별 정렬 요청: emotion={emotion}, order={order}, limit={limit}")

        # 1. 해당 감정을 포함한 리뷰를 movie_id별로 집계
        # SQLite와 PostgreSQL 모두 지원하는 방법 사용
        from django.db.models import JSONField
        from django.db.models.functions import Cast
        from django.db.models import TextField

        # 모든 리뷰 가져오기
        all_reviews = Review.objects.all()

        # Python에서 필터링 (JSONField contains가 SQLite에서 안 될 수 있음)
        movie_emotion_counts = {}
        for review in all_reviews:
            if emotion in review.emotion_tags:
                movie_id = review.movie_id
                movie_emotion_counts[movie_id] = movie_emotion_counts.get(movie_id, 0) + 1

        if not movie_emotion_counts:
            return Response({
                "results": [],
                "emotion": emotion,
                "order": order,
                "message": f"'{emotion}' 감정의 리뷰가 없습니다."
            })

        # 정렬
        sorted_movies = sorted(
            movie_emotion_counts.items(),
            key=lambda x: x[1],
            reverse=(order == 'desc')
        )[:limit]

        movie_emotion_data = dict(sorted_movies)
        print(f"✅ 집계 완료: {len(movie_emotion_data)}개 영화")

        # 2. TMDB API에서 영화 정보 가져오기
        movies_data = []
        for movie_id, emotion_count in movie_emotion_data.items():
            try:
                # TMDB API 호출
                url = f"{TMDB_URL}/movie/{movie_id}"
                params = {
                    "api_key": settings.TMDB_API_KEY,
                    "language": "ko-KR",
                }

                res = requests.get(url, params=params, timeout=5)

                if res.status_code == 200:
                    movie_data = res.json()
                    movie_data['emotion_count'] = emotion_count
                    movies_data.append(movie_data)

            except Exception as e:
                print(f"영화 {movie_id} 정보 가져오기 실패: {str(e)}")
                continue

        # 4. emotion_count 기준으로 정렬 (API 호출 순서가 바뀔 수 있으므로)
        movies_data.sort(
            key=lambda x: x['emotion_count'],
            reverse=(order == 'desc')
        )

        return Response({
            "results": movies_data,
            "emotion": emotion,
            "order": order,
            "total": len(movies_data)
        })

    except Exception as e:
        print(f"❌ 감정별 영화 정렬 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# DB에서 인기 영화 조회
@api_view(['GET'])
@permission_classes([AllowAny])
def popular_movies_db(request):
    """DB에서 인기 영화 반환"""
    try:
        limit = int(request.GET.get('limit', 20))
        movies = Movie.objects.all()[:limit]
        serializer = MovieListSerializer(movies, many=True)
        
        return Response({
            "results": serializer.data,
            "total": Movie.objects.count()
        })
    
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# DB 우선, 없으면 API
@api_view(['GET'])
@permission_classes([AllowAny])
def movie_detail_db(request, movie_id):
    """DB에서 찾고, 없으면 TMDB API 호출"""
    try:
        movie = Movie.objects.get(tmdb_id=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
        
    except Movie.DoesNotExist:
        # DB에 없으면 TMDB API 호출 (기존 방식)
        url = f"{TMDB_URL}/movie/{movie_id}"
        params = {
            "api_key": settings.TMDB_API_KEY,
            "language": "ko-KR",
        }

        try:
            res = requests.get(url, params=params, timeout=10)
            res.raise_for_status()
            return Response(res.json())

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )