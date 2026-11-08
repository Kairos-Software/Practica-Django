"""
=======================================================================
 PASO 4 — USUARIOS (ENTRAR, SALIR, REGISTRARSE) Y VISTAS DE CLASE
=======================================================================

Hasta ahora cualquiera podía hacer cualquier cosa en tus páginas. Ahora:
cada persona tiene su USUARIO y su contraseña, hay cosas que solo se pueden
hacer con la sesión iniciada, y cada uno ve SOLO lo suyo.

El ejemplo de toda la clase: "MIS PELÍCULAS", donde cada usuario tiene su
propia lista de películas, cada una con varios géneros.


¿QUÉ VAS A APRENDER?
--------------------
   1. choices: un campo con opciones fijas (un desplegable)
   2. ManyToMany: una película con VARIOS géneros
   3. Usuarios: entrar (login), salir (logout), registrarse, y páginas
      que piden haber entrado
   4. Que cada usuario vea SOLO lo suyo (¡seguridad!)
   5. Vistas de CLASE (ListView, CreateView...): menos código repetido
   6. Un admin más completo
   7. Pruebas automáticas con usuarios
   8. y 9. Dos cosas útiles: ordenar con vacíos al final, y la
      configuración para publicar un sistema


¿QUÉ NECESITÁS?
---------------
El entorno virtual activado, con Django instalado (como en los pasos 2 y 3).


CÓMO SE USA ESTE ARCHIVO
------------------------
Igual que en el paso 3, de dos formas (parado en "Aprender Django"):

  1) SIMULACIÓN:   python paso_4_usuarios\\clase.py
     Hace de navegador: entra con un usuario, mira páginas, intenta ver
     cosas de otro usuario, se registra uno nuevo... Lo que muestra cada
     visita está anotado en la PARTE 11, al final.

  2) DE VERDAD:    python paso_4_usuarios\\clase.py runserver
     Abrí http://127.0.0.1:8000 y entrá con alguno de estos usuarios:
         usuario: ana    contraseña: clave-de-ana-123
         usuario: beto   contraseña: clave-de-beto-123
     Para probar con los DOS a la vez: uno en una ventana normal y el otro
     en una ventana de incógnito (Ctrl+Shift+N). Vas a ver que cada uno
     ve solo sus películas. Ctrl+C en la terminal para apagar el servidor.
     (Crea un archivo clase4.sqlite3 al lado de este: se puede borrar.)

Las PARTES 1 a 9 explican; la PARTE 10 es el código que se ejecuta. Como
en el paso 3, lo marcado como MAQUINARIA DE LA CLASE no hace falta
entenderlo ni copiarlo.


=======================================================================
PARTE 1 — CHOICES: UN CAMPO CON OPCIONES FIJAS
=======================================================================
Cuando un campo solo puede valer algunas cosas (un estado, un formato, una
especie...), se definen las opciones adentro del modelo:

    class Pelicula(models.Model):
        class Formato(models.TextChoices):
            DVD = 'dvd', 'DVD'                    <- 'dvd' se GUARDA en la base, 'DVD' se MUESTRA
            BLURAY = 'bluray', 'Blu-ray'
            DIGITAL = 'digital', 'Digital'

        formato = models.CharField(max_length=10, choices=Formato.choices, default=Formato.DIGITAL)

  - En la base se guarda 'bluray'. Para mostrar el texto lindo ('Blu-ray'):
        pelicula.get_formato_display()                 (en Python)
        {{ pelicula.get_formato_display }}             (en un template: sin paréntesis)
    (Django crea ese método solo: get_ + el nombre del campo + _display)
  - En el código se compara con la constante:   if p.formato == Pelicula.Formato.DVD:
  - El formulario y el admin muestran un desplegable solos.
  - Para opciones que son números: models.IntegerChoices.


=======================================================================
PARTE 2 — MANY TO MANY: "MUCHOS A MUCHOS"
=======================================================================
Una película tiene VARIOS géneros, y un género tiene VARIAS películas. Con
ForeignKey no alcanza (es "uno"). Django crea una tabla intermedia sola:

    class Genero(models.Model):
        nombre = models.CharField(max_length=40, unique=True)

    class Pelicula(models.Model):
        generos = models.ManyToManyField(Genero, blank=True, related_name='peliculas')

    pelicula.generos.add(accion, comedia)     <- agregar (se guarda solo, sin save())
    pelicula.generos.remove(comedia)          <- sacar
    pelicula.generos.set([drama])             <- reemplazar todos por estos
    pelicula.generos.all()                    <- los géneros de la película
    accion.peliculas.all()                    <- las películas de un género (related_name)
    Pelicula.objects.filter(generos__nombre='Acción')    <- filtrar por la relación

  - En un ModelForm aparece como una lista para elegir varios. Para que sean
    casillas para tildar: widgets = {'generos': forms.CheckboxSelectMultiple}
  - form.save() guarda también los géneros elegidos. OJO: si usás
    form.save(commit=False), después del save() del objeto hay que llamar a
    form.save_m2m() (los géneros se guardan aparte, cuando el objeto ya tiene id).


=======================================================================
PARTE 3 — USUARIOS: ENTRAR, SALIR Y REGISTRARSE
=======================================================================
Django ya trae todo lo de usuarios (la app django.contrib.auth, que viene en
todo proyecto nuevo): el modelo User (con username, password, email...), las
contraseñas guardadas de forma segura (nunca se guardan tal cual), y las
páginas de entrar y salir.

  a) Las páginas de login y logout ya están hechas. Se agregan en config/urls.py:

         path('cuentas/', include('django.contrib.auth.urls')),

     Eso crea las direcciones cuentas/login/, cuentas/logout/ (y otras,
     como cuentas/password_change/), con los nombres 'login' y 'logout'.
     Vos solo hacés el template del login:  templates/registration/login.html
     con un formulario que muestre {{ form }} (ver el de la PARTE 10).
     Para que Django busque templates en una carpeta "templates" en la raíz
     del proyecto, en settings.py:   TEMPLATES -> 'DIRS': [BASE_DIR / 'templates']

  b) En settings.py, a dónde se va en cada caso (son NOMBRES de direcciones):

         LOGIN_URL = 'login'                      <- a dónde manda si hace falta entrar
         LOGIN_REDIRECT_URL = 'peliculas:lista'   <- a dónde va después de entrar
         LOGOUT_REDIRECT_URL = 'login'            <- a dónde va después de salir

  c) El LOGOUT es con POST (un botón adentro de un form con {% csrf_token %}),
     no con un link. Como todo lo que cambia algo (paso 3, PARTE 5).

  d) Saber QUIÉN está:
         en un template:   {% if user.is_authenticated %} Hola, {{ user.username }} {% else %} ... {% endif %}
         en una vista:     request.user   (si no entró, es un "usuario anónimo",
                                           y request.user.is_authenticated es False)

  e) Una página que pide haber entrado: el decorador @login_required

         from django.contrib.auth.decorators import login_required

         @login_required
         def mi_vista(request): ...

     Si alguien sin sesión la abre, lo manda al login, con la dirección a la
     que quería ir en "?next=": después de entrar, vuelve ahí solo.
     (Si la vista también tiene @require_POST, van los dos, uno arriba del otro.)
     (En las vistas de clase: LoginRequiredMixin, ver la PARTE 5.)

  f) Registrarse: el formulario ya existe, UserCreationForm (pide usuario y
     la contraseña dos veces, y revisa que sea segura). Se usa como cualquier
     formulario (paso 3). Para que quede con la sesión iniciada después de
     registrarse:  login(request, usuario)   (from django.contrib.auth import login)
     Mirá la vista "registro" en la PARTE 10.

  g) Una dirección con un name SIN apellido (ej: name='registro', y no
     'peliculas:registro') va en config/urls.py, no en el urls.py de la app.


=======================================================================
PARTE 4 — CADA USUARIO VE LO SUYO (¡SEGURIDAD!)
=======================================================================
El modelo guarda DE QUIÉN es cada cosa, con una ForeignKey al usuario:

    from django.conf import settings

    class Pelicula(models.Model):
        usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  - SIEMPRE filtrar por el usuario:   Pelicula.objects.filter(usuario=request.user)
  - Y en detalle, editar y borrar TAMBIÉN:
        get_object_or_404(Pelicula, pk=pk, usuario=request.user)
    Si no, cualquiera que cambie el número en la dirección (/peliculas/3/
    por /peliculas/4/) ve, edita o BORRA lo de otro. Es uno de los errores
    de seguridad más comunes del mundo. Así, si no es tuyo, da 404.
  - El usuario NO va en el formulario: lo pone la VISTA
    (form.instance.usuario = request.user, o con save(commit=False) como en
    el paso 3). Nunca confíes en un dato así que venga del navegador:
    cualquiera puede mandar lo que quiera.


=======================================================================
PARTE 5 — VISTAS DE CLASE (CBV)
=======================================================================
Lo que hiciste en el paso 3 (lista, detalle, crear, editar, borrar) es tan
común que Django ya lo trae hecho, en forma de CLASES. En vez de programar
el "baile", se CONFIGURA: se dice qué modelo, qué formulario, a dónde ir
después... y el resto lo hace Django.

    from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
    from django.contrib.auth.mixins import LoginRequiredMixin

    class Lista(LoginRequiredMixin, ListView):     <- "una lista, que pide haber entrado"
        model = Pelicula
        paginate_by = 10                            <- paginación gratis (?page=2)
        def get_queryset(self):                     <- QUÉ objetos mostrar (acá: solo los míos)
            return Pelicula.objects.filter(usuario=self.request.user)

    class Crear(LoginRequiredMixin, CreateView):
        model = Pelicula
        form_class = PeliculaForm                   <- el formulario (o: fields = ['titulo', ...])
        success_url = reverse_lazy('lista')         <- a dónde ir después de guardar
        def form_valid(self, form):                 <- "cuando el form está bien, antes de guardar"
            form.instance.usuario = self.request.user
            return super().form_valid(form)         <- y después, lo que hace siempre (guardar y redirigir)

  - En una clase, el pedido está en self.request (no en request).
  - "Mixin" = una clase que agrega UNA habilidad (LoginRequiredMixin agrega
    "pedir haber entrado"). Se ponen PRIMERO, a la izquierda.
  - Cada vista de clase busca un template con un nombre fijo (si no le
    decís otro con template_name = '...'):
        ListView    ->  app/pelicula_list.html             recibe "object_list" (y "page_obj" si pagina)
        DetailView  ->  app/pelicula_detail.html           recibe "object" y también "pelicula"
        CreateView  ->  app/pelicula_form.html             recibe "form"
        UpdateView  ->  app/pelicula_form.html (el mismo)  recibe "form" y "object"
        DeleteView  ->  app/pelicula_confirm_delete.html   con GET pregunta; con POST borra
  - En urls.py se usan con .as_view():   path('', Lista.as_view(), name='lista')
  - Para editar o borrar solo lo propio: el mismo get_queryset filtrando por
    usuario. Si no es tuyo, da 404 solo.
  - Para mandarle datos EXTRA al template: get_context_data (ver
    MisPeliculas en la PARTE 10).
  - ¿Funciones o clases? Las dos están bien. Las funciones son más fáciles
    de leer al principio; las clases ahorran código cuando es lo de siempre.


=======================================================================
PARTE 6 — UN ADMIN MÁS COMPLETO
=======================================================================
    class ComentarioInline(admin.TabularInline):     <- editar los "hijos" ADENTRO del "padre"
        model = Comentario
        extra = 1                                    <- cuántas filas vacías para agregar

    @admin.register(Pelicula)
    class PeliculaAdmin(admin.ModelAdmin):
        list_display = ['titulo', 'usuario', 'formato', 'vista']
        list_editable = ['vista']                    <- se cambia desde la lista misma
        list_filter = ['formato', 'generos']
        search_fields = ['titulo', 'usuario__username']   <- buscar también por un campo relacionado
        filter_horizontal = ['generos']              <- un selector cómodo para ManyToMany
        inlines = [ComentarioInline]


=======================================================================
PARTE 7 — PRUEBAS AUTOMÁTICAS (como las de los ejercicios)
=======================================================================
Son código que prueba tu código, para no tener que probar todo a mano cada
vez que cambiás algo. Van en archivos que empiezan con test (tests.py,
test_paso4.py...) y se ejecutan con:   python manage.py test
Django crea una base de datos APARTE y vacía: no toca tus datos.

    from django.contrib.auth.models import User
    from django.test import TestCase
    from django.urls import reverse
    from .models import Pelicula

    class PeliculasTests(TestCase):

        def setUp(self):                                  <- se ejecuta antes de CADA prueba
            self.ana = User.objects.create_user('ana', password='clave-larga-123')
            self.client.login(username='ana', password='clave-larga-123')   <- "entrar"

        def test_la_lista_responde(self):                <- cada método que empieza con test_ es una prueba
            respuesta = self.client.get(reverse('lista'))     <- self.client = un navegador de mentira
            self.assertEqual(respuesta.status_code, 200)       <- "tiene que ser igual a 200"
            self.assertContains(respuesta, 'Mis películas')    <- "la página tiene que decir esto"

        def test_crear(self):
            self.client.post(reverse('crear'), {'titulo': 'Up', 'formato': 'digital'})
            self.assertEqual(Pelicula.objects.get().usuario, self.ana)

        def test_sin_sesion_va_al_login(self):
            self.client.logout()
            respuesta = self.client.get(reverse('lista'))
            self.assertRedirects(respuesta, '/cuentas/login/?next=/')

  reverse('nombre') es como {% url 'nombre' %}, pero en Python.
  Las comprobaciones más usadas: assertEqual(a, b), assertTrue(x),
  assertFalse(x), assertIn(a, lista), assertContains(respuesta, texto),
  assertNotContains, assertRedirects(respuesta, direccion), y
  with self.assertRaises(ValueError): ...   (que ESO provoque ese error).
  Si una falla, Django dice cuál, qué esperaba y qué encontró.
  (Las pruebas con usuarios tardan un poco: guardar contraseñas de forma
  segura es lento a propósito.)


=======================================================================
PARTE 8 — DOS DETALLES AL ORDENAR
=======================================================================
  a) DESEMPATE: si ordenás por la fecha de creación (ordering = ['-creada'],
     "de la más nueva a la más vieja") y dos se crean en el mismo instante,
     empatan, y el orden entre ellas queda "el que salga". Agregá un segundo
     criterio que nunca empata, el id (los nuevos tienen id más grande):
         ordering = ['-creada', '-id']

  b) VACÍOS AL FINAL: al ordenar por un campo que puede estar vacío (ej: una
     fecha opcional), los vacíos quedan primero o último según la base. Para
     decidirlo vos:
         from django.db.models import F
         ordering = [F('fecha_limite').asc(nulls_last=True), 'titulo']      <- en Meta, o en .order_by(...)


=======================================================================
PARTE 9 — PARA CUANDO QUIERAS PUBLICARLO (resumen, para leer)
=======================================================================
  - DEBUG = False   (con True, cuando hay un error se le muestra tu código a cualquiera)
  - SECRET_KEY secreta y fuera del código:   os.environ['SECRET_KEY']
  - ALLOWED_HOSTS = ['midominio.com']
  - La clave de la base de datos, también en una variable de entorno
  - python manage.py collectstatic   -> junta los CSS/JS en una carpeta para el servidor
  - Se publica con un servidor de aplicaciones (gunicorn) detrás de un
    servidor web (nginx), que también entrega /static/ y /media/. Así está
    publicado Kairos TV.
  - python manage.py check --deploy  -> te lista lo que falta para publicarlo


=======================================================================
PARTE 10 — "MIS PELÍCULAS" (desde acá, el archivo se ejecuta)
=======================================================================
"""

