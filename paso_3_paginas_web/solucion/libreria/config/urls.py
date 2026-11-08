from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("libros.urls")),   # todo lo demás lo atiende la app libros
]
