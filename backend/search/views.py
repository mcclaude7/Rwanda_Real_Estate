from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from listings.models import Property
from listings.serializers import PropertyListSerializer

class SearchViewSet(viewsets.ViewSet):
    """
    ViewSet for Search.
    - list: GET /api/v1/search/properties/?q=...
    - suggestions: GET /api/v1/search/suggestions/?q=...
    - valuation: POST /api/v1/search/valuation/
    """
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        """GET /api/v1/search/properties/?q=...&purpose=..."""
        params = request.query_params
        query = params.get('q', '')
        qs = Property.objects.filter(listing_status='active')
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(city__icontains=query) | Q(area__icontains=query))
        purpose = params.get('purpose')
        if purpose: qs = qs.filter(purpose=purpose)
        property_type = params.get('property_type')
        if property_type: qs = qs.filter(property_type=property_type)
        price_min = params.get('price_min')
        if price_min: qs = qs.filter(price__gte=float(price_min))
        price_max = params.get('price_max')
        if price_max: qs = qs.filter(price__lte=float(price_max))
        province = params.get('province')
        if province: qs = qs.filter(province=province)
        ordering = params.get('ordering', '-created_at')
        qs = qs.order_by(ordering)
        page_size = int(params.get('page_size', 20))
        page_num = int(params.get('page', 1))
        start = (page_num - 1) * page_size
        end = start + page_size
        page = qs[start:end]
        serializer = PropertyListSerializer(page, many=True, context={'request': request})
        return Response({'count': qs.count(), 'results': serializer.data})

    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        """GET /api/v1/search/suggestions/?q=..."""
        query = request.query_params.get('q', '')
        if not query or len(query) < 2:
            return Response([])
        cities = Property.objects.filter(city__icontains=query).values_list('city', flat=True).distinct()[:5]
        areas = Property.objects.filter(area__icontains=query).values_list('area', flat=True).distinct()[:5]
        suggestions = [{'type': 'city', 'value': c, 'label': c} for c in cities] + [{'type': 'area', 'value': a, 'label': a} for a in areas]
        return Response(suggestions[:10])

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def valuation(self, request):
        """POST /api/v1/search/valuation/"""
        data = request.data
        property_type = data.get('property_type')
        province = data.get('province')
        built_up_area = float(data.get('built_up_area', 0))
        bedrooms = int(data.get('bedrooms', 0))
        base_prices = {'apartment': 800000, 'house': 600000, 'villa': 1200000, 'land': 200000, 'commercial': 1000000, 'office': 900000}
        location_multiplier = {'Kigali': 1.5, 'Northern': 1.0, 'Southern': 0.9, 'Eastern': 0.85, 'Western': 0.9}
        price_per_sqm = base_prices.get(property_type, 500000)
        multiplier = location_multiplier.get(province, 1.0)
        estimated_value = built_up_area * price_per_sqm * multiplier
        if bedrooms: estimated_value += bedrooms * 5000000 * multiplier
        comparables = Property.objects.filter(property_type=property_type, province=province, listing_status='active').order_by('?')[:5]
        comparable_prices = [p.price for p in comparables]
        avg_comparable = sum(comparable_prices) / len(comparable_prices) if comparable_prices else None
        return Response({
            'estimated_value': round(estimated_value, 2),
            'price_per_sqm': round(price_per_sqm * multiplier, 2),
            'comparables': PropertyListSerializer(comparables, many=True, context={'request': request}).data,
            'average_comparable_price': round(avg_comparable, 2) if avg_comparable else None
        })