import logging
import os
import sys

import django
from django.apps import AppConfig
from django.conf import settings

BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DB = os.path.join(BASE, "clase4.sqlite3")


class ClaseConfig(AppConfig):            # MAQUINARIA DE LA CLASE
    name = "__main__"
    label = "clase"


# ── Los TEMPLATES (→ en tu proyecto: un archivo .html cada uno) ──
# Fijate en los NOMBRES: son los que las vistas de clase buscan solas (PARTE 5).
TEMPLATES_DE_LA_CLASE = {
    "base.html": """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mis películas</title>
<style>
 body{font-family:sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem}
 nav{display:flex;gap:1rem;align-items:center;margin-bottom:1rem;flex-wrap:wrap}
 .mensaje{background:#e6f4ea;padding:.5rem 1rem;border-radius:6px}
 .chip{background:#eee;border-radius:99px;padding:0 .5rem;font-size:.85rem}
</style></head><body>
<nav>
  {% if user.is_authenticated %}
    <a href="{% url 'lista' %}">Mis películas</a>
    <a href="{% url 'crear' %}">+ Nueva</a>
    <span>Hola, {{ user.username }}</span>
    <form method="post" action="{% url 'logout' %}">{% csrf_token %}<button>Salir</button></form>
  {% else %}
    <a href="{% url 'login' %}">Entrar</a> <a href="{% url 'registro' %}">Registrarme</a>
  {% endif %}
</nav>
{% for m in messages %}<p class="mensaje">{{ m }}</p>{% endfor %}
{% block contenido %}{% endblock %}
</body></html>""",

    # → en tu proyecto: templates/registration/login.html (ahí lo busca el login de Django)
    "registration/login.html": """{% extends "base.html" %}{% block contenido %}
<h1>Entrar</h1>
<form method="post">{% csrf_token %}{{ form.as_p }}<button>Entrar</button></form>
<p>¿No tenés cuenta? <a href="{% url 'registro' %}">Registrate</a></p>
{% endblock %}""",

    "registro.html": """{% extends "base.html" %}{% block contenido %}
<h1>Crear cuenta</h1>
<form method="post">{% csrf_token %}{{ form.as_p }}<button>Registrarme</button></form>
{% endblock %}""",

    # ListView: <app>/<modelo>_list.html  (recibe page_obj porque pagina)
    "clase/pelicula_list.html": """{% extends "base.html" %}{% block contenido %}
<h1>Mis películas</h1>
<form method="get">
  <select name="genero" onchange="this.form.submit()">
    <option value="">Todos los géneros</option>
    {% for g in generos %}
      {# stringformat:"d" pasa el número a texto, para compararlo con lo que vino en la dirección #}
      <option value="{{ g.pk }}" {% if genero == g.pk|stringformat:"d" %}selected{% endif %}>{{ g }}</option>
    {% endfor %}
  </select>
</form>
<ul>
{% for p in page_obj %}
  <li><a href="{% url 'detalle' p.pk %}">{{ p.titulo }}</a> · {{ p.get_formato_display }}
      {% for g in p.generos.all %}<span class="chip">{{ g }}</span>{% endfor %}</li>
{% empty %}<li>No tenés películas{% if genero %} de ese género{% endif %}.</li>
{% endfor %}
</ul>
{% if page_obj.has_other_pages %}Página {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}{% endif %}
{% endblock %}""",

    # DetailView: <app>/<modelo>_detail.html  (recibe "object" y también "pelicula")
    "clase/pelicula_detail.html": """{% extends "base.html" %}{% block contenido %}
<h1>{{ pelicula.titulo }}</h1>
<p>Formato: {{ pelicula.get_formato_display }}</p>
<p>Géneros: {% for g in pelicula.generos.all %}{{ g }}{% if not forloop.last %}, {% endif %}{% empty %}ninguno{% endfor %}</p>
<a href="{% url 'editar' pelicula.pk %}">Editar</a> · <a href="{% url 'borrar' pelicula.pk %}">Borrar</a>
{% endblock %}""",

    # CreateView y UpdateView: <app>/<modelo>_form.html  (recibe "form"; al editar, también "object")
    "clase/pelicula_form.html": """{% extends "base.html" %}{% block contenido %}
<h1>{% if object %}Editar «{{ object.titulo }}»{% else %}Nueva película{% endif %}</h1>
<form method="post">{% csrf_token %}{{ form.as_p }}<button>Guardar</button></form>
{% endblock %}""",

    # DeleteView: <app>/<modelo>_confirm_delete.html  (con GET muestra esto; con POST borra)
    "clase/pelicula_confirm_delete.html": """{% extends "base.html" %}{% block contenido %}
<h1>¿Borrar «{{ object.titulo }}»?</h1>
<form method="post">{% csrf_token %}<button>Sí, borrar</button> <a href="{% url 'detalle' object.pk %}">No</a></form>
{% endblock %}""",
}
# (El "clase/" de los nombres es el nombre de la app de esta clase. En tu
#  proyecto sería, por ejemplo, "libros/resenia_list.html".)


