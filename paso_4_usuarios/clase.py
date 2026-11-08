"""
═══════════════════════════════════════════════════════════════════════
 PASO 4 — USUARIOS (LOGIN) Y VISTAS DE CLASE
═══════════════════════════════════════════════════════════════════════

Ejecutalo (con el entorno activado), igual que el paso 3:
    python clase.py              -> simula visitas y te muestra qué pasa
    python clase.py runserver    -> la página de verdad: http://127.0.0.1:8000
                                    usuario: ana   contraseña: clave-de-ana-123
                                    usuario: beto  contraseña: clave-de-beto-123

Qué vas a aprender (el ejemplo: "Mis películas", cada usuario con SU lista):
   1. choices: un campo con opciones fijas
   2. ManyToMany: relación "muchos a muchos" (una película, varios géneros)
   3. Usuarios: login, logout, registrarse, "solo si iniciaste sesión"
   4. Cada usuario ve SOLO lo suyo
   5. Vistas basadas en CLASES (ListView, CreateView...): menos código repetido
   6. Admin más completo
   7. Pruebas automáticas con usuarios
   (Subir imágenes es el paso 5 y la API el paso 6.)


═══════════════════════════════════════════════════════════════════════
 PARTE 1 — LA EXPLICACIÓN
═══════════════════════════════════════════════════════════════════════

1) CHOICES: opciones fijas
──────────────────────────
Cuando un campo solo puede valer algunas cosas (un estado, una prioridad):

    class Pelicula(models.Model):
        class Formato(models.TextChoices):
            DVD = 'dvd', 'DVD'                    <- valor que se guarda, texto que se muestra
            BLURAY = 'bluray', 'Blu-ray'
            DIGITAL = 'digital', 'Digital'

        formato = models.CharField(max_length=10, choices=Formato.choices, default=Formato.DIGITAL)

  - En la base se guarda 'bluray'; en pantalla se muestra 'Blu-ray' con
    pelicula.get_formato_display()  (en el template: {{ p.get_formato_display }})
  - En el código se compara con la constante: if p.formato == Pelicula.Formato.DVD:
  - El formulario y el admin muestran un desplegable solos.
  - Para números: models.IntegerChoices.

2) MANY TO MANY: muchos a muchos
────────────────────────────────
Una película tiene VARIOS géneros, y un género tiene VARIAS películas.
Con ForeignKey no alcanza (es "uno"). Django crea una tabla intermedia sola:

    class Genero(models.Model):
        nombre = models.CharField(max_length=40, unique=True)

    class Pelicula(models.Model):
        generos = models.ManyToManyField(Genero, blank=True, related_name='peliculas')

    pelicula.generos.add(accion, comedia)     <- agregar (no hace falta save)
    pelicula.generos.remove(comedia)          <- sacar
    pelicula.generos.set([drama])             <- reemplazar todos
    pelicula.generos.all()                    <- los géneros de la película
    accion.peliculas.all()                    <- las películas de un género
    Pelicula.objects.filter(generos__nombre='Acción')    <- filtrar por la relación
  - En un ModelForm aparece como lista de selección múltiple (para checkboxes:
    widgets = {'generos': forms.CheckboxSelectMultiple}). form.save() guarda la
    relación sola. OJO: con save(commit=False) hay que llamar después a
    form.save_m2m() (porque la relación necesita que el objeto ya tenga id).

3) USUARIOS: login, logout, registro
────────────────────────────────────
Django ya trae usuarios (app django.contrib.auth, viene en todo proyecto):
el modelo User (username, password encriptada, email, is_staff...).

  a) Las páginas de login/logout ya están hechas. En config/urls.py:
         path('cuentas/', include('django.contrib.auth.urls')),
     Eso crea: cuentas/login/, cuentas/logout/, cuentas/password_change/ y más.
     Vos solo hacés el template: templates/registration/login.html con {{ form }}.
     (Para que Django encuentre una carpeta "templates" en la raíz del proyecto,
     en settings: TEMPLATES -> 'DIRS': [BASE_DIR / 'templates'])

  b) En settings.py:
         LOGIN_URL = 'login'                  <- a dónde manda si no iniciaste sesión
         LOGIN_REDIRECT_URL = 'lista'         <- a dónde va después de entrar
         LOGOUT_REDIRECT_URL = 'login'        <- a dónde va después de salir

  c) El LOGOUT es con POST (un botón en un form con {% csrf_token %}), no un link.

  d) En cualquier template:
         {% if user.is_authenticated %} Hola {{ user.username }} {% else %} <a ...>Entrar</a> {% endif %}
     En cualquier vista: request.user  (si no inició sesión es un "AnonymousUser")

  e) Proteger una página:
         from django.contrib.auth.decorators import login_required
         @login_required
         def mi_vista(request): ...           <- sin sesión, lo manda al login
     (en las vistas de clase: LoginRequiredMixin, ver punto 5)

  f) Registrarse: el formulario ya existe, UserCreationForm (pide usuario y
     la contraseña dos veces, y valida que sea segura). Se usa como cualquier
     formulario. Para que quede logueado al registrarse: login(request, usuario).

4) CADA USUARIO VE LO SUYO
──────────────────────────
    class Pelicula(models.Model):
        usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  - SIEMPRE filtrar por el usuario:   Pelicula.objects.filter(usuario=request.user)
  - En detalle/editar/borrar también:  get_object_or_404(Pelicula, pk=pk, usuario=request.user)
    Si no, cualquiera que cambie el número en la dirección ve (¡o borra!) lo
    de otro. Este es uno de los errores de seguridad más comunes del mundo.
  - El usuario NO va en el formulario: se pone en la vista (form.instance.usuario
    = request.user). Nunca confíes en un dato así que venga del navegador.

5) VISTAS BASADAS EN CLASES (CBV)
─────────────────────────────────
Lo que hiciste en el paso 3 (lista, detalle, crear, editar, borrar) es tan
común que Django lo trae hecho. Se configura en vez de programarse:

    from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

    class Lista(LoginRequiredMixin, ListView):
        model = Pelicula
        paginate_by = 10                       <- paginación gratis
        def get_queryset(self):                <- QUÉ objetos (acá: solo los míos)
            return Pelicula.objects.filter(usuario=self.request.user)

    class Crear(LoginRequiredMixin, CreateView):
        model = Pelicula
        fields = ['titulo', 'formato', 'generos']     <- o form_class = PeliculaForm
        success_url = reverse_lazy('lista')           <- a dónde ir después de guardar
        def form_valid(self, form):                   <- "cuando el form es válido, antes de guardar"
            form.instance.usuario = self.request.user
            return super().form_valid(form)

  - Templates por defecto ("convención"): app/pelicula_list.html,
    pelicula_detail.html, pelicula_form.html (crear Y editar),
    pelicula_confirm_delete.html. En la lista el template recibe
    "object_list" (y "page_obj" si pagina); en el detalle, "object" (y también
    "pelicula", el nombre del modelo en minúscula).
  - En urls.py se usan con .as_view():   path('', Lista.as_view(), name='lista')
  - Los "Mixin" se ponen PRIMERO (a la izquierda): LoginRequiredMixin, ...
  - Para editar/borrar solo lo propio: el mismo get_queryset filtrando por
    usuario. Si no es tuyo, da 404 solo.
  - ¿Funciones o clases? Las dos están bien. Las funciones son más fáciles de
    leer al principio; las clases ahorran código cuando es el CRUD de siempre.

6) ADMIN MÁS COMPLETO
─────────────────────
    class ComentarioInline(admin.TabularInline):     <- editar los "hijos" adentro del "padre"
        model = Comentario
        extra = 1

    @admin.register(Pelicula)
    class PeliculaAdmin(admin.ModelAdmin):
        list_display = ['titulo', 'usuario', 'formato', 'vista']
        list_editable = ['vista']                    <- se cambia desde la lista misma
        list_filter = ['formato', 'generos']
        search_fields = ['titulo', 'usuario__username']
        filter_horizontal = ['generos']              <- un selector cómodo para ManyToMany
        inlines = [ComentarioInline]

7) PRUEBAS AUTOMÁTICAS (tests.py)
─────────────────────────────────
Código que prueba tu código, para no tener que probar todo a mano cada vez
que cambiás algo. Se ejecutan con:  python manage.py test
Django crea una base APARTE y vacía para cada prueba: no toca tus datos.

    from django.contrib.auth.models import User
    from django.test import TestCase
    from django.urls import reverse
    from .models import Pelicula

    class PeliculasTests(TestCase):

        def setUp(self):                                  <- se ejecuta antes de CADA prueba
            self.ana = User.objects.create_user('ana', password='clave-larga-123')
            self.client.login(username='ana', password='clave-larga-123')   <- "iniciar sesión"

        def test_la_lista_responde(self):                <- cada método que empieza con test_ es una prueba
            respuesta = self.client.get(reverse('lista'))     <- self.client = un navegador de mentira
            self.assertEqual(respuesta.status_code, 200)
            self.assertContains(respuesta, 'Mis películas')    <- el HTML dice eso

        def test_crear(self):
            self.client.post(reverse('crear'), {'titulo': 'Up', 'formato': 'digital'})
            self.assertEqual(Pelicula.objects.get().usuario, self.ana)

        def test_sin_sesion_va_al_login(self):
            self.client.logout()
            respuesta = self.client.get(reverse('lista'))
            self.assertRedirects(respuesta, '/cuentas/login/?next=/')

  Las comprobaciones más usadas: assertEqual(a, b), assertTrue(x),
  assertFalse(x), assertIn(a, lista), assertContains(respuesta, texto),
  assertNotContains, assertRedirects(respuesta, url),
  with self.assertRaises(Error): ...  (que ESO tire ese error)
  Si una falla, Django te dice cuál, qué esperaba y qué encontró.
  (Las pruebas con usuarios tardan un poco: encriptar contraseñas es lento a propósito.)

8) UN ORDEN CON LOS VACÍOS AL FINAL
────────────────────────────────────
Ordenar por una fecha que puede estar vacía pone las vacías primero (o
último, según la base). Para decidirlo vos:
    from django.db.models import F
    ordering = [F('fecha_limite').asc(nulls_last=True), 'titulo']      <- en Meta, o en .order_by(...)

9) SETTINGS PARA PRODUCCIÓN Y PUBLICAR (resumen para cuando llegue el día)
──────────────────────────────────────────────────────────────────────────
  - DEBUG = False (con True, un error le muestra tu código a cualquiera)
  - SECRET_KEY secreta y fuera del código: os.environ['SECRET_KEY']
  - ALLOWED_HOSTS = ['midominio.com']
  - La clave de la base, también en variables de entorno
  - python manage.py collectstatic -> junta los CSS/JS en una carpeta para el servidor web
  - Se publica con un servidor de aplicaciones (gunicorn) detrás de un
    servidor web (nginx) que también sirve /static/ y /media/. Así está
    publicado Kairos TV.
  - python manage.py check --deploy -> te lista lo que falta para producción


═══════════════════════════════════════════════════════════════════════
 PARTE 2 — "MIS PELÍCULAS" (desde acá se ejecuta)
═══════════════════════════════════════════════════════════════════════
"""

