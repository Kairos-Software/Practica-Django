"""
=======================================================================
 PASO 5 — IMÁGENES Y ARCHIVOS: SUBIR, MOSTRAR, VALIDAR, BORRAR,
          DESCARGAR UNA PLANILLA E IMPORTAR UNA PLANILLA
=======================================================================

El ejemplo de toda la clase: películas con su PÓSTER (una imagen), una
planilla para DESCARGAR todas las películas, y cargar muchas películas de
una sola vez SUBIENDO una planilla.


¿QUÉ NECESITÁS?
---------------
El entorno virtual activado, con Django instalado, y además Pillow (la
librería que le enseña a Python a entender imágenes). Si no la instalaste:

    pip install pillow            <- con el entorno activado


CÓMO SE USA ESTE ARCHIVO
------------------------
Igual que en los pasos 3 y 4 (parado en "Aprender Django"):

  1) SIMULACIÓN:   python paso_5_imagenes_y_archivos\\clase.py
     Sube imágenes, prueba subir cosas que no son imágenes o que pesan
     mucho, cambia y borra pósters, importa y descarga una planilla. Lo que
     muestra está anotado en la PARTE 10, al final.

  2) DE VERDAD:    python paso_5_imagenes_y_archivos\\clase.py runserver
     Abrí http://127.0.0.1:8000. Probá crear una película con una imagen
     tuya, cambiarle la imagen, bajar la planilla y abrirla con Excel, y
     subir una planilla (más abajo, en la PARTE 8, está cómo armarla).
     Mientras probás, mirá la carpeta media_clase5\\posters\\ que se crea al
     lado de este archivo: ahí aparecen (y desaparecen) las imágenes.
     Ctrl+C en la terminal para apagar el servidor. (La base clase5.sqlite3
     y la carpeta media_clase5 se pueden borrar después.)

Las PARTES 1 a 8 explican; la PARTE 9 es el código que se ejecuta. Lo
marcado como MAQUINARIA DE LA CLASE no hace falta entenderlo ni copiarlo.


=======================================================================
PARTE 1 — DOS TIPOS DE ARCHIVOS
=======================================================================
  - ESTÁTICOS (static): los que hacés VOS y vienen con el código: tu CSS,
    tu logo, tu JavaScript. Viven en app/static/ (paso 3, PARTE 8).
  - SUBIDOS (media): los que suben los USUARIOS mientras usan el sistema:
    fotos, PDFs, planillas. Viven en una carpeta aparte, media/, que NO va
    con el código ni al repositorio (cada compu o servidor tiene los suyos).
    Por eso media/ está en el .gitignore.


=======================================================================
PARTE 2 — CONFIGURAR (una vez por proyecto)
=======================================================================
  En config/settings.py (al final):

        MEDIA_URL = '/media/'               <- con qué dirección se piden: /media/posters/up.png
        MEDIA_ROOT = BASE_DIR / 'media'     <- en qué carpeta de la compu se guardan

  En config/urls.py, para poder VER las imágenes mientras desarrollás:

        from django.conf import settings
        from django.conf.urls.static import static

        urlpatterns = [
            ...lo que ya tenías...
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

  (Cuando el sistema se publica, las imágenes las entrega el servidor web
   (nginx), no Django.)


=======================================================================
PARTE 3 — EL CAMPO EN EL MODELO
=======================================================================
        poster = models.ImageField(upload_to='posters/', blank=True)     <- solo imágenes (necesita Pillow)
        guion  = models.FileField(upload_to='guiones/', blank=True)      <- cualquier archivo

  - upload_to = la subcarpeta adentro de media/. Puede llevar la fecha:
    'posters/%Y/%m/' -> media/posters/2026/10/
  - blank=True = opcional (se puede dejar sin imagen).
  - En la BASE se guarda solo el NOMBRE ("posters/up.png"); el archivo en sí
    va a la carpeta. Si ya hay uno con ese nombre, Django le agrega letras al
    azar ("up_aB3xY9.png"): nunca pisa uno que ya existe.
  - Desde el código:
        pelicula.poster              -> el archivo ("vacío" si no tiene: se pregunta con  if pelicula.poster:)
        pelicula.poster.url          -> la dirección para mostrarlo: /media/posters/up.png
        pelicula.poster.name         -> "posters/up.png"
        pelicula.poster.size         -> cuánto pesa, en bytes
        pelicula.poster.delete(save=False)   -> BORRA el archivo de la carpeta
  - Es un campo nuevo en el modelo: makemigrations + migrate.


=======================================================================
PARTE 4 — EL FORMULARIO Y LA VISTA
=======================================================================
  En el HTML, el <form> necesita enctype="multipart/form-data". SIN ESTO EL
  ARCHIVO NO VIAJA: llega vacío, y no da ningún error (es el olvido más común).

        <form method="post" enctype="multipart/form-data">

  En la vista, los archivos llegan APARTE de los demás datos, en request.FILES:

        form = PeliculaForm(request.POST, request.FILES)                       <- crear
        form = PeliculaForm(request.POST, request.FILES, instance=pelicula)    <- editar

  (Las vistas de clase CreateView y UpdateView ya lo hacen solas.)
  El ModelForm muestra un botón "Elegir archivo" y, si ya tiene uno, un link
  al actual y una casilla "Limpiar" para sacarlo.


=======================================================================
PARTE 5 — MOSTRARLO EN UN TEMPLATE
=======================================================================
        {% if pelicula.poster %}
            <img src="{{ pelicula.poster.url }}" alt="Póster de {{ pelicula.titulo }}" width="200">
        {% endif %}
        <a href="{{ pelicula.guion.url }}" download>Bajar el guion</a>

  Siempre con el if: pedir el .url de un campo vacío da error.


=======================================================================
PARTE 6 — VALIDAR (nunca confíes en lo que sube la gente)
=======================================================================
  - ImageField YA rechaza lo que no es una imagen (aunque se llame foto.png).
  - El TAMAÑO se revisa en el formulario, con un clean_<campo> (paso 3, PARTE 5):

        def clean_poster(self):
            poster = self.cleaned_data.get('poster')
            if poster and poster.size > 2 * 1024 * 1024:        # 2 MB, en bytes (1 MB = 1024 x 1024 bytes)
                raise forms.ValidationError('La imagen no puede pesar más de 2 MB.')
            return poster

    (El "if poster and ..." es porque, si no subieron nada, poster está vacío.)
  - Para un FileField, qué extensiones se permiten:
        from django.core.validators import FileExtensionValidator
        guion = models.FileField(..., validators=[FileExtensionValidator(['pdf'])])


=======================================================================
PARTE 7 — BORRAR LOS ARCHIVOS VIEJOS
=======================================================================
Django NO borra el archivo de la carpeta cuando cambiás la imagen o borrás
la película. Si no lo hacés vos, la carpeta media/ se llena de basura.

  - Al BORRAR la película:
        if pelicula.poster:
            pelicula.poster.delete(save=False)     <- primero el archivo...
        pelicula.delete()                          <- ...después la película

  - Al CAMBIAR la imagen, en la vista de editar. El truco: anotar cuál era
    la vieja ANTES de guardar el formulario (después, ya es la nueva):
        viejo = pelicula.poster                    <- antes de armar el formulario
        ...
        nueva = form.save()
        if viejo and viejo != nueva.poster:        <- cambió (o la sacaron con "Limpiar")
            viejo.delete(save=False)
    Si solo cambiaron el título y no la imagen, viejo == nueva.poster, y no se borra nada.


=======================================================================
PARTE 8 — PLANILLAS: DESCARGAR E IMPORTAR (CSV)
=======================================================================
Un CSV es una planilla guardada como TEXTO: cada fila es una línea, y las
columnas se separan con un signo. Excel lo abre y lo guarda. Como Excel en
castellano usa la coma para los decimales, separa las columnas con ";":

        titulo;anio              <- la primera fila: los títulos de las columnas
        Toy Story;1995
        Coco;2017

  a) DESCARGAR (exportar): una vista puede devolver un ARCHIVO en vez de una página.

        import csv
        from django.http import HttpResponse

        def exportar(request):
            respuesta = HttpResponse(content_type='text/csv; charset=utf-8')
            respuesta['Content-Disposition'] = 'attachment; filename="peliculas.csv"'   <- "bajalo con este nombre"
            respuesta.write('\\ufeff')                       <- una marca invisible, para que Excel lea bien los acentos
            escritor = csv.writer(respuesta, delimiter=';')
            escritor.writerow(['titulo', 'anio'])             <- la fila de títulos
            for p in Pelicula.objects.all():
                escritor.writerow([p.titulo, p.anio])         <- una fila por película
            return respuesta

     Un link común lo descarga:   <a href="{% url 'exportar' %}">Bajar planilla</a>

  b) IMPORTAR: leer una planilla que sube el usuario, y cargar una película
     por fila.

     El formulario para subirla no es de un modelo (paso 3, PARTE 5):
        class ImportarForm(forms.Form):
            archivo = forms.FileField()

     En la vista, el archivo subido llega en BYTES (no es texto todavía):
        archivo = form.cleaned_data['archivo']
        texto = archivo.read().decode('utf-8-sig')     <- bytes -> texto. 'utf-8-sig' descarta la marca de Excel.
        filas = csv.DictReader(io.StringIO(texto), delimiter=';')
            <- cada fila llega como un DICCIONARIO con los títulos como claves:
               {'titulo': 'Toy Story', 'anio': '1995'}   (¡todo como texto!)

     Si alguien sube algo que no es texto (una foto), .decode() da el error
     UnicodeDecodeError: atajalo y mostrá un mensaje.

     LAS FILAS MALAS: en una planilla de verdad siempre hay alguna (un año
     con letras, una columna de menos, un título vacío...). La regla: la
     fila mala se SALTEA, se anota su número, y se sigue con las demás.
     Lo más fácil y seguro: validar cada fila con el MISMO FORMULARIO de las
     páginas, que ya tiene todas las reglas:

        for numero, fila in enumerate(filas, start=2):     <- start=2: la fila 1 es la de los títulos
            form = PeliculaForm({'titulo': fila.get('titulo'), 'anio': fila.get('anio')})
            if form.is_valid():
                form.save()
            else:
                errores.append(numero)

     OJO, una fila con columnas DE MENOS ("Shrek" sola, sin ";anio"): para
     DictReader, las columnas que faltan valen None. Por eso fila.get(...)
     y el formulario: un None en un campo obligatorio es un error del
     formulario, no un error de Python.

     Si en vez del formulario convertís a mano (int(fila['anio']),
     Decimal(fila['precio'])...), estos son los errores que pueden aparecer
     y hay que atajar:
         KeyError          falta una columna en la fila de títulos
         ValueError        int('dosmil')
         TypeError         int(None) o Decimal(None): la fila tenía columnas de menos
         AttributeError    None.strip(): lo mismo
         InvalidOperation  Decimal('caro')   (from decimal import InvalidOperation)
     y además vas a tener que revisar vos las reglas (no negativo, etc.).
     Por eso conviene el formulario.

     Si para cada fila hay que crear también OTRA cosa (ej: el autor de un
     libro, si no existe), y la fila resulta mala, eso que creaste queda
     guardado igual. Para que no pase: todo lo de la fila adentro de un
     with transaction.atomic(): (paso 2, PARTE B8), y si la fila está mal,
     un raise adentro del with deshace todo lo de esa fila.

  Para probarlo, armá una planilla en el Bloc de notas y guardala como
  peliculas.csv (o en Excel: Guardar como → "CSV delimitado por punto y coma"):

        titulo;anio
        Toy Story;1995
        Coco;2017


=======================================================================
PARTE 9 — EN ACCIÓN (desde acá, el archivo se ejecuta)
=======================================================================
"""