# ── MAQUINARIA DE LA CLASE: la configuración (→ en tu proyecto: config/settings.py) ──
settings.configure(
    DEBUG=True,
    SECRET_KEY="solo-para-la-clase-4",
    ALLOWED_HOSTS=["*"],
    ROOT_URLCONF="__main__",
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.auth",          # los usuarios
        "django.contrib.sessions",      # para recordar quién entró (una cookie + una tabla)
        "django.contrib.messages",
        "__main__.ClaseConfig",
    ],
    MIDDLEWARE=[
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",    # pone request.user
        "django.contrib.messages.middleware.MessageMiddleware",
    ],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ARCHIVO_DB}},
    TEMPLATES=[{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "loaders": [("django.template.loaders.locmem.Loader", TEMPLATES_DE_LA_CLASE)],
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",        # pone {{ user }} en los templates
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }],
    LOGIN_URL="login",                  # 3b)
    LOGIN_REDIRECT_URL="lista",
    LOGOUT_REDIRECT_URL="login",
    LANGUAGE_CODE="es-ar",
    TIME_ZONE="America/Argentina/Buenos_Aires",
    USE_TZ=True,
    DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
)
django.setup()

from django import forms
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import redirect, render
from django.urls import include, path, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


# ── Los MODELOS (→ en tu proyecto: models.py) ──
class Genero(models.Model):
    nombre = models.CharField(max_length=40, unique=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Pelicula(models.Model):
    class Formato(models.TextChoices):                       # PARTE 1: choices
        DVD = "dvd", "DVD"
        BLURAY = "bluray", "Blu-ray"
        DIGITAL = "digital", "Digital"

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,   # PARTE 4: de quién es
                                related_name="peliculas")
    titulo = models.CharField("título", max_length=120)
    formato = models.CharField(max_length=10, choices=Formato.choices, default=Formato.DIGITAL)
    generos = models.ManyToManyField(Genero, blank=True, related_name="peliculas", verbose_name="géneros")  # PARTE 2

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo


