from django.db import models
from django.conf import settings

class Payment(models.Model):
    PAYMENT_STATUS = (('pending', 'Pending'), ('initiated', 'Initiated'), ('completed', 'Completed'), ('failed', 'Failed'))
    PAYMENT_METHODS = (('mtn-momo', 'MTN Mobile Money'), ('airtel-money', 'Airtel Money'), ('card', 'Credit/Debit Card'), ('bank-transfer', 'Bank Transfer'))
    PAYMENT_PURPOSES = (('listing-fee', 'Listing Fee'), ('featured-fee', 'Featured Listing'), ('agent-subscription', 'Agent Subscription'), ('legal-service', 'Legal Service'), ('interior-design', 'Interior Design'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    property = models.ForeignKey('listings.Property', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='RWF')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    purpose = models.CharField(max_length=30, choices=PAYMENT_PURPOSES)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    momo_phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']