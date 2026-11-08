"""
Prueba automática del PASO 5.

Copiá este archivo adentro de tu carpeta "libros" y, desde la carpeta de manage.py:

    python manage.py test libros.test_paso5
"""

import csv
import io
import os
import shutil
import tempfile

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import NoReverseMatch, reverse

from libros.models import Autor, Libro

CARPETA = tempfile.mkdtemp()


def url(nombre, *args):
    try:
        return reverse(f"libros:{nombre}", args=args)
    except NoReverseMatch:
        raise AssertionError(f"No encontré la dirección con name='{nombre}'") from None


def mensajes(respuesta):
    return [str(m) for m in respuesta.context["messages"]] if respuesta.context else []


def imagen(nombre="tapa.png", lado=40, color="red"):
    from PIL import Image
    buffer = io.BytesIO()
    Image.new("RGB", (lado, lado), color).save(buffer, "PNG")
    return SimpleUploadedFile(nombre, buffer.getvalue(), content_type="image/png")


def imagen_grande():
    from PIL import Image
    buffer = io.BytesIO()
    Image.frombytes("RGB", (1000, 1000), os.urandom(1000 * 1000 * 3)).save(buffer, "PNG")
    return SimpleUploadedFile("grande.png", buffer.getvalue(), content_type="image/png")


def archivos(subcarpeta="portadas"):
    carpeta = os.path.join(CARPETA, subcarpeta)
    return sorted(os.listdir(carpeta)) if os.path.isdir(carpeta) else []


