from django.urls import path

from . import api, views

app_name = "libros"

urlpatterns = [
    # Libros
    path("", views.lista, name="lista"),
    path("libros/nuevo/", views.crear, name="crear"),
    path("libros/exportar/", views.exportar, name="exportar"),
    path("libros/importar/", views.importar, name="importar"),
    path("libros/<int:pk>/", views.detalle, name="detalle"),
    path("libros/<int:pk>/editar/", views.editar, name="editar"),
    path("libros/<int:pk>/borrar/", views.borrar, name="borrar"),
    path("libros/<int:pk>/vender/", views.vender, name="vender"),
    # Autores
    path("autores/", views.autores, name="autores"),
    path("autores/nuevo/", views.crear_autor, name="crear_autor"),
    path("autores/<int:pk>/", views.autor, name="autor"),
    # Reseñas
    path("libros/<int:pk>/resenia/", views.resenia, name="resenia"),
    path("resenias/<int:pk>/borrar/", views.borrar_resenia, name="borrar_resenia"),
    path("mis-resenias/", views.MisResenias.as_view(), name="mis_resenias"),
    # El buscador en vivo (una página que usa la API)
    path("buscador/", views.buscador, name="buscador"),
    # La API (JSON)
    path("api/libros/", api.libros, name="api_libros"),
    path("api/libros/<int:pk>/", api.libro, name="api_libro"),
    path("api/libros/<int:pk>/vender/", api.vender, name="api_vender"),
]
