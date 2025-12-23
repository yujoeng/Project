from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from datetime import date

from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer

# ========== 리뷰 목록 조회 ==========
@api_view(['GET'])
@permission_classes([AllowAny])
def review_list(request, movie_id):
    reviews = Review.objects.filter(movie_id=movie_id).order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True, context={'request': request})
    return Response(serializer.data)

# ========== 리뷰 작성 ==========
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, movie_id):
    print("=" * 50)
    print(f"📝 리뷰 작성 요청")
    print(f"👤 사용자: {request.user.username}")
    print(f"🎬 영화 ID: {movie_id}")
    print(f"📦 받은 데이터: {request.data}")
    print(f"📦 데이터 타입: {type(request.data)}")
    print("=" * 50)
    
    serializer = ReviewSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        serializer.save(
            user=request.user,
            movie_id=movie_id
        )
        print(f"✅ 리뷰 작성 성공!")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    print(f"❌ Serializer 검증 실패:")
    print(f"   에러: {serializer.errors}")
    print("=" * 50)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ========== 리뷰 수정 ==========
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if review.user != request.user:
        return Response(
            {'detail': '수정 권한이 없습니다.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = ReviewSerializer(review, data=request.data, partial=True, context={'request': request})
    
    if serializer.is_valid():
        serializer.save()
        print(f"✅ 리뷰 수정 성공: {review.id}")
        return Response(serializer.data)
    
    print(f"❌ 리뷰 수정 실패: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ========== 리뷰 삭제 ==========
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if review.user != request.user and not request.user.is_superuser:
        return Response(
            {'detail': '삭제 권한이 없습니다.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    review.delete()
    print(f"✅ 리뷰 삭제 성공: {review_id}")
    return Response(
        {'message': '리뷰가 삭제되었습니다.'},
        status=status.HTTP_204_NO_CONTENT
    )

# ========== 좋아요 토글 ==========
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    user = request.user

    if user in review.likes.all():
        review.likes.remove(user)
        liked = False
    else:
        review.likes.add(user)
        liked = True

    return Response({
        'liked': liked,
        'like_count': review.likes.count()
    })

# ========== 댓글 목록 조회 ==========
@api_view(['GET'])
@permission_classes([AllowAny])
def comment_list(request, review_id):
    comments = Comment.objects.filter(review_id=review_id).order_by('created_at')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

# ========== 댓글 작성 ==========
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, review_id):
    print("=" * 50)
    print(f"💬 댓글 작성 요청")
    print(f"👤 사용자: {request.user.username}")
    print(f"📝 리뷰 ID: {review_id}")
    print(f"📦 받은 데이터: {request.data}")
    print("=" * 50)
    
    review = get_object_or_404(Review, id=review_id)
    serializer = CommentSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(
            user=request.user,
            review=review
        )
        print(f"✅ 댓글 작성 성공!")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    print(f"❌ Serializer 검증 실패:")
    print(f"   에러: {serializer.errors}")
    print("=" * 50)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ========== 댓글 수정 ==========
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.user != request.user:
        return Response(
            {'detail': '수정 권한이 없습니다.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = CommentSerializer(comment, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        print(f"✅ 댓글 수정 성공: {comment.id}")
        return Response(serializer.data)
    
    print(f"❌ 댓글 수정 실패: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ========== 댓글 삭제 ==========
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.user != request.user and not request.user.is_superuser:
        return Response(
            {'detail': '삭제 권한이 없습니다.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    comment.delete()
    print(f"✅ 댓글 삭제 성공: {comment_id}")
    return Response(
        {'message': '댓글이 삭제되었습니다.'},
        status=status.HTTP_204_NO_CONTENT
    )