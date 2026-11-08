"""
Parte E: probar las consultas a mano.
Desde esta carpeta (la de manage.py):   python practica.py
"""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Los imports de los modelos, DESPUÉS de django.setup()
from libros import consultas  # noqa: E402
from libros.models import Autor, Libro  # noqa: E402

# Arrancar siempre igual: primero los libros (por el PROTECT), después los autores
Libro.objects.all().delete()
Autor.objects.all().delete()

borges = Autor.objects.create(nombre="Borges", pais="Argentina")
cortazar = Autor.objects.create(nombre="Cortázar", pais="Argentina")
quino = Autor.objects.create(nombre="Quino", pais="Argentina")
Libro.objects.bulk_create([
    Libro(titulo="Ficciones", autor=borges, precio=15000, stock=4, anio=1944),
    Libro(titulo="El Aleph", autor=borges, precio=14000, stock=0, anio=1949),
    Libro(titulo="Rayuela", autor=cortazar, precio=20000, stock=3, anio=1963),
    Libro(titulo="Bestiario", autor=cortazar, precio=12000, stock=5, anio=1951),
    Libro(titulo="Toda Mafalda", autor=quino, precio=35000, stock=2, anio=1993),
])

print("Todos:", list(Libro.objects.all()))
print("Sin stock:", list(consultas.sin_stock()))
print("Más baratos que 16000:", list(consultas.mas_baratos_que(16000)))
print("Buscar 'al':", list(consultas.buscar("al")))
print("De Cortázar:", list(consultas.de_autor("Cortázar")))

ficciones = Libro.objects.get(titulo="Ficciones")
ficciones.vender(2)
print("Vendí 2 de Ficciones, quedan", ficciones.stock)
try:
    ficciones.vender(100)
except ValueError as error:
    print("No se pudo vender:", error)

print("Subí el 10% a", consultas.subir_precios(cortazar, 10), "libros de Cortázar")
print("Pasaron a no disponibles:", consultas.marcar_no_disponibles_sin_stock())
for autor in consultas.resumen_por_autor():
    print(f"  {autor.nombre}: {autor.cantidad} libros, {autor.stock_total or 0} en stock")
print("Precio promedio:", round(consultas.precio_promedio(), 2))
print("Borrados (no disponibles):", consultas.borrar_no_disponibles())
