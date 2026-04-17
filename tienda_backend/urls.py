from django.contrib import admin
from django.urls import path, include
from tienda.views import google_login  # 👈 NUEVO
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tienda.urls')),

    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # 👇 GOOGLE LOGIN
    path('api/google-login/', google_login),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
