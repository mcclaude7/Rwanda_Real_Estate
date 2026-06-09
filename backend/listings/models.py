from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class Property(models.Model):
    PURPOSE_CHOICES = (('sale', 'For Sale'), ('rent', 'For Rent'), ('lease', 'For Lease'), ('pg', 'Paying Guest'))
    PROPERTY_TYPES = (('apartment', 'Apartment'), ('house', 'House'), ('villa', 'Villa'), ('land', 'Land/Plot'), ('commercial', 'Commercial'), ('office', 'Office Space'), ('warehouse', 'Warehouse'), ('industrial', 'Industrial'), ('hotel', 'Hotel/Resort'), ('farm', 'Farm'))
    FURNISHING_CHOICES = (('unfurnished', 'Unfurnished'), ('semi-furnished', 'Semi-Furnished'), ('furnished', 'Furnished'))
    LISTING_STATUS = (('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive'), ('sold', 'Sold'), ('rented', 'Rented'), ('featured', 'Featured'))
    VERIFICATION_STATUS = (('pending', 'Pending'), ('verified', 'Verified'), ('rejected', 'Rejected'))
    PROVINCE_CHOICES = (('Kigali', 'Kigali City'), ('Southern', 'Southern Province'), ('Western', 'Western Province'), ('Northern', 'Northern Province'), ('Eastern', 'Eastern Province'))

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    description_fr = models.TextField(blank=True)
    description_rw = models.TextField(blank=True)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    property_type = models.CharField(max_length=30, choices=PROPERTY_TYPES)
    furnishing_status = models.CharField(max_length=20, choices=FURNISHING_CHOICES, blank=True, null=True)
    listing_status = models.CharField(max_length=20, choices=LISTING_STATUS, default='draft')
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    locality = models.CharField(max_length=200, blank=True)
    landmark = models.CharField(max_length=200, blank=True)
    full_address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    bedrooms = models.PositiveIntegerField(blank=True, null=True)
    bathrooms = models.PositiveIntegerField(blank=True, null=True)
    balconies = models.PositiveIntegerField(default=0)
    total_floors = models.PositiveIntegerField(blank=True, null=True)
    floor_number = models.PositiveIntegerField(blank=True, null=True)
    built_up_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    carpet_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    maintenance_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_price_negotiable = models.BooleanField(default=False)
    amenities = models.JSONField(default=list, blank=True)
    facing_direction = models.CharField(max_length=20, blank=True, null=True)
    year_built = models.PositiveIntegerField(blank=True, null=True)
    parking_spaces = models.PositiveIntegerField(default=0)
    is_gated_community = models.BooleanField(default=False)
    has_power_backup = models.BooleanField(default=False)
    has_lift = models.BooleanField(default=False)
    cover_image = models.ImageField(upload_to='properties/covers/', blank=True, null=True)
    agent_name = models.CharField(max_length=100, blank=True)
    agent_phone = models.CharField(max_length=20, blank=True)
    is_agent_verified = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    favorites_count = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)], default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'properties'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['purpose', 'property_type']), models.Index(fields=['province', 'city']), models.Index(fields=['listing_status'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.price_per_sqm and self.built_up_area:
            self.price_per_sqm = self.price / self.built_up_area
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.city}"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/images/')
    caption = models.CharField(max_length=200, blank=True)
    is_cover = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'property_images'
        ordering = ['display_order', 'id']

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'favorites'
        unique_together = ['user', 'property']
        ordering = ['-created_at']

class SavedSearch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_searches')
    name = models.CharField(max_length=100, blank=True)
    search_params = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'saved_searches'
        ordering = ['-created_at']

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_rw = models.CharField(max_length=100, blank=True)
    name_fr = models.CharField(max_length=100, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, default='other')
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'amenities'
        ordering = ['category', 'name']
    def __str__(self):
        return self.name

class PropertyReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='property_reviews')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'property_reviews'
        unique_together = ['user', 'property']
        ordering = ['-created_at']