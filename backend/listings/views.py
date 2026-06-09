from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django.shortcuts import get_object_or_404
from .models import Property, PropertyImage, Amenity, Favorite, SavedSearch, PropertyReview
from .serializers import (
    PropertyListSerializer, PropertyDetailSerializer, PropertyCreateSerializer,
    PropertyImageSerializer, AmenitySerializer, FavoriteSerializer,
    SavedSearchSerializer, PropertyReviewSerializer
)
from .filters import PropertyFilter

class PropertyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Property CRUD.
    - list: GET /api/v1/listings/properties/
    - retrieve: GET /api/v1/listings/properties/{id}/
    - create: POST /api/v1/listings/properties/
    - update: PUT /api/v1/listings/properties/{id}/
    - partial_update: PATCH /api/v1/listings/properties/{id}/
    - destroy: DELETE /api/v1/listings/properties/{id}/
    - mine: GET /api/v1/listings/properties/mine/
    - nearby: GET /api/v1/listings/properties/nearby/
    - favorite: POST /api/v1/listings/properties/{id}/favorite/
    """
    filterset_class = PropertyFilter
    search_fields = ['title', 'description', 'city', 'area', 'locality']
    ordering_fields = ['price', 'created_at', 'views_count', 'favorites_count']

    def get_queryset(self):
        qs = Property.objects.filter(listing_status__in=['active', 'featured'])
        return qs.annotate(favorites_count=Count('favorited_by', distinct=True))

    def get_serializer_class(self):
        if self.action == 'list': return PropertyListSerializer
        if self.action in ['create', 'update', 'partial_update']: return PropertyCreateSerializer
        return PropertyDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        """GET /api/v1/listings/properties/mine/ - Current user's properties"""
        qs = self.get_queryset().filter(owner=request.user)
        serializer = PropertyListSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """GET /api/v1/listings/properties/nearby/?lat=x&lng=y&radius=5"""
        lat = request.query_params.get('latitude')
        lng = request.query_params.get('longitude')
        if not lat or not lng:
            return Response({'error': 'latitude and longitude required'}, status=status.HTTP_400_BAD_REQUEST)
        lat, lng = float(lat), float(lng)
        radius = float(request.query_params.get('radius', 0.05))
        qs = self.get_queryset().filter(
            latitude__gte=lat-radius, latitude__lte=lat+radius,
            longitude__gte=lng-radius, longitude__lte=lng+radius
        )
        serializer = PropertyListSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        """POST /api/v1/listings/properties/{id}/favorite/ - Toggle favorite"""
        prop = self.get_object()
        fav, created = Favorite.objects.get_or_create(user=request.user, property=prop)
        if not created:
            fav.delete()
            return Response({'is_favorited': False}, status=status.HTTP_200_OK)
        return Response({'is_favorited': True}, status=status.HTTP_201_CREATED)

class PropertyImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Property Images.
    """
    serializer_class = PropertyImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return PropertyImage.objects.filter(property_id=self.kwargs.get('property_pk'))

    def perform_create(self, serializer):
        prop = get_object_or_404(Property, id=self.kwargs.get('property_pk'))
        serializer.save(property=prop)

class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Amenities (read-only).
    GET /api/v1/listings/amenities/
    """
    queryset = Amenity.objects.filter(is_active=True)
    serializer_class = AmenitySerializer
    permission_classes = [permissions.AllowAny]

class FavoriteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Favorites.
    """
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('property')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SavedSearchViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Saved Searches.
    """
    serializer_class = SavedSearchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedSearch.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PropertyReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Property Reviews.
    """
    serializer_class = PropertyReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return PropertyReview.objects.filter(property_id=self.kwargs.get('property_pk'))

    def perform_create(self, serializer):
        prop = get_object_or_404(Property, id=self.kwargs.get('property_pk'))
        serializer.save(property=prop, user=self.request.user)