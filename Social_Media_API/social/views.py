from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Post, Comment, Like, Follow
from .serializers import PostSerializer, CommentSerializer, LikeSerializer



class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        content = request.data.get('content')
        if not content:
            return Response({"message": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new post
        post = Post.objects.create(user=request.user, content=content)
        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)


class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        content = request.data.get('content')
        if not content:
            return Response({"message": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.create(user=request.user, post=post, content=content)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class LikeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if created:
            post.update_like_count()  # Update like count on the post
            serializer = LikeSerializer(like, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You already liked this post."}, status=status.HTTP_200_OK)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        post = instance.post
        super().perform_destroy(instance)  # Delete the like instance
        post.update_like_count()  # Update the like count on the related post



class FollowCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        following_username = request.data.get('following_username')
        if not following_username:
            return Response({"message": "Following username is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            following_user = User.objects.get(username=following_username)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user == following_user:
            return Response({"message": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=following_user)
        if created:
            return Response({"message": f"You are now following {following_user.username}."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You already follow this user."}, status=status.HTTP_200_OK)


class FollowDeleteView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        # Prevent unfollowing yourself
        if instance.follower == instance.following:
            return Response({"message": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        super().perform_destroy(instance)
        return Response({"message": "You have unfollowed the user."}, status=status.HTTP_200_OK)
