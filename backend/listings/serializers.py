from rest_framework import serializers
from .models import Property, PropertyImage, Favorite, SavedSearch, Amenity, PropertyReview

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'name_rw', 'name_fr', 'icon', 'category']

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'caption', 'is_cover', 'display_order']

class PropertyListSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    class Meta:
        model = Property
        fields = ['id', 'title', 'slug', 'purpose', 'property_type', 'province', 'city', 'area', 'price', 'price_per_sqm', 'bedrooms', 'bathrooms', 'built_up_area', 'cover_image', 'images', 'furnishing_status', 'listing_status', 'owner_name', 'is_agent_verified', 'favorites_count', 'rating', 'created_at']

class PropertyDetailSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    owner_phone = serializers.CharField(source='owner.phone', read_only=True)
    is_favorited = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = '__all__'
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(user=request.user).exists()
        return False

class PropertyCreateSerializer(serializers.ModelSerializer):
    amenities = serializers.ListField(child=serializers.IntegerField(), required=False, allow_empty=True)
    class Meta:
        model = Property
        exclude = ['owner', 'slug', 'views_count', 'favorites_count', 'rating', 'listing_status', 'verification_status', 'created_at', 'updated_at', 'published_at']
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class FavoriteSerializer(serializers.ModelSerializer):
    property_detail = PropertyListSerializer(source='property', read_only=True)
    class Meta:
        model = Favorite
        fields = ['id', 'property', 'property_detail', 'created_at']
        read_only_fields = ['id', 'created_at']

class SavedSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedSearch
        fields = ['id', 'name', 'search_params', 'created_at']
        read_only_fields = ['id', 'created_at']

class PropertyReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    class Meta:
        model = PropertyReview
        fields = ['id', 'user', 'user_name', 'property', 'rating', 'title', 'review', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)