"""
═══════════════════════════════════════════════════════════════════════
 PASO 3 — VISTAS, URLS, TEMPLATES Y FORMULARIOS (la parte web)
═══════════════════════════════════════════════════════════════════════

Dos formas de ejecutarlo (con el entorno activado):

    python clase.py              -> simula visitas a las páginas y te muestra
                                    qué responde cada una (sin navegador)
    python clase.py runserver    -> una página de verdad: abrí
                                    http://127.0.0.1:8000  (Ctrl+C para cortar)

Igual que en el paso 2, este archivo es un Django "en miniatura" para que
corra solo. En un proyecto real cada parte va en SU archivo: te lo marco con
"→ en tu proyecto: ...".


═══════════════════════════════════════════════════════════════════════
 PARTE 1 — CÓMO FUNCIONA UNA PÁGINA EN DJANGO
═══════════════════════════════════════════════════════════════════════

El viaje de un pedido (request):

  Navegador                Django
  ─────────                ──────
  GET /peliculas/3/  ──►  1. urls.py: ¿qué VISTA atiende "peliculas/3/"?
                          2. la VISTA (una función de Python) recibe el
                             pedido, usa los MODELOS (la base, paso 2) y
                             arma la respuesta con un TEMPLATE (HTML)
  <html>...</html>   ◄──  3. devuelve la respuesta (response)

  - URL      -> la dirección ("peliculas/3/"). Vive en urls.py.
  - VISTA    -> la función que decide qué hacer. Vive en views.py.
  - TEMPLATE -> el HTML con huecos para los datos. Vive en templates/.
  - MODELO   -> los datos (paso 2). Vive en models.py.


1) URLS
───────
El proyecto tiene UN urls.py principal (config/urls.py) que reparte a las
apps, y cada app tiene el suyo (hay que CREARLO: startapp no lo hace).

  → en tu proyecto, config/urls.py:
        from django.contrib import admin
        from django.urls import include, path

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', include('peliculas.urls')),      <- todo lo demás, a la app
        ]

  → en tu proyecto, peliculas/urls.py (archivo nuevo):
        from django.urls import path
        from . import views

        app_name = 'peliculas'                         <- el "apellido" de los nombres
        urlpatterns = [
            path('', views.lista, name='lista'),
            path('<int:pk>/', views.detalle, name='detalle'),
            path('nueva/', views.crear, name='crear'),
            path('<int:pk>/editar/', views.editar, name='editar'),
            path('<int:pk>/borrar/', views.borrar, name='borrar'),
        ]

  - '<int:pk>/' -> la parte variable de la dirección: "3/" llega a la vista
    como el parámetro pk=3. (Tipos: int, str, slug...)
  - name='detalle' -> un NOMBRE para la dirección. En el resto del código
    NUNCA se escribe "/peliculas/3/" a mano: se pide por nombre
    ('peliculas:detalle', pk=3). Si mañana cambiás la dirección, cambia sola
    en todos lados.

2) VISTAS
─────────
Una vista es una función que recibe el pedido (request) y devuelve una
respuesta. Las herramientas que más vas a usar:

    render(request, 'peliculas/lista.html', {'peliculas': ...})
        -> arma el HTML con el template y los datos (el "contexto")
    get_object_or_404(Pelicula, pk=pk)
        -> el objeto, o la página "404 no existe" si no está (en vez de un error)
    redirect('peliculas:detalle', pk=pelicula.pk)
        -> "andá a esta otra página" (después de guardar algo)
    request.method      -> 'GET' (mirar) o 'POST' (mandar un formulario)
    request.GET.get('q', '')   -> lo que viene en la dirección: /?q=toy
    request.POST        -> lo que se mandó en el formulario

3) TEMPLATES
────────────
  → en tu proyecto: peliculas/templates/peliculas/lista.html
    (sí, "peliculas" dos veces: es la costumbre para que no choquen nombres
    entre apps. Django los encuentra solo gracias a APP_DIRS=True en settings).

El lenguaje de templates:
    {{ pelicula.titulo }}                 mostrar un dato (se escapa solo: seguro)
    {{ pelicula.anio|default:"?" }}       FILTROS: transforman lo que se muestra
    {{ fecha|date:"d/m/Y" }}  {{ lista|length }}  {{ texto|upper }}  {{ texto|truncatechars:30 }}
    {% for p in peliculas %} ... {% empty %} no hay {% endfor %}
    {% if p.vista %} ... {% elif ... %} ... {% else %} ... {% endif %}
    {% url 'peliculas:detalle' p.pk %}    la dirección por su nombre
    {% csrf_token %}                      OBLIGATORIO en todo <form method="post">
    {# un comentario #}

HERENCIA: un base.html con lo que se repite (menú, estilos) y "huecos"
({% block %}) que cada página llena:
    base.html:   <html>...<nav>...</nav> {% block contenido %}{% endblock %} ...</html>
    lista.html:  {% extends "base.html" %}
                 {% block contenido %} ...lo propio de esta página... {% endblock %}

Archivos estáticos (CSS, imágenes, JS): en peliculas/static/peliculas/estilo.css
y en el template:  {% load static %}  <link rel="stylesheet" href="{% static 'peliculas/estilo.css' %}">

4) FORMULARIOS
──────────────
Un ModelForm arma el formulario A PARTIR DEL MODELO: los campos, los tipos,
y la VALIDACIÓN (incluido tu clean() del modelo, ¿te acordás?):

  → en tu proyecto, peliculas/forms.py (archivo nuevo):
        from django import forms
        from .models import Pelicula

        class PeliculaForm(forms.ModelForm):
            class Meta:
                model = Pelicula
                fields = ['titulo', 'anio', 'minutos', 'vista']

El "baile" de siempre en la vista que crea o edita (memorizalo):

    if request.method == 'POST':                 # mandaron el formulario
        form = PeliculaForm(request.POST)        # lo llenamos con lo que mandaron
        if form.is_valid():                      # ¿está todo bien?
            pelicula = form.save()               # guarda en la base
            return redirect(...)                 # y vamos a otra página
        # si NO es válido, sigue de largo: se muestra de nuevo CON los errores
    else:                                        # GET: recién entra
        form = PeliculaForm()                    # vacío
    return render(request, 'peliculas/form.html', {'form': form})

  - Para EDITAR es igual, pero con instance=pelicula: PeliculaForm(request.POST, instance=pelicula)
  - ¿Por qué redirect después de guardar? Si no, al apretar F5 el navegador
    vuelve a mandar el formulario y se guarda DOS veces. (Patrón POST/Redirect/GET.)
  - BORRAR siempre con POST (un botón dentro de un form), nunca con un link:
    un link lo puede "visitar" cualquiera (o un buscador) y borrarte todo.
    Si querés una página "¿Seguro?": la vista muestra la confirmación con GET
    y borra solo cuando llega el POST del botón.

Si al objeto le falta algo que NO viene del formulario (ej: un comentario
necesita saber de qué película es), se guarda en dos pasos:

        comentario = form.save(commit=False)     <- arma el objeto SIN guardarlo
        comentario.pelicula = pelicula           <- le completás lo que falta
        comentario.save()                        <- ahora sí

Forma corta (y común) del baile:  form = PeliculaForm(request.POST or None)
    -> con los datos si es POST, vacío si es GET. Después:
       if request.method == 'POST' and form.is_valid(): ...

Un formulario que arranca con algo YA elegido (ej: "Nueva película" desde
una categoría, con esa categoría puesta): initial
        form = PeliculaForm(initial={'categoria': request.GET.get('categoria')})
    (el link:  {% url 'peliculas:crear' %}?categoria={{ categoria.pk }})

Si al borrar algo salta un ProtectedError (paso 2), se ataja en la vista:
        try:
            categoria.delete()
        except ProtectedError:
            messages.error(request, 'No se puede: tiene películas.')
            return redirect(...)

Un formulario que NO guarda un modelo (ej: pedir una cantidad) es forms.Form:

        class CantidadForm(forms.Form):
            cantidad = forms.IntegerField(min_value=1)

    En la vista:  form = CantidadForm(request.POST)
                  if form.is_valid():
                      cantidad = form.cleaned_data['cantidad']    <- ya es un int, validado
    (no tiene .save(): con el dato hacés lo que necesites)

5) PAGINAR (de a N por página)
──────────────────────────────
    from django.core.paginator import Paginator
    pagina = Paginator(peliculas, 12).get_page(request.GET.get('pagina'))   # /?pagina=2
y en el template se recorre "pagina" como si fuera la lista, con:
    {{ pagina.number }} de {{ pagina.paginator.num_pages }}
    {% if pagina.has_next %}<a href="?pagina={{ pagina.next_page_number }}">Siguiente</a>{% endif %}
    (has_previous / previous_page_number para "Anterior")
OJO: si la lista tiene filtros (?q=toy), el link de la página tiene que
llevarlos también (?q=toy&pagina=2) o se pierden. Una forma: en la vista
        filtros = request.GET.copy(); filtros.pop('pagina', None)
        ... {'filtros': filtros.urlencode()}       y en el link:  ?{{ filtros }}&pagina=2

6) MENSAJES ("Se guardó bien")
──────────────────────────────
    from django.contrib import messages
    messages.success(request, 'Película guardada.')      (también .error, .warning, .info)
y en base.html se muestran con {% for m in messages %}{{ m }}{% endfor %}.
Viene configurado en todo proyecto nuevo de Django.


═══════════════════════════════════════════════════════════════════════
 PARTE 2 — LA MINI VIDEOTECA (desde acá se ejecuta)
═══════════════════════════════════════════════════════════════════════
"""

