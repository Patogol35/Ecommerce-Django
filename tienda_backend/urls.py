from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # TU APP
    path('', include('tienda.urls')),

    # AUTH BASE
    path('api/auth/', include('dj_rest_auth.urls')),

    # REGISTRO + SOCIAL LOGIN
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