# ── El FORMULARIO (→ en tu proyecto: forms.py) ──
class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ["titulo", "formato", "generos"]       # ¡sin "usuario"! (PARTE 4)
        widgets = {"generos": forms.CheckboxSelectMultiple}


# ── Las vistas de CLASE (→ en tu proyecto: views.py) ──
class MisPeliculas(LoginRequiredMixin, ListView):
    model = Pelicula
    paginate_by = 10

    def get_queryset(self):                                     # PARTE 4: solo las mías
        peliculas = Pelicula.objects.filter(usuario=self.request.user).prefetch_related("generos")
        genero = self.request.GET.get("genero", "")
        if genero.isdigit():                                    # isdigit(): ¿son todos números? (para no filtrar con basura)
            peliculas = peliculas.filter(generos__id=genero)
        return peliculas

    def get_context_data(self, **kwargs):                       # datos EXTRA para el template
        contexto = super().get_context_data(**kwargs)           # lo que ya manda la ListView...
        contexto["generos"] = Genero.objects.all()              # ...más los géneros para el desplegable
        contexto["genero"] = self.request.GET.get("genero", "")
        return contexto


class SoloLasMias(LoginRequiredMixin):
    """Un mixin PROPIO: detalle, editar y borrar solo encuentran las del usuario (si no, 404)."""
    model = Pelicula

    def get_queryset(self):
        return Pelicula.objects.filter(usuario=self.request.user)


