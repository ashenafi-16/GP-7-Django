from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import CustomTokenObtainPairView
from .views import DashboardView 

urlpatterns = [
    # JWT Authentication endpoints
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', views.dashboard, name='dashboard'),
     path('protected-endpoint/', DashboardView.as_view(), name='protected-endpoint'),

]






