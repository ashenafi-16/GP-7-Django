from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView, DashboardView, user_logout
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path # type: ignore
from .views import user_logout
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView # type: ignore
from .views import RegisterView
from .views import PostUpdateView
from .views import LoginView



urlpatterns = [
    # JWT Authentication endpoints
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('protected-endpoint/', DashboardView.as_view(), name='protected-endpoint'),
    path('login/', LoginView.as_view(), name='login'),

    # Authentication and password management
    path('logout/', user_logout, name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('auth/register/', RegisterView.as_view(), name='register'),
    path('posts/<int:id>/edit/', PostUpdateView.as_view(), name='post-edit'),
]
