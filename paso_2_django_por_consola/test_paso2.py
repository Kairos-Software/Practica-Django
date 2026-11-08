"""
Prueba automática del PASO 2.

Copiá este archivo adentro de tu carpeta "libros" (al lado de models.py) y,
desde la carpeta de manage.py:

    python manage.py test libros.test_paso2
"""

from datetime import date
from decimal import Decimal

from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.test import TestCase

from libros.models import Autor, Libro

try:
    from libros import consultas
except ImportError:
    consultas = None


def funcion(nombre):
    if consultas is None:
        raise AssertionError("Falta el archivo libros/consultas.py")
    if not hasattr(consultas, nombre):
        raise AssertionError(f"Falta la función {nombre}() en libros/consultas.py")
    return getattr(consultas, nombre)


def datos():
    borges = Autor.objects.create(nombre="Borges", pais="Argentina")
    cortazar = Autor.objects.create(nombre="Cortázar")
    quino = Autor.objects.create(nombre="Quino")
    Libro.objects.create(titulo="Ficciones", autor=borges, precio=Decimal("15000"), stock=4, anio=1944)
    Libro.objects.create(titulo="El Aleph", autor=borges, precio=Decimal("14000"), stock=0, anio=1949)
    Libro.objects.create(titulo="Rayuela", autor=cortazar, precio=Decimal("20000"), stock=3, anio=1963)
    Libro.objects.create(titulo="Bestiario", autor=cortazar, precio=Decimal("12000"), stock=5, anio=1951)
    return borges, cortazar, quino


class A_Proyecto(TestCase):

    def test_app_idioma_y_hora(self):
        """A. La app 'libros' está registrada, en castellano y con hora de Buenos Aires"""
        self.assertTrue(any(app == "libros" or app.startswith("libros.") for app in settings.INSTALLED_APPS))
        self.assertEqual(settings.LANGUAGE_CODE, "es-ar")
        self.assertEqual(settings.TIME_ZONE, "America/Argentina/Buenos_Aires")


class B_Modelos(TestCase):

    def test_autor(self):
        """B3. Autor: campos, sin repetir el nombre, se muestra y ordena por nombre"""
        Autor.objects.create(nombre="Quino")
        Autor.objects.create(nombre="Borges", pais="Argentina", nacimiento=date(1899, 8, 24))
        Autor.objects.create(nombre="Cortázar")      # pais y nacimiento son opcionales
        self.assertEqual([str(a) for a in Autor.objects.all()], ["Borges", "Cortázar", "Quino"])
        with self.assertRaises(Exception, msg="el nombre del autor no se tiene que poder repetir"):
            Autor.objects.create(nombre="Borges")

    def test_libro(self):
        """B4. Libro: campos, valores por defecto, cómo se muestra y su orden"""
        borges = Autor.objects.create(nombre="Borges")
        libro = Libro.objects.create(titulo="Ficciones", autor=borges, precio=Decimal("15000.50"), anio=1944)
        Libro.objects.create(titulo="El Aleph", autor=borges, precio=1, anio=1949)
        libro.refresh_from_db()
        self.assertEqual((libro.stock, libro.disponible), (0, True), "stock por defecto 0 y disponible por defecto sí")
        self.assertEqual(libro.precio, Decimal("15000.50"))
        self.assertIsNotNone(libro.cargado, "'cargado' se tiene que poner solo")
        self.assertEqual(str(libro), "Ficciones — Borges")
        self.assertEqual([l.titulo for l in Libro.objects.all()], ["El Aleph", "Ficciones"])
        self.assertEqual([l.titulo for l in borges.libros.all()], ["El Aleph", "Ficciones"],
                         "related_name: los libros de un autor se piden con autor.libros")

    def test_no_se_borra_un_autor_con_libros(self):
        """B4. on_delete=PROTECT: no se puede borrar un autor con libros"""
        borges = Autor.objects.create(nombre="Borges")
        Libro.objects.create(titulo="Ficciones", autor=borges, precio=1, anio=1944)
        with self.assertRaises(ProtectedError):
            borges.delete()

    def test_hay_stock(self):
        """B5. hay_stock()"""
        self.assertTrue(Libro(stock=2).hay_stock())
        self.assertFalse(Libro(stock=0).hay_stock())

    def test_vender(self):
        """B5. vender(): resta y guarda; si no alcanza o la cantidad es mala, ValueError sin cambiar nada"""
        borges = Autor.objects.create(nombre="Borges")
        libro = Libro.objects.create(titulo="Ficciones", autor=borges, precio=1, anio=1944, stock=5)
        libro.vender(2)
        libro.refresh_from_db()
        self.assertEqual(libro.stock, 3, "vender() tiene que GUARDAR el nuevo stock")
        for mala in (10, 0, -1):
            with self.assertRaises(ValueError, msg=f"vender({mala}) tiene que dar ValueError"):
                libro.vender(mala)
        libro.refresh_from_db()
        self.assertEqual(libro.stock, 3)

    def test_validacion_del_anio(self):
        """B5. clean(): el año no puede ser en el futuro"""
        borges = Autor.objects.create(nombre="Borges")
        futuro = Libro(titulo="X", autor=borges, precio=1, anio=date.today().year + 1)
        with self.assertRaises(ValidationError):
            futuro.full_clean()
        Libro(titulo="Y", autor=borges, precio=1, anio=date.today().year).full_clean()   # este año sí


