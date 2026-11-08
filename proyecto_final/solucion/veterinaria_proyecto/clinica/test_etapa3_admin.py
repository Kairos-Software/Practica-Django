"""
Prueba de la ETAPA 3 (el admin).
Copiala a tu carpeta "clinica" y:   python manage.py test clinica.test_etapa3_admin
"""

from django.contrib import admin
from django.test import SimpleTestCase

from clinica.models import Duenio, Mascota, Vacuna, Visita


class Etapa3(SimpleTestCase):

    def admin_de(self, modelo):
        self.assertIn(modelo, admin.site._registry, f"Falta registrar {modelo.__name__} en clinica/admin.py")
        return admin.site._registry[modelo]

    def test_todos_registrados(self):
        """Los 4 modelos en el admin"""
        for modelo in (Duenio, Mascota, Vacuna, Visita):
            self.admin_de(modelo)

    def test_duenio_con_sus_mascotas(self):
        """Dueño: las mascotas adentro (inline)"""
        inlines = [i.model for i in self.admin_de(Duenio).inlines]
        self.assertIn(Mascota, inlines)

    def test_mascota(self):
        """Mascota: visitas adentro, filtro por especie, buscador, selector de vacunas"""
        m = self.admin_de(Mascota)
        self.assertIn(Visita, [i.model for i in m.inlines])
        self.assertIn("especie", m.list_filter)
        self.assertIn("nombre", m.search_fields)
        self.assertIn("duenio__nombre", m.search_fields)
        self.assertIn("vacunas", m.filter_horizontal)

    def test_visita_pagada_editable(self):
        """Visita: 'pagada' editable desde la lista"""
        self.assertIn("pagada", self.admin_de(Visita).list_editable)
