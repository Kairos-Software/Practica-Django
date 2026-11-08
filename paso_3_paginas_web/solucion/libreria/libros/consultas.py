"""
Las consultas de la librería, con el ORM (nada de SQL a mano).
Son funciones comunes: se pueden usar desde un script, desde la consola
(python manage.py shell) y, en el paso 3, desde las páginas.
"""

from decimal import Decimal

from django.db.models import Avg, Count, F, Sum

from .models import Autor, Libro


def sin_stock():
    return Libro.objects.filter(stock=0).order_by("titulo")


def mas_baratos_que(precio):
    return Libro.objects.filter(precio__lt=precio).order_by("precio")


def buscar(texto):
    return Libro.objects.filter(titulo__icontains=texto).order_by("titulo")


def de_autor(nombre):
    # autor__nombre: Django hace el JOIN solo, en UNA consulta
    return Libro.objects.filter(autor__nombre=nombre).order_by("titulo")


def subir_precios(autor, porcentaje):
    # F("precio") = el precio que ya tiene cada uno; la cuenta la hace la base
    factor = 1 + Decimal(porcentaje) / 100
    return Libro.objects.filter(autor=autor).update(precio=F("precio") * factor)


def marcar_no_disponibles_sin_stock():
    return Libro.objects.filter(stock=0).update(disponible=False)


def resumen_por_autor():
    return Autor.objects.annotate(cantidad=Count("libros"), stock_total=Sum("libros__stock"))


def precio_promedio():
    return Libro.objects.aggregate(promedio=Avg("precio"))["promedio"]


def borrar_no_disponibles():
    borrados, _ = Libro.objects.filter(disponible=False).delete()
    return borrados
