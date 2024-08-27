from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.authtoken import views
from texnomart import custom_token
from texnomart.custom_obtain_view import CustomTokenObtainPairView, LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
    TokenVerifyView,
)
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('texnomart-uz/', include('texnomart.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view()),
    path('api/token/blacklist/', TokenBlacklistView.as_view()),
    path('api-logout/', LogoutView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += debug_toolbar_urls()
