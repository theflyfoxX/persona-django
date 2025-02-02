from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from app.serializers.user_serializer import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User  # Using Django's built-in User model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from app.serializers.user_serializer import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate




class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        example_json = {
            "username": "exampleuser",
            "email": "example@example.com",
            "password": "securepassword123"
        }
        return Response({"message": "Send a POST request with this format:", "example": example_json}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

# Get user by ID
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]  # Require authentication


class CustomLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]  # Allow anyone to login

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")  # Expect only username
        password = request.data.get("password")

        user = authenticate(username=username, password=password)  # Authenticate with username & password

        if user:
            response = super().post(request, *args, **kwargs)
            response.data.update({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email  # Optional: Include email in response
                }
            })
            return response
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)