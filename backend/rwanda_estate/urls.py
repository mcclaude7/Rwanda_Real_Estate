
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/listings/', include('listings.urls')),
    path('api/v1/agents/', include('agents.urls')),
    path('api/v1/messaging/', include('messaging.urls')),
    path('api/v1/payments/', include('payments.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    path('api/v1/search/', include('search.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
