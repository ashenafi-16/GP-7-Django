from django.urls import path
from .views import PostDeleteView, CommentDeleteView, LikeDeleteView

urlpatterns = [
    path('posts/<int:post_id>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('comments/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('posts/<int:post_id>/like/delete/', LikeDeleteView.as_view(), name='like-delete'),
]
