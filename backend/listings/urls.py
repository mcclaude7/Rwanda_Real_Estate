from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, AmenityViewSet, FavoriteViewSet, SavedSearchViewSet, PropertyReviewViewSet

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'amenities', AmenityViewSet, basename='amenity')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'saved-searches', SavedSearchViewSet, basename='saved-search')

# Nested reviews router
reviews_router = DefaultRouter()
reviews_router.register(r'reviews', PropertyReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(reviews_router.urls)),
    ]