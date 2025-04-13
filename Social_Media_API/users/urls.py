from django.urls import path
from .views import (
    RegisterView,
    LoginUserView,
    LogoutUserView,
    UserProfileView,
    UserSearchView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login', LoginUserView.as_view(), name='auth-login'),
    path('logout/', LogoutUserView.as_view(), name='auth-logout'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('profile/', UserProfileView.as_view(), name='user-profile-current'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user-profile-detail'),
    path('profile/search/', UserSearchView.as_view(), name='user-search'),
]
