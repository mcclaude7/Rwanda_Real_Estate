from django_filters import rest_framework as filters
from .models import Property

class PropertyFilter(filters.FilterSet):
    purpose = filters.MultipleChoiceFilter(choices=Property.PURPOSE_CHOICES)
    property_type = filters.MultipleChoiceFilter(choices=Property.PROPERTY_TYPES)
    furnishing_status = filters.MultipleChoiceFilter(choices=Property.FURNISHING_CHOICES)
    province = filters.CharFilter()
    city = filters.CharFilter(lookup_expr='icontains')
    area = filters.CharFilter(lookup_expr='icontains')
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    bedrooms_min = filters.NumberFilter(field_name='bedrooms', lookup_expr='gte')
    built_up_area_min = filters.NumberFilter(field_name='built_up_area', lookup_expr='gte')
    is_gated_community = filters.BooleanFilter()
    has_power_backup = filters.BooleanFilter()
    has_lift = filters.BooleanFilter()
    ordering = filters.OrderingFilter(fields=(('price', 'price'), ('created_at', 'newest'), ('-views_count', 'popular'), ('favorites_count', 'most_favorited')))

    class Meta:
        model = Property
        fields = ['purpose', 'property_type', 'furnishing_status', 'province', 'city', 'area', 'price_min', 'price_max', 'bedrooms_min', 'is_gated_community', 'has_power_backup', 'has_lift']