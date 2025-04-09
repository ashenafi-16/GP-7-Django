from rest_framework import generics, status,serializers,permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException,PermissionDenied
from rest_framework.permissions import AllowAny
from .serializers import (
    UserRegistrationSerializer, 
    MyTokenObtainPairSerializer,
    UserProfileSerializer,
    PostSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.core.exceptions import ValidationError

from .models import User
from social.models import Post
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def manage_bio(request):
    user = request.user
    
    if request.method == 'GET':
        return Response({'bio': user.bio})
    
    elif request.method == 'PUT':
        new_bio = request.data.get('bio', '')
        user.bio = new_bio
        user.save()
        return Response({'status': 'bio updated', 'bio': user.bio})
    
class UserProfileDetail(generics.RetrieveUpdateAPIView):
    # parser_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    
    def get_object(self):
        # Return the user profile based on id in URL
        try:
            return self.queryset.get(pk=self.kwargs['id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
    
    def update(self, request, *args, **kwargs):
        # Only allow users to update their own profile
        if request.user.pk != int(kwargs['id']):
            raise PermissionDenied("You can only update your own profile.")
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Public access
    
    def post(self, request, *args, **kwargs):
        try:
            # Log incoming data for debugging
            print("Received registration data:", request.data)
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
            
            # Return user data and tokens upon successful registration
            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            # If validation fails, show error details
            print("Validation error:", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log any other errors
            print("Unexpected error:", e)
            return Response(
                {"error": f"Registration failed. Please try again. Error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserLogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        """
        POST /users/logout/
        Requires: 
        - Authorization header with valid JWT token
        - refresh token in request body
        """
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT
            )
            
        except TokenError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Could not log out"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    def get_view_name(self):
        return "User Login"

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
            
        except InvalidToken as e:
            return Response(
                {"error": "Invalid token"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        except APIException as e:
            return Response(
                {"error": e.detail}, 
                status=e.status_code
            )
        except Exception as e:
            return Response(
                {"error": "Login failed"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Post CRUD Views

class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the user as the one who creates the post
        serializer.save(user=self.request.user)

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        post = self.get_object()
        if post.user != self.request.user:
            raise PermissionDenied("You can only update your own posts.")
        serializer.save()

class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own posts.")
        instance.delete()