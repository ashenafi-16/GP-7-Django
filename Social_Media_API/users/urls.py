<<<<<<< HEAD
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView, DashboardView, user_logout
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    # JWT Authentication endpoints
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('protected-endpoint/', DashboardView.as_view(), name='protected-endpoint'),

    # Authentication and password management
    path('logout/', user_logout, name='logout'),
=======
from django.urls import path # type: ignore
from .views import UserLogoutView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView # type: ignore

urlpatterns = [
    path('logout/', UserLogoutView.as_view(), name='logout'),  
>>>>>>> bc6c9869b3b3ecc4031a37cd3dbf562b8ff99454
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]
