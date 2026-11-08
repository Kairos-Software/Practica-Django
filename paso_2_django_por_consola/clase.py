"""
═══════════════════════════════════════════════════════════════════════
 PASO 2 — DJANGO: PROYECTO, MODELOS, MIGRACIONES Y EL ORM
═══════════════════════════════════════════════════════════════════════

Ejecutalo:   python clase.py      (con el entorno activado y Django instalado)

PRIMERA PARTE (comentarios): cómo es un proyecto Django de verdad.
SEGUNDA PARTE (código que corre): el ORM en acción. Para que puedas
ejecutarlo SIN armar un proyecto, este archivo configura un Django mínimo
él solito. En un proyecto real eso lo hacen settings.py y manage.py.


═══════════════════════════════════════════════════════════════════════
 PARTE 1 — CÓMO SE ARMA UN PROYECTO (esto lo vas a hacer en el ejercicio)
═══════════════════════════════════════════════════════════════════════

1) PROYECTO Y APP
─────────────────
    mkdir biblioteca
    cd biblioteca
    django-admin startproject config .      <- el punto: "acá mismo"
    python manage.py startapp libros

Queda así:

    biblioteca/
    ├── manage.py            <- el "control remoto": todos los comandos pasan por acá
    ├── config/              <- la CONFIGURACIÓN del proyecto (una sola)
    │   ├── settings.py      <- base de datos, apps instaladas, idioma, etc.
    │   ├── urls.py          <- las direcciones (paso 3)
    │   └── wsgi.py/asgi.py  <- para publicarlo en un servidor (no se tocan)
    └── libros/              <- una APP: una parte del sistema con sus cosas
        ├── models.py        <- las TABLAS (como clases de Python)
        ├── admin.py         <- qué se ve en el panel de administración
        ├── views.py         <- las páginas (paso 3)
        ├── migrations/      <- el historial de cambios de las tablas
        └── tests.py         <- pruebas automáticas

  - PROYECTO = todo el sistema. APP = una parte (ej: libros, clientes, ventas).
    Un proyecto chico puede tener una sola app. Kairos TV tiene varias
    (canales, reventa, usuarios...).
  - Cada app nueva hay que AGREGARLA en settings.py, en INSTALLED_APPS:
        INSTALLED_APPS = [
            'django.contrib.admin',
            ...,
            'libros',               <- si te olvidás, Django "no la ve"
        ]

2) LA BASE DE DATOS (settings.py)
─────────────────────────────────
Por defecto viene SQLite (un archivo db.sqlite3 al lado de manage.py):

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

Para PostgreSQL (pip install "psycopg[binary]" y crear la base antes):

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'biblioteca',          <- la base que creaste
            'USER': 'postgres',
            'PASSWORD': 'tu_clave',        <- en un proyecto real, NUNCA escrita acá:
            'HOST': 'localhost',              se lee de una variable de entorno
            'PORT': '5432',                   (os.environ['DB_PASSWORD'])
        }
    }

Y nada más: TODO el resto del código queda igual. Esa es la magia del ORM.

Ya que estás en settings.py: LANGUAGE_CODE = 'es-ar' y TIME_ZONE =
'America/Argentina/Buenos_Aires' (el admin y los errores quedan en castellano).

3) MODELOS = TABLAS
───────────────────
En libros/models.py cada CLASE es una tabla y cada ATRIBUTO una columna.
Django crea el "id" solo. (Abajo, en la parte 2, están los modelos de
ejemplo con cada tipo de campo explicado.)

Tres herramientas más que vas a necesitar:

  a) Que no se repita una COMBINACIÓN de campos (ej: mismo título Y mismo
     año), en la clase Meta del modelo:
         constraints = [models.UniqueConstraint(fields=['titulo', 'anio'], name='titulo_y_anio_unicos')]
     (unique=True en un campo = ese campo solo no se repite)

  b) Límites para un número, con "validadores":
         from django.core.validators import MinValueValidator, MaxValueValidator
         puntaje = models.PositiveSmallIntegerField(null=True, blank=True,
                       validators=[MinValueValidator(1), MaxValueValidator(10)])
     (se revisan en full_clean() y en los formularios, no en save())

  c) Hacer algo SIEMPRE que se guarda: redefinir save() y llamar al original:
         def save(self, *args, **kwargs):
             self.titulo = self.titulo.strip()       <- lo que quieras hacer antes
             super().save(*args, **kwargs)           <- el guardado de verdad (¡no te lo olvides!)

4) MIGRACIONES: pasar los modelos a la base
───────────────────────────────────────────
Cada vez que creás o CAMBIÁS un modelo (agregar un campo, cambiar uno...):

    python manage.py makemigrations     <- escribe el "plan" (un archivo en migrations/)
    python manage.py migrate            <- lo ejecuta en la base (crea/cambia tablas)

  - makemigrations NO toca la base: solo escribe el plan. migrate lo aplica.
  - Los archivos de migrations/ se guardan en git: así otra compu (o el
    servidor) llega a la misma estructura con solo hacer migrate.
  - El primer migrate también crea las tablas de Django (usuarios, sesiones...).
  - python manage.py showmigrations  -> cuáles están aplicadas ([X]) y cuáles no.
  - python manage.py sqlmigrate libros 0001 -> el SQL que va a ejecutar (¡es el del paso 1!).

5) EL ADMIN: un panel gratis
────────────────────────────
    python manage.py createsuperuser      <- tu usuario administrador
    python manage.py runserver            <- y entrás a http://127.0.0.1:8000/admin

En libros/admin.py:

    from django.contrib import admin
    from .models import Categoria, Pelicula

    admin.site.register(Categoria)               <- la forma mínima

    @admin.register(Pelicula)                    <- la forma con opciones
    class PeliculaAdmin(admin.ModelAdmin):
        list_display = ['titulo', 'anio', 'categoria', 'vista']   <- columnas de la lista
        list_filter = ['categoria', 'vista']                       <- filtros a la derecha
        search_fields = ['titulo']                                 <- buscador arriba

Con eso ya podés guardar, editar y borrar desde una página, sin programar nada.

6) LA CONSOLA DE DJANGO (para practicar el ORM en un proyecto real)
───────────────────────────────────────────────────────────────────
    python manage.py shell
    >>> from libros.models import Libro
    >>> Libro.objects.all()

(Todo lo de la parte 2 se puede escribir ahí, una línea a la vez.)

Para no escribir línea por línea: un ARCHIVO propio al lado de manage.py
(ej: practica_orm.py) que arranca Django él mismo con estas 3 líneas, y
después usa los modelos como siempre:

    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')   <- "config" = tu carpeta de settings
    django.setup()

    from libros.models import Libro          <- los imports de TUS modelos, DESPUÉS de setup()
    print(Libro.objects.count())

    python practica_orm.py                   <- se ejecuta así, desde la carpeta de manage.py


═══════════════════════════════════════════════════════════════════════
 PARTE 2 — EL ORM EN ACCIÓN (desde acá el archivo se ejecuta)
═══════════════════════════════════════════════════════════════════════
ORM = "mapeo objeto-relacional": en vez de escribir SQL, usás objetos de
Python, y Django escribe el SQL por vos (bien escrito y sin inyección SQL).
"""

