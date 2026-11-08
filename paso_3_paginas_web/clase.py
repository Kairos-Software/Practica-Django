"""
=======================================================================
 PASO 3 — PÁGINAS WEB: URLS, VISTAS, TEMPLATES Y FORMULARIOS
=======================================================================

Hasta ahora todo se hacía desde la consola o desde el admin. Ahora vas a
hacer PÁGINAS: lo que alguien abre en el navegador para usar tu sistema.

El ejemplo de toda la clase: una mini VIDEOTECA (películas).


ANTES DE ESTE ARCHIVO
---------------------
Abrí primero  clase_0_html_basico.html  (en esta misma carpeta) con DOBLE
CLIC: se abre en el navegador. Ahí está lo mínimo de HTML, el idioma con el
que se escriben las páginas. Después volvé acá.


¿QUÉ NECESITÁS?
---------------
El entorno virtual activado, con Django instalado (como en el paso 2).
La línea de la terminal tiene que empezar con (entorno).


CÓMO SE USA ESTE ARCHIVO
------------------------
Se puede ejecutar de DOS formas, parado en la carpeta "Aprender Django":

  1) SIMULACIÓN (sin navegador):

         python paso_3_paginas_web\\clase.py

     El archivo hace de navegador: "visita" las páginas una por una y te
     muestra qué respondió cada una. Al final de este archivo (PARTE 10)
     está anotado lo que muestra cada visita.

  2) LA PÁGINA DE VERDAD:

         python paso_3_paginas_web\\clase.py runserver

     Prende un servidor. Abrí el navegador en  http://127.0.0.1:8000
     y vas a ver la videoteca: una lista de películas, un buscador, y
     links para ver, crear, editar y borrar. Probá todo.
     La terminal queda OCUPADA mientras el servidor está prendido (ahí
     aparece cada visita). Para apagarlo: Ctrl+C en la terminal.
     (Crea un archivo clase3.sqlite3 al lado de este: se puede borrar.)

Leé el archivo de arriba a abajo: las PARTES 1 a 8 explican, y la PARTE 9
es el código de la videoteca que se ejecuta.

Un detalle: en un proyecto de verdad, cada pieza va en SU archivo
(urls.py, views.py, forms.py, templates/...). Acá está todo junto para que
se pueda ejecutar con un solo comando. Cada pieza dice dónde iría en tu
proyecto con "→ en tu proyecto: ...". Las partes marcadas como MAQUINARIA
DE LA CLASE no hace falta entenderlas ni copiarlas.


=======================================================================
PARTE 1 — QUÉ PASA CUANDO ABRÍS UNA PÁGINA
=======================================================================
Pensalo como un restaurante:

  - El NAVEGADOR (Chrome, Firefox...) es el cliente: hace un PEDIDO.
  - Django es la cocina: recibe el pedido y prepara la RESPUESTA.

  Navegador                         Django
  ─────────                         ──────
  "quiero /peliculas/3/"   ──►  1. urls.py: ¿qué VISTA atiende la dirección "peliculas/3/"?
                                2. la VISTA (una función de Python) recibe el
                                   pedido, busca los datos con los MODELOS (paso 2)
                                   y arma la página con un TEMPLATE (HTML con huecos)
  la página (HTML)         ◄──  3. devuelve la respuesta

Las cuatro piezas, y en qué archivo viven:

  - URL       la dirección ("peliculas/3/").             -> urls.py
  - VISTA     la función que decide qué hacer.           -> views.py
  - TEMPLATE  el HTML, con huecos para los datos.        -> templates/
  - MODELO    los datos (lo del paso 2).                 -> models.py

Palabras que vas a ver todo el tiempo:

  - PEDIDO (request): lo que manda el navegador. Tiene un MÉTODO:
        GET  = "quiero VER algo" (abrir una página, buscar)
        POST = "quiero CAMBIAR algo" (mandar un formulario para guardar o borrar)
  - RESPUESTA (response): lo que devuelve Django, con un CÓDIGO (un número)
    que dice cómo salió:
        200  OK: acá está la página
        302  REDIRIGE: "andá a esta otra dirección" (el navegador va solo)
        404  NO EXISTE esa página (o ese objeto)
        405  MÉTODO NO PERMITIDO: por ejemplo, un GET donde solo se acepta POST
        500  ERROR en el código de la vista (un error de Python)


=======================================================================
PARTE 2 — URLS: QUÉ DIRECCIÓN VA A QUÉ VISTA
=======================================================================
El proyecto tiene UN urls.py principal (config/urls.py) que reparte las
direcciones a las apps. Cada app tiene el suyo, que hay que CREAR a mano
(startapp no lo crea).

  → en tu proyecto, config/urls.py (ya existe, se le agrega una línea):

        from django.contrib import admin
        from django.urls import include, path

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', include('peliculas.urls')),      <- "todo lo demás, lo atiende la app peliculas"
        ]

  → en tu proyecto, peliculas/urls.py (archivo NUEVO):

        from django.urls import path
        from . import views                           <- las vistas de esta app

        app_name = 'peliculas'                        <- el "apellido" de los nombres (ver abajo)
        urlpatterns = [
            path('', views.lista, name='lista'),
            path('<int:pk>/', views.detalle, name='detalle'),
            path('nueva/', views.crear, name='crear'),
            path('<int:pk>/editar/', views.editar, name='editar'),
            path('<int:pk>/borrar/', views.borrar, name='borrar'),
        ]

Cada path() dice: "esta dirección → esta vista, y se llama así".

  - '<int:pk>/' es una parte VARIABLE de la dirección: si alguien abre
    "3/", la vista recibe un parámetro pk=3. (int = tiene que ser un
    número; si escriben letras, da 404.) pk quiere decir "primary key", el id.
  - Las direcciones terminan con barra: 'nueva/', no 'nueva'.
  - name='detalle' le pone un NOMBRE a la dirección. En el resto del código
    NUNCA se escribe "/peliculas/3/" a mano: se pide por nombre, con el
    apellido adelante: 'peliculas:detalle'. Si mañana cambiás la dirección,
    se actualiza sola en todos lados.


=======================================================================
PARTE 3 — VISTAS: LA FUNCIÓN QUE ARMA LA RESPUESTA
=======================================================================
Una vista es una función que recibe el pedido (request) y devuelve una
respuesta. Mirá la vista "detalle" en la PARTE 9. Las herramientas que más
vas a usar (todas se importan de django.shortcuts):

  render(request, 'peliculas/lista.html', {'peliculas': peliculas})
      arma el HTML usando ese template y esos datos. El diccionario del
      final se llama CONTEXTO: cada clave es un nombre que el template
      puede usar ({{ peliculas }}).

  get_object_or_404(Pelicula, pk=pk)
      trae el objeto; si no existe, responde "404 no existe" (en vez de
      un error 500).

  redirect('peliculas:detalle', pk=pelicula.pk)
      responde "andá a esta otra página" (código 302). Se usa después de
      guardar o borrar algo.

Y del pedido (request) se leen:

  request.method              'GET' o 'POST'
  request.GET.get('q', '')    lo que viene en la DIRECCIÓN: /?q=toy  ->  'toy'
                              (el '' es el valor si no vino nada: como el .get() del paso 0)
  request.POST                lo que se mandó con un formulario POST


=======================================================================
PARTE 4 — TEMPLATES: EL HTML CON HUECOS
=======================================================================
  → en tu proyecto: peliculas/templates/peliculas/lista.html
    (sí, "peliculas" dos veces: es la costumbre, para que no se mezclen
    templates de apps distintas con el mismo nombre. Django los encuentra
    solo. En la vista se piden como 'peliculas/lista.html'.)

Un template es HTML normal con dos tipos de "huecos":

  {{ algo }}          MOSTRAR un dato del contexto
                      {{ pelicula.titulo }}   (con punto, como en Python)
  {% algo %}          una ORDEN: un for, un if, un link...

Los más usados:

  {% for p in peliculas %}            repetir una vez por cada película
      <li>{{ p.titulo }}</li>
  {% empty %}                         (si la lista está vacía)
      <li>No hay películas.</li>
  {% endfor %}                        (todo lo que se abre, se cierra)

  {% if p.vista %} Sí {% elif p.anio > 2000 %} Nueva {% else %} No {% endif %}

  {% url 'peliculas:detalle' p.pk %}  la DIRECCIÓN por su nombre -> /3/
  {% csrf_token %}                    OBLIGATORIO adentro de todo <form method="post">
                                      (una protección: ver la PARTE 5)
  {# un comentario #}

FILTROS: cambian CÓMO se muestra un dato. Van con | (la barra vertical):

  {{ p.anio|default:"?" }}            "?" si está vacío
  {{ p.creada|date:"d/m/Y" }}         una fecha como 25/10/2026
  {{ peliculas|length }}              cuántos elementos tiene una lista
  {{ texto|upper }}                   en mayúsculas
  {{ texto|truncatechars:30 }}        cortado a 30 letras, con "…"
  {{ p.vista|yesno:"Vista,Sin ver" }} un texto para True y otro para False
  {{ n }} libro{{ n|pluralize }}      agrega una "s" si n no es 1:
                                      "1 libro", "2 libros", "0 libros"

Lo que se muestra con {{ }} se ESCAPA solo: si alguien guarda un título con
<script>, se muestra como texto, no se ejecuta. Es una protección gratis.

HERENCIA DE TEMPLATES: lo que se repite en todas las páginas (el <head>, el
menú, los mensajes) va en un base.html, con "huecos" llamados block. Cada
página dice "soy como base.html, y en este hueco va esto":

    base.html:    <html> ... <nav>el menú</nav>
                  {% block contenido %}{% endblock %}
                  ... </html>

    lista.html:   {% extends "peliculas/base.html" %}       <- SIEMPRE la primera línea
                  {% block contenido %}
                      ...lo propio de esta página...
                  {% endblock %}

Mirá los templates de la PARTE 9: son de verdad, y funcionan.


=======================================================================
PARTE 5 — FORMULARIOS
=======================================================================
Un ModelForm arma el formulario A PARTIR DEL MODELO: los campos, el tipo de
cada uno, y la VALIDACIÓN (incluido el clean() del modelo del paso 2).

  → en tu proyecto, peliculas/forms.py (archivo NUEVO):

        from django import forms
        from .models import Pelicula

        class PeliculaForm(forms.ModelForm):
            class Meta:
                model = Pelicula
                fields = ['titulo', 'anio', 'minutos', 'vista']     <- qué campos muestra

Validación propia de UN campo: un método clean_<campo>. Recibe el dato ya
convertido en self.cleaned_data['campo'], y devuelve el valor, o provoca un
ValidationError con el mensaje (que aparece al lado del campo):

            def clean_minutos(self):
                minutos = self.cleaned_data['minutos']
                if minutos < 1:
                    raise forms.ValidationError('Tiene que durar al menos 1 minuto.')
                return minutos                   <- ¡no te olvides de devolverlo!

El "BAILE" de siempre en una vista que CREA (memorizalo):

    def crear(request):
        if request.method == 'POST':                 # 1. mandaron el formulario
            form = PeliculaForm(request.POST)        #    lo llenamos con lo que mandaron
            if form.is_valid():                      #    ¿está todo bien? (valida TODO)
                pelicula = form.save()               #    guarda en la base
                return redirect('peliculas:detalle', pk=pelicula.pk)   # y vamos a otra página
            # si NO es válido, sigue de largo: abajo se muestra de nuevo, CON los errores
        else:                                        # 2. GET: recién entra a la página
            form = PeliculaForm()                    #    el formulario vacío
        return render(request, 'peliculas/form.html', {'form': form})

  - Para EDITAR es igual, pero diciendo CUÁL se edita, con instance=:
        PeliculaForm(request.POST, instance=pelicula)     y     PeliculaForm(instance=pelicula)
  - ¿Por qué redirect después de guardar? Si no, al apretar F5 el navegador
    vuelve a mandar el formulario y se guarda DOS veces.
  - En el template, {{ form.as_p }} dibuja todos los campos con sus errores.
  - Forma corta (y común) del baile:  form = PeliculaForm(request.POST or None)
        -> con los datos si es POST, vacío si es GET. Y después:
           if request.method == 'POST' and form.is_valid(): ...

BORRAR (y todo lo que cambia datos) SIEMPRE con POST: un botón adentro de un
<form method="post">, nunca un link. Un link lo puede "visitar" cualquiera
(o un buscador de internet) y borrarte todo. Si querés una página
"¿Seguro?": la vista muestra la pregunta con GET, y borra recién cuando
llega el POST del botón.
Para que una vista acepte SOLO POST (con GET responde 405):
        from django.views.decorators.http import require_POST
        @require_POST                    <- un "decorador": va justo arriba del def
        def borrar(request, pk): ...

¿Y el {% csrf_token %}? Es una protección: sin él, otra página de internet
podría mandar formularios a TU sistema haciéndose pasar por tu usuario.
Django rechaza todo POST que no lo tenga ("CSRF verification failed").

Si al objeto le falta algo que NO viene del formulario (ej: un comentario
tiene que saber de qué película es), se guarda en dos pasos:

        comentario = form.save(commit=False)     <- arma el objeto SIN guardarlo
        comentario.pelicula = pelicula           <- le completás lo que falta
        comentario.save()                        <- ahora sí

Un formulario que arranca con algo YA elegido (ej: "Nueva película" desde
una categoría): initial
        form = PeliculaForm(initial={'categoria': request.GET.get('categoria')})
    (y el link:  {% url 'peliculas:crear' %}?categoria={{ categoria.pk }})

Un formulario que NO guarda un modelo (ej: pedir una cantidad) es forms.Form:

        class CantidadForm(forms.Form):
            cantidad = forms.IntegerField(min_value=1)

    En la vista:  form = CantidadForm(request.POST)
                  if form.is_valid():
                      cantidad = form.cleaned_data['cantidad']    <- ya es un int, validado
    (No tiene .save(): con el dato hacés lo que necesites.)


=======================================================================
PARTE 6 — MENSAJES ("Se guardó bien")
=======================================================================
Un mensaje que se muestra UNA vez, en la página siguiente (aunque haya un
redirect en el medio):

    from django.contrib import messages
    messages.success(request, 'Película guardada.')      (también .error, .warning, .info)

y en base.html se muestran todos con:
    {% for mensaje in messages %}<p>{{ mensaje }}</p>{% endfor %}

Ya viene configurado en todo proyecto nuevo de Django.

Muy útil con los errores del modelo (paso 2): si un método provoca un
ValueError, la vista lo ataja y lo muestra como mensaje:

    try:
        pelicula.alquilar(cantidad)                  <- un método del modelo que puede dar ValueError
        messages.success(request, 'Alquilada.')
    except ValueError as error:
        messages.error(request, str(error))          <- str(error) = el texto del error
    return redirect('peliculas:detalle', pk=pelicula.pk)


=======================================================================
PARTE 7 — PAGINAR (DE A N POR PÁGINA)
=======================================================================
Si hay 500 películas, no se muestran todas juntas: de a 10, con "Anterior" y
"Siguiente".

  En la vista:
    from django.core.paginator import Paginator
    pagina = Paginator(peliculas, 10).get_page(request.GET.get('pagina'))     # /?pagina=2

  En el template, "pagina" se recorre como si fuera la lista:
    {% for p in pagina %} ... {% endfor %}
    Página {{ pagina.number }} de {{ pagina.paginator.num_pages }}
    {% if pagina.has_previous %}<a href="?pagina={{ pagina.previous_page_number }}">Anterior</a>{% endif %}
    {% if pagina.has_next %}<a href="?pagina={{ pagina.next_page_number }}">Siguiente</a>{% endif %}

OJO: si la lista tiene filtros (/?q=toy), el link a la otra página tiene que
llevarlos también (/?q=toy&pagina=2), o se pierden. Una forma, en la vista:
        filtros = request.GET.copy()          <- una copia de lo que vino en la dirección
        filtros.pop('pagina', None)           <- sin la página
        ... {'filtros': filtros.urlencode()}  <- como texto: "q=toy"
    y en el link:   ?{{ filtros }}&pagina={{ pagina.next_page_number }}

OJO 2: si la lista se armó con annotate() (paso 2, PARTE B6), ponele un
.order_by(...): sin orden fijo, el Paginator avisa que los resultados
pueden salir mezclados.


=======================================================================
PARTE 8 — CSS E IMÁGENES PROPIAS (archivos "estáticos")
=======================================================================
Tu CSS, tu logo, tu JavaScript: van en  peliculas/static/peliculas/estilo.css
y en el template:
    {% load static %}                          <- una vez, arriba (después del extends)
    <link rel="stylesheet" href="{% static 'peliculas/estilo.css' %}">
(El diseño es OPCIONAL en este curso: con HTML simple alcanza.)


=======================================================================
PARTE 9 — LA MINI VIDEOTECA (desde acá, el archivo se ejecuta)
=======================================================================
"""

