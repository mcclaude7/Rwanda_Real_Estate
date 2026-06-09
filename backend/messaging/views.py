from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Conversations.
    - list: GET /api/v1/messaging/conversations/
    - retrieve: GET /api/v1/messaging/conversations/{id}/
    - messages: GET/POST /api/v1/messaging/conversations/{id}/messages/
    - mark_read: POST /api/v1/messaging/conversations/{id}/mark_read/
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user1=self.request.user) | Conversation.objects.filter(user2=self.request.user)

    @action(detail=True, methods=['get', 'post'])
    def messages(self, request, pk=None):
        """GET/POST /api/v1/messaging/conversations/{id}/messages/"""
        conv = self.get_object()
        if request.method == 'GET':
            msgs = Message.objects.filter(conversation=conv).order_by('created_at')
            return Response(MessageSerializer(msgs, many=True).data)
        # POST - send message
        receiver = conv.user2 if conv.user1 == request.user else conv.user1
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        msg = serializer.save(sender=request.user, receiver=receiver, conversation=conv)
        conv.last_message_at = timezone.now()
        if receiver == conv.user2: conv.user2_unread += 1
        else: conv.user1_unread += 1
        conv.save()
        return Response(MessageSerializer(msg).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        """POST /api/v1/messaging/conversations/{id}/mark-read/"""
        conv = self.get_object()
        if conv.user1 == request.user: conv.user1_unread = 0
        else: conv.user2_unread = 0
        conv.save()
        Message.objects.filter(conversation=conv, receiver=request.user, is_read=False).update(is_read=True, read_at=timezone.now())
        return Response({'message': 'Messages marked as read.'})