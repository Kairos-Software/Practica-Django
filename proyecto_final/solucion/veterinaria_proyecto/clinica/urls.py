from django.urls import path

from . import views

app_name = "clinica"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    # Dueños
    path("duenios/", views.Duenios.as_view(), name="duenios"),
    path("duenios/nuevo/", views.CrearDuenio.as_view(), name="crear_duenio"),
    path("duenios/<int:pk>/", views.DetalleDuenio.as_view(), name="duenio"),
    path("duenios/<int:pk>/editar/", views.EditarDuenio.as_view(), name="editar_duenio"),
    path("duenios/<int:pk>/borrar/", views.borrar_duenio, name="borrar_duenio"),
    # Mascotas
    path("mascotas/", views.mascotas, name="mascotas"),
    path("mascotas/nueva/", views.crear_mascota, name="crear_mascota"),
    path("mascotas/<int:pk>/", views.mascota, name="mascota"),
    path("mascotas/<int:pk>/editar/", views.EditarMascota.as_view(), name="editar_mascota"),
    path("mascotas/<int:pk>/borrar/", views.BorrarMascota.as_view(), name="borrar_mascota"),
    # Visitas
    path("visitas/<int:pk>/pagada/", views.marcar_pagada, name="pagada"),
    path("deudas/", views.deudas, name="deudas"),
    # API
    path("api/mascotas/<int:pk>/", views.api_mascota, name="api_mascota"),
]