# ── Configuración mínima (en un proyecto real esto está en settings.py) ──
import django
from django.apps import AppConfig
from django.conf import settings


class ClaseConfig(AppConfig):
    """Este mismo archivo hace de "app" (en tu proyecto, la app es la carpeta que crea startapp)."""
    name = "__main__"
    label = "clase"


settings.configure(
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth", "__main__.ClaseConfig"],
    USE_TZ=True,
    LANGUAGE_CODE="es-ar",   # los mensajes de Django en castellano
    TIME_ZONE="America/Argentina/Buenos_Aires",
)
django.setup()

from datetime import date  # noqa: E402
from decimal import Decimal  # noqa: E402

from django.core.exceptions import ValidationError  # noqa: E402
from django.db import connection, models, transaction  # noqa: E402
from django.db.models import Avg, Count, F, Q, Sum  # noqa: E402


def titulo(texto):
    print("\n" + "─" * 60 + f"\n {texto}\n" + "─" * 60)


# ═══════════════════════════════════════════════════════════════════════
# 7) LOS MODELOS (esto iría en libros/models.py)
# ═══════════════════════════════════════════════════════════════════════
class Categoria(models.Model):
    # CharField = texto corto: max_length es OBLIGATORIO
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["nombre"]        # el orden por defecto al pedirlas
        verbose_name_plural = "categorías"   # cómo se llama en el admin

    # __str__ = cómo se muestra el objeto (en el admin, en print, en los <select>)
    def __str__(self):
        return self.nombre


