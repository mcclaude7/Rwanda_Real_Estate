from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    ROLE_CHOICES = (('buyer', 'Buyer'), ('seller', 'Seller'), ('agent', 'Agent'), ('developer', 'Developer'), ('admin', 'Admin'))
    phone = PhoneNumberField(region='RW', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='buyer')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    LANGUAGE_CHOICES = (('en', 'English'), ('fr', 'French'), ('rw', 'Kinyarwanda'))
    preferred_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return self.get_full_name() or self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    PROVINCE_CHOICES = (('Kigali', 'Kigali City'), ('Southern', 'Southern Province'), ('Western', 'Western Province'), ('Northern', 'Northern Province'), ('Eastern', 'Eastern Province'))
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES, blank=True)
    district = models.CharField(max_length=100, blank=True)
    sector = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    budget_min = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    preferred_property_types = models.JSONField(default=list, blank=True)
    bio = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
