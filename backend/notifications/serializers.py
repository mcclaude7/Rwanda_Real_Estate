from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='property.title', read_only=True, allow_null=True)
    class Meta:
        model = Notification
        fields = ['id', 'user', 'property', 'property_title', 'notification_type', 'title', 'message', 'data', 'is_read', 'read_at', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']