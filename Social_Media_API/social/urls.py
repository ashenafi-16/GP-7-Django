from django.urls import path
from .views import (
    PostCreateView,
    PostListView,
    PostDeleteView,
    CommentCreateView,
    CommentDeleteView,
    LikeCreateView,
    LikeDeleteView,
)

urlpatterns = [

    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),


    path('posts/<int:post_id>/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),

   
    path('posts/<int:post_id>/like/', LikeCreateView.as_view(), name='like-create'),
    path('likes/delete/<int:pk>/', LikeDeleteView.as_view(), name='like-delete'),
]
