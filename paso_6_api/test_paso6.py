"""
Prueba automática del PASO 6.

Copiá este archivo adentro de tu carpeta "libros" y, desde la carpeta de manage.py:

    python manage.py test libros.test_paso6
"""

import io
import json
import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import NoReverseMatch, reverse

from libros.models import Autor, Libro, Resenia

CARPETA = tempfile.mkdtemp()
SIN_SESION = {"error": "Tenés que iniciar sesión."}
NO_EXISTE = {"error": "No existe ese libro."}


def url(nombre, *args):
    try:
        return reverse(f"libros:{nombre}", args=args)
    except NoReverseMatch:
        raise AssertionError(f"No encontré la dirección con name='{nombre}'") from None


@override_settings(MEDIA_ROOT=CARPETA)
class Paso6(TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(CARPETA, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.ana = User.objects.create_user("ana", password=None)
        self.beto = User.objects.create_user("beto", password=None)
        self.borges = Autor.objects.create(nombre="Borges")
        self.cortazar = Autor.objects.create(nombre="Cortázar")
        self.ficciones = Libro.objects.create(titulo="Ficciones", autor=self.borges, precio=15000, stock=4, anio=1944)
        self.aleph = Libro.objects.create(titulo="El Aleph", autor=self.borges, precio=14000, stock=0, anio=1949)
        self.rayuela = Libro.objects.create(titulo="Rayuela", autor=self.cortazar, precio=20000, stock=3, anio=1963)

    def post_json(self, direccion, datos):
        texto = datos if isinstance(datos, str) else json.dumps(datos)
        return self.client.post(direccion, texto, content_type="application/json")

    # ── 1. Lista ──
    def test_01_lista(self):
        """1. GET api_libros: formato, orden y precio como texto"""
        respuesta = self.client.get(url("api_libros"))
        self.assertEqual(respuesta.status_code, 200)
        datos = respuesta.json()
        self.assertEqual(datos["cantidad"], 3)
        self.assertEqual([l["titulo"] for l in datos["libros"]], ["El Aleph", "Ficciones", "Rayuela"])
        self.assertEqual(datos["libros"][1], {"id": self.ficciones.pk, "titulo": "Ficciones", "autor": "Borges",
                                              "precio": "15000.00", "stock": 4, "disponible": True})

    def test_02_lista_filtros(self):
        """1. GET api_libros con ?q= y ?autor= (también juntos)"""
        titulos = lambda **filtros: [l["titulo"] for l in self.client.get(url("api_libros"), filtros).json()["libros"]]
        self.assertEqual(titulos(q="RAY"), ["Rayuela"])
        self.assertEqual(titulos(autor=self.borges.pk), ["El Aleph", "Ficciones"])
        self.assertEqual(titulos(autor=self.borges.pk, q="fic"), ["Ficciones"])
        self.assertEqual(self.client.get(url("api_libros"), {"q": "nada"}).json(), {"cantidad": 0, "libros": []})

    def test_03_crear(self):
        """1. POST api_libros: con sesión, crea y responde 201 con el detalle"""
        self.client.force_login(self.ana)
        respuesta = self.post_json(url("api_libros"), {"titulo": "Bestiario", "autor": self.cortazar.pk,
                                                       "precio": "12000", "stock": 5, "anio": 1951})
        self.assertEqual(respuesta.status_code, 201)
        nuevo = Libro.objects.get(titulo="Bestiario")
        datos = respuesta.json()
        self.assertEqual(datos["id"], nuevo.pk)
        self.assertEqual(datos["autor"], {"id": self.cortazar.pk, "nombre": "Cortázar"})
        self.assertEqual(datos["resenias"], [])

    def test_04_crear_errores(self):
        """1. POST api_libros: 401 sin sesión, 400 con JSON roto o datos mal"""
        respuesta = self.post_json(url("api_libros"), {"titulo": "X"})
        self.assertEqual((respuesta.status_code, respuesta.json()), (401, SIN_SESION))
        self.client.force_login(self.ana)
        respuesta = self.post_json(url("api_libros"), "{esto no es json")
        self.assertEqual((respuesta.status_code, respuesta.json()), (400, {"error": "El JSON está mal escrito."}))
        respuesta = self.post_json(url("api_libros"), {"titulo": "", "autor": self.borges.pk, "precio": "0",
                                                       "stock": 1, "anio": 2000})
        self.assertEqual(respuesta.status_code, 400)
        errores = respuesta.json().get("errores", {})
        self.assertIn("titulo", errores)
        self.assertIn("precio", errores, "tiene que usar tu formulario (con la regla de precio mayor a 0)")
        self.assertEqual(Libro.objects.count(), 3)
        self.assertEqual(self.client.put(url("api_libros")).status_code, 405)

    # ── 2. Un libro ──
    def test_05_detalle(self):
        """2. GET api_libro: autor, portada, promedio y reseñas"""
        Resenia.objects.create(usuario=self.ana, libro=self.ficciones, puntaje=5, texto="Genial")
        Resenia.objects.create(usuario=self.beto, libro=self.ficciones, puntaje=4, texto="Muy bueno")
        from PIL import Image
        buffer = io.BytesIO()
        Image.new("RGB", (10, 10), "red").save(buffer, "PNG")
        self.ficciones.portada = SimpleUploadedFile("ficciones.png", buffer.getvalue(), content_type="image/png")
        self.ficciones.save()
        datos = self.client.get(url("api_libro", self.ficciones.pk)).json()
        self.assertEqual(datos["autor"], {"id": self.borges.pk, "nombre": "Borges"})
        self.assertEqual((datos["precio"], datos["stock"], datos["anio"], datos["disponible"]),
                         ("15000.00", 4, 1944, True))
        self.assertEqual(datos["portada"], self.ficciones.portada.url)
        self.assertEqual(datos["promedio"], 4.5)
        self.assertEqual(datos["resenias"], [{"usuario": "beto", "puntaje": 4, "texto": "Muy bueno"},
                                             {"usuario": "ana", "puntaje": 5, "texto": "Genial"}])
        sin_nada = self.client.get(url("api_libro", self.aleph.pk)).json()
        self.assertEqual((sin_nada["portada"], sin_nada["promedio"], sin_nada["resenias"]), (None, None, []))

    def test_06_no_existe(self):
        """2. 404 en JSON"""
        respuesta = self.client.get(url("api_libro", 9999))
        self.assertEqual((respuesta.status_code, respuesta.json()), (404, NO_EXISTE))

    def test_07_borrar(self):
        """2. DELETE api_libro: 401 sin sesión; con sesión 204 y se borra"""
        respuesta = self.client.delete(url("api_libro", self.aleph.pk))
        self.assertEqual((respuesta.status_code, respuesta.json()), (401, SIN_SESION))
        self.client.force_login(self.ana)
        respuesta = self.client.delete(url("api_libro", self.aleph.pk))
        self.assertEqual(respuesta.status_code, 204)
        self.assertFalse(Libro.objects.filter(pk=self.aleph.pk).exists())
        self.assertEqual(self.client.delete(url("api_libro", self.aleph.pk)).status_code, 404)

    # ── 3. Vender ──
    def test_08_vender(self):
        """3. POST api_vender: 200 con el stock que quedó"""
        self.client.force_login(self.ana)
        respuesta = self.post_json(url("api_vender", self.ficciones.pk), {"cantidad": 3})
        self.assertEqual((respuesta.status_code, respuesta.json()), (200, {"stock": 1}))
        self.ficciones.refresh_from_db()
        self.assertEqual(self.ficciones.stock, 1)

    def test_09_vender_errores(self):
        """3. api_vender: 405, 401, 400 (no alcanza / cantidad mala), 404"""
        direccion = url("api_vender", self.ficciones.pk)
        self.assertEqual(self.client.get(direccion).status_code, 405)
        respuesta = self.post_json(direccion, {"cantidad": 1})
        self.assertEqual((respuesta.status_code, respuesta.json()), (401, SIN_SESION))
        self.client.force_login(self.ana)
        respuesta = self.post_json(direccion, {"cantidad": 50})
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn("No alcanza", respuesta.json().get("error", ""))
        for mala in ({"cantidad": "dos"}, {}, {"cantidad": 1.5}):
            respuesta = self.post_json(direccion, mala)
            self.assertEqual((respuesta.status_code, respuesta.json()),
                             (400, {"error": "La cantidad tiene que ser un número entero."}), mala)
        respuesta = self.post_json(direccion, {"cantidad": 0})
        self.assertEqual(respuesta.status_code, 400)
        self.ficciones.refresh_from_db()
        self.assertEqual(self.ficciones.stock, 4, "nada de lo anterior tenía que vender")
        respuesta = self.post_json(url("api_vender", 9999), {"cantidad": 1})
        self.assertEqual((respuesta.status_code, respuesta.json()), (404, NO_EXISTE))

    # ── 4. Buscador ──
    def test_10_buscador(self):
        """4. El buscador en vivo: el cuadro, la lista, el JavaScript y el link en el menú"""
        respuesta = self.client.get(url("buscador"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'id="buscar"')
        self.assertContains(respuesta, 'id="resultados"')
        self.assertContains(respuesta, "fetch(", msg_prefix="falta el JavaScript que le pide los datos a la API")
        self.assertContains(respuesta, url("api_libros"), msg_prefix="el JavaScript tiene que usar tu API")
        self.assertContains(self.client.get(url("lista")), f'href="{url("buscador")}"',
                            msg_prefix="falta el link 'Buscador' en el menú")
