"""
Prueba de la ETAPA 5 (la API).
Copiala a tu carpeta "clinica" y:   python manage.py test clinica.test_etapa5_api
"""

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from clinica.models import Duenio, Mascota, Vacuna, Visita


class Etapa5Api(TestCase):

    def setUp(self):
        self.client.force_login(User.objects.create_user("vero", password=None))
        lucia = Duenio.objects.create(nombre="Lucía Pérez", telefono="+54 9 11 5555-1234")
        self.toby = Mascota.objects.create(nombre="Toby", especie="perro", duenio=lucia,
                                           nacimiento=date.today() - timedelta(days=800))
        self.toby.vacunas.add(Vacuna.objects.create(nombre="Séxtuple"), Vacuna.objects.create(nombre="Antirrábica"))
        self.vieja = Visita.objects.create(mascota=self.toby, motivo="Vacunas", costo=Decimal("12000"), pagada=True,
                                           fecha=date.today() - timedelta(days=200))
        self.nueva = Visita.objects.create(mascota=self.toby, motivo="Control anual", costo=Decimal("8000"))

    def test_la_api(self):
        """api_mascota: todos los datos en el formato pedido"""
        respuesta = self.client.get(reverse("clinica:api_mascota", args=[self.toby.pk]))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json(), {
            "id": self.toby.pk,
            "nombre": "Toby",
            "especie": "Perro",
            "edad": "2 años",
            "duenio": {"nombre": "Lucía Pérez", "telefono": "+54 9 11 5555-1234"},
            "vacunas": ["Antirrábica", "Séxtuple"],
            "visitas": [
                {"fecha": self.nueva.fecha.isoformat(), "motivo": "Control anual", "costo": "8000.00", "pagada": False},
                {"fecha": self.vieja.fecha.isoformat(), "motivo": "Vacunas", "costo": "12000.00", "pagada": True},
            ],
        })

    def test_no_existe(self):
        """api_mascota: 404 en JSON"""
        respuesta = self.client.get(reverse("clinica:api_mascota", args=[9999]))
        self.assertEqual(respuesta.status_code, 404)
        self.assertEqual(respuesta.json(), {"error": "No existe esa mascota."})