class Detalle(SoloLasMias, DetailView):
    pass                                                        # no hace falta nada más


class Crear(LoginRequiredMixin, CreateView):
    model = Pelicula
    form_class = PeliculaForm
    success_url = reverse_lazy("lista")     # reverse_lazy (y no reverse) porque se calcula al cargar la clase

    def form_valid(self, form):
        form.instance.usuario = self.request.user               # PARTE 4: el dueño lo pone la vista
        messages.success(self.request, f"Se guardó «{form.instance.titulo}».")
        return super().form_valid(form)


class Editar(SoloLasMias, UpdateView):
    form_class = PeliculaForm
    success_url = reverse_lazy("lista")


class Borrar(SoloLasMias, DeleteView):
    success_url = reverse_lazy("lista")


# ── Una vista de FUNCIÓN (se pueden mezclar con las de clase) ──
def registro(request):                                          # PARTE 3f
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()                                   # crea el usuario (con la contraseña guardada segura)
        login(request, usuario)                                 # y lo deja con la sesión iniciada
        messages.success(request, f"¡Bienvenido/a, {usuario.username}!")
        return redirect("lista")
    return render(request, "registro.html", {"form": form})


# ── Las URLS (→ en tu proyecto: urls.py) ──
urlpatterns = [
    path("", MisPeliculas.as_view(), name="lista"),
    path("nueva/", Crear.as_view(), name="crear"),
    path("<int:pk>/", Detalle.as_view(), name="detalle"),
    path("<int:pk>/editar/", Editar.as_view(), name="editar"),
    path("<int:pk>/borrar/", Borrar.as_view(), name="borrar"),
    path("registro/", registro, name="registro"),
    path("cuentas/", include("django.contrib.auth.urls")),       # PARTE 3a: login, logout... ya hechos
]


