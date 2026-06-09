from rest_framework import serializers
from .models import Message, Conversation

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'receiver', 'text', 'image', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message_text = serializers.CharField(source='messages.last.text', read_only=True, allow_null=True)
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'other_user', 'property', 'last_message_text', 'last_message_at', 'unread_count']

    def get_other_user(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated: return None
        other = obj.user2 if obj.user1 == request.user else obj.user1
        return {'id': other.id, 'name': other.get_full_name() or other.username}

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated: return 0
        return obj.user2_unread if request.user == obj.user1 else obj.user1_unread