import os
import sys

import django
from django.apps import AppConfig
from django.conf import settings

BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DB = os.path.join(BASE, "clase4.sqlite3")


class ClaseConfig(AppConfig):
    name = "__main__"
    label = "clase"


# ── Templates (→ en tu proyecto: un archivo cada uno) ──
# Fijate los NOMBRES: son los que las vistas de clase buscan solas.
TEMPLATES_DE_LA_CLASE = {
    "base.html": """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Mis películas</title>
<style>
 body{font-family:sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem}
 nav{display:flex;gap:1rem;align-items:center;margin-bottom:1rem}
 .mensaje{background:#e6f4ea;padding:.5rem 1rem;border-radius:6px}
 .chip{background:#eee;border-radius:99px;padding:0 .5rem;font-size:.85rem}
 img{max-width:120px}
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

    # → en tu proyecto: templates/registration/login.html (lo busca la vista de login de Django)
    "registration/login.html": """{% extends "base.html" %}{% block contenido %}
<h1>Entrar</h1>
<form method="post">{% csrf_token %}{{ form.as_p }}<button>Entrar</button></form>
<p>¿No tenés cuenta? <a href="{% url 'registro' %}">Registrate</a></p>
{% endblock %}""",

    "registro.html": """{% extends "base.html" %}{% block contenido %}
<h1>Crear cuenta</h1>
<form method="post">{% csrf_token %}{{ form.as_p }}<button>Registrarme</button></form>
{% endblock %}""",

    # ListView: <app>/<modelo>_list.html  (recibe page_obj si pagina)
    "clase/pelicula_list.html": """{% extends "base.html" %}{% block contenido %}
<h1>Mis películas</h1>
<form method="get">
  <select name="genero" onchange="this.form.submit()">
    <option value="">Todos los géneros</option>
    {% for g in generos %}<option value="{{ g.pk }}" {% if genero == g.pk|stringformat:"d" %}selected{% endif %}>{{ g }}</option>{% endfor %}
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

    # DetailView: <app>/<modelo>_detail.html  (recibe "object" y "pelicula")
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

    # DeleteView: <app>/<modelo>_confirm_delete.html  (GET muestra esto, POST borra)
    "clase/pelicula_confirm_delete.html": """{% extends "base.html" %}{% block contenido %}
<h1>¿Borrar «{{ object.titulo }}»?</h1>
<form method="post">{% csrf_token %}<button>Sí, borrar</button> <a href="{% url 'detalle' object.pk %}">No</a></form>
{% endblock %}""",
}