import logging
import os
import sys

import django
from django.apps import AppConfig
from django.conf import settings

BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DB = os.path.join(BASE, "clase3.sqlite3")


class ClaseConfig(AppConfig):            # MAQUINARIA DE LA CLASE
    name = "__main__"
    label = "clase"


# ── Los TEMPLATES ──
# → en tu proyecto: cada uno es un archivo .html en peliculas/templates/peliculas/
#   (acá están escritos como textos, para que todo entre en un solo archivo)
TEMPLATES_DE_LA_CLASE = {
    # base.html: lo que se repite en TODAS las páginas
    "base.html": """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block titulo %}Videoteca{% endblock %}</title>
  <style>
    body { font-family: sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; }
    nav a { margin-right: 1rem; }
    .mensaje { background: #e6f4ea; padding: .5rem 1rem; border-radius: 6px; }
    table { border-collapse: collapse; width: 100%; }
    td, th { border-bottom: 1px solid #ddd; padding: .4rem; text-align: left; }
  </style>
</head>
<body>
  <nav>
    <a href="{% url 'lista' %}">Películas</a>
    <a href="{% url 'crear' %}">+ Nueva</a>
  </nav>
  {% for mensaje in messages %}<p class="mensaje">{{ mensaje }}</p>{% endfor %}
  {% block contenido %}{% endblock %}
</body>
</html>""",

    # lista.html: la tabla de películas, con el buscador
    "lista.html": """{% extends "base.html" %}
{% block contenido %}
<h1>Películas ({{ peliculas|length }})</h1>
<form method="get">
  <input name="q" value="{{ q }}" placeholder="Buscar por título">
  <button>Buscar</button>
  {% if q %}<a href="{% url 'lista' %}">Limpiar</a>{% endif %}
</form>
<table>
  <tr><th>Título</th><th>Año</th><th>¿Vista?</th></tr>
  {% for pelicula in peliculas %}
  <tr>
    <td><a href="{% url 'detalle' pelicula.pk %}">{{ pelicula.titulo }}</a></td>
    <td>{{ pelicula.anio }}</td>
    <td>{% if pelicula.vista %}Sí{% else %}No{% endif %}</td>
  </tr>
  {% empty %}
  <tr><td colspan="3">No hay películas{% if q %} con "{{ q }}"{% endif %}.</td></tr>
  {% endfor %}
</table>
{% endblock %}""",

    # detalle.html: una película, con los botones de editar y borrar
    "detalle.html": """{% extends "base.html" %}
{% block titulo %}{{ pelicula.titulo }}{% endblock %}
{% block contenido %}
<h1>{{ pelicula.titulo }}</h1>
<p>Año {{ pelicula.anio }} · {{ pelicula.minutos }} minutos · {{ pelicula.vista|yesno:"Vista,Sin ver" }}</p>
<p>Cargada el {{ pelicula.creada|date:"d/m/Y H:i" }}</p>
<a href="{% url 'editar' pelicula.pk %}">Editar</a>
<form method="post" action="{% url 'borrar' pelicula.pk %}" style="display:inline">
  {% csrf_token %}
  <button onclick="return confirm('¿Borrar {{ pelicula.titulo|escapejs }}?')">Borrar</button>
</form>
{% endblock %}""",

    # form.html: el MISMO template sirve para crear y para editar
    "form.html": """{% extends "base.html" %}
{% block contenido %}
<h1>{% if pelicula %}Editar «{{ pelicula.titulo }}»{% else %}Nueva película{% endif %}</h1>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button>Guardar</button>
</form>
{% endblock %}""",
}
# {{ form.as_p }} dibuja todos los campos con sus errores. Para elegir vos
# cómo se ve cada campo, se dibujan a mano:
#     {{ form.titulo.label_tag }} {{ form.titulo }} {{ form.titulo.errors }}


