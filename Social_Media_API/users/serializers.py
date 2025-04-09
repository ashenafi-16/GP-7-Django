from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.core.validators import validate_email  
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from social.models import Post
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'bio']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            bio=validated_data.get('bio', '')  # Bio is optional
        )
        return user
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    first_name = serializers.CharField(required=False, allow_blank=True)  # Make first_name optional


    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name')  # Include first_name here
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def validate_email(self, value):
        value = value.lower().strip()
        try:
            validate_email(value)  # Now this will work
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_username(self, value):
        value = value.strip()
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        if len(value) < 4:
            raise serializers.ValidationError("Username must be at least 4 characters.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # custom claims
        token['name'] = user.get_full_name()
        token['email'] = user.email
        
        return token
def validate(self, attrs):
        data = super().validate(attrs)
        
        # extra responses here
        data['user'] = {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name
        }
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'date_joined']
        read_only_fields = ['id', 'email', 'date_joined']  # Prevent these from being updated

    def validate_username(self, value):
        # Check if username is already taken by another user
        if User.objects.filter(username=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value
    
class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at', 'updated_at', 'likes', 'comments']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'likes', 'comments']

    def create(self, validated_data):
        """
        Create a new post instance while automatically setting the user field.
        Assumes the user is authenticated.
        """
        user = self.context['request'].user  # Get the current authenticated user
        post = Post.objects.create(user=user, **validated_data)
        return post

    def update(self, instance, validated_data):
        """
        Update the content of the post instance.
        """
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

    def validate_content(self, value):
        """
        Custom validation for content length. You can adjust this to any specific rules you need.
        """
        if len(value) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters.")
        return value
