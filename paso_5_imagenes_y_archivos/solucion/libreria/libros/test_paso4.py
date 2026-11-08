"""
Prueba automática del PASO 4.

Copiá este archivo adentro de tu carpeta "libros" y, desde la carpeta de manage.py:

    python manage.py test libros.test_paso4
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import NoReverseMatch, resolve, reverse

from libros.models import Autor, Libro

try:
    from libros.models import Resenia
except ImportError:
    Resenia = None


def url(nombre, *args):
    try:
        return reverse(nombre, args=args)
    except NoReverseMatch:
        raise AssertionError(f"No encontré la dirección con name='{nombre}'") from None


def mensajes(respuesta):
    return [str(m) for m in respuesta.context["messages"]] if respuesta.context else []


class Paso4(TestCase):

    def setUp(self):
        if Resenia is None:
            self.fail("Falta el modelo Resenia en libros/models.py")
        # Sin contraseña real (None): más rápido. Para "iniciar sesión" se usa force_login.
        self.ana = User.objects.create_user("ana", password=None)
        self.beto = User.objects.create_user("beto", password=None)
        self.borges = Autor.objects.create(nombre="Borges")
        self.ficciones = Libro.objects.create(titulo="Ficciones", autor=self.borges, precio=15000, stock=4, anio=1944)

    # ── Login y registro ──
    def test_01_configuracion(self):
        """2. LOGIN_URL, y después de entrar y salir, a la lista"""
        self.assertEqual(reverse(settings.LOGIN_URL) if not settings.LOGIN_URL.startswith("/") else settings.LOGIN_URL,
                         url("login"))
        for nombre in ("LOGIN_REDIRECT_URL", "LOGOUT_REDIRECT_URL"):
            valor = getattr(settings, nombre)
            self.assertEqual(valor if str(valor).startswith("/") else reverse(valor), url("libros:lista"), nombre)

    def test_02_login_y_logout(self):
        """1. Login y logout en cuentas/"""
        self.assertEqual(url("login"), "/cuentas/login/")
        self.assertEqual(url("logout"), "/cuentas/logout/")
        self.assertEqual(self.client.get(url("login")).status_code, 200, "falta el template registration/login.html")
        User.objects.create_user("carla", password="una-clave-larga-123")
        respuesta = self.client.post(url("login"), {"username": "carla", "password": "una-clave-larga-123"})
        self.assertRedirects(respuesta, url("libros:lista"))
        respuesta = self.client.post(url("logout"))
        self.assertRedirects(respuesta, url("libros:lista"))

    def test_03_registro(self):
        """3. Registro: crea el usuario, inicia la sesión y va a la lista"""
        self.assertEqual(url("registro"), "/cuentas/registro/")
        respuesta = self.client.post(url("registro"), {"username": "dani", "password1": "otra-clave-larga-789",
                                                       "password2": "otra-clave-larga-789"})
        self.assertRedirects(respuesta, url("libros:lista"))
        self.assertTrue(User.objects.filter(username="dani").exists())
        self.assertEqual(self.client.get(url("libros:lista")).context["user"].username, "dani",
                         "después de registrarse tiene que quedar con la sesión iniciada")

    def test_04_menu(self):
        """4. Menú: 'Hola, usuario' y Salir, o Entrar y Registrarme"""
        sin_sesion = self.client.get(url("libros:lista"))
        self.assertContains(sin_sesion, url("login"))
        self.assertContains(sin_sesion, url("registro"))
        self.client.force_login(self.ana)
        con_sesion = self.client.get(url("libros:lista"))
        self.assertContains(con_sesion, "Hola, ana")
        self.assertContains(con_sesion, url("logout"))

    # ── Quién puede qué ──
    def test_05_mirar_es_libre(self):
        """5. Mirar no necesita sesión"""
        for direccion in (url("libros:lista"), url("libros:detalle", self.ficciones.pk), url("libros:autores"),
                          url("libros:autor", self.borges.pk)):
            self.assertEqual(self.client.get(direccion).status_code, 200, direccion)

    def test_06_cambiar_pide_sesion(self):
        """6. Crear, editar, borrar, vender y crear autor piden sesión (y vuelven a donde ibas)"""
        pk = self.ficciones.pk
        for direccion, metodo in ((url("libros:crear"), "get"), (url("libros:editar", pk), "get"),
                                  (url("libros:borrar", pk), "get"), (url("libros:vender", pk), "post"),
                                  (url("libros:crear_autor"), "get")):
            respuesta = getattr(self.client, metodo)(direccion)
            self.assertRedirects(respuesta, f"{url('login')}?next={direccion}", fetch_redirect_response=False,
                                 msg_prefix=f"{direccion} sin sesión")
        self.ficciones.refresh_from_db()
        self.assertEqual(self.ficciones.stock, 4, "sin sesión no se tiene que poder vender")

    # ── Reseñas ──
    def test_07_modelo_resenia(self):
        """7. Resenia: campos, related_name, orden y una sola por usuario y libro"""
        primera = Resenia.objects.create(usuario=self.ana, libro=self.ficciones, puntaje=5, texto="Genial")
        segunda = Resenia.objects.create(usuario=self.beto, libro=self.ficciones, puntaje=3, texto="Meh")
        self.assertIsNotNone(primera.creada)
        self.assertEqual(list(self.ficciones.resenias.all()), [segunda, primera], "de la más nueva a la más vieja")
        self.assertEqual(list(self.ana.resenias.all()), [primera])
        with self.assertRaises(IntegrityError, msg="no se tienen que poder 2 reseñas del mismo usuario al mismo libro"):
            with transaction.atomic():
                Resenia.objects.create(usuario=self.ana, libro=self.ficciones, puntaje=1, texto="otra")

    def test_08_detalle_con_resenias(self):
        """8. Detalle: reseñas, promedio, y formulario o link según la sesión"""
        Resenia.objects.create(usuario=self.ana, libro=self.ficciones, puntaje=5, texto="Genial")
        Resenia.objects.create(usuario=self.beto, libro=self.ficciones, puntaje=2, texto="No me gustó")
        sin_sesion = self.client.get(url("libros:detalle", self.ficciones.pk))
        self.assertContains(sin_sesion, "No me gustó")
        html = sin_sesion.content.decode()
        self.assertTrue("3,5" in html or "3.5" in html, "falta el promedio (3,5)")
        self.assertContains(sin_sesion, "Entrá para opinar")
        self.assertNotContains(sin_sesion, url("libros:resenia", self.ficciones.pk))
        carla = User.objects.create_user("carla", password=None)
        self.client.force_login(carla)
        con_sesion = self.client.get(url("libros:detalle", self.ficciones.pk))
        self.assertContains(con_sesion, url("libros:resenia", self.ficciones.pk),
                            msg_prefix="con sesión y sin haber opinado tiene que estar el formulario")

    def test_09_guardar_resenia(self):
        """9. Guardar reseña: solo POST y con sesión, el usuario lo pone la vista"""
        direccion = url("libros:resenia", self.ficciones.pk)
        self.assertRedirects(self.client.post(direccion, {"puntaje": 5, "texto": "x"}),
                             f"{url('login')}?next={direccion}", fetch_redirect_response=False)
        self.client.force_login(self.ana)
        self.assertEqual(self.client.get(direccion).status_code, 405)
        respuesta = self.client.post(direccion, {"puntaje": 4, "texto": "Muy bueno", "usuario": self.beto.pk},
                                     follow=True)
        self.assertRedirects(respuesta, url("libros:detalle", self.ficciones.pk))
        self.assertIn("¡Gracias por tu reseña!", mensajes(respuesta))
        resenia = Resenia.objects.get()
        self.assertEqual((resenia.usuario, resenia.libro, resenia.puntaje), (self.ana, self.ficciones, 4),
                         "el usuario lo pone la vista (aunque manden otro en el formulario)")

    def test_10_resenia_repetida_y_puntaje_malo(self):
        """9. Ya opinaste / puntaje fuera de 1 a 5: no se guarda"""
        self.client.force_login(self.ana)
        direccion = url("libros:resenia", self.ficciones.pk)
        self.client.post(direccion, {"puntaje": 4, "texto": "Primera"})
        respuesta = self.client.post(direccion, {"puntaje": 1, "texto": "Segunda"}, follow=True)
        self.assertIn("Ya opinaste sobre este libro.", mensajes(respuesta))
        self.assertEqual(Resenia.objects.count(), 1)
        self.client.force_login(self.beto)
        for malo in (0, 6):
            self.client.post(direccion, {"puntaje": malo, "texto": "x"})
        self.assertEqual(Resenia.objects.count(), 1, "un puntaje fuera de 1 a 5 no se tiene que guardar")

    def test_11_borrar_resenia(self):
        """10. Borrar reseña: solo POST, solo la propia (la de otro: 404)"""
        de_ana = Resenia.objects.create(usuario=self.ana, libro=self.ficciones, puntaje=5, texto="Genial")
        direccion = url("libros:borrar_resenia", de_ana.pk)
        self.client.force_login(self.beto)
        self.assertEqual(self.client.post(direccion).status_code, 404, "Beto no puede borrar la reseña de Ana")
        self.client.force_login(self.ana)
        self.assertEqual(self.client.get(direccion).status_code, 405)
        self.assertRedirects(self.client.post(direccion), url("libros:detalle", self.ficciones.pk))
        self.assertFalse(Resenia.objects.exists())

    def test_12_mis_resenias(self):
        """11. Mis reseñas: solo las mías, con sesión, con una ListView"""
        direccion = url("libros:mis_resenias")
        self.assertRedirects(self.client.get(direccion), f"{url('login')}?next={direccion}",
                             fetch_redirect_response=False)
        aleph = Libro.objects.create(titulo="El Aleph", autor=self.borges, precio=1, anio=1949)
        Resenia.objects.create(usuario=self.ana, libro=self.ficciones, puntaje=5, texto="Genial")
        Resenia.objects.create(usuario=self.beto, libro=aleph, puntaje=1, texto="Lo de Beto")
        self.client.force_login(self.ana)
        respuesta = self.client.get(direccion)
        self.assertContains(respuesta, "Genial")
        self.assertContains(respuesta, url("libros:detalle", self.ficciones.pk))
        self.assertNotContains(respuesta, "Lo de Beto")
        from django.views.generic import ListView
        vista = getattr(resolve(direccion).func, "view_class", None)
        self.assertTrue(vista and issubclass(vista, ListView), "mis_resenias tiene que ser una vista de clase ListView")

    def test_13_admin(self):
        """12. Resenia en el admin"""
        self.assertIn(Resenia, admin.site._registry)
