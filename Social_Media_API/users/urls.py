from django.urls import path
from .views import (
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    UserRegistrationView,
    UserLogoutView,
    MyTokenObtainPairView,
    UserProfileDetail,
)
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # User-related endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # User profile-related endpoints
    path('api/users/<int:id>/', UserProfileDetail.as_view(), name='user-profile'),
    path('api/users/me/bio/', views.manage_bio, name='manage-bio'),

    # Post-related endpoints
    path('api/posts/', PostCreateView.as_view(), name='create-post'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('api/posts/<int:pk>/update/', PostUpdateView.as_view(), name='update-post'),
    path('api/posts/<int:pk>/delete/', PostDeleteView.as_view(), name='delete-post'),
]
