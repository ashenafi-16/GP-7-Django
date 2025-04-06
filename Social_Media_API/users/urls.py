from django.urls import path
from .views import (
    UserRegistrationView,
    UserLogoutView,
    MyTokenObtainPairView,
    UserProfileDetail,
)
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('api/users/<int:id>', UserProfileDetail.as_view(), name='user-profile'),
    path('api/users/me/bio', views.manage_bio, name='manage-bio'),
]
