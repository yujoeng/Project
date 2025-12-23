from django.urls import path
from . import views
from .views import CustomTokenObtainPairView, logout_view, delete_account, get_user_info
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', views.signup, name='signup'),

    # 로그인 (JWT 발급)
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 토큰 재발급
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #비밀번호 변경 
    path('change-password/', views.change_password, name='change_password'),

    #로그아웃
    path('logout/', logout_view, name='logout'),

    # 회원탈퇴
    path('delete/', delete_account, name='delete_account'),

    # 프로필
    path('profile/', views.profile_view, name='profile'),

    # 현재 사용자 정보 조회
    path('me/', get_user_info, name='user_info'),
]