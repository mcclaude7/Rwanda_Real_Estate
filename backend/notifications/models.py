from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPE_CHOICES = (('new_listing', 'New Listing Alert'), ('price_drop', 'Price Drop'), ('message', 'New Message'), ('system', 'System Notification'), ('saved_search', 'Saved Search Alert'), ('payment', 'Payment Confirmation'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    property = models.ForeignKey('listings.Property', on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']