def preparar_base():
    """MAQUINARIA: crear las tablas (en tu proyecto: migrate), 2 usuarios y algunas películas."""
    from django.core.management import call_command
    from django.db import connection
    call_command("migrate", verbosity=0)                         # las tablas de Django (usuarios, sesiones)
    if Genero._meta.db_table not in connection.introspection.table_names():
        with connection.schema_editor() as editor:
            editor.create_model(Genero)
            editor.create_model(Pelicula)      # crea también la tabla intermedia de los géneros
    if not User.objects.exists():
        ana = User.objects.create_user("ana", password="clave-de-ana-123")
        beto = User.objects.create_user("beto", password="clave-de-beto-123")
        accion, drama, comedia = (Genero.objects.create(nombre=n) for n in ("Acción", "Drama", "Comedia"))
        matrix = Pelicula.objects.create(usuario=ana, titulo="Matrix", formato=Pelicula.Formato.BLURAY)
        matrix.generos.add(accion)
        Pelicula.objects.create(usuario=ana, titulo="Relatos salvajes").generos.add(drama, comedia)
        Pelicula.objects.create(usuario=beto, titulo="Shrek", formato=Pelicula.Formato.DVD).generos.add(comedia)


# =======================================================================
# PARTE 11 — LA SIMULACIÓN
# =======================================================================
# Ana tiene "Matrix" y "Relatos salvajes"; Beto tiene "Shrek".
# Debajo de cada visita está anotado lo que muestra.

