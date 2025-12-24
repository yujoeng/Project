from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, logout


from .serializers import SignupSerializer
from .serializers import (
    PasswordChangeSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)
from community.serializers import ReviewSerializer, CommentSerializer
from community.models import Review, Comment

# 회원가입 
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {"message": "회원가입 성공", "username": user.username},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    return TokenObtainPairView.as_view()(request)

# 비밀번호 변경 (인증 필요)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "비밀번호 변경 성공"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인 요청 
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)  # 인증 없이 접근 가능

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        # 사용자 인증
        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"detail": "가입되지 않은 계정입니다."},  # 사용자 인증 실패 시 메시지
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        # 인증이 성공하면 JWT 토큰 발급
        response = super().post(request, *args, **kwargs)
        return response

# 로그아웃 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)


# 회원 삭제
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user  
    user.delete()

    return Response({"message": "탈퇴가 완료되었습니다."}, status=status.HTTP_200_OK)

# 사용자 정보 조회 (기존 get_user_info와 기능 통합)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """현재 로그인한 사용자 정보 반환 (간단한 버전)"""
    user = request.user
    return Response({
        'username': user.username,
        'id': user.id,
        'nickname': user.nickname,
    }, status=status.HTTP_200_OK)


# 프로필 조회 및 수정
@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    GET: 프로필 조회
    PUT/PATCH: 프로필 수정
    """
    user = request.user
    
    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 내가 작성한 리뷰 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_reviews(request):
    """현재 로그인한 사용자가 작성한 리뷰 목록 반환"""
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# 내가 작성한 댓글 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_comments(request):
    """현재 로그인한 사용자가 작성한 댓글 목록 반환"""
    comments = Comment.objects.filter(user=request.user).order_by('-created_at').select_related('review')
    serializer = CommentSerializer(comments, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# 찜한 영화 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_movies(request):
    """현재 로그인한 사용자가 찜한 영화 목록 반환"""
    user = request.user
    return Response({
        'favorite_movies': user.favorite_movies
    }, status=status.HTTP_200_OK)


# 찜하기 토글
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite_movie(request):
    """영화 찜하기 추가/제거"""
    user = request.user
    movie_id = request.data.get('movie_id')

    if not movie_id:
        return Response(
            {'error': 'movie_id가 필요합니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # movie_id를 정수로 변환
    try:
        movie_id = int(movie_id)
    except (ValueError, TypeError):
        return Response(
            {'error': '유효하지 않은 movie_id입니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 찜하기 토글
    if movie_id in user.favorite_movies:
        user.favorite_movies.remove(movie_id)
        is_favorite = False
        message = '찜하기가 취소되었습니다.'
    else:
        user.favorite_movies.append(movie_id)
        is_favorite = True
        message = '찜하기에 추가되었습니다.'

    user.save()

    return Response({
        'message': message,
        'is_favorite': is_favorite,
        'favorite_movies': user.favorite_movies
    }, status=status.HTTP_200_OK)