class Pelicula(models.Model):
    titulo = models.CharField(max_length=120)
    # TextField = texto largo sin límite. blank=True: el formulario lo deja vacío
    sinopsis = models.TextField(blank=True)
    # IntegerField = entero. PositiveIntegerField = entero >= 0
    anio = models.PositiveIntegerField("año")        # el primer texto = nombre "lindo" (formularios, admin)
    minutos = models.PositiveIntegerField(default=90)
    # DecimalField = plata (NUNCA FloatField para plata: 0.1 + 0.2 = 0.30000000000000004)
    precio_alquiler = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    # BooleanField = sí / no
    vista = models.BooleanField(default=False)
    # DateField = fecha. null=True: en la base puede quedar vacío (NULL)
    fecha_vista = models.DateField(null=True, blank=True)
    # auto_now_add = se pone sola al crear; auto_now = se actualiza sola al guardar
    creada = models.DateTimeField(auto_now_add=True)
    modificada = models.DateTimeField(auto_now=True)
    # ForeignKey = la relación "muchos a uno" del paso 1 (categoria_id).
    #   on_delete: qué pasa con las películas si se borra su categoría:
    #     CASCADE  -> se borran también      PROTECT -> no deja borrar la categoría
    #     SET_NULL -> quedan sin categoría (necesita null=True)
    #   related_name: cómo se llega desde la categoría: categoria.peliculas.all()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="peliculas")

    class Meta:
        ordering = ["-anio", "titulo"]     # el "-" = de mayor a menor

    def __str__(self):
        return f"{self.titulo} ({self.anio})"

    # Un modelo puede tener métodos propios: la lógica vive CON los datos
    def duracion_en_horas(self):
        return f"{self.minutos // 60} h {self.minutos % 60} min"

    def marcar_vista(self):
        self.vista = True
        self.fecha_vista = date.today()
        self.save()

    # clean() = validaciones que necesitan más de un campo o una regla tuya
    def clean(self):
        if self.anio and self.anio < 1888:   # la primera película es de 1888
            raise ValidationError({"anio": "No hay películas tan viejas."})


# Esto lo hace "migrate" en un proyecto real: crear las tablas
with connection.schema_editor() as editor:
    editor.create_model(Categoria)
    editor.create_model(Pelicula)


# ═══════════════════════════════════════════════════════════════════════
# 8) CREAR (INSERT)
# ═══════════════════════════════════════════════════════════════════════
titulo("8) Crear")

# Forma 1: crear el objeto y guardarlo con save()
infantil = Categoria(nombre="Infantil")
print("Antes de save() no tiene id:", infantil.id)
infantil.save()
print("Después de save() sí:", infantil.id)        # también se puede decir .pk

# Forma 2: objects.create() = crear + guardar en un paso
accion = Categoria.objects.create(nombre="Acción")
drama = Categoria.objects.create(nombre="Drama")

# La ForeignKey se asigna con el OBJETO (no con el número)
Pelicula.objects.create(titulo="Toy Story", anio=1995, minutos=81, categoria=infantil,
                        precio_alquiler=Decimal("1500.00"))
Pelicula.objects.create(titulo="Matrix", anio=1999, minutos=136, categoria=accion, precio_alquiler=2000)
Pelicula.objects.create(titulo="Shrek", anio=2001, minutos=90, categoria=infantil, precio_alquiler=1500)
Pelicula.objects.create(titulo="Gladiador", anio=2000, minutos=155, categoria=accion, precio_alquiler=1800)
Pelicula.objects.create(titulo="Up", anio=2009, minutos=96, categoria=infantil, precio_alquiler=1700, vista=True)
Pelicula.objects.create(titulo="El secreto de sus ojos", anio=2009, minutos=129, categoria=drama,
                        precio_alquiler=2200)

# Muchos de una vez (un solo INSERT): bulk_create
Pelicula.objects.bulk_create([
    Pelicula(titulo="Toy Story 2", anio=1999, minutos=92, categoria=infantil),
    Pelicula(titulo="Duro de matar", anio=1988, minutos=132, categoria=accion),
])

# get_or_create: lo trae si existe, si no lo crea. Devuelve (objeto, ¿se creó?)
comedia, se_creo = Categoria.objects.get_or_create(nombre="Comedia")
print("¿Se creó Comedia?", se_creo)
comedia, se_creo = Categoria.objects.get_or_create(nombre="Comedia")
print("¿Y la segunda vez?", se_creo)


# ═══════════════════════════════════════════════════════════════════════
# 9) LEER (SELECT)
# ═══════════════════════════════════════════════════════════════════════
# Modelo.objects es el "manager": la puerta a la tabla. Lo que devuelve
# (all, filter, order_by...) es un QUERYSET: una consulta que se puede
# seguir encadenando y que NO va a la base hasta que la usás (en un for,
# list(), len, print...). Eso se llama "perezoso" (lazy).
titulo("9) Leer")

print("Todas:", list(Pelicula.objects.all()))
print("Cuántas:", Pelicula.objects.count())

