from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer

class PostDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            

            if post.user == request.user:
               
                Comment.objects.filter(post=post).delete()  
                Like.objects.filter(post=post).delete()  
                
                
                post.delete()
                
                return Response({"message": "Post and its related comments and likes deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You are not authorized to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            
  
            if comment.user == request.user:
                comment.delete()
                return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You are not authorized to delete this comment."}, status=status.HTTP_403_FORBIDDEN)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

class LikeDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        try:
            like = Like.objects.get(post_id=post_id, user=request.user)
            like.delete()
            return Response({"message": "Like removed successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"message": "Like not found."}, status=status.HTTP_404_NOT_FOUND)