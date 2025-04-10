from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# ✅ Updated Registration Serializer (with Refresh and Access Token)
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

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'password2', 'bio']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # remove password2 field
        password = validated_data.pop('password')
        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "bio": user.bio,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

# ✅ Login Serializer
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        data['user'] = user
        return data

# ✅ User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'date_joined']
        read_only_fields = ['email', 'date_joined']
        extra_kwargs = {
            'username': {'required': False}
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance
