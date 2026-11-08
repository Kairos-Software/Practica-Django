"""
═══════════════════════════════════════════════════════════════════════
 PASO 5 — IMÁGENES Y ARCHIVOS: SUBIR, MOSTRAR, VALIDAR, BORRAR,
          DESCARGAR (exportar) E IMPORTAR
═══════════════════════════════════════════════════════════════════════

Necesita Pillow (la librería que entiende imágenes):   pip install pillow

Ejecutalo (con el entorno activado):
    python clase.py              -> simula todo y te muestra qué pasa
    python clase.py runserver    -> la página de verdad: http://127.0.0.1:8000

El ejemplo: películas con su PÓSTER, una planilla para DESCARGAR, y cargar
muchas películas de una subiendo una planilla.


═══════════════════════════════════════════════════════════════════════
 PARTE 1 — LA EXPLICACIÓN
═══════════════════════════════════════════════════════════════════════

0) DOS TIPOS DE ARCHIVOS
────────────────────────
  - ESTÁTICOS (static): los que hacés VOS y vienen con el código: tu CSS,
    tu logo, un JS. Viven en app/static/. Se usan con {% static '...' %}.
  - SUBIDOS (media): los que suben los USUARIOS mientras usan el sistema:
    fotos, PDFs, planillas. Viven en una carpeta aparte (media/) que NO va al
    código ni a git (cada compu / servidor tiene los suyos, y van al backup).

1) CONFIGURAR (una vez por proyecto)
────────────────────────────────────
  settings.py:
        MEDIA_URL = '/media/'               <- la dirección con que se piden
        MEDIA_ROOT = BASE_DIR / 'media'     <- la carpeta donde se guardan
  config/urls.py (para verlos en desarrollo; en producción los sirve nginx):
        from django.conf import settings
        from django.conf.urls.static import static
        urlpatterns = [ ... ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

2) EL CAMPO EN EL MODELO
────────────────────────
        poster = models.ImageField(upload_to='posters/', blank=True)     <- solo imágenes (necesita Pillow)
        guion  = models.FileField(upload_to='guiones/%Y/', blank=True)   <- cualquier archivo
  - upload_to = la subcarpeta adentro de media/. Puede llevar la fecha:
    '%Y/%m/' -> media/posters/2026/10/
  - En la BASE se guarda solo el NOMBRE ("posters/matrix.jpg"); el archivo va
    a la carpeta. Si ya hay uno con ese nombre, Django le agrega letras al
    azar ("matrix_aB3xY9.jpg"): nunca pisa uno existente.
  - Desde el código:
        pelicula.poster              -> el archivo ("vacío" si no tiene: if pelicula.poster:)
        pelicula.poster.url          -> la dirección para el <img>: /media/posters/matrix.jpg
        pelicula.poster.name         -> "posters/matrix.jpg"
        pelicula.poster.path         -> dónde está en el disco
        pelicula.poster.size         -> cuánto pesa (bytes)
        pelicula.poster.delete(save=False)   -> BORRA el archivo del disco
  - Es un campo nuevo: makemigrations + migrate.

3) EL FORMULARIO Y LA VISTA
───────────────────────────
  En el HTML, sin esto el archivo NO viaja (llega vacío y no da error):
        <form method="post" enctype="multipart/form-data">
  En la vista, los archivos vienen aparte, en request.FILES:
        form = PeliculaForm(request.POST, request.FILES)
        form = PeliculaForm(request.POST, request.FILES, instance=pelicula)    <- editar
  (las vistas de clase CreateView/UpdateView ya lo hacen solas)
  El ModelForm muestra un "Elegir archivo" y, si ya tiene uno, un link al
  actual y una casilla "Limpiar" para sacarlo.

4) MOSTRARLO
────────────
        {% if pelicula.poster %}<img src="{{ pelicula.poster.url }}" alt="Póster" width="200">{% endif %}
        <a href="{{ pelicula.guion.url }}" download>Bajar el guion</a>
  (siempre con el if: .url de un campo vacío da error)

5) VALIDAR (nunca confíes en lo que sube la gente)
──────────────────────────────────────────────────
  - ImageField YA rechaza lo que no es una imagen ("Subí una imagen válida").
  - El tamaño, en el formulario:
        def clean_poster(self):
            poster = self.cleaned_data.get('poster')
            if poster and poster.size > 2 * 1024 * 1024:        # 2 MB en bytes
                raise forms.ValidationError('La imagen no puede pesar más de 2 MB.')
            return poster
  - Para FileField, las extensiones permitidas:
        from django.core.validators import FileExtensionValidator
        guion = models.FileField(..., validators=[FileExtensionValidator(['pdf'])])

6) BORRAR LOS ARCHIVOS VIEJOS
─────────────────────────────
Django NO borra el archivo del disco cuando cambiás la imagen o borrás el
objeto (por si otro lo usa). Si no lo hacés vos, la carpeta se llena de basura.
  - Al borrar el objeto:
        pelicula.poster.delete(save=False)     <- primero el archivo
        pelicula.delete()                      <- después el registro
  - Al reemplazar, en la vista de editar, ANTES de guardar el formulario:
        viejo = Pelicula.objects.get(pk=pk).poster            <- el que estaba en la base
        if form.is_valid():
            nueva = form.save()
            if viejo and viejo != nueva.poster:               <- cambió (o lo sacaron)
                viejo.delete(save=False)

7) DESCARGAR: generar un archivo (exportar a CSV / Excel)
─────────────────────────────────────────────────────────
Una vista puede devolver un ARCHIVO en vez de una página. CSV = "valores
separados por comas": una planilla en texto, que Excel abre.
        import csv
        from django.http import HttpResponse

        def exportar(request):
            respuesta = HttpResponse(content_type='text/csv; charset=utf-8')
            respuesta['Content-Disposition'] = 'attachment; filename="peliculas.csv"'   <- "bajalo con este nombre"
            respuesta.write('\\ufeff')                    <- (una marca para que Excel lea bien los acentos)
            escritor = csv.writer(respuesta, delimiter=';')   <- Excel en castellano usa ; (no ,)
            escritor.writerow(['titulo', 'anio'])          <- la fila de títulos
            for p in Pelicula.objects.all():
                escritor.writerow([p.titulo, p.anio])
            return respuesta
  - Un link común lo descarga:  <a href="{% url 'exportar' %}">Bajar planilla</a>
  - Para devolver un archivo que YA existe en el disco: FileResponse(open(ruta, 'rb'), as_attachment=True)

8) IMPORTAR: leer un archivo que sube el usuario
────────────────────────────────────────────────
Ejemplo: cargar 200 películas de una, subiendo una planilla CSV.
  - El formulario (no es de un modelo):
        class ImportarForm(forms.Form):
            archivo = forms.FileField()
  - En la vista, el archivo subido se lee (viene en bytes) y se convierte a texto:
        archivo = form.cleaned_data['archivo']
        texto = archivo.read().decode('utf-8-sig')            <- utf-8-sig: ignora la marca de Excel
        filas = csv.DictReader(io.StringIO(texto), delimiter=';')   <- cada fila: un diccionario {'titulo': ..., 'anio': ...}
        for numero, fila in enumerate(filas, start=2):         <- start=2: la 1 es la de títulos
            try:
                Pelicula.objects.create(titulo=fila['titulo'].strip(), anio=int(fila['anio']))
            except (KeyError, ValueError):
                errores.append(numero)                         <- se saltea la fila mala y se sigue
  - Nunca se guarda el archivo: se lee y listo.
  - Si el archivo no es texto (alguien sube una foto): .decode() da UnicodeDecodeError -> atajalo.


═══════════════════════════════════════════════════════════════════════
 PARTE 2 — EN ACCIÓN (desde acá se ejecuta)
═══════════════════════════════════════════════════════════════════════
"""

import csv
import io
import os
import shutil
import sys

try:
    import PIL  # noqa: F401
except ImportError:
    sys.exit("Esta clase necesita Pillow. Con el entorno activado:  pip install pillow")

import django
from django.apps import AppConfig
from django.conf import settings

BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DB = os.path.join(BASE, "clase5.sqlite3")
CARPETA_MEDIA = os.path.join(BASE, "media_clase5")


class ClaseConfig(AppConfig):
    name = "__main__"
    label = "clase"


TEMPLATES_DE_LA_CLASE = {
    "base.html": """<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Películas</title>
<style>body{font-family:sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem} .mensaje{background:#e6f4ea;padding:.5rem}
 .error{background:#fde8e8} img{max-width:160px;display:block}</style></head><body>
<nav><a href="{% url 'lista' %}">Películas</a> · <a href="{% url 'crear' %}">+ Nueva</a> ·
<a href="{% url 'exportar' %}">⬇ Bajar planilla</a> · <a href="{% url 'importar' %}">⬆ Importar planilla</a></nav>
{% for m in messages %}<p class="mensaje {{ m.tags }}">{{ m }}</p>{% endfor %}
{% block contenido %}{% endblock %}</body></html>""",

    "lista.html": """{% extends "base.html" %}{% block contenido %}<h1>Películas</h1>
{% for p in peliculas %}
  <div>{% if p.poster %}<img src="{{ p.poster.url }}" alt="">{% endif %}
  <a href="{% url 'editar' p.pk %}">{{ p.titulo }}</a> ({{ p.anio }})
  <form method="post" action="{% url 'borrar' p.pk %}" style="display:inline">{% csrf_token %}<button>Borrar</button></form></div>
{% empty %}<p>No hay películas.</p>{% endfor %}{% endblock %}""",

    "form.html": """{% extends "base.html" %}{% block contenido %}<h1>{{ titulo }}</h1>
{# enctype: SIN esto la imagen no viaja #}
<form method="post" enctype="multipart/form-data">{% csrf_token %}{{ form.as_p }}<button>Guardar</button></form>
{% endblock %}""",

    "importar.html": """{% extends "base.html" %}{% block contenido %}<h1>Importar películas</h1>
<p>Una planilla CSV separada por <b>;</b> con las columnas <code>titulo;anio</code>.</p>
<form method="post" enctype="multipart/form-data">{% csrf_token %}{{ form.as_p }}<button>Importar</button></form>
{% endblock %}""",
}

