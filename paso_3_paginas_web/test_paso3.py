"""
Prueba automática del PASO 3.

Copiá este archivo adentro de tu carpeta "libros" y, desde la carpeta de manage.py:

    python manage.py test libros.test_paso3
"""


from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import NoReverseMatch, reverse

from libros.models import Autor, Libro


def url(nombre, *args):
    try:
        return reverse(f"libros:{nombre}", args=args)
    except NoReverseMatch:
        raise AssertionError(f"No encontré la dirección con name='{nombre}' (¿app_name = 'libros' en libros/urls.py "
                             f"y el include en config/urls.py?)") from None


def mensajes(respuesta):
    return [str(m) for m in respuesta.context["messages"]] if respuesta.context else []


class Paso3(TestCase):

    def setUp(self):
        # Se inicia sesión con un administrador: así la prueba sigue andando en el paso 4 (que pide login)
        self.client.force_login(User.objects.create_superuser("prueba", "prueba@x.com", None))
        self.borges = Autor.objects.create(nombre="Borges")
        self.cortazar = Autor.objects.create(nombre="Cortázar")
        self.ficciones = Libro.objects.create(titulo="Ficciones", autor=self.borges, precio=15000, stock=4, anio=1944)
        self.aleph = Libro.objects.create(titulo="El Aleph", autor=self.borges, precio=14000, stock=0, anio=1949)
        self.rayuela = Libro.objects.create(titulo="Rayuela", autor=self.cortazar, precio=20000, stock=3, anio=1963)

    def datos_de_libro(self, **cambios):
        datos = {"titulo": "Bestiario", "autor": self.cortazar.pk, "precio": "12000", "stock": 5, "anio": 1951,
                 "disponible": "on"}
        datos.update(cambios)
        return datos

    # ── Lista ──
    def test_01_lista(self):
        """1. La lista muestra los libros, con link al detalle, y 'Sin stock' cuando no hay"""
        respuesta = self.client.get(url("lista"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Ficciones")
        self.assertContains(respuesta, "Borges")
        self.assertContains(respuesta, url("detalle", self.ficciones.pk))
        self.assertContains(respuesta, "Sin stock")

    def test_02_base_y_menu(self):
        """2. Template base con menú: links a la lista, autores, crear libro y crear autor"""
        respuesta = self.client.get(url("lista"))
        for nombre in ("lista", "autores", "crear", "crear_autor"):
            self.assertContains(respuesta, f'href="{url(nombre)}"', msg_prefix=f"falta el link a '{nombre}' en el menú")

    def test_03_buscar_y_filtrar(self):
        """3. Buscador (q) y filtro por autor (autor), juntos, y el texto sigue escrito"""
        respuesta = self.client.get(url("lista"), {"q": "ray"})
        self.assertContains(respuesta, "Rayuela")
        self.assertNotContains(respuesta, "Ficciones")
        self.assertContains(respuesta, 'value="ray"', msg_prefix="después de buscar, el texto tiene que seguir en el buscador")
        respuesta = self.client.get(url("lista"), {"autor": self.borges.pk})
        self.assertContains(respuesta, "Ficciones")
        self.assertNotContains(respuesta, "Rayuela")
        respuesta = self.client.get(url("lista"), {"autor": self.borges.pk, "q": "aleph"})
        self.assertContains(respuesta, "El Aleph")
        self.assertNotContains(respuesta, "Ficciones")

    def test_04_paginacion(self):
        """3. De a 10 por página (pagina=2) sin perder la búsqueda"""
        for n in range(1, 13):
            Libro.objects.create(titulo=f"Zeta {n:02d}", autor=self.borges, precio=1, anio=2000)
        primera = self.client.get(url("lista"), {"q": "zeta"})
        self.assertContains(primera, "Zeta 01")
        self.assertNotContains(primera, "Zeta 11", msg_prefix="tiene que mostrar de a 10")
        segunda = self.client.get(url("lista"), {"q": "zeta", "pagina": 2})
        self.assertContains(segunda, "Zeta 11")
        self.assertNotContains(segunda, "Zeta 01")
        self.assertContains(primera, "pagina=2", msg_prefix="falta el link a la página siguiente")
        self.assertContains(primera, "q=zeta", msg_prefix="el link de la página tiene que llevar la búsqueda")

    # ── Detalle ──
    def test_05_detalle(self):
        """6. Detalle: datos, links a editar y borrar; 404 si no existe"""
        respuesta = self.client.get(url("detalle", self.ficciones.pk))
        self.assertContains(respuesta, "Ficciones")
        self.assertContains(respuesta, "1944")
        self.assertContains(respuesta, url("editar", self.ficciones.pk))
        self.assertContains(respuesta, url("borrar", self.ficciones.pk))
        self.assertContains(respuesta, url("vender", self.ficciones.pk), msg_prefix="falta el formulario de vender")
        self.assertEqual(self.client.get(url("detalle", 9999)).status_code, 404)

    # ── Crear y editar ──
    def test_06_crear(self):
        """7. Crear: guarda, va al detalle con 'Se guardó «título».'"""
        respuesta = self.client.post(url("crear"), self.datos_de_libro(), follow=True)
        nuevo = Libro.objects.get(titulo="Bestiario")
        self.assertRedirects(respuesta, url("detalle", nuevo.pk))
        self.assertIn("Se guardó «Bestiario».", mensajes(respuesta))

    def test_07_crear_con_errores(self):
        """7. Datos mal: vuelve a mostrar el formulario con los errores y no guarda"""
        respuesta = self.client.post(url("crear"), self.datos_de_libro(titulo="", anio="abc"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(Libro.objects.filter(titulo="Bestiario").exists())
        respuesta = self.client.post(url("crear"), self.datos_de_libro(precio="0"))
        self.assertContains(respuesta, "mayor a 0")
        self.assertFalse(Libro.objects.filter(titulo="Bestiario").exists())

    def test_08_editar(self):
        """7. Editar: el formulario trae los datos, guarda y va al detalle"""
        respuesta = self.client.get(url("editar", self.ficciones.pk))
        self.assertContains(respuesta, 'value="Ficciones"', msg_prefix="el formulario de editar tiene que traer los datos")
        respuesta = self.client.post(url("editar", self.ficciones.pk),
                                     self.datos_de_libro(titulo="Ficciones (edición nueva)", autor=self.borges.pk),
                                     follow=True)
        self.assertRedirects(respuesta, url("detalle", self.ficciones.pk))
        self.ficciones.refresh_from_db()
        self.assertEqual(self.ficciones.titulo, "Ficciones (edición nueva)")
        self.assertIn("Se guardó «Ficciones (edición nueva)».", mensajes(respuesta))

    # ── Borrar ──
    def test_09_borrar(self):
        """8. Borrar: GET pregunta (no borra), POST borra y va a la lista con 'Se borró «título».'"""
        respuesta = self.client.get(url("borrar", self.aleph.pk))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "El Aleph")
        self.assertTrue(Libro.objects.filter(pk=self.aleph.pk).exists(), "¡con GET no se tiene que borrar!")
        respuesta = self.client.post(url("borrar", self.aleph.pk), follow=True)
        self.assertRedirects(respuesta, url("lista"))
        self.assertFalse(Libro.objects.filter(pk=self.aleph.pk).exists())
        self.assertIn("Se borró «El Aleph».", mensajes(respuesta))

    # ── Vender ──
    def test_10_vender(self):
        """9. Vender: solo POST, usa vender(), vuelve al detalle con mensaje"""
        self.assertEqual(self.client.get(url("vender", self.ficciones.pk)).status_code, 405, "con GET tiene que dar 405")
        respuesta = self.client.post(url("vender", self.ficciones.pk), {"cantidad": 3}, follow=True)
        self.assertRedirects(respuesta, url("detalle", self.ficciones.pk))
        self.ficciones.refresh_from_db()
        self.assertEqual(self.ficciones.stock, 1)
        self.assertIn("Se vendieron 3.", mensajes(respuesta))

    def test_11_vender_mas_de_lo_que_hay(self):
        """9. Vender de más: vuelve al detalle con el error, sin cambiar el stock"""
        respuesta = self.client.post(url("vender", self.ficciones.pk), {"cantidad": 50}, follow=True)
        self.assertRedirects(respuesta, url("detalle", self.ficciones.pk))
        self.assertTrue(any("No alcanza" in m for m in mensajes(respuesta)),
                        f"tiene que mostrar el error de vender(); los mensajes fueron: {mensajes(respuesta)}")
        self.ficciones.refresh_from_db()
        self.assertEqual(self.ficciones.stock, 4)

    # ── Autores ──
    def test_12_autores(self):
        """10. Autores: cada uno con cuántos libros tiene"""
        respuesta = self.client.get(url("autores"))
        self.assertContains(respuesta, "Borges")
        self.assertContains(respuesta, url("autor", self.borges.pk))
        self.assertContains(respuesta, "2 libros")
        self.assertContains(respuesta, "1 libro")

    def test_13_detalle_de_autor(self):
        """11. Detalle de autor: sus libros con link"""
        respuesta = self.client.get(url("autor", self.borges.pk))
        self.assertContains(respuesta, "Ficciones")
        self.assertContains(respuesta, url("detalle", self.ficciones.pk))
        self.assertNotContains(respuesta, "Rayuela")
        self.assertEqual(self.client.get(url("autor", 9999)).status_code, 404)

    def test_14_crear_autor(self):
        """12. Crear autor: guarda y va a su detalle"""
        respuesta = self.client.post(url("crear_autor"), {"nombre": "Quino", "pais": "Argentina"})
        quino = Autor.objects.get(nombre="Quino")
        self.assertRedirects(respuesta, url("autor", quino.pk))