import os
import sys

import django
from django.apps import AppConfig
from django.conf import settings

BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DB = os.path.join(BASE, "clase3.sqlite3")


class ClaseConfig(AppConfig):
    name = "__main__"
    label = "clase"


# ── Los TEMPLATES (→ en tu proyecto, cada uno es un archivo .html en templates/) ──
TEMPLATES_DE_LA_CLASE = {
    # base.html: lo que se repite en todas las páginas
    "base.html": """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{% block titulo %}Videoteca{% endblock %}</title>
  <style>
    body { font-family: sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; }
    nav a { margin-right: 1rem; }
    .mensaje { background: #e6f4ea; padding: .5rem 1rem; border-radius: 6px; }
    .error { color: #b00020; }
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
# {{ form.as_p }} dibuja todos los campos con sus errores. Para controlar el
# diseño se dibujan a mano:  {{ form.titulo.label_tag }} {{ form.titulo }} {{ form.titulo.errors }}


# ── La configuración (→ en tu proyecto: config/settings.py, ya viene casi todo hecho) ──
settings.configure(
    DEBUG=True,
    SECRET_KEY="solo-para-la-clase",           # en un proyecto real: secreta y fuera del código
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

from django import forms  # noqa: E402
from django.contrib import messages  # noqa: E402
from django.db import connection, models  # noqa: E402
from django.shortcuts import get_object_or_404, redirect, render  # noqa: E402
from django.urls import path  # noqa: E402
from django.views.decorators.http import require_POST  # noqa: E402


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

    # Validación propia de UN campo: clean_<campo>. Devuelve el valor (limpio) o lanza ValidationError
    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].strip()
        if titulo.lower() == "prueba":
            raise forms.ValidationError("Poné un título de verdad.")
        return titulo


# ── Las VISTAS (→ en tu proyecto: peliculas/views.py) ──
def lista(request):
    q = request.GET.get("q", "").strip()            # /?q=toy  ->  "toy"
    peliculas = Pelicula.objects.all()
    if q:
        peliculas = peliculas.filter(titulo__icontains=q)
    return render(request, "lista.html", {"peliculas": peliculas, "q": q})


def detalle(request, pk):                            # pk llega de la URL: <int:pk>
    pelicula = get_object_or_404(Pelicula, pk=pk)
    return render(request, "detalle.html", {"pelicula": pelicula})


def crear(request):
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
        form = PeliculaForm(instance=pelicula)                   # con los datos actuales
    return render(request, "form.html", {"form": form, "pelicula": pelicula})


@require_POST                                        # si alguien entra con GET: error 405
def borrar(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    pelicula.delete()
    messages.success(request, f"Se borró «{pelicula.titulo}».")
    return redirect("lista")


# ── Las URLS (→ en tu proyecto: peliculas/urls.py, con app_name = 'peliculas') ──
urlpatterns = [
    path("", lista, name="lista"),
    path("<int:pk>/", detalle, name="detalle"),
    path("nueva/", crear, name="crear"),
    path("<int:pk>/editar/", editar, name="editar"),
    path("<int:pk>/borrar/", borrar, name="borrar"),
]


def preparar_base():
    """Esto lo hace "migrate" en un proyecto real: crear la tabla, y unas películas de ejemplo."""
    if Pelicula._meta.db_table not in connection.introspection.table_names():
        with connection.schema_editor() as editor:
            editor.create_model(Pelicula)
    if not Pelicula.objects.exists():
        Pelicula.objects.bulk_create([
            Pelicula(titulo="Toy Story", anio=1995, minutos=81, vista=True),
            Pelicula(titulo="Matrix", anio=1999, minutos=136),
            Pelicula(titulo="Up", anio=2009, minutos=96),
        ])


def simular_visitas():
    """
    Sin navegador: el "Client" de Django hace de navegador (es lo mismo que
    se usa para las PRUEBAS AUTOMÁTICAS, en tests.py). Mirá qué responde cada página.
    """
    from django.test import Client
    from django.test.utils import setup_test_environment

    setup_test_environment()          # para poder mirar el contexto y el template de cada respuesta
    navegador = Client()
    # (Los avisos "Not Found" y "Method Not Allowed" de arriba son el registro de Django: es lo esperado)

    def visita(que, respuesta):
        destino = f" -> redirige a {respuesta['Location']}" if respuesta.status_code in (301, 302) else ""
        print(f"\n{que}\n   código {respuesta.status_code}{destino}")
        return respuesta

    r = visita("GET /  (la lista)", navegador.get("/"))
    print("   películas que mandó la vista al template:", list(r.context["peliculas"]))

    r = visita("GET /?q=toy  (buscar)", navegador.get("/", {"q": "toy"}))
    print("   encontradas:", list(r.context["peliculas"]))

    matrix = Pelicula.objects.get(titulo="Matrix")
    r = visita(f"GET /{matrix.pk}/  (detalle)", navegador.get(f"/{matrix.pk}/"))
    print("   ¿el HTML dice 136 minutos?", "136 minutos" in r.content.decode())

    visita("GET /999/  (una que no existe: get_object_or_404)", navegador.get("/999/"))

    r = visita("POST /nueva/  con datos MAL (título vacío, año con letras)",
               navegador.post("/nueva/", {"titulo": "", "anio": "abc", "minutos": 90}))
    print("   errores del formulario:", dict(r.context["form"].errors))
    print("   -> código 200: vuelve a mostrar el formulario con los errores, NO guardó nada")

    r = visita("POST /nueva/  con datos BIEN", navegador.post("/nueva/", {"titulo": "Shrek", "anio": 2001, "minutos": 90}))
    print("   ¿se guardó?", Pelicula.objects.filter(titulo="Shrek").exists(), "(y redirigió al detalle)")

    shrek = Pelicula.objects.get(titulo="Shrek")
    visita(f"POST /{shrek.pk}/editar/  (cambiar los minutos)",
           navegador.post(f"/{shrek.pk}/editar/", {"titulo": "Shrek", "anio": 2001, "minutos": 92}))
    shrek.refresh_from_db()
    print("   minutos ahora:", shrek.minutos)

    visita(f"GET /{shrek.pk}/borrar/  (¡con GET no se puede borrar!)", navegador.get(f"/{shrek.pk}/borrar/"))
    visita(f"POST /{shrek.pk}/borrar/  (con POST sí)", navegador.post(f"/{shrek.pk}/borrar/"))
    print("   ¿sigue existiendo?", Pelicula.objects.filter(pk=shrek.pk).exists())

    print("\nAhora probalo de verdad:  python clase.py runserver   y abrí http://127.0.0.1:8000")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Simulación: arranca siempre con la base limpia
        if os.path.exists(ARCHIVO_DB):
            os.remove(ARCHIVO_DB)
        preparar_base()
        simular_visitas()
        connection.close()          # Windows no deja borrar un archivo abierto
        os.remove(ARCHIVO_DB)
    else:
        preparar_base()
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)     # → en tu proyecto, esto es manage.py
