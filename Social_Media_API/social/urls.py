from django.urls import path
from .views import (
    PostCreateView,
    PostDeleteView,
    PostListView,
    CommentCreateView,
    CommentDeleteView,
    LikeCreateView,
    LikeDeleteView
)



urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('posts/<int:post_id>/comments/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    path('posts/<int:post_id>/likes/', LikeCreateView.as_view(), name='like-create'),
    path('likes/<int:pk>/delete/', LikeDeleteView.as_view(), name='like-delete'),
]