# get = UNA sola. Si no hay -> DoesNotExist. Si hay más de una -> MultipleObjectsReturned
matrix = Pelicula.objects.get(titulo="Matrix")
print("get:", matrix, "| categoría:", matrix.categoria.nombre, "|", matrix.duracion_en_horas())
try:
    Pelicula.objects.get(titulo="No existe")
except Pelicula.DoesNotExist:
    print("get de algo que no existe -> Pelicula.DoesNotExist")

# filter = las que cumplen (puede ser 0, 1 o muchas). exclude = las que NO.
print("Del 2009:", list(Pelicula.objects.filter(anio=2009)))
print("No vistas:", Pelicula.objects.exclude(vista=True).count())

# "Lookups": campo__condicion
print("De 2000 en adelante (__gte):", list(Pelicula.objects.filter(anio__gte=2000)))
print("Antes de 1995 (__lt):", list(Pelicula.objects.filter(anio__lt=1995)))
print("Que dicen 'toy' (__icontains, sin importar mayúsculas):",
      list(Pelicula.objects.filter(titulo__icontains="toy")))
print("Empiezan con 'S' (__startswith):", list(Pelicula.objects.filter(titulo__startswith="S")))
print("Años 1995 o 2001 (__in):", list(Pelicula.objects.filter(anio__in=[1995, 2001])))
print("Entre 1990 y 2000 (__range):", list(Pelicula.objects.filter(anio__range=(1990, 2000))))
print("Sin fecha de vista (__isnull):", Pelicula.objects.filter(fecha_vista__isnull=True).count())

# Varias condiciones en el mismo filter = Y (AND)
print("Infantiles de más de 85 min:",
      list(Pelicula.objects.filter(categoria=infantil, minutos__gt=85)))
# O (OR) se escribe con Q y el símbolo |
print("Del 1995 O de más de 150 min:",
      list(Pelicula.objects.filter(Q(anio=1995) | Q(minutos__gt=150))))

# Filtrar por un campo de la tabla RELACIONADA: con doble guión bajo (hace el JOIN solo)
print("De la categoría Acción:", list(Pelicula.objects.filter(categoria__nombre="Acción")))

# Ordenar, limitar (como LIMIT: con [inicio:fin]), primero / último
print("Las 3 más largas:", list(Pelicula.objects.order_by("-minutos")[:3]))
print("La más vieja:", Pelicula.objects.order_by("anio").first())
print("¿Existe alguna de 1980?:", Pelicula.objects.filter(anio=1980).exists())

# values / values_list = traer solo algunos campos (diccionarios o tuplas)
print("Solo títulos:", list(Pelicula.objects.values_list("titulo", flat=True)[:4]))

# Desde la categoría hacia sus películas (gracias a related_name)
print("Películas de Infantil:", list(infantil.peliculas.all()))

# ¿Qué SQL escribió Django? (¡es el del paso 1!)
print("\nEl SQL de una consulta:\n ", Pelicula.objects.filter(anio__gte=2000).order_by("titulo").query)


# ═══════════════════════════════════════════════════════════════════════
# 10) EDITAR (UPDATE)
# ═══════════════════════════════════════════════════════════════════════
titulo("10) Editar")

# Forma 1: traer, cambiar, save()  (un objeto)
shrek = Pelicula.objects.get(titulo="Shrek")
shrek.minutos = 92
shrek.save()                               # guarda TODOS los campos
shrek.marcar_vista()                       # un método del modelo que cambia y guarda
print("Shrek:", shrek.minutos, "min, vista:", shrek.vista, shrek.fecha_vista)

# Forma 2: update() sobre un queryset = muchos de una vez, sin traerlos
cuantas = Pelicula.objects.filter(categoria=accion).update(precio_alquiler=2100)
print(f"Se cambió el precio de {cuantas} películas de acción.")

# F() = "el valor que YA tiene en la base" (como "minutos = minutos + 5" del paso 1)
Pelicula.objects.filter(categoria=infantil).update(precio_alquiler=F("precio_alquiler") * Decimal("1.10"))
print("Infantiles +10%:", list(Pelicula.objects.filter(categoria=infantil).values_list("titulo", "precio_alquiler")))

# refresh_from_db(): volver a leer un objeto (si la base cambió por otro lado)
matrix.refresh_from_db()
print("Matrix, leída de nuevo:", matrix.precio_alquiler)


# ═══════════════════════════════════════════════════════════════════════
# 11) BORRAR (DELETE)
# ═══════════════════════════════════════════════════════════════════════
titulo("11) Borrar")
Pelicula.objects.get(titulo="Toy Story 2").delete()               # uno
borradas, _ = Pelicula.objects.filter(anio__lt=1990).delete()      # varios
print("Borradas las anteriores a 1990:", borradas)
print("Quedan:", Pelicula.objects.count())