settings.configure(
    DEBUG=True,
    SECRET_KEY="solo-para-la-clase-5",
    ALLOWED_HOSTS=["*"],
    ROOT_URLCONF="__main__",
    INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.messages", "__main__.ClaseConfig"],
    MIDDLEWARE=[
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ],
    MESSAGE_STORAGE="django.contrib.messages.storage.cookie.CookieStorage",
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ARCHIVO_DB}},
    TEMPLATES=[{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "loaders": [("django.template.loaders.locmem.Loader", TEMPLATES_DE_LA_CLASE)],
            "context_processors": ["django.template.context_processors.request",
                                   "django.contrib.messages.context_processors.messages"],
        },
    }],
    MEDIA_URL="/media/",                 # 1)
    MEDIA_ROOT=CARPETA_MEDIA,            # 1)
    LANGUAGE_CODE="es-ar",
    TIME_ZONE="America/Argentina/Buenos_Aires",
    USE_TZ=True,
    DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
)
django.setup()

from django import forms  # noqa: E402
from django.conf.urls.static import static  # noqa: E402
from django.contrib import messages  # noqa: E402
from django.db import models  # noqa: E402
from django.http import HttpResponse  # noqa: E402
from django.shortcuts import get_object_or_404, redirect, render  # noqa: E402
from django.urls import path  # noqa: E402
from django.views.decorators.http import require_POST  # noqa: E402

