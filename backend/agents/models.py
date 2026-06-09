from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Agent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent_profile')
    company_name = models.CharField(max_length=200, blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    PROVINCE_CHOICES = (('Kigali', 'Kigali City'), ('Southern', 'Southern Province'), ('Western', 'Western Province'), ('Northern', 'Northern Province'), ('Eastern', 'Eastern Province'))
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES)
    districts_served = models.JSONField(default=list, blank=True)
    specializes_in = models.JSONField(default=list, blank=True)
    bio = models.TextField(blank=True, max_length=1000)
    website = models.URLField(blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    reviews_count = models.PositiveIntegerField(default=0)
    properties_count = models.PositiveIntegerField(default=0)
    response_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agents'
        ordering = ['-rating', '-properties_count']

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class AgentReview(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent_reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    review = models.TextField()
    professionalism = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=0)
    communication = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=0)
    market_knowledge = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agent_reviews'
        unique_together = ['agent', 'reviewer']
        ordering = ['-created_at']