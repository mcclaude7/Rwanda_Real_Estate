from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from .models import UserProfile
from .serializers import UserSerializer, UserDetailSerializer, RegisterSerializer, UserProfileSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management.
    - list: GET /api/v1/accounts/users/
    - retrieve: GET /api/v1/accounts/users/{id}/
    - create: POST /api/v1/accounts/users/
    - update: PUT /api/v1/accounts/users/{id}/
    - partial_update: PATCH /api/v1/accounts/users/{id}/
    - destroy: DELETE /api/v1/accounts/users/{id}/
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return UserDetailSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """GET /api/v1/accounts/users/me/ - Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def update_me(self, request):
        """PUT/PATCH /api/v1/accounts/users/update_me/ - Update current user"""
        user = request.user
        partial = request.method == 'PATCH'
        serializer = self.get_serializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser], permission_classes=[permissions.IsAuthenticated])
    def upload_avatar(self, request):
        """POST /api/v1/accounts/users/upload_avatar/ - Upload user avatar"""
        user = request.user
        if 'avatar' not in request.FILES:
            return Response({'error': 'No avatar file provided'}, status=status.HTTP_400_BAD_REQUEST)
        user.avatar = request.FILES['avatar']
        user.save()
        return Response(UserSerializer(user).data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        """POST /api/v1/accounts/users/change_password/ - Change user password"""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not user.check_password(old_password):
            return Response({'old_password': 'Wrong password.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully.'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user profiles.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RegisterViewSet(viewsets.GenericViewSet):
    """
    ViewSet for user registration.
    POST /api/v1/accounts/register/
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'user': UserSerializer(user).data, 'message': 'Registration successful'}, status=status.HTTP_201_CREATED)