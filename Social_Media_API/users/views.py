from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserSearchSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data_with_tokens = serializer.save()

        return Response({
            "user": {
                "id": user_data_with_tokens["id"],
                "email": user_data_with_tokens["email"],
                "username": user_data_with_tokens["username"],
                "bio": user_data_with_tokens["bio"],
            },
            "tokens": {
                "refresh": user_data_with_tokens["refresh"],
                "access": user_data_with_tokens["access"]
            },
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)

class LoginUserView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "bio": user.bio
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_200_OK)

class UserProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None, *args, **kwargs):
    
        if user_id is None:
            user = request.user 
        else:
            if request.user.id != user_id:
                raise PermissionDenied("You do not have permission to view this user's profile.")
            user = get_object_or_404(User, id=user_id)

        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, user_id=None, *args, **kwargs):
        """
        Update own profile only.
        """
        user = request.user if user_id is None else get_object_or_404(User, id=user_id)
        if request.user != user:
            raise PermissionDenied("You cannot update another user's profile")

        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutUserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query:
            return User.objects.filter(username__icontains=query)
        return User.objects.none() 