"""
Prueba de la ETAPA 1 (el proyecto).
Copiala a tu carpeta "clinica" y:   python manage.py test clinica.test_etapa1_proyecto
"""

from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase


class Etapa1(SimpleTestCase):

    def test_app(self):
        """La app 'clinica' está registrada"""
        self.assertTrue(any(app == "clinica" or app.startswith("clinica.") for app in settings.INSTALLED_APPS))

    def test_idioma_y_hora(self):
        """Castellano de Argentina y hora de Buenos Aires"""
        self.assertEqual(settings.LANGUAGE_CODE, "es-ar")
        self.assertEqual(settings.TIME_ZONE, "America/Argentina/Buenos_Aires")

    def test_sqlite(self):
        """La base es SQLite"""
        self.assertEqual(settings.DATABASES["default"]["ENGINE"], "django.db.backends.sqlite3")

    def test_carpeta_templates(self):
        """Una carpeta 'templates' en la raíz, en TEMPLATES -> DIRS"""
        dirs = [Path(d) for d in settings.TEMPLATES[0].get("DIRS", [])]
        self.assertIn(Path(settings.BASE_DIR) / "templates", dirs)

    def test_media(self):
        """Archivos subidos: MEDIA_URL = '/media/' y MEDIA_ROOT en la carpeta media"""
        self.assertEqual(settings.MEDIA_URL, "/media/")
        self.assertEqual(Path(settings.MEDIA_ROOT), Path(settings.BASE_DIR) / "media")