import csv
import io
import logging
import os
import shutil
import sys

try:
    import PIL  # noqa: F401   (solo para revisar que Pillow esté instalado)
except ImportError:
    sys.exit("Esta clase necesita Pillow. Con el entorno activado:  pip install pillow")

import django
from django.apps import AppConfig
from django.conf import settings

BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DB = os.path.join(BASE, "clase5.sqlite3")
CARPETA_MEDIA = os.path.join(BASE, "media_clase5")      # el "media/" de esta clase


class ClaseConfig(AppConfig):            # MAQUINARIA DE LA CLASE
    name = "__main__"
    label = "clase"


# ── Los TEMPLATES (→ en tu proyecto: un archivo .html cada uno) ──
TEMPLATES_DE_LA_CLASE = {
    "base.html": """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Películas</title>
<style>body{font-family:sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem} .mensaje{background:#e6f4ea;padding:.5rem}
 .error{background:#fde8e8} img{max-width:160px;display:block}</style></head><body>
<nav><a href="{% url 'lista' %}">Películas</a> · <a href="{% url 'crear' %}">+ Nueva</a> ·
<a href="{% url 'exportar' %}">Bajar planilla</a> · <a href="{% url 'importar' %}">Importar planilla</a></nav>
{% for m in messages %}<p class="mensaje {{ m.tags }}">{{ m }}</p>{% endfor %}
{% block contenido %}{% endblock %}</body></html>""",

    "lista.html": """{% extends "base.html" %}{% block contenido %}<h1>Películas</h1>
{% for p in peliculas %}
  <div>{% if p.poster %}<img src="{{ p.poster.url }}" alt="Póster de {{ p.titulo }}">{% endif %}
  <a href="{% url 'editar' p.pk %}">{{ p.titulo }}</a> ({{ p.anio }})
  <form method="post" action="{% url 'borrar' p.pk %}" style="display:inline">{% csrf_token %}<button>Borrar</button></form></div>
{% empty %}<p>No hay películas.</p>{% endfor %}{% endblock %}""",

    "form.html": """{% extends "base.html" %}{% block contenido %}<h1>{{ titulo }}</h1>
{# enctype: SIN esto la imagen no viaja (PARTE 4) #}
<form method="post" enctype="multipart/form-data">{% csrf_token %}{{ form.as_p }}<button>Guardar</button></form>
{% endblock %}""",

    "importar.html": """{% extends "base.html" %}{% block contenido %}<h1>Importar películas</h1>
<p>Una planilla CSV separada por <b>;</b> con las columnas <code>titulo;anio</code>.</p>
<form method="post" enctype="multipart/form-data">{% csrf_token %}{{ form.as_p }}<button>Importar</button></form>
{% endblock %}""",
}

