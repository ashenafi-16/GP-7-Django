from django.urls import path # type: ignore
from .views import user_logout
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView # type: ignore

urlpatterns = [
    path('logout/', user_logout, name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done')
]
