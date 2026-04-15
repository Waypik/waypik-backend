from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserMeSerializer, UserSerializer


# Test view for checking authentication
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    """
    Test endpoint to verify JWT authentication is working.
    """
    user = request.user
    identifier = user.phone or user.email or "User"
    return Response({
        "message": f"Hello {identifier}, you are authenticated!",
        "user": {
            "id": user.id,
            "phone": user.phone,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
        }
    })


# Registration endpoint (alternative to dj-rest-auth)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user with phone, first_name, last_name, and password.

    Expected payload:
    {
        "username": "+1234567890",  // phone number
        "first_name": "John",
        "last_name": "Doe",
        "password1": "securepassword123",
        "password2": "securepassword123"  // optional
    }
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(request)
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                "message": "Account created successfully",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                "user": {
                    "id": user.id,
                    "phone": user.phone,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                }
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get current user profile
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    """
    Get the current authenticated user's profile information.
    """
    serializer = UserMeSerializer(request.user)
    return Response(serializer.data)


# Update current user profile
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update the current authenticated user's profile.

    Allowed fields: first_name, last_name, email
    Phone and role cannot be changed.
    """
    serializer = UserMeSerializer(
        request.user,
        data=request.data,
        partial=request.method == "PATCH",
        context={'request': request}
    )

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Profile updated successfully",
            "user": serializer.data
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List all users (admin only - you can add permission checks)
class UserListView(generics.ListAPIView):
    """
    List all users. Should be restricted to admin users.
    """
    queryset = None
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # You can add role-based filtering here
        # For now, return all users
        from .models import User
        return User.objects.all()