# ── MAQUINARIA DE LA CLASE: la configuración (→ en tu proyecto: config/settings.py) ──
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
    MEDIA_URL="/media/",                 # PARTE 2
    MEDIA_ROOT=CARPETA_MEDIA,            # PARTE 2
    LANGUAGE_CODE="es-ar",
    TIME_ZONE="America/Argentina/Buenos_Aires",
    USE_TZ=True,
    DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
)
django.setup()

from django import forms
from django.conf.urls.static import static
from django.contrib import messages
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path
from django.views.decorators.http import require_POST

MAXIMO = 2 * 1024 * 1024    # 2 MB, en bytes


# ── El MODELO (→ models.py) ──
class Pelicula(models.Model):
    titulo = models.CharField("título", max_length=120)
    anio = models.PositiveIntegerField("año")
    poster = models.ImageField("póster", upload_to="posters/", blank=True)        # PARTE 3

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo


# ── Los FORMULARIOS (→ forms.py) ──
class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ["titulo", "anio", "poster"]

    def clean_poster(self):                                                       # PARTE 6
        poster = self.cleaned_data.get("poster")
        if poster and poster.size > MAXIMO:
            raise forms.ValidationError("La imagen no puede pesar más de 2 MB.")
        return poster


class ImportarForm(forms.Form):                                                   # PARTE 8b
    archivo = forms.FileField(label="Planilla (.csv)")