# ── MAQUINARIA DE LA CLASE: la configuración ──
# → en tu proyecto: config/settings.py (ya viene casi todo hecho por startproject)
settings.configure(
    DEBUG=True,
    SECRET_KEY="solo-para-la-clase",
    ALLOWED_HOSTS=["*"],
    ROOT_URLCONF="__main__",                   # las urls están en este mismo archivo
    INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.messages", "__main__.ClaseConfig"],
    MIDDLEWARE=[
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",      # la protección del {% csrf_token %}
        "django.contrib.messages.middleware.MessageMiddleware",
    ],
    MESSAGE_STORAGE="django.contrib.messages.storage.cookie.CookieStorage",
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ARCHIVO_DB}},
    TEMPLATES=[{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "loaders": [("django.template.loaders.locmem.Loader", TEMPLATES_DE_LA_CLASE)],
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }],
    LANGUAGE_CODE="es-ar",
    TIME_ZONE="America/Argentina/Buenos_Aires",
    USE_TZ=True,
)
django.setup()

from django import forms
from django.contrib import messages
from django.db import connection, models
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path
from django.views.decorators.http import require_POST


# ── El MODELO (→ en tu proyecto: peliculas/models.py) ──
class Pelicula(models.Model):
    titulo = models.CharField("título", max_length=120)
    anio = models.PositiveIntegerField("año")
    minutos = models.PositiveIntegerField(default=90)
    vista = models.BooleanField("¿ya la vi?", default=False)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo


