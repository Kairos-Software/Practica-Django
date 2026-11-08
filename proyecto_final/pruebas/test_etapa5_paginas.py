"""
Prueba de la ETAPA 5 (las páginas).
Copiala a tu carpeta "clinica" y:   python manage.py test clinica.test_etapa5_paginas
"""

import io
import shutil
import tempfile
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import NoReverseMatch, reverse

from clinica.models import Duenio, Mascota, Vacuna, Visita

CARPETA = tempfile.mkdtemp()


def url(nombre, *args):
    try:
        return reverse(f"clinica:{nombre}", args=args)
    except NoReverseMatch:
        raise AssertionError(f"No encontré la dirección con name='{nombre}' (¿app_name = 'clinica'?)") from None


def mensajes(respuesta):
    return [str(m) for m in respuesta.context["messages"]] if respuesta.context else []


def tiene_plata(html, numero):
    """¿El HTML muestra ese importe? Acepta 7500.50, 7500,50 o 7.500,50."""
    entero, decimales = numero.split(".")
    con_miles = f"{int(entero):,}".replace(",", ".")
    return any(v in html for v in (numero, f"{entero},{decimales}", f"{con_miles},{decimales}"))


def imagen():
    from PIL import Image
    buffer = io.BytesIO()
    Image.new("RGB", (20, 20), "green").save(buffer, "PNG")
    return SimpleUploadedFile("toby.png", buffer.getvalue(), content_type="image/png")