# ── Las VISTAS (→ views.py) ──
def lista(request):
    return render(request, "lista.html", {"peliculas": Pelicula.objects.all()})


def crear(request):
    form = PeliculaForm(request.POST or None, request.FILES or None)              # PARTE 4: request.FILES
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Guardada.")
        return redirect("lista")
    return render(request, "form.html", {"form": form, "titulo": "Nueva película"})


def editar(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    viejo = pelicula.poster                     # PARTE 7: el que tenía ANTES de cambiar nada
    form = PeliculaForm(request.POST or None, request.FILES or None, instance=pelicula)
    if request.method == "POST" and form.is_valid():
        nueva = form.save()
        if viejo and viejo != nueva.poster:     # cambió (o lo sacaron): el archivo viejo se borra
            viejo.delete(save=False)
        messages.success(request, "Cambios guardados.")
        return redirect("lista")
    return render(request, "form.html", {"form": form, "titulo": f"Editar «{pelicula}»"})


@require_POST
def borrar(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if pelicula.poster:
        pelicula.poster.delete(save=False)      # PARTE 7: primero el archivo...
    pelicula.delete()                           # ...después la película
    messages.success(request, "Borrada (con su póster).")
    return redirect("lista")


def exportar(request):                                                            # PARTE 8a
    respuesta = HttpResponse(content_type="text/csv; charset=utf-8")
    respuesta["Content-Disposition"] = 'attachment; filename="peliculas.csv"'
    respuesta.write("﻿")                   # la marca para que Excel lea bien los acentos
    escritor = csv.writer(respuesta, delimiter=";")
    escritor.writerow(["titulo", "anio"])
    for p in Pelicula.objects.all():
        escritor.writerow([p.titulo, p.anio])
    return respuesta


def importar(request):                                                            # PARTE 8b
    form = ImportarForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        try:
            texto = form.cleaned_data["archivo"].read().decode("utf-8-sig")
        except UnicodeDecodeError:
            messages.error(request, "Ese archivo no es una planilla CSV.")
            return redirect("importar")
        creadas, errores = 0, []
        for numero, fila in enumerate(csv.DictReader(io.StringIO(texto), delimiter=";"), start=2):
            datos = PeliculaForm({"titulo": fila.get("titulo"), "anio": fila.get("anio")})   # cada fila, con el formulario
            if datos.is_valid():
                datos.save()
                creadas += 1
            else:
                errores.append(numero)          # la fila mala se saltea y se anota
        messages.success(request, f"Se importaron {creadas} películas.")
        if errores:
            messages.error(request, f"Filas con errores (no se cargaron): {', '.join(map(str, errores))}.")
        return redirect("lista")
    return render(request, "importar.html", {"form": form})


# ── Las URLS (→ urls.py) ──
urlpatterns = [
    path("", lista, name="lista"),
    path("nueva/", crear, name="crear"),
    path("<int:pk>/editar/", editar, name="editar"),
    path("<int:pk>/borrar/", borrar, name="borrar"),
    path("exportar/", exportar, name="exportar"),
    path("importar/", importar, name="importar"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)                 # PARTE 2


def preparar_base():
    """MAQUINARIA: crear la tabla (en tu proyecto: migrate) y una película de ejemplo."""
    from django.db import connection
    if Pelicula._meta.db_table not in connection.introspection.table_names():
        with connection.schema_editor() as editor:
            editor.create_model(Pelicula)
    if not Pelicula.objects.exists():
        Pelicula.objects.create(titulo="Matrix", anio=1999)


# =======================================================================
# PARTE 10 — LA SIMULACIÓN
# =======================================================================
# Empieza con una sola película (Matrix, sin póster).
# Debajo de cada paso está anotado lo que muestra.

def simular():
    from django.core.files.uploadedfile import SimpleUploadedFile
    from django.test import Client
    from django.test.utils import setup_test_environment
    from PIL import Image

    setup_test_environment()                                       # MAQUINARIA
    logging.getLogger("django.request").setLevel(logging.ERROR)    # MAQUINARIA
    navegador = Client()

    def imagen(nombre, color="red", lado=60):
        """MAQUINARIA: fabrica una imagen PNG de verdad (un cuadrado de un color), como si la subiera alguien."""
        buffer = io.BytesIO()
        Image.new("RGB", (lado, lado), color).save(buffer, "PNG")
        return SimpleUploadedFile(nombre, buffer.getvalue(), content_type="image/png")

    def archivos():
        """Qué archivos hay en la carpeta media_clase5/posters."""
        carpeta = os.path.join(CARPETA_MEDIA, "posters")
        return sorted(os.listdir(carpeta)) if os.path.isdir(carpeta) else []

    print()
    print("========== PARTE 10: la simulación ==========")

    print()
    print("1) Subir una película CON póster")
    # follow=True: el navegador sigue la redirección (así se ven los mensajes)
    navegador.post("/nueva/", {"titulo": "Up", "anio": 2009, "poster": imagen("up.png")}, follow=True)
    up = Pelicula.objects.get(titulo="Up")
    print("   en la base se guardó el nombre:", up.poster.name)
    print("   su dirección:", up.poster.url)
    print("   pesa:", up.poster.size, "bytes")
    print("   en la carpeta posters:", archivos())
    # Muestra:
    #   1) Subir una película CON póster
    #      en la base se guardó el nombre: posters/up.png
    #      su dirección: /media/posters/up.png
    #      pesa: 175 bytes                      <- (puede variar un poco)
    #      en la carpeta posters: ['up.png']

    print()
    print("2) Subir algo que NO es una imagen (un texto, con nombre .png)")
    falsa = SimpleUploadedFile("virus.png", b"no soy una imagen", "image/png")
    r = navegador.post("/nueva/", {"titulo": "Trucha", "anio": 2000, "poster": falsa})
    print("   errores:", dict(r.context["form"].errors))
    # Muestra:
    #   2) Subir algo que NO es una imagen (un texto, con nombre .png)
    #      errores: {'poster': ['Seleccione una imagen válida. El archivo que ha seleccionado no es
    #               una imagen o es un archivo de imagen corrupto.']}
    # El nombre no importa: ImageField mira el contenido.

    print()
    print("3) Subir una imagen de más de 2 MB")
    # Una imagen DE VERDAD de casi 3 MB: puntos de colores al azar (así no se puede achicar)
    buffer = io.BytesIO()
    Image.frombytes("RGB", (1000, 1000), os.urandom(1000 * 1000 * 3)).save(buffer, "PNG")
    print(f"   (la imagen pesa {len(buffer.getvalue()) / 1024 / 1024:.1f} MB)")
    grande = SimpleUploadedFile("grande.png", buffer.getvalue(), content_type="image/png")
    r = navegador.post("/nueva/", {"titulo": "Pesada", "anio": 2000, "poster": grande})
    print("   errores:", dict(r.context["form"].errors))
    # Muestra:
    #   3) Subir una imagen de más de 2 MB
    #      (la imagen pesa 2.9 MB)
    #      errores: {'poster': ['La imagen no puede pesar más de 2 MB.']}     <- nuestro clean_poster

    print()
    print("4) Cambiarle el póster a Up (el viejo se tiene que borrar de la carpeta)")
    navegador.post(f"/{up.pk}/editar/", {"titulo": "Up", "anio": 2009, "poster": imagen("up2.png", "blue")},
                   follow=True)
    print("   en la carpeta posters:", archivos())
    # Muestra:
    #   4) Cambiarle el póster a Up (el viejo se tiene que borrar de la carpeta)
    #      en la carpeta posters: ['up2.png']           <- up.png ya no está

    print()
    print("5) Borrar Up (se tiene que borrar también su póster)")
    navegador.post(f"/{up.pk}/borrar/", follow=True)
    print("   en la carpeta posters:", archivos())
    # Muestra:
    #   5) Borrar Up (se tiene que borrar también su póster)
    #      en la carpeta posters: []

    print()
    print("6) Importar una planilla con 5 filas (3 tienen errores)")
    planilla = (
        "titulo;anio\n"          # fila 1: los títulos
        "Toy Story;1995\n"       # fila 2: bien
        "Shrek;dosmil\n"         # fila 3: el año tiene letras
        "Coco;2017\n"            # fila 4: bien
        "Solo el título\n"       # fila 5: le falta una columna (el año llega como None)
        ";2020\n"                # fila 6: el título está vacío
    ).encode("utf-8")            # .encode(): texto -> bytes, como llega un archivo subido
    r = navegador.post("/importar/", {"archivo": SimpleUploadedFile("pelis.csv", planilla, "text/csv")},
                       follow=True)
    print("   mensajes:", [str(m) for m in r.context["messages"]])
    # Muestra:
    #   6) Importar una planilla con 5 filas (3 tienen errores)
    #      mensajes: ['Se importaron 2 películas.', 'Filas con errores (no se cargaron): 3, 5, 6.']

    print()
    print("7) Descargar la planilla")
    r = navegador.get("/exportar/")
    print("   tipo:", r["Content-Type"])
    print("   cómo se descarga:", r["Content-Disposition"])
    print("   contenido:")
    for linea in r.content.decode("utf-8-sig").splitlines():
        print("     ", linea)
    # Muestra:
    #   7) Descargar la planilla
    #      tipo: text/csv; charset=utf-8
    #      cómo se descarga: attachment; filename="peliculas.csv"
    #      contenido:
    #        titulo;anio
    #        Coco;2017
    #        Matrix;1999
    #        Toy Story;1995

    print()
    print("Ahora probala de verdad:   python paso_5_imagenes_y_archivos\\clase.py runserver")
    print("y abrí http://127.0.0.1:8000 (Ctrl+C en la terminal para apagarlo).")


def limpiar():
    """MAQUINARIA: borrar la base y la carpeta de imágenes de la clase."""
    from django.db import connection
    connection.close()
    if os.path.exists(ARCHIVO_DB):
        os.remove(ARCHIVO_DB)
    shutil.rmtree(CARPETA_MEDIA, ignore_errors=True)


# =======================================================================
# RESUMEN
# =======================================================================
#  settings        MEDIA_URL = '/media/'   MEDIA_ROOT = BASE_DIR / 'media'
#  urls            + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#  modelo          models.ImageField(upload_to='carpeta/', blank=True)      (necesita Pillow)
#  form HTML       <form method="post" enctype="multipart/form-data">
#  vista           Form(request.POST, request.FILES)
#  mostrar         {% if p.poster %}<img src="{{ p.poster.url }}">{% endif %}
#  validar         clean_<campo>: archivo.size > 2 * 1024 * 1024
#  borrar archivo  campo.delete(save=False)   (al borrar el objeto y al reemplazar la imagen)
#  exportar        HttpResponse(content_type='text/csv') + Content-Disposition + csv.writer(..., delimiter=';')
#  importar        .read().decode('utf-8-sig') + csv.DictReader(io.StringIO(texto), delimiter=';')
#                  cada fila validada con el formulario; las malas se anotan y se sigue


# MAQUINARIA: arrancar en modo simulación o en modo servidor
if __name__ == "__main__":
    if len(sys.argv) == 1:
        limpiar()
        preparar_base()
        simular()
        limpiar()
        print()
        print("Fin de la clase 5. Ahora abrí ejercicio.md (está en esta misma carpeta).")
    else:
        preparar_base()
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