# ── El FORMULARIO (→ en tu proyecto: peliculas/forms.py) ──
class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ["titulo", "anio", "minutos", "vista"]

    # Validación propia del campo "titulo" (PARTE 5)
    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].strip()
        if titulo.lower() == "prueba":
            raise forms.ValidationError("Poné un título de verdad.")
        return titulo


# ── Las VISTAS (→ en tu proyecto: peliculas/views.py) ──
def lista(request):
    q = request.GET.get("q", "").strip()            # /?q=toy  ->  "toy"   (si no vino, "")
    peliculas = Pelicula.objects.all()
    if q:                                           # si buscaron algo, filtramos
        peliculas = peliculas.filter(titulo__icontains=q)
    return render(request, "lista.html", {"peliculas": peliculas, "q": q})


def detalle(request, pk):                            # pk llega de la dirección: <int:pk>
    pelicula = get_object_or_404(Pelicula, pk=pk)
    return render(request, "detalle.html", {"pelicula": pelicula})


def crear(request):                                  # el "baile" de la PARTE 5
    if request.method == "POST":
        form = PeliculaForm(request.POST)
        if form.is_valid():
            pelicula = form.save()
            messages.success(request, f"Se guardó «{pelicula.titulo}».")
            return redirect("detalle", pk=pelicula.pk)
    else:
        form = PeliculaForm()
    return render(request, "form.html", {"form": form})