@override_settings(MEDIA_ROOT=CARPETA)
class Paso5(TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(CARPETA, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        shutil.rmtree(CARPETA, ignore_errors=True)
        self.client.force_login(User.objects.create_superuser("prueba", "p@x.com", None))
        self.borges = Autor.objects.create(nombre="Borges")
        self.ficciones = Libro.objects.create(titulo="Ficciones", autor=self.borges, precio=15000, stock=4, anio=1944)

    def datos(self, **cambios):
        datos = {"titulo": "Ficciones", "autor": self.borges.pk, "precio": "15000", "stock": 4, "anio": 1944,
                 "disponible": "on"}
        datos.update(cambios)
        return datos

    def test_01_configuracion(self):
        """1. MEDIA_URL y MEDIA_ROOT"""
        self.assertEqual(settings.MEDIA_URL, "/media/")

    def test_02_campos(self):
        """2. Libro.portada y Autor.foto: imágenes opcionales"""
        for modelo, campo, carpeta in ((Libro, "portada", "portadas/"), (Autor, "foto", "autores/")):
            try:
                field = modelo._meta.get_field(campo)
            except Exception:
                self.fail(f"Falta el campo {modelo.__name__}.{campo}")
            self.assertEqual(field.__class__.__name__, "ImageField", f"{campo} tiene que ser ImageField")
            self.assertTrue(field.blank, f"{campo} tiene que ser opcional")
            self.assertEqual(field.upload_to, carpeta)

    def test_03_subir_portada(self):
        """3 y 5. Subir la portada al crear, y verla en el detalle y en la lista"""
        respuesta = self.client.post(url("crear"), self.datos(titulo="Bestiario", portada=imagen("bestiario.png")))
        bestiario = Libro.objects.get(titulo="Bestiario")
        self.assertRedirects(respuesta, url("detalle", bestiario.pk))
        self.assertTrue(bestiario.portada, "la portada no se guardó (¿enctype en el form? ¿request.FILES en la vista?)")
        self.assertTrue(bestiario.portada.name.startswith("portadas/"))
        self.assertContains(self.client.get(url("detalle", bestiario.pk)), bestiario.portada.url)
        self.assertContains(self.client.get(url("lista")), bestiario.portada.url)

    def test_04_foto_del_autor(self):
        """3 y 5. Subir la foto del autor y verla en su detalle"""
        respuesta = self.client.post(url("crear_autor"), {"nombre": "Quino", "foto": imagen("quino.png")})
        quino = Autor.objects.get(nombre="Quino")
        self.assertRedirects(respuesta, url("autor", quino.pk))
        self.assertTrue(quino.foto)
        self.assertContains(self.client.get(url("autor", quino.pk)), quino.foto.url)

    def test_05_validaciones(self):
        """4. Ni más de 2 MB ni algo que no sea imagen"""
        respuesta = self.client.post(url("editar", self.ficciones.pk), self.datos(portada=imagen_grande()))
        self.assertContains(respuesta, "La imagen no puede pesar más de 2 MB.")
        trucha = SimpleUploadedFile("virus.png", b"no soy una imagen", content_type="image/png")
        self.client.post(url("editar", self.ficciones.pk), self.datos(portada=trucha))
        self.ficciones.refresh_from_db()
        self.assertFalse(self.ficciones.portada, "no se tiene que haber guardado ninguna")

    def test_06_cambiar_borra_la_vieja(self):
        """6. Al cambiar la portada, el archivo viejo se borra"""
        self.client.post(url("editar", self.ficciones.pk), self.datos(portada=imagen("vieja.png")))
        self.assertEqual(archivos(), ["vieja.png"])
        self.client.post(url("editar", self.ficciones.pk), self.datos(portada=imagen("nueva.png", color="blue")))
        self.assertEqual(archivos(), ["nueva.png"], "el archivo viejo tiene que borrarse del disco")

    def test_07_borrar_el_libro_borra_la_portada(self):
        """6. Al borrar el libro, se borra su portada"""
        self.client.post(url("editar", self.ficciones.pk), self.datos(portada=imagen("tapa.png")))
        self.assertEqual(archivos(), ["tapa.png"])
        self.client.post(url("borrar", self.ficciones.pk))
        self.assertFalse(Libro.objects.filter(pk=self.ficciones.pk).exists())
        self.assertEqual(archivos(), [], "la portada tiene que borrarse junto con el libro")

    def test_08_exportar(self):
        """7. Bajar la planilla: libros.csv con titulo;autor;precio;stock"""
        Libro.objects.create(titulo="El Aleph", autor=self.borges, precio=14000, stock=0, anio=1949)
        self.client.logout()                       # cualquiera puede bajarla
        respuesta = self.client.get(url("exportar"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("text/csv", respuesta["Content-Type"])
        self.assertIn("attachment", respuesta.get("Content-Disposition", ""))
        self.assertIn('filename="libros.csv"', respuesta["Content-Disposition"])
        filas = list(csv.reader(io.StringIO(respuesta.content.decode("utf-8-sig")), delimiter=";"))
        self.assertEqual(filas[0], ["titulo", "autor", "precio", "stock"])
        self.assertEqual([f[0] for f in filas[1:]], ["El Aleph", "Ficciones"])
        self.assertEqual(filas[2][1:], ["Borges", "15000.00", "4"])
        self.assertContains(self.client.get(url("lista")), url("exportar"), msg_prefix="falta el link en la lista")

    def test_09_importar(self):
        """8. Importar: crea autores si faltan, saltea filas malas, mensajes"""
        self.assertEqual(self.client.get(url("importar")).status_code, 200)
        planilla = ("titulo;autor;precio;stock;anio\n"
                    "Rayuela;Cortázar;20000;3;1963\n"
                    "El Aleph;Borges;14000;0;1949\n"
                    "Mal;Quino;caro;1;1966\n"
                    "Mafalda 1;Quino;8000;10;1966\n").encode("utf-8")
        respuesta = self.client.post(url("importar"),
                                     {"archivo": SimpleUploadedFile("libros.csv", planilla, "text/csv")}, follow=True)
        self.assertRedirects(respuesta, url("lista"))
        self.assertIn("Se importaron 3 libros.", mensajes(respuesta))
        self.assertTrue(any("4" in m and m != "Se importaron 3 libros." for m in mensajes(respuesta)),
                        f"tiene que avisar que la fila 4 tuvo errores; mensajes: {mensajes(respuesta)}")
        self.assertEqual(Autor.objects.filter(nombre="Borges").count(), 1, "Borges ya existía: no se repite")
        self.assertTrue(Autor.objects.filter(nombre="Cortázar").exists())
        self.assertEqual(Libro.objects.get(titulo="Rayuela").autor.nombre, "Cortázar")
        self.assertFalse(Libro.objects.filter(titulo="Mal").exists())
        self.assertContains(self.client.get(url("lista")), url("importar"), msg_prefix="falta el link en la lista")

    def test_10_importar_algo_que_no_es_csv(self):
        """8. Si no es un CSV de texto: error y no importa nada"""
        respuesta = self.client.post(url("importar"), {"archivo": imagen("foto.png")}, follow=True)
        self.assertIn("El archivo no es una planilla CSV.", mensajes(respuesta))
        self.assertEqual(Libro.objects.count(), 1)

    def test_11_importar_pide_sesion(self):
        """8. Importar pide sesión"""
        self.client.logout()
        self.assertRedirects(self.client.get(url("importar")), f"{reverse('login')}?next={url('importar')}",
                             fetch_redirect_response=False)
