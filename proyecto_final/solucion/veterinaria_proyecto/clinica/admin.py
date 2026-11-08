from django.contrib import admin

from .models import Duenio, Mascota, Vacuna, Visita


class MascotaInline(admin.TabularInline):
    model = Mascota
    fields = ["nombre", "especie", "raza", "nacimiento"]
    extra = 0


class VisitaInline(admin.TabularInline):
    model = Visita
    fields = ["fecha", "motivo", "costo", "pagada", "atendida_por"]
    extra = 0


@admin.register(Duenio)
class DuenioAdmin(admin.ModelAdmin):
    list_display = ["nombre", "telefono", "email"]
    search_fields = ["nombre", "telefono"]
    inlines = [MascotaInline]


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "especie", "duenio"]
    list_filter = ["especie"]
    search_fields = ["nombre", "duenio__nombre"]
    filter_horizontal = ["vacunas"]
    inlines = [VisitaInline]


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ["fecha", "mascota", "motivo", "costo", "pagada"]
    list_editable = ["pagada"]
    list_filter = ["pagada", "fecha"]


admin.site.register(Vacuna)
