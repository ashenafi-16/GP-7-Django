# urls.py
from django.urls import path
from .views import RegisterUserView, LoginUserView, LogoutUserView,UserProfileView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('users/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
]