MAXIMO = 2 * 1024 * 1024    # 2 MB


# ── Modelo ──
class Pelicula(models.Model):
    titulo = models.CharField("título", max_length=120)
    anio = models.PositiveIntegerField("año")
    poster = models.ImageField("póster", upload_to="posters/", blank=True)        # 2)

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo


# ── Formularios ──
class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ["titulo", "anio", "poster"]

    def clean_poster(self):                                                       # 5)
        poster = self.cleaned_data.get("poster")
        if poster and poster.size > MAXIMO:
            raise forms.ValidationError("La imagen no puede pesar más de 2 MB.")
        return poster


class ImportarForm(forms.Form):                                                   # 8)
    archivo = forms.FileField(label="Planilla (.csv)")


# ── Vistas ──
def lista(request):
    return render(request, "lista.html", {"peliculas": Pelicula.objects.all()})


def crear(request):
    form = PeliculaForm(request.POST or None, request.FILES or None)              # 3) request.FILES
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Guardada.")
        return redirect("lista")
    return render(request, "form.html", {"form": form, "titulo": "Nueva película"})


def editar(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    viejo = pelicula.poster                     # 6) el que tenía antes de cambiar nada
    form = PeliculaForm(request.POST or None, request.FILES or None, instance=pelicula)
    if request.method == "POST" and form.is_valid():
        nueva = form.save()
        if viejo and viejo != nueva.poster:     # 6) cambió o lo sacaron: el archivo viejo se borra
            viejo.delete(save=False)
        messages.success(request, "Cambios guardados.")
        return redirect("lista")
    return render(request, "form.html", {"form": form, "titulo": f"Editar «{pelicula}»"})


@require_POST
def borrar(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if pelicula.poster:
        pelicula.poster.delete(save=False)      # 6) primero el archivo
    pelicula.delete()                           #    después el registro
    messages.success(request, "Borrada (con su póster).")
    return redirect("lista")


def exportar(request):                                                            # 7)
    respuesta = HttpResponse(content_type="text/csv; charset=utf-8")
    respuesta["Content-Disposition"] = 'attachment; filename="peliculas.csv"'
    respuesta.write("﻿")                   # para que Excel lea bien los acentos
    escritor = csv.writer(respuesta, delimiter=";")
    escritor.writerow(["titulo", "anio"])
    for p in Pelicula.objects.all():
        escritor.writerow([p.titulo, p.anio])
    return respuesta


def importar(request):                                                            # 8)
    form = ImportarForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        try:
            texto = form.cleaned_data["archivo"].read().decode("utf-8-sig")
        except UnicodeDecodeError:
            messages.error(request, "Ese archivo no es una planilla CSV.")
            return redirect("importar")
        creadas, errores = 0, []
        for numero, fila in enumerate(csv.DictReader(io.StringIO(texto), delimiter=";"), start=2):
            try:
                Pelicula.objects.create(titulo=fila["titulo"].strip(), anio=int(fila["anio"]))
                creadas += 1
            except (KeyError, ValueError, AttributeError):
                errores.append(numero)
        messages.success(request, f"Se importaron {creadas} películas.")
        if errores:
            messages.error(request, f"Filas con errores (no se cargaron): {', '.join(map(str, errores))}.")
        return redirect("lista")
    return render(request, "importar.html", {"form": form})


urlpatterns = [
    path("", lista, name="lista"),
    path("nueva/", crear, name="crear"),
    path("<int:pk>/editar/", editar, name="editar"),
    path("<int:pk>/borrar/", borrar, name="borrar"),
    path("exportar/", exportar, name="exportar"),
    path("importar/", importar, name="importar"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)                 # 1)


def preparar_base():
    from django.db import connection
    if Pelicula._meta.db_table not in connection.introspection.table_names():
        with connection.schema_editor() as editor:
            editor.create_model(Pelicula)
    if not Pelicula.objects.exists():
        Pelicula.objects.create(titulo="Matrix", anio=1999)


def simular():
    from django.core.files.uploadedfile import SimpleUploadedFile
    from django.test import Client
    from django.test.utils import setup_test_environment
    from PIL import Image

    setup_test_environment()
    navegador = Client()

    def imagen(nombre, color="red", lado=60):
        buffer = io.BytesIO()
        Image.new("RGB", (lado, lado), color).save(buffer, "PNG")
        return SimpleUploadedFile(nombre, buffer.getvalue(), content_type="image/png")

    def archivos():
        carpeta = os.path.join(CARPETA_MEDIA, "posters")
        return sorted(os.listdir(carpeta)) if os.path.isdir(carpeta) else []

    print("1) Subir una película CON póster")
    # follow=True: sigue la redirección (y así se "leen" los mensajes de cada paso)
    navegador.post("/nueva/", {"titulo": "Up", "anio": 2009, "poster": imagen("up.png")}, follow=True)
    up = Pelicula.objects.get(titulo="Up")
    print(f"   en la base: {up.poster.name!r} · url: {up.poster.url} · pesa {up.poster.size} bytes")
    print("   en la carpeta media/posters:", archivos())

    print("\n2) Subir algo que NO es una imagen (un texto con nombre .png)")
    r = navegador.post("/nueva/", {"titulo": "Trucha", "anio": 2000,
                                   "poster": SimpleUploadedFile("virus.png", b"no soy una imagen", "image/png")})
    print("   errores:", dict(r.context["form"].errors))

    print("\n3) Subir una imagen de más de 2 MB")
    # Una imagen DE VERDAD de unos 3 MB: puntos al azar (no se puede comprimir)
    buffer = io.BytesIO()
    Image.frombytes("RGB", (1000, 1000), os.urandom(1000 * 1000 * 3)).save(buffer, "PNG")
    print(f"   (pesa {len(buffer.getvalue()) / 1024 / 1024:.1f} MB)")
    grande = SimpleUploadedFile("grande.png", buffer.getvalue(), content_type="image/png")
    r = navegador.post("/nueva/", {"titulo": "Pesada", "anio": 2000, "poster": grande})
    print("   errores:", dict(r.context["form"].errors))

    print("\n4) Cambiar el póster de Up por otro (el viejo se borra del disco)")
    navegador.post(f"/{up.pk}/editar/", {"titulo": "Up", "anio": 2009, "poster": imagen("up2.png", "blue")},
                   follow=True)
    print("   en la carpeta:", archivos())

    print("\n5) Borrar Up (se borra también su póster)")
    navegador.post(f"/{up.pk}/borrar/", follow=True)
    print("   en la carpeta:", archivos())

    print("\n6) Importar una planilla (una fila con error)")
    planilla = "titulo;anio\nToy Story;1995\nShrek;dosmil\nCoco;2017\n".encode("utf-8")
    r = navegador.post("/importar/", {"archivo": SimpleUploadedFile("pelis.csv", planilla, "text/csv")}, follow=True)
    print("   mensajes:", [str(m) for m in r.context["messages"]])

    print("\n7) Descargar la planilla")
    r = navegador.get("/exportar/")
    print("   tipo:", r["Content-Type"], "·", r["Content-Disposition"])
    print("   contenido:\n   " + r.content.decode("utf-8-sig").replace("\r\n", "\n   "))

    print("Ahora probalo de verdad:  python clase.py runserver   y abrí http://127.0.0.1:8000")


def limpiar():
    from django.db import connection
    connection.close()
    if os.path.exists(ARCHIVO_DB):
        os.remove(ARCHIVO_DB)
    shutil.rmtree(CARPETA_MEDIA, ignore_errors=True)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        limpiar()
        preparar_base()
        simular()
        limpiar()
    else:
        preparar_base()
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
