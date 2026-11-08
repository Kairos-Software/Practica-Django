from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from libros.views import registro

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cuentas/", include("django.contrib.auth.urls")),    # login/, logout/ y más, ya hechos
    path("cuentas/registro/", registro, name="registro"),
    path("", include("libros.urls")),
]

# Ver las imágenes subidas (solo en desarrollo: en producción las sirve el servidor web)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