class C_Admin(TestCase):

    def test_admin(self):
        """C7. Admin: los dos modelos, con columnas, filtros y buscador"""
        self.assertIn(Autor, admin.site._registry, "Falta registrar Autor en libros/admin.py")
        self.assertIn(Libro, admin.site._registry, "Falta registrar Libro en libros/admin.py")
        libro_admin = admin.site._registry[Libro]
        for campo in ("titulo", "autor", "precio", "stock", "disponible"):
            self.assertIn(campo, libro_admin.list_display, f"falta '{campo}' en list_display")
        for campo in ("autor", "disponible"):
            self.assertIn(campo, libro_admin.list_filter, f"falta '{campo}' en list_filter")
        self.assertIn("titulo", libro_admin.search_fields)


class D_Consultas(TestCase):

    def setUp(self):
        self.borges, self.cortazar, self.quino = datos()

    def titulos(self, libros):
        return [l.titulo for l in libros]

    def test_sin_stock(self):
        """D9. sin_stock()"""
        self.assertEqual(self.titulos(funcion("sin_stock")()), ["El Aleph"])

    def test_mas_baratos_que(self):
        """D10. mas_baratos_que()"""
        self.assertEqual(self.titulos(funcion("mas_baratos_que")(15000)), ["Bestiario", "El Aleph"])

    def test_buscar(self):
        """D11. buscar()"""
        self.assertEqual(self.titulos(funcion("buscar")("AL")), ["El Aleph"])
        self.assertEqual(self.titulos(funcion("buscar")("ray")), ["Rayuela"])

    def test_de_autor(self):
        """D12. de_autor(): en UNA consulta"""
        with self.assertNumQueries(1, msg="de_autor tiene que hacer una sola consulta (autor__nombre=...)"):
            self.assertEqual(self.titulos(funcion("de_autor")("Cortázar")), ["Bestiario", "Rayuela"])

    def test_subir_precios(self):
        """D13. subir_precios(): una sola consulta, devuelve cuántos"""
        with self.assertNumQueries(1, msg="subir_precios tiene que ser UNA consulta (update con F)"):
            cuantos = funcion("subir_precios")(self.cortazar, 10)
        self.assertEqual(cuantos, 2)
        self.assertEqual(sorted(round(l.precio) for l in self.cortazar.libros.all()), [13200, 22000])
        self.assertEqual(Libro.objects.get(titulo="Ficciones").precio, 15000, "los de otros autores no cambian")

    def test_marcar_no_disponibles_sin_stock(self):
        """D14. marcar_no_disponibles_sin_stock()"""
        with self.assertNumQueries(1):
            self.assertEqual(funcion("marcar_no_disponibles_sin_stock")(), 1)
        self.assertFalse(Libro.objects.get(titulo="El Aleph").disponible)
        self.assertTrue(Libro.objects.get(titulo="Ficciones").disponible)

    def test_resumen_por_autor(self):
        """D15. resumen_por_autor(): cantidad y stock_total calculados por la base"""
        with self.assertNumQueries(1, msg="tiene que ser UNA consulta (annotate)"):
            resumen = {a.nombre: (a.cantidad, a.stock_total) for a in funcion("resumen_por_autor")()}
        self.assertEqual(resumen["Borges"], (2, 4))
        self.assertEqual(resumen["Cortázar"], (2, 8))
        self.assertEqual(resumen["Quino"][0], 0)
        self.assertIn(resumen["Quino"][1], (0, None))

    def test_precio_promedio(self):
        """D16. precio_promedio()"""
        self.assertEqual(round(funcion("precio_promedio")()), 15250)
        Libro.objects.all().delete()
        self.assertIsNone(funcion("precio_promedio")())

    def test_borrar_no_disponibles(self):
        """D17. borrar_no_disponibles()"""
        Libro.objects.filter(titulo__in=["El Aleph", "Rayuela"]).update(disponible=False)
        self.assertEqual(funcion("borrar_no_disponibles")(), 2)
        self.assertEqual(Libro.objects.count(), 2)
