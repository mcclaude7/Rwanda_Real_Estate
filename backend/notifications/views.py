from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Notifications.
    - list: GET /api/v1/notifications/notifications/
    - retrieve: GET /api/v1/notifications/notifications/{id}/
    - mark_read: PUT /api/v1/notifications/notifications/{id}/mark_read/
    - mark_all_read: PUT /api/v1/notifications/notifications/mark_all_read/
    - unread_count: GET /api/v1/notifications/notifications/unread_count/
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['put'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        """PUT /api/v1/notifications/notifications/{id}/mark-read/"""
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        return Response(self.get_serializer(notification).data)

    @action(detail=False, methods=['put'], url_path='mark-all-read')
    def mark_all_read(self, request):
        """PUT /api/v1/notifications/notifications/mark-all-read/"""
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True, read_at=timezone.now())
        return Response({'message': 'All notifications marked as read.'})

    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request):
        """GET /api/v1/notifications/notifications/unread_count/"""
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': count})