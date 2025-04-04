from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.contrib.auth import logout 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from rest_framework import status
from .serializers import (
    LogoutSerializer,
    ChangePasswordSerializer
)
from .models import Post
from .serializers import PostSerializer
from .serializers import LoginSerializer

class RegisterView(APIView):
    def post(self, request):
       
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class LoginView(APIView):
    def post(self, request):
        
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
          
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data["refresh_token"]
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
            except Exception:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]

            if not user.check_password(old_password):
                return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({"message": "Password changed successfully. Please log in again."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class PostUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        try:
            post = Post.objects.get(id=id, user=request.user) 
        except Post.DoesNotExist:
            return Response({"error": "Post not found or you don't have permission to edit this post."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Post updated successfully.", "post": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
