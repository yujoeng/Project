from django.urls import path
from . import views

urlpatterns = [
    # ========== 리뷰 관련 ==========
    path('reviews/<int:movie_id>/', views.review_list),
    path('reviews/<int:movie_id>/create/', views.create_review),
    path('reviews/<int:review_id>/like/', views.toggle_like),
    

    path('reviews/<int:review_id>/update/', views.update_review, name='update-review'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete-review'),
    
    # ========== 댓글 관련 ==========
    path('reviews/<int:review_id>/comments/', views.comment_list),
    path('reviews/<int:review_id>/comments/create/', views.create_comment),
    

    path('comments/<int:comment_id>/update/', views.update_comment, name='update-comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete-comment'),
]