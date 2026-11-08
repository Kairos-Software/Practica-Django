from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cuentas/", include("django.contrib.auth.urls")),    # login y logout (sin registro: los usuarios los crea el admin)
    path("", include("clinica.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # las fotos, en desarrollo