SIGNIFICADO = {
    200: "OK: se mostró la página",
    302: "REDIRIGE a otra dirección",
    404: "NO EXISTE (o no es tuyo)",
    405: "MÉTODO NO PERMITIDO",
}


def visita(que, respuesta):
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

    setup_test_environment()                                       # MAQUINARIA
    logging.getLogger("django.request").setLevel(logging.ERROR)    # MAQUINARIA: sin avisos de cada 404
    navegador = Client()

    print()
    print("========== PARTE 11: la simulación ==========")

    visita("GET /   SIN haber entrado", navegador.get("/"))
    # Muestra:
    #   GET /   SIN haber entrado
    #      código 302 (REDIRIGE a otra dirección) -> va a /cuentas/login/?next=/
    # LoginRequiredMixin lo mandó al login. "?next=/" = después de entrar, volver a "/".

    r = visita("POST /cuentas/login/   con la contraseña MAL",
               navegador.post("/cuentas/login/", {"username": "ana", "password": "otra"}))
    print("   error:", list(r.context["form"].non_field_errors()))
    # Muestra:
    #   POST /cuentas/login/   con la contraseña MAL
    #      código 200 (OK: se mostró la página)
    #      error: ['Por favor introduzca un nombre de usuario y una contraseña correctos. Tenga en cuenta
    #              que ambos campos son sensibles a mayúsculas/minúsculas.']
    # Vuelve a mostrar el login, con el error.

    visita("POST /cuentas/login/   bien (entra Ana)",
           navegador.post("/cuentas/login/", {"username": "ana", "password": "clave-de-ana-123"}))
    # Muestra:
    #   POST /cuentas/login/   bien (entra Ana)
    #      código 302 (REDIRIGE a otra dirección) -> va a /
    # Entró: va a LOGIN_REDIRECT_URL. Desde ahora el navegador "recuerda" que es Ana (la sesión).

    r = visita("GET /   (Ana ve SOLO las suyas)", navegador.get("/"))
    print("   películas:", list(r.context["page_obj"]))
    # Muestra:
    #   GET /   (Ana ve SOLO las suyas)
    #      código 200 (OK: se mostró la página)
    #      películas: [<Pelicula: Matrix>, <Pelicula: Relatos salvajes>]       <- Shrek no aparece: es de Beto

    accion = Genero.objects.get(nombre="Acción")
    r = visita(f"GET /?genero={accion.pk}   (filtrar por el género Acción: ManyToMany)",
               navegador.get("/", {"genero": accion.pk}))
    print("   películas:", list(r.context["page_obj"]))
    # Muestra:
    #   GET /?genero=1   (filtrar por el género Acción: ManyToMany)
    #      código 200 (OK: se mostró la página)
    #      películas: [<Pelicula: Matrix>]

    shrek = Pelicula.objects.get(titulo="Shrek")
    visita(f"GET /{shrek.pk}/   (Shrek es de BETO: para Ana no existe)", navegador.get(f"/{shrek.pk}/"))
    visita(f"POST /{shrek.pk}/borrar/   (tampoco lo puede borrar)", navegador.post(f"/{shrek.pk}/borrar/"))
    # Muestra:
    #   GET /3/   (Shrek es de BETO: para Ana no existe)
    #      código 404 (NO EXISTE (o no es tuyo))
    #   POST /3/borrar/   (tampoco lo puede borrar)
    #      código 404 (NO EXISTE (o no es tuyo))
    # Gracias al get_queryset que filtra por usuario (el mixin SoloLasMias).

    drama = Genero.objects.get(nombre="Drama")
    comedia = Genero.objects.get(nombre="Comedia")
    visita("POST /nueva/   (Ana crea 'Up', con 2 géneros)",
           navegador.post("/nueva/", {"titulo": "Up", "formato": "digital", "generos": [drama.pk, comedia.pk]}))
    up = Pelicula.objects.get(titulo="Up")
    print("   dueña:", up.usuario, "· géneros:", list(up.generos.all()))
    # Muestra:
    #   POST /nueva/   (Ana crea 'Up', con 2 géneros)
    #      código 302 (REDIRIGE a otra dirección) -> va a /
    #      dueña: ana · géneros: [<Genero: Comedia>, <Genero: Drama>]
    # El formulario no tenía "usuario": lo puso la vista (form_valid).

    visita("POST /cuentas/logout/   (Ana sale)", navegador.post("/cuentas/logout/"))
    # Muestra:
    #   POST /cuentas/logout/   (Ana sale)
    #      código 302 (REDIRIGE a otra dirección) -> va a /cuentas/login/      <- LOGOUT_REDIRECT_URL

    datos = {"username": "carla", "password1": "una-clave-larga-789", "password2": "una-clave-larga-789"}
    visita("POST /registro/   (alguien nuevo se registra: Carla)", navegador.post("/registro/", datos))
    r = visita("GET /   (Carla, recién registrada, todavía no tiene películas)", navegador.get("/"))
    print("   usuario:", r.context["user"], "· películas:", list(r.context["page_obj"]))
    # Muestra:
    #   POST /registro/   (alguien nuevo se registra: Carla)
    #      código 302 (REDIRIGE a otra dirección) -> va a /
    #   GET /   (Carla, recién registrada, todavía no tiene películas)
    #      código 200 (OK: se mostró la página)
    #      usuario: carla · películas: []
    # Quedó con la sesión iniciada gracias a login(request, usuario).

    print()
    print("Ahora probala de verdad:   python paso_4_usuarios\\clase.py runserver")
    print("y entrá en http://127.0.0.1:8000 con  ana / clave-de-ana-123  (Ctrl+C para apagarlo).")


