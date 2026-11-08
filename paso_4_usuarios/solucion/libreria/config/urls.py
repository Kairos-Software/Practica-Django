from django.contrib import admin
from django.urls import include, path

from libros.views import registro

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cuentas/", include("django.contrib.auth.urls")),    # login/, logout/ y más, ya hechos
    path("cuentas/registro/", registro, name="registro"),
    path("", include("libros.urls")),
]