# on_delete=PROTECT: no deja borrar una categoría que tiene películas
from django.db.models import ProtectedError  # noqa: E402

try:
    accion.delete()
except ProtectedError:
    print("No se puede borrar 'Acción': tiene películas (PROTECT).")
comedia.delete()     # esta no tiene ninguna: se borra sin problema
print("Comedia borrada (no tenía películas).")


# ═══════════════════════════════════════════════════════════════════════
# 12) CONTAR Y SUMAR (aggregate y annotate)
# ═══════════════════════════════════════════════════════════════════════
titulo("12) Contar y sumar")
# aggregate = UN resultado para todo el queryset (como SELECT SUM(...))
print(Pelicula.objects.aggregate(total_min=Sum("minutos"), promedio=Avg("minutos")))
# annotate = un número POR CADA objeto (como GROUP BY)
for categoria in Categoria.objects.annotate(cantidad=Count("peliculas")).order_by("-cantidad"):
    print(f"  {categoria.nombre}: {categoria.cantidad} películas")

# Contar o sumar SOLO algunas (filter=Q(...) adentro del Count/Sum)
por_categoria = Categoria.objects.annotate(
    total=Count("peliculas"),
    vistas=Count("peliculas", filter=Q(peliculas__vista=True)),
    plata=Sum("peliculas__precio_alquiler", filter=Q(peliculas__vista=False)),
)
for c in por_categoria:
    print(f"  {c.nombre}: {c.vistas} de {c.total} vistas · alquiler de las no vistas: ${(c.plata or 0):.2f}")
# (Sum de nada da None: por eso el "or 0". Y se puede atravesar más de una
#  relación con __: dueno__mascotas__visitas__costo)

# Fechas: __year, __month, __day (también __gte con una fecha)
from django.utils import timezone  # noqa: E402

hoy = timezone.localdate()
print("Cargadas este mes:", Pelicula.objects.filter(creada__year=hoy.year, creada__month=hoy.month).count())
print("Vistas hasta hoy:", Pelicula.objects.filter(fecha_vista__lte=hoy).count())


# ═══════════════════════════════════════════════════════════════════════
# 13) VALIDAR ANTES DE GUARDAR
# ═══════════════════════════════════════════════════════════════════════
# OJO: save() NO valida (max_length, choices, tu clean()...). La base te
# frena algunas cosas (NOT NULL, UNIQUE), pero no todas. full_clean() valida
# todo. Los FORMULARIOS de Django (paso 3) lo llaman solos: por eso en una
# página casi nunca lo escribís a mano.
titulo("13) Validar")
mala = Pelicula(titulo="", anio=1500, categoria=drama)
try:
    mala.full_clean()
except ValidationError as error:
    for campo, mensajes in error.message_dict.items():
        print(f"  {campo}: {mensajes}")


# ═══════════════════════════════════════════════════════════════════════
# 14) TRANSACCIONES: todo o nada
# ═══════════════════════════════════════════════════════════════════════
titulo("14) Transacciones")
try:
    with transaction.atomic():           # todo lo de adentro, o se hace entero, o nada
        Pelicula.objects.create(titulo="Fantasma", anio=2020, categoria=drama)
        raise RuntimeError("algo salió mal")
except RuntimeError:
    pass
print("¿Quedó 'Fantasma'?", Pelicula.objects.filter(titulo="Fantasma").exists())


# ═══════════════════════════════════════════════════════════════════════
# RESUMEN: SQL (paso 1)  ->  ORM de Django
# ═══════════════════════════════════════════════════════════════════════
#  INSERT ...                     Modelo.objects.create(campo=valor)   /  obj.save()
#  SELECT ... WHERE id = 1        Modelo.objects.get(pk=1)
#  SELECT ... WHERE ...           Modelo.objects.filter(campo__lookup=valor)
#  ... ORDER BY x DESC LIMIT 3    .order_by("-x")[:3]
#  UPDATE ... SET ... WHERE       obj.campo = x; obj.save()  /  qs.update(campo=x)
#  ... SET n = n + 1              qs.update(n=F("n") + 1)
#  DELETE ... WHERE               obj.delete()  /  qs.delete()
#  JOIN                           categoria__nombre="X"  /  obj.categoria.nombre
#  COUNT / SUM + GROUP BY         aggregate(...)  /  annotate(...)
#  BEGIN ... COMMIT / ROLLBACK    with transaction.atomic():
print("\nFin de la clase 2. Ahora: ejercicio.md")