settings.configure(
    DEBUG=True,
    SECRET_KEY="solo-para-la-clase-4",
    ALLOWED_HOSTS=["*"],
    ROOT_URLCONF="__main__",
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.auth",          # los usuarios
        "django.contrib.sessions",      # recordar quién inició sesión (una cookie + una tabla)
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
    LOGIN_URL="login",
    LOGIN_REDIRECT_URL="lista",
    LOGOUT_REDIRECT_URL="login",
    LANGUAGE_CODE="es-ar",
    TIME_ZONE="America/Argentina/Buenos_Aires",
    USE_TZ=True,
    DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
)
django.setup()

from django import forms  # noqa: E402
from django.contrib import messages  # noqa: E402
from django.contrib.auth import login  # noqa: E402
from django.contrib.auth.forms import UserCreationForm  # noqa: E402
from django.contrib.auth.mixins import LoginRequiredMixin  # noqa: E402
from django.contrib.auth.models import User  # noqa: E402
from django.contrib.auth.decorators import login_required  # noqa: E402
from django.db import models  # noqa: E402
from django.shortcuts import redirect, render  # noqa: E402
from django.urls import include, path, reverse_lazy  # noqa: E402
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView  # noqa: E402


# ── Modelos (→ models.py) ──
class Genero(models.Model):
    nombre = models.CharField(max_length=40, unique=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Pelicula(models.Model):
    class Formato(models.TextChoices):                       # 1) choices
        DVD = "dvd", "DVD"
        BLURAY = "bluray", "Blu-ray"
        DIGITAL = "digital", "Digital"

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,   # 4) de quién es
                                related_name="peliculas")
    titulo = models.CharField("título", max_length=120)
    formato = models.CharField(max_length=10, choices=Formato.choices, default=Formato.DIGITAL)
    generos = models.ManyToManyField(Genero, blank=True, related_name="peliculas", verbose_name="géneros")  # 2)

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo


# ── Formulario (→ forms.py) ──
class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ["titulo", "formato", "generos"]       # ¡sin "usuario"!
        widgets = {"generos": forms.CheckboxSelectMultiple}


# ── Vistas de CLASE (→ views.py) ──
class MisPeliculas(LoginRequiredMixin, ListView):                # 5) + 3e)
    model = Pelicula
    paginate_by = 10

    def get_queryset(self):                                     # 4) solo las mías
        peliculas = Pelicula.objects.filter(usuario=self.request.user).prefetch_related("generos")
        genero = self.request.GET.get("genero", "")
        if genero.isdigit():
            peliculas = peliculas.filter(generos__id=genero)
        return peliculas

    def get_context_data(self, **kwargs):                       # datos EXTRA para el template
        contexto = super().get_context_data(**kwargs)
        contexto["generos"] = Genero.objects.all()
        contexto["genero"] = self.request.GET.get("genero", "")
        return contexto


class SoloLasMias(LoginRequiredMixin):
    """Un mixin propio: detalle, editar y borrar solo encuentran las del usuario (si no, 404)."""
    model = Pelicula

    def get_queryset(self):
        return Pelicula.objects.filter(usuario=self.request.user)


class Detalle(SoloLasMias, DetailView):
    pass


class Crear(LoginRequiredMixin, CreateView):
    model = Pelicula
    form_class = PeliculaForm
    success_url = reverse_lazy("lista")     # reverse_lazy (y no reverse) porque se calcula al cargar la clase

    def form_valid(self, form):
        form.instance.usuario = self.request.user               # 4) el dueño lo pone la vista
        messages.success(self.request, f"Se guardó «{form.instance.titulo}».")
        return super().form_valid(form)


