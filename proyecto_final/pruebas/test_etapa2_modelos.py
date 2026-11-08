"""
Prueba de la ETAPA 2 (los modelos).
Copiala a tu carpeta "clinica" y:   python manage.py test clinica.test_etapa2_modelos
"""

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.test import TestCase

from clinica.models import Duenio, Mascota, Vacuna, Visita


class Etapa2(TestCase):

    def setUp(self):
        self.lucia = Duenio.objects.create(nombre="Lucía Pérez", telefono="+54 9 11 5555-1234")
        self.toby = Mascota.objects.create(nombre="Toby", especie="perro", duenio=self.lucia)

    def test_duenio(self):
        """Duenio: email y dirección opcionales, ordenados por nombre"""
        Duenio.objects.create(nombre="Ana Gómez", telefono="123")
        Duenio(nombre="X", telefono="1").full_clean()        # sin email ni dirección: vale
        self.assertEqual([d.nombre for d in Duenio.objects.all()], ["Ana Gómez", "Lucía Pérez"])

    def test_vacuna(self):
        """Vacuna: nombre sin repetir, ordenadas"""
        Vacuna.objects.create(nombre="Séxtuple")
        Vacuna.objects.create(nombre="Antirrábica")
        self.assertEqual([v.nombre for v in Vacuna.objects.all()], ["Antirrábica", "Séxtuple"])
        with self.assertRaises(Exception):
            Vacuna.objects.create(nombre="Séxtuple")

    def test_especies(self):
        """Mascota.especie: las 5 opciones con sus textos"""
        opciones = dict(Mascota._meta.get_field("especie").choices)
        self.assertEqual(opciones, {"perro": "Perro", "gato": "Gato", "ave": "Ave", "conejo": "Conejo", "otro": "Otro"})
        self.assertEqual(self.toby.get_especie_display(), "Perro")

    def test_mascota_campos_y_relaciones(self):
        """Mascota: opcionales, foto en mascotas/, duenio.mascotas, vacunas (muchas) y vacuna.mascotas"""
        Mascota(nombre="Michi", especie="gato", duenio=self.lucia).full_clean()   # raza, nacimiento, foto opcionales
        self.assertEqual(Mascota._meta.get_field("foto").upload_to, "mascotas/")
        self.assertEqual(Mascota._meta.get_field("foto").__class__.__name__, "ImageField")
        antirrabica = Vacuna.objects.create(nombre="Antirrábica")
        self.toby.vacunas.add(antirrabica)
        self.assertEqual(list(self.lucia.mascotas.all()), [self.toby])
        self.assertEqual(list(antirrabica.mascotas.all()), [self.toby])

    def test_no_se_borra_un_duenio_con_mascotas(self):
        """Un dueño con mascotas no se puede borrar"""
        with self.assertRaises(ProtectedError):
            self.lucia.delete()

    def test_edad(self):
        """edad(hoy): todos los casos"""
        hoy = date(2026, 10, 10)
        casos = [(None, "Edad desconocida"), (date(2026, 10, 1), "Recién nacido"), (date(2026, 9, 10), "1 mes"),
                 (date(2026, 2, 11), "7 meses"), (date(2026, 2, 10), "8 meses"), (date(2025, 10, 10), "1 año"),
                 (date(2023, 5, 1), "3 años")]
        for nacimiento, esperado in casos:
            self.assertEqual(Mascota(nacimiento=nacimiento).edad(hoy), esperado, f"nacido el {nacimiento}")
        self.assertEqual(Mascota(nacimiento=date.today()).edad(), "Recién nacido", "sin 'hoy' usa la fecha de hoy")

    def test_nacimiento_futuro(self):
        """No puede nacer en el futuro"""
        futura = Mascota(nombre="X", especie="perro", duenio=self.lucia, nacimiento=date.today() + timedelta(days=1))
        with self.assertRaises(ValidationError) as error:
            futura.full_clean()
        self.assertIn("La fecha de nacimiento no puede ser en el futuro.", str(error.exception))

    def test_visita(self):
        """Visita: fecha de hoy y no pagada por defecto; relaciones; orden"""
        vieja = Visita.objects.create(mascota=self.toby, motivo="Vacunas", costo=Decimal("12000"),
                                      fecha=date.today() - timedelta(days=30))
        nueva = Visita.objects.create(mascota=self.toby, motivo="Control", costo=Decimal("8000.50"))
        self.assertEqual((nueva.fecha, nueva.pagada), (date.today(), False))
        self.assertEqual(list(self.toby.visitas.all()), [nueva, vieja], "la más nueva primero")
        nueva.refresh_from_db()
        self.assertEqual(nueva.costo, Decimal("8000.50"))

    def test_visita_validaciones(self):
        """Visita: ni en el futuro ni con costo negativo"""
        futura = Visita(mascota=self.toby, motivo="X", costo=1, fecha=date.today() + timedelta(days=1))
        with self.assertRaises(ValidationError) as error:
            futura.full_clean()
        self.assertIn("La visita no puede ser en el futuro.", str(error.exception))
        with self.assertRaises(ValidationError):
            Visita(mascota=self.toby, motivo="X", costo=Decimal("-1")).full_clean()

    def test_borrados_en_cadena(self):
        """Borrar la mascota borra sus visitas; borrar el usuario NO borra la visita"""
        vero = User.objects.create_user("vero", password=None)
        visita = Visita.objects.create(mascota=self.toby, motivo="X", costo=1, atendida_por=vero)
        vero.delete()
        visita.refresh_from_db()
        self.assertIsNone(visita.atendida_por)
        self.toby.delete()
        self.assertFalse(Visita.objects.exists())
