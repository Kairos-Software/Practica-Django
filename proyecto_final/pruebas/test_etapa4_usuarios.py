"""
Prueba de la ETAPA 4 (usuarios).
Copiala a tu carpeta "clinica" y:   python manage.py test clinica.test_etapa4_usuarios
(Necesita que las direcciones de la etapa 5 existan en clinica/urls.py, aunque
las vistas todavía no hagan mucho.)
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import NoReverseMatch, reverse

from clinica.models import Duenio, Mascota, Visita


class Etapa4(TestCase):

    def setUp(self):
        self.lucia = Duenio.objects.create(nombre="Lucía Pérez", telefono="123")
        self.toby = Mascota.objects.create(nombre="Toby", especie="perro", duenio=self.lucia)
        self.visita = Visita.objects.create(mascota=self.toby, motivo="Control", costo=100)

    def test_login_y_logout_en_cuentas(self):
        """Login y logout de Django en cuentas/, con tu template de login"""
        self.assertEqual(reverse("login"), "/cuentas/login/")
        self.assertEqual(reverse("logout"), "/cuentas/logout/")
        self.assertEqual(self.client.get(reverse("login")).status_code, 200, "falta templates/registration/login.html")

    def test_no_hay_registro(self):
        """No hay página de registro"""
        with self.assertRaises(NoReverseMatch, msg="no tiene que existir una dirección 'registro'"):
            reverse("registro")

    def test_todo_pide_sesion(self):
        """Sin sesión, todas las páginas mandan al login (la API: login o 401)"""
        pk_d, pk_m, pk_v = self.lucia.pk, self.toby.pk, self.visita.pk
        paginas = [("inicio",), ("duenios",), ("duenio", pk_d), ("crear_duenio",), ("editar_duenio", pk_d),
                   ("borrar_duenio", pk_d), ("mascotas",), ("mascota", pk_m), ("crear_mascota",),
                   ("editar_mascota", pk_m), ("borrar_mascota", pk_m), ("deudas",)]
        for nombre, *args in paginas:
            direccion = reverse(f"clinica:{nombre}", args=args)
            respuesta = self.client.get(direccion)
            self.assertEqual(respuesta.status_code, 302, f"{direccion} sin sesión")
            self.assertTrue(respuesta["Location"].startswith(reverse("login")), f"{direccion} tiene que ir al login")
        respuesta = self.client.post(reverse("clinica:pagada", args=[pk_v]))
        self.assertIn(respuesta.status_code, (302, 401))
        self.visita.refresh_from_db()
        self.assertFalse(self.visita.pagada, "sin sesión no se puede marcar pagada")
        self.assertIn(self.client.get(reverse("clinica:api_mascota", args=[pk_m])).status_code, (302, 401))

    def test_entrar_y_salir(self):
        """Después de entrar: el inicio. Después de salir: el login"""
        User.objects.create_user("vero", password="una-clave-larga-123")
        respuesta = self.client.post(reverse("login"), {"username": "vero", "password": "una-clave-larga-123"})
        self.assertRedirects(respuesta, reverse("clinica:inicio"))
        self.assertContains(self.client.get(reverse("clinica:inicio")), "vero",
                            msg_prefix="en el menú tiene que estar el nombre de quien trabaja")
        self.assertRedirects(self.client.post(reverse("logout")), reverse("login"))
