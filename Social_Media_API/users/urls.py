from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .views import (
    UserLogoutView,
    RegisterView,
    PostUpdateView,
    LikeCreateView,
    CommentCreateView,
    LoginView,
    PostListView,
    LikePostView,
    get_likes,
    get_comments,
)

urlpatterns = [
    # JWT Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Authentication and password management
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    # User and post-related endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('posts/<int:id>/edit/', PostUpdateView.as_view(), name='post-edit'),
    path('like/', LikeCreateView.as_view(), name='like-post'),
    path('comment/', CommentCreateView.as_view(), name='comment-post'),
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>/like/', LikePostView.as_view(), name='post-like'),
    path('posts/<int:post_id>/likes/', get_likes, name='get_likes'),
    path('posts/<int:post_id>/comments/', get_comments, name='get_comments'),
]