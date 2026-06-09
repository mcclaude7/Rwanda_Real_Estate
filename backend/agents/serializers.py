from rest_framework import serializers
from .models import Agent, AgentReview

class AgentListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    class Meta:
        model = Agent
        fields = ['id', 'name', 'avatar', 'company_name', 'province', 'is_verified', 'is_featured', 'properties_count', 'rating', 'reviews_count', 'response_rate']

class AgentDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    class Meta:
        model = Agent
        fields = '__all__'

class AgentReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)
    class Meta:
        model = AgentReview
        fields = ['id', 'agent', 'reviewer', 'reviewer_name', 'rating', 'title', 'review', 'professionalism', 'communication', 'market_knowledge', 'created_at']
        read_only_fields = ['id', 'reviewer', 'created_at']
    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)