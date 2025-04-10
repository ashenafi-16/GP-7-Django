from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like, Follow

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)  
    likes = serializers.StringRelatedField(many=True, read_only=True)  

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image', 'video', 'created_at', 'likes_count', 'comments_count', 'comments', 'likes']
        read_only_fields = ['id', 'created_at', 'likes_count', 'comments_count']

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.StringRelatedField(read_only=True)  
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at', 'parent']
        read_only_fields = ['id', 'created_at']

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError("Content cannot be empty.")
        return value



class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.StringRelatedField(read_only=True) 

    class Meta:
        model = Like
        fields = ['user', 'post', 'liked_at']
        read_only_fields = ['liked_at']


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    following = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Follow
        fields = ['follower', 'following', 'followed_at']
        read_only_fields = ['followed_at']
