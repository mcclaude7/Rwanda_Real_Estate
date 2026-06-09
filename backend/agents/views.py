from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count
from .models import Agent, AgentReview
from .serializers import AgentListSerializer, AgentDetailSerializer, AgentReviewSerializer

class AgentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Agent profiles.
    - list: GET /api/v1/agents/
    - retrieve: GET /api/v1/agents/{id}/
    - top: GET /api/v1/agents/top/
    - properties: GET /api/v1/agents/{id}/properties/
    - rate: POST /api/v1/agents/{id}/rate/
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Agent.objects.filter(is_active=True).annotate(properties_count=Count('user__properties'), reviews_count=Count('reviews'))
        if self.request.query_params.get('verified') == 'true': qs = qs.filter(is_verified=True)
        if self.request.query_params.get('featured') == 'true': qs = qs.filter(is_featured=True)
        return qs

    def get_serializer_class(self):
        return AgentDetailSerializer if self.action == 'retrieve' else AgentListSerializer

    @action(detail=False, methods=['get'])
    def top(self, request):
        """GET /api/v1/agents/top/ - Top rated agents"""
        qs = self.get_queryset().order_by('-rating', '-properties_count')[:10]
        return Response(AgentListSerializer(qs, many=True).data)

    @action(detail=True, methods=['get'])
    def properties(self, request, pk=None):
        """GET /api/v1/agents/{id}/properties/ - Agent's properties"""
        agent = self.get_object()
        properties = agent.user.properties.filter(listing_status__in=['active', 'featured'])
        from listings.serializers import PropertyListSerializer
        return Response(PropertyListSerializer(properties, many=True, context={'request': request}).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def rate(self, request, pk=None):
        """POST /api/v1/agents/{id}/rate/ - Rate an agent"""
        agent = self.get_object()
        data = request.data
        review, created = AgentReview.objects.update_or_create(
            agent=agent, reviewer=request.user,
            defaults={'rating': data.get('rating'), 'title': data.get('title', ''), 'review': data.get('review', ''), 'professionalism': data.get('professionalism', 0), 'communication': data.get('communication', 0), 'market_knowledge': data.get('market_knowledge', 0)}
        )
        avg = agent.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        agent.rating = round(avg, 2)
        agent.reviews_count = agent.reviews.count()
        agent.save(update_fields=['rating', 'reviews_count'])
        return Response(AgentReviewSerializer(review).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class AgentReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Agent reviews.
    """
    serializer_class = AgentReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return AgentReview.objects.filter(agent_id=self.kwargs.get('agent_pk'))

    def perform_create(self, serializer):
        agent = get_object_or_404(Agent, id=self.kwargs.get('agent_pk'))
        serializer.save(agent=agent, reviewer=self.request.user)