def editar(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if request.method == "POST":
        form = PeliculaForm(request.POST, instance=pelicula)     # instance = editar ESTA
        if form.is_valid():
            form.save()
            messages.success(request, "Cambios guardados.")
            return redirect("detalle", pk=pelicula.pk)
    else:
        form = PeliculaForm(instance=pelicula)                   # con los datos que ya tiene
    return render(request, "form.html", {"form": form, "pelicula": pelicula})


@require_POST                                        # si alguien entra con GET: código 405
def borrar(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    pelicula.delete()
    messages.success(request, f"Se borró «{pelicula.titulo}».")
    return redirect("lista")


# ── Las URLS (→ en tu proyecto: peliculas/urls.py, con app_name = 'peliculas') ──
# (Acá no hay app_name, por eso en los templates es {% url 'detalle' %} y no
#  {% url 'peliculas:detalle' %}. En tu proyecto SÍ va el app_name.)
urlpatterns = [
    path("", lista, name="lista"),
    path("<int:pk>/", detalle, name="detalle"),
    path("nueva/", crear, name="crear"),
    path("<int:pk>/editar/", editar, name="editar"),
    path("<int:pk>/borrar/", borrar, name="borrar"),
]


def preparar_base():
    """MAQUINARIA: crear la tabla (en tu proyecto: migrate) y 3 películas de ejemplo."""
    if Pelicula._meta.db_table not in connection.introspection.table_names():
        with connection.schema_editor() as editor:
            editor.create_model(Pelicula)
    if not Pelicula.objects.exists():
        Pelicula.objects.bulk_create([
            Pelicula(titulo="Toy Story", anio=1995, minutos=81, vista=True),
            Pelicula(titulo="Matrix", anio=1999, minutos=136),
            Pelicula(titulo="Up", anio=2009, minutos=96),
        ])


# =======================================================================
# PARTE 10 — LA SIMULACIÓN: QUÉ RESPONDE CADA PÁGINA
# =======================================================================
# Sin navegador: el "Client" de Django hace de navegador. Es lo mismo que
# usan las PRUEBAS AUTOMÁTICAS de los ejercicios (test_paso3.py).
# Debajo de cada visita está anotado lo que muestra.

SIGNIFICADO = {
    200: "OK: se mostró la página",
    302: "REDIRIGE a otra dirección",
    404: "NO EXISTE",
    405: "MÉTODO NO PERMITIDO",
}


def visita(que, respuesta):
    """Muestra qué se visitó, el código de la respuesta y qué quiere decir."""
    texto = f"código {respuesta.status_code} ({SIGNIFICADO.get(respuesta.status_code, '')})"
    if respuesta.status_code == 302:
        texto += f" -> va a {respuesta['Location']}"
    print()
    print(que)
    print("  ", texto)
    return respuesta


def simular_visitas():
    from django.test import Client
    from django.test.utils import setup_test_environment

    setup_test_environment()                          # MAQUINARIA: para poder mirar el contexto de cada respuesta
    logging.getLogger("django.request").setLevel(logging.ERROR)   # MAQUINARIA: que Django no avise de cada 404/405
    navegador = Client()

    print()
    print("========== PARTE 10: la simulación ==========")

    r = visita("GET /   (la lista)", navegador.get("/"))
    print("   películas que la vista le mandó al template:", list(r.context["peliculas"]))
    # Muestra:
    #   GET /   (la lista)
    #      código 200 (OK: se mostró la página)
    #      películas que la vista le mandó al template: [<Pelicula: Matrix>, <Pelicula: Toy Story>, <Pelicula: Up>]

    r = visita("GET /?q=toy   (buscar 'toy')", navegador.get("/", {"q": "toy"}))
    print("   encontradas:", list(r.context["peliculas"]))
    # Muestra:
    #   GET /?q=toy   (buscar 'toy')
    #      código 200 (OK: se mostró la página)
    #      encontradas: [<Pelicula: Toy Story>]

    matrix = Pelicula.objects.get(titulo="Matrix")
    r = visita(f"GET /{matrix.pk}/   (el detalle de Matrix)", navegador.get(f"/{matrix.pk}/"))
    print("   ¿el HTML dice '136 minutos'?", "136 minutos" in r.content.decode())
    # Muestra:
    #   GET /2/   (el detalle de Matrix)
    #      código 200 (OK: se mostró la página)
    #      ¿el HTML dice '136 minutos'? True
    # (r.content es el HTML que recibiría el navegador.)

    visita("GET /999/   (una película que no existe)", navegador.get("/999/"))
    # Muestra:
    #   GET /999/   (una película que no existe)
    #      código 404 (NO EXISTE)              <- gracias a get_object_or_404

    r = visita("POST /nueva/   con datos MAL (título vacío, año con letras)",
               navegador.post("/nueva/", {"titulo": "", "anio": "abc", "minutos": 90}))
    print("   errores del formulario:", dict(r.context["form"].errors))
    # Muestra:
    #   POST /nueva/   con datos MAL (título vacío, año con letras)
    #      código 200 (OK: se mostró la página)
    #      errores del formulario: {'titulo': ['Este campo es obligatorio.'], 'anio': ['Introduzca un número entero.']}
    # Código 200 y NO redirige: vuelve a mostrar el formulario, con los
    # errores al lado de cada campo. No se guardó nada.

    r = visita("POST /nueva/   con datos BIEN (y el navegador sigue la redirección)",
               navegador.post("/nueva/", {"titulo": "Shrek", "anio": 2001, "minutos": 90}, follow=True))
    print("   pasó por:", r.redirect_chain)
    print("   mensajes:", [str(m) for m in r.context["messages"]])
    # Muestra:
    #   POST /nueva/   con datos BIEN (y el navegador sigue la redirección)
    #      código 200 (OK: se mostró la página)
    #      pasó por: [('/4/', 302)]
    #      mensajes: ['Se guardó «Shrek».']
    # Se guardó, respondió 302 "andá a /4/" (el detalle de Shrek), el
    # navegador fue solo, y ahí apareció el mensaje.

    shrek = Pelicula.objects.get(titulo="Shrek")
    visita(f"POST /{shrek.pk}/editar/   (cambiarle los minutos a Shrek)",
           navegador.post(f"/{shrek.pk}/editar/", {"titulo": "Shrek", "anio": 2001, "minutos": 92}))
    shrek.refresh_from_db()
    print("   minutos ahora:", shrek.minutos)
    # Muestra:
    #   POST /4/editar/   (cambiarle los minutos a Shrek)
    #      código 302 (REDIRIGE a otra dirección) -> va a /4/
    #      minutos ahora: 92

    visita(f"GET /{shrek.pk}/borrar/   (¡con GET no se puede borrar!)", navegador.get(f"/{shrek.pk}/borrar/"))
    # Muestra:
    #   GET /4/borrar/   (¡con GET no se puede borrar!)
    #      código 405 (MÉTODO NO PERMITIDO)     <- gracias a @require_POST

    visita(f"POST /{shrek.pk}/borrar/   (con POST sí)", navegador.post(f"/{shrek.pk}/borrar/"))
    print("   ¿Shrek sigue existiendo?", Pelicula.objects.filter(pk=shrek.pk).exists())
    # Muestra:
    #   POST /4/borrar/   (con POST sí)
    #      código 302 (REDIRIGE a otra dirección) -> va a /
    #      ¿Shrek sigue existiendo? False

    print()
    print("Ahora probala de verdad:   python paso_3_paginas_web\\clase.py runserver")
    print("y abrí http://127.0.0.1:8000 en el navegador (Ctrl+C en la terminal para apagarlo).")


# =======================================================================
# RESUMEN
# =======================================================================
#  urls.py      path('<int:pk>/', views.detalle, name='detalle')     + app_name = 'peliculas'
#  views.py     def detalle(request, pk):
#                   pelicula = get_object_or_404(Pelicula, pk=pk)
#                   return render(request, 'peliculas/detalle.html', {'pelicula': pelicula})
#  template     {% extends %} {% block %} {{ dato }} {% for %} {% if %} {% url 'app:nombre' pk %}
#               filtros: |default |date |length |yesno |pluralize
#  forms.py     class PeliculaForm(forms.ModelForm): class Meta: model, fields     + clean_<campo>
#  el baile     POST -> form(request.POST) -> is_valid() -> save() -> redirect
#               GET  -> form() vacío -> render
#  borrar       siempre con POST (@require_POST) y {% csrf_token %} en el form
#  mensajes     messages.success(request, '...')  y  {% for m in messages %} en base.html
#  paginar      Paginator(lista, 10).get_page(request.GET.get('pagina'))


# MAQUINARIA: arrancar en modo simulación o en modo servidor
if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Simulación: arranca siempre con la base limpia, y la borra al final
        if os.path.exists(ARCHIVO_DB):
            os.remove(ARCHIVO_DB)
        preparar_base()
        simular_visitas()
        connection.close()          # (Windows no deja borrar un archivo abierto)
        os.remove(ARCHIVO_DB)
        print()
        print("Fin de la clase 3. Ahora abrí ejercicio.md (está en esta misma carpeta).")
    else:
        preparar_base()
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)     # → en tu proyecto, esto es lo que hace manage.py
