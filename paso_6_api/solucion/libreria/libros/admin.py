from django.contrib import admin

from .models import Autor, Libro, Resenia


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ["nombre", "pais", "nacimiento"]
    search_fields = ["nombre"]


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ["titulo", "autor", "precio", "stock", "disponible"]
    list_filter = ["autor", "disponible"]
    search_fields = ["titulo"]


@admin.register(Resenia)
class ReseniaAdmin(admin.ModelAdmin):
    list_display = ["libro", "usuario", "puntaje", "creada"]
    list_filter = ["puntaje"]