@override_settings(MEDIA_ROOT=CARPETA)
class Etapa5(TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(CARPETA, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.vero = User.objects.create_user("vero", password=None)
        self.client.force_login(self.vero)
        self.lucia = Duenio.objects.create(nombre="Lucía Pérez", telefono="+54 9 11 5555-1234")
        self.carlos = Duenio.objects.create(nombre="Carlos Gómez", telefono="011 4444-9876")
        self.toby = Mascota.objects.create(nombre="Toby", especie="perro", duenio=self.lucia)
        self.michi = Mascota.objects.create(nombre="Michi", especie="gato", duenio=self.lucia)
        self.piolin = Mascota.objects.create(nombre="Piolín", especie="ave", duenio=self.carlos)

    # ── Generales ──
    def test_01_paginas_responden(self):
        """Todas las páginas responden, y lo que no existe da 404"""
        for nombre, *args in [("inicio",), ("duenios",), ("duenio", self.lucia.pk), ("crear_duenio",),
                              ("editar_duenio", self.lucia.pk), ("borrar_duenio", self.lucia.pk), ("mascotas",),
                              ("mascota", self.toby.pk), ("crear_mascota",), ("editar_mascota", self.toby.pk),
                              ("borrar_mascota", self.toby.pk), ("deudas",)]:
            self.assertEqual(self.client.get(url(nombre, *args)).status_code, 200, nombre)
        for nombre in ("duenio", "mascota", "editar_mascota", "borrar_duenio"):
            self.assertEqual(self.client.get(url(nombre, 9999)).status_code, 404, nombre)

    def test_02_inicio(self):
        """Inicio: mascotas por especie, visitas del mes, cobrado del mes, deuda total, últimas visitas"""
        hoy = date.today()
        Visita.objects.create(mascota=self.toby, motivo="Control anual", costo=Decimal("8000"), pagada=True)
        Visita.objects.create(mascota=self.michi, motivo="Vómitos", costo=Decimal("2500.50"))
        Visita.objects.create(mascota=self.piolin, motivo="Vieja", costo=Decimal("99"), pagada=True,
                              fecha=hoy - timedelta(days=400))
        html = self.client.get(url("inicio")).content.decode()
        self.assertTrue(tiene_plata(html, "8000.00"), "falta lo cobrado este mes (8000,00)")
        self.assertTrue(tiene_plata(html, "2500.50"), "falta la deuda total (2500,50)")
        for texto in ("Perro", "Gato", "Ave", "Control anual", "Vómitos"):
            self.assertIn(texto, html)

    # ── Dueños ──
    def test_03_lista_de_duenios(self):
        """Dueños: buscador por nombre o teléfono, cantidad de mascotas y deuda"""
        Visita.objects.create(mascota=self.toby, motivo="A", costo=Decimal("5000"))
        Visita.objects.create(mascota=self.michi, motivo="B", costo=Decimal("2500.50"))
        Visita.objects.create(mascota=self.michi, motivo="C", costo=Decimal("9999"), pagada=True)
        html = self.client.get(url("duenios")).content.decode()
        self.assertIn("Lucía Pérez", html)
        self.assertTrue(tiene_plata(html, "7500.50"), "la deuda de Lucía es 7500,50 (las visitas pagadas no cuentan)")
        por_telefono = self.client.get(url("duenios"), {"q": "4444"}).content.decode()
        self.assertIn("Carlos Gómez", por_telefono)
        self.assertNotIn("Lucía Pérez", por_telefono)

    def test_04_detalle_de_duenio(self):
        """Detalle del dueño: sus mascotas y el botón para agregar una con él elegido"""
        respuesta = self.client.get(url("duenio", self.lucia.pk))
        self.assertContains(respuesta, "Toby")
        self.assertContains(respuesta, url("mascota", self.toby.pk))
        self.assertContains(respuesta, f"{url('crear_mascota')}?duenio={self.lucia.pk}")

    def test_05_crear_duenio_y_telefono(self):
        """Crear dueño; el teléfono se valida"""
        respuesta = self.client.post(url("crear_duenio"), {"nombre": "Marta", "telefono": "llamame"})
        self.assertContains(respuesta, "Solo números, espacios, guiones y un + al principio.")
        self.client.post(url("crear_duenio"), {"nombre": "Marta", "telefono": "+54 362 400-1122"})
        self.assertTrue(Duenio.objects.filter(nombre="Marta").exists())

    def test_06_editar_duenio(self):
        """Editar un dueño cambia ESE dueño (no crea otro)"""
        self.client.post(url("editar_duenio", self.carlos.pk), {"nombre": "Carlos A. Gómez", "telefono": "123"})
        self.carlos.refresh_from_db()
        self.assertEqual(self.carlos.nombre, "Carlos A. Gómez")
        self.assertEqual(Duenio.objects.count(), 2)

    def test_07_borrar_duenio(self):
        """Borrar dueño: con mascotas no se borra (mensaje), sin mascotas sí"""
        respuesta = self.client.post(url("borrar_duenio", self.lucia.pk), follow=True)
        self.assertRedirects(respuesta, url("duenio", self.lucia.pk))
        self.assertTrue(any("tiene mascotas" in m for m in mensajes(respuesta)), mensajes(respuesta))
        solo = Duenio.objects.create(nombre="Sin mascotas", telefono="1")
        self.client.get(url("borrar_duenio", solo.pk))
        self.assertTrue(Duenio.objects.filter(pk=solo.pk).exists(), "con GET no se borra")
        self.client.post(url("borrar_duenio", solo.pk))
        self.assertFalse(Duenio.objects.filter(pk=solo.pk).exists())

    # ── Mascotas ──
    def test_08_lista_de_mascotas(self):
        """Mascotas: busca por el dueño también, filtra por especie, pagina de a 12"""
        por_duenio = self.client.get(url("mascotas"), {"q": "carlos"}).content.decode()
        self.assertIn("Piolín", por_duenio)
        self.assertNotIn("Toby", por_duenio)
        gatos = self.client.get(url("mascotas"), {"especie": "gato"}).content.decode()
        self.assertIn("Michi", gatos)
        self.assertNotIn("Toby", gatos)
        for n in range(1, 14):
            Mascota.objects.create(nombre=f"Zeta {n:02d}", especie="perro", duenio=self.carlos)
        primera = self.client.get(url("mascotas"), {"q": "zeta"}).content.decode()
        self.assertIn("Zeta 12", primera)
        self.assertNotIn("Zeta 13", primera)
        self.assertIn("q=zeta", primera, "el link de la página siguiente tiene que llevar la búsqueda")
        self.assertIn("Zeta 13", self.client.get(url("mascotas"), {"q": "zeta", "pagina": 2}).content.decode())

    def test_09_crear_mascota_con_foto_y_vacunas(self):
        """Crear mascota: foto y vacunas; con ?duenio= arranca con ese dueño elegido"""
        respuesta = self.client.get(url("crear_mascota"), {"duenio": self.carlos.pk})
        self.assertContains(respuesta, f'value="{self.carlos.pk}" selected')
        antirrabica = Vacuna.objects.create(nombre="Antirrábica")
        self.client.post(url("crear_mascota"), {"nombre": "Rocco", "especie": "perro", "duenio": self.carlos.pk,
                                                "vacunas": [antirrabica.pk], "foto": imagen()})
        rocco = Mascota.objects.get(nombre="Rocco")
        self.assertEqual(list(rocco.vacunas.all()), [antirrabica])
        self.assertTrue(rocco.foto, "la foto no se guardó (¿enctype? ¿request.FILES?)")
        self.assertContains(self.client.get(url("mascota", rocco.pk)), rocco.foto.url)

    def test_10_ficha_de_la_mascota(self):
        """Ficha: dueño, edad, vacunas, visitas con el total gastado"""
        self.toby.nacimiento = date.today() - timedelta(days=800)
        self.toby.save()
        self.toby.vacunas.add(Vacuna.objects.create(nombre="Séxtuple"))
        Visita.objects.create(mascota=self.toby, motivo="Control", costo=Decimal("1000.25"))
        Visita.objects.create(mascota=self.toby, motivo="Vacunas", costo=Decimal("2000.25"), pagada=True)
        html = self.client.get(url("mascota", self.toby.pk)).content.decode()
        for texto in ("Lucía Pérez", "2 años", "Séxtuple", "Control", "Vacunas"):
            self.assertIn(texto, html)
        self.assertIn(url("duenio", self.lucia.pk), html)
        self.assertTrue(tiene_plata(html, "3000.50"), "falta el total gastado (3000,50)")

    def test_11_cargar_visita_desde_la_ficha(self):
        """Visita desde la ficha: quien atiende es el usuario; no en el futuro"""
        self.client.post(url("mascota", self.toby.pk), {"fecha": date.today().isoformat(),
                                                        "motivo": "Vacuna anual", "costo": "8000"})
        visita = Visita.objects.get()
        self.assertEqual((visita.mascota, visita.atendida_por, visita.pagada), (self.toby, self.vero, False))
        respuesta = self.client.post(url("mascota", self.toby.pk), {"fecha": "2999-01-01", "motivo": "X",
                                                                    "costo": "1"})
        self.assertContains(respuesta, "La visita no puede ser en el futuro.")
        self.assertEqual(Visita.objects.count(), 1)

    def test_12_editar_y_borrar_mascota(self):
        """Editar cambia ESA mascota; borrar pregunta con GET y borra con POST (con sus visitas)"""
        self.client.post(url("editar_mascota", self.michi.pk), {"nombre": "Michifuz", "especie": "gato",
                                                                "duenio": self.lucia.pk})
        self.michi.refresh_from_db()
        self.assertEqual(self.michi.nombre, "Michifuz")
        Visita.objects.create(mascota=self.michi, motivo="X", costo=1)
        self.client.get(url("borrar_mascota", self.michi.pk))
        self.assertTrue(Mascota.objects.filter(pk=self.michi.pk).exists(), "con GET no se borra")
        self.client.post(url("borrar_mascota", self.michi.pk))
        self.assertFalse(Mascota.objects.filter(pk=self.michi.pk).exists())
        self.assertFalse(Visita.objects.exists())

    # ── Visitas y deudas ──
    def test_13_marcar_pagada(self):
        """Marcar pagada: solo POST; vuelve a la ficha o a deudas"""
        visita = Visita.objects.create(mascota=self.toby, motivo="Control", costo=5000)
        self.assertEqual(self.client.get(url("pagada", visita.pk)).status_code, 405)
        self.assertRedirects(self.client.post(url("pagada", visita.pk)), url("mascota", self.toby.pk))
        visita.refresh_from_db()
        self.assertTrue(visita.pagada)

    def test_14_deudas(self):
        """Deudas: las visitas sin pagar con el total, y el botón de pagar"""
        sin_pagar = Visita.objects.create(mascota=self.toby, motivo="Control", costo=Decimal("1500.25"))
        Visita.objects.create(mascota=self.piolin, motivo="Canto", costo=Decimal("500.25"))
        Visita.objects.create(mascota=self.michi, motivo="Pagada", costo=Decimal("99999"), pagada=True)
        html = self.client.get(url("deudas")).content.decode()
        self.assertIn("Toby", html)
        self.assertIn("Carlos Gómez", html)
        self.assertNotIn("99999", html)
        self.assertTrue(tiene_plata(html, "2000.50"), "falta el total (2000,50)")
        self.assertIn(url("pagada", sin_pagar.pk), html)
