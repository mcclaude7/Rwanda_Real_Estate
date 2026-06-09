from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='property.title', read_only=True, allow_null=True)
    class Meta:
        model = Payment
        fields = ['id', 'user', 'property', 'property_title', 'amount', 'currency', 'payment_method', 'purpose', 'transaction_id', 'momo_phone', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']