def limpiar():
    """MAQUINARIA: borrar la base de la clase."""
    from django.db import connection
    connection.close()
    if os.path.exists(ARCHIVO_DB):
        os.remove(ARCHIVO_DB)


# =======================================================================
# RESUMEN
# =======================================================================
#  choices             class Formato(models.TextChoices) + get_formato_display
#  muchos a muchos     models.ManyToManyField(Genero)  ->  .add() .remove() .set() .all()
#  login / logout      path('cuentas/', include('django.contrib.auth.urls')) + templates/registration/login.html
#  a dónde ir          LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL (en settings)
#  quién es            request.user  /  {{ user.username }}  /  user.is_authenticated
#  pedir sesión        @login_required (funciones)  /  LoginRequiredMixin (clases, a la izquierda)
#  registrarse         UserCreationForm + login(request, usuario)
#  lo suyo             filter(usuario=request.user)  y  get_object_or_404(..., usuario=request.user)
#  vistas de clase     ListView, DetailView, CreateView, UpdateView, DeleteView
#                      model, form_class, success_url, get_queryset, form_valid, get_context_data
#  pruebas             class ...(TestCase): def test_...: self.client.get(...) + assertEqual / assertContains


# MAQUINARIA: arrancar en modo simulación o en modo servidor
if __name__ == "__main__":
    if len(sys.argv) == 1:
        limpiar()
        preparar_base()
        simular_visitas()
        limpiar()
        print()
        print("Fin de la clase 4. Ahora abrí ejercicio.md (está en esta misma carpeta).")
    else:
        preparar_base()
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