class Editar(SoloLasMias, UpdateView):
    form_class = PeliculaForm
    success_url = reverse_lazy("lista")


class Borrar(SoloLasMias, DeleteView):
    success_url = reverse_lazy("lista")


# ── Vistas de FUNCIÓN (también se pueden mezclar) ──
def registro(request):                                          # 3f)
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        login(request, usuario)                                 # queda con la sesión iniciada
        messages.success(request, f"¡Bienvenido/a, {usuario.username}!")
        return redirect("lista")
    return render(request, "registro.html", {"form": form})


# ── URLs (→ urls.py) ──
urlpatterns = [
    path("", MisPeliculas.as_view(), name="lista"),
    path("nueva/", Crear.as_view(), name="crear"),
    path("<int:pk>/", Detalle.as_view(), name="detalle"),
    path("<int:pk>/editar/", Editar.as_view(), name="editar"),
    path("<int:pk>/borrar/", Borrar.as_view(), name="borrar"),
    path("registro/", registro, name="registro"),
    path("cuentas/", include("django.contrib.auth.urls")),       # login, logout... ya hechos
]


def preparar_base():
    """migrate crea las tablas de Django (usuarios, sesiones); las de esta clase, a mano (en tu proyecto: migrate)."""
    from django.core.management import call_command
    from django.db import connection
    call_command("migrate", verbosity=0)
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


def simular_visitas():
    from django.test import Client
    from django.test.utils import setup_test_environment

    setup_test_environment()
    navegador = Client()

    def visita(que, respuesta):
        destino = f" -> redirige a {respuesta['Location']}" if respuesta.status_code in (301, 302) else ""
        print(f"\n{que}\n   código {respuesta.status_code}{destino}")
        return respuesta

    visita("GET /  SIN iniciar sesión (LoginRequiredMixin te manda al login)", navegador.get("/"))

    visita("POST /cuentas/login/  con la contraseña MAL",
           navegador.post("/cuentas/login/", {"username": "ana", "password": "otra"}))
    visita("POST /cuentas/login/  bien (Ana)",
           navegador.post("/cuentas/login/", {"username": "ana", "password": "clave-de-ana-123"}))

    r = visita("GET /  (Ana ve SOLO las suyas)", navegador.get("/"))
    print("   ", list(r.context["page_obj"]))

    accion = Genero.objects.get(nombre="Acción")
    r = visita("GET /?genero=Acción  (filtrar por un género: ManyToMany)", navegador.get("/", {"genero": accion.pk}))
    print("   ", list(r.context["page_obj"]))

    shrek = Pelicula.objects.get(titulo="Shrek")
    visita(f"GET /{shrek.pk}/  (Shrek es de BETO: para Ana no existe)", navegador.get(f"/{shrek.pk}/"))
    visita(f"POST /{shrek.pk}/borrar/  (tampoco lo puede borrar)", navegador.post(f"/{shrek.pk}/borrar/"))

    drama = Genero.objects.get(nombre="Drama")
    comedia = Genero.objects.get(nombre="Comedia")
    visita("POST /nueva/  (con 2 géneros)",
           navegador.post("/nueva/", {"titulo": "Up", "formato": "digital", "generos": [drama.pk, comedia.pk]}))
    up = Pelicula.objects.get(titulo="Up")
    print(f"    dueña: {up.usuario} · géneros: {list(up.generos.all())}")

    visita("POST /cuentas/logout/  (salir)", navegador.post("/cuentas/logout/"))
    visita("POST /registro/  (alguien nuevo se registra)",
           navegador.post("/registro/", {"username": "carla", "password1": "una-clave-larga-789",
                                        "password2": "una-clave-larga-789"}))
    r = visita("GET /  (Carla todavía no tiene películas)", navegador.get("/"))
    print("    usuario:", r.context["user"], "· películas:", list(r.context["page_obj"]))

    print("\nAhora probalo de verdad:  python clase.py runserver   (usuario ana / clave-de-ana-123)")


def limpiar():
    from django.db import connection
    connection.close()
    if os.path.exists(ARCHIVO_DB):
        os.remove(ARCHIVO_DB)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        limpiar()
        preparar_base()
        simular_visitas()
        limpiar()
    else:
        preparar_base()
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
