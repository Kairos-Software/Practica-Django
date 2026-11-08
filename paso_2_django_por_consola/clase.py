"""
=======================================================================
 PASO 2 — DJANGO: PROYECTO, MODELOS, MIGRACIONES Y EL ORM
=======================================================================

Es lo mismo del paso 1 (guardar, buscar, editar y borrar en una base de
datos), pero SIN escribir SQL: Django lo escribe por vos.

El ejemplo de toda la clase: PELÍCULAS y sus CATEGORÍAS.


¿QUÉ NECESITÁS?
---------------
Desde este paso necesitás Django, instalado adentro de un ENTORNO VIRTUAL
(una carpeta con su propio Python y sus paquetes: ver COMANDOS.md, punto 1).
Si todavía no lo creaste, en la terminal, parado en "Aprender Django":

    python -m venv entorno               <- crea el entorno (una sola vez)
    .\\entorno\\Scripts\\activate           <- lo ACTIVA (cada vez que abrís una terminal nueva)
    pip install django pillow            <- instala Django (una sola vez)

Sabés que el entorno está activado porque la línea de la terminal empieza
con (entorno). Si te dice "No module named 'django'", es que no lo activaste.


CÓMO SE USA ESTE ARCHIVO
------------------------
1. Con el entorno activado, parado en la carpeta "Aprender Django":

       python paso_2_django_por_consola\\clase.py

2. Este archivo tiene DOS MITADES:

   PRIMERA MITAD (PARTES A1 a A7): para LEER. Cómo se arma un proyecto
   Django de verdad, con sus carpetas y comandos. Es lo que vas a hacer en
   el ejercicio. No se ejecuta nada.

   SEGUNDA MITAD (PARTES B1 a B8): se EJECUTA. Muestra el ORM en acción:
   crear, buscar, editar y borrar películas. Debajo de cada print() está
   anotado lo que muestra (después de "# Muestra:").

3. Un detalle: un proyecto Django de verdad son MUCHOS archivos (los vas a
   ver en la PARTE A2). Para que esta clase se pueda ejecutar con un solo
   comando, este archivo arma un Django "en miniatura" él solito. Esa parte
   está marcada como MAQUINARIA DE LA CLASE: no hace falta que la entiendas
   ni la copies. En tu proyecto, eso lo hacen settings.py y manage.py.


=======================================================================
PARTE A1 — ¿QUÉ ES DJANGO?
=======================================================================
Django es un "framework": un conjunto de herramientas ya hechas para armar
sistemas web. En vez de programar todo desde cero (cómo hablar con la
base, cómo mostrar páginas, cómo manejar usuarios...), usás las piezas que
trae Django y te concentrás en lo TUYO: qué datos guardás y qué hace tu
sistema.

Una de esas piezas es el ORM ("mapeo objeto-relacional"): en vez de
escribir SQL, escribís Python con objetos, y el ORM lo traduce a SQL:

    SQL (paso 1):   SELECT * FROM peliculas WHERE anio >= 2000
    Django (ORM):   Pelicula.objects.filter(anio__gte=2000)

Y lo escribe bien: siempre protegido contra la inyección SQL.


=======================================================================
PARTE A2 — PROYECTO Y APP
=======================================================================
En la terminal (con el entorno activado):

    mkdir biblioteca                         <- crea una carpeta
    cd biblioteca                            <- entra a la carpeta
    django-admin startproject config .       <- crea el PROYECTO (¡ojo con el punto final!)
    python manage.py startapp libros         <- crea una APP llamada "libros"

Y queda así:

    biblioteca/
    ├── manage.py            <- el "control remoto": todos los comandos pasan por acá
    ├── config/              <- la CONFIGURACIÓN del proyecto
    │   ├── settings.py      <- la base de datos, las apps, el idioma, etc.
    │   ├── urls.py          <- las direcciones de las páginas (paso 3)
    │   └── wsgi.py, asgi.py <- para publicarlo en un servidor (no se tocan)
    └── libros/              <- una APP: una parte del sistema, con sus cosas
        ├── models.py        <- los MODELOS: las tablas, escritas como clases
        ├── admin.py         <- qué se ve en el panel de administración
        ├── views.py         <- las páginas (paso 3)
        ├── migrations/      <- el historial de cambios de las tablas
        └── tests.py         <- pruebas automáticas

  - PROYECTO = todo el sistema. APP = una parte (libros, clientes, ventas...).
    Un proyecto chico puede tener una sola app.
  - El punto de "startproject config ." quiere decir "acá mismo". Sin el
    punto, se crea una carpeta de más (config/config/) y todo queda en un
    lío. Si te pasa, borrá todo y empezá de nuevo.


=======================================================================
PARTE A3 — LA CONFIGURACIÓN (config/settings.py)
=======================================================================
Tres cosas que vas a tocar siempre:

  a) Cada app nueva hay que REGISTRARLA en INSTALLED_APPS. Si te olvidás,
     Django "no la ve" (no encuentra sus modelos ni sus páginas):

        INSTALLED_APPS = [
            'django.contrib.admin',
            ...                       <- las que ya vienen, no se tocan
            'libros',                 <- la tuya, al final
        ]

  b) Idioma y hora (así el admin y los mensajes de error salen en castellano):

        LANGUAGE_CODE = 'es-ar'
        TIME_ZONE = 'America/Argentina/Buenos_Aires'

  c) La base de datos. Por defecto ya viene SQLite (un archivo db.sqlite3
     al lado de manage.py), y no hace falta tocar nada:

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

     Para PostgreSQL (con pip install "psycopg[binary]" y la base creada):

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'biblioteca',
                'USER': 'postgres',
                'PASSWORD': os.environ['DB_PASSWORD'],   <- la clave NUNCA escrita en el código:
                'HOST': 'localhost',                        se lee de una "variable de entorno"
                'PORT': '5432',
            }
        }

     Y NADA MÁS cambia: todo el resto del código queda igual.


=======================================================================
PARTE A4 — MODELOS = TABLAS (libros/models.py)
=======================================================================
Cada CLASE es una tabla, y cada ATRIBUTO es una columna. Compará:

    SQL (paso 1)                              Django (models.py)
    ----------------------------------------  -----------------------------------------------
    CREATE TABLE autores (                    class Autor(models.Model):
      id INTEGER PRIMARY KEY AUTOINCREMENT,       (el id lo agrega Django solo)
      nombre TEXT NOT NULL UNIQUE                 nombre = models.CharField(max_length=100, unique=True)
    )

La clase hereda de models.Model (¿te acordás de la herencia del paso 0?).
Por eso, sin programarlo, ya sabe guardarse, buscarse y borrarse.
En la PARTE B1, más abajo, están los modelos de ejemplo con cada tipo de
campo explicado.

Tres herramientas más que te van a servir:

  a) Que no se repita una COMBINACIÓN de campos (ej: el mismo usuario no
     puede opinar dos veces del mismo libro). Va en la clase Meta:
         class Meta:
             constraints = [models.UniqueConstraint(fields=['usuario', 'libro'], name='una_opinion_por_libro')]
     (unique=True en UN campo = ese campo solo no se repite)

  b) Límites para un número, con "validadores":
         from django.core.validators import MinValueValidator, MaxValueValidator
         puntaje = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
     (se revisan al validar, con full_clean() o en los formularios, no al
      hacer save(): ver la PARTE B7)

  c) Hacer algo SIEMPRE que se guarda: redefinir save() y llamar al original:
         def save(self, *args, **kwargs):
             self.titulo = self.titulo.strip()       <- lo que quieras hacer antes
             super().save(*args, **kwargs)           <- el guardado de verdad (¡no te lo olvides!)


=======================================================================
PARTE A5 — MIGRACIONES: PASAR LOS MODELOS A LA BASE
=======================================================================
Escribir un modelo NO crea la tabla. Hacen falta dos comandos, que se
ejecutan cada vez que creás o CAMBIÁS un modelo (agregar un campo, etc.):

    python manage.py makemigrations     <- escribe el "PLANO" de los cambios
                                           (un archivo nuevo en libros/migrations/)
    python manage.py migrate            <- CONSTRUYE: ejecuta el plano en la base
                                           (crea o cambia las tablas)

  - Como en una obra: makemigrations dibuja el plano, migrate construye.
    makemigrations NO toca la base.
  - El primer migrate de un proyecto también crea las tablas propias de
    Django (usuarios, sesiones...).
  - Los archivos de migrations/ se guardan junto con el código: así otra
    compu llega a las mismas tablas haciendo solo "migrate".
  - python manage.py showmigrations     -> cuáles están aplicadas [X] y cuáles no [ ]
  - python manage.py sqlmigrate libros 0001   -> el SQL que va a ejecutar (¡es como el del paso 1!)


=======================================================================
PARTE A6 — EL ADMIN: UN PANEL DE ADMINISTRACIÓN GRATIS
=======================================================================
Django trae un panel para cargar, editar y borrar datos sin programar páginas.

    python manage.py createsuperuser     <- crea TU usuario administrador
                                            (la contraseña no se ve mientras la
                                            escribís: es normal)
    python manage.py runserver           <- prende el servidor
                                            abrí http://127.0.0.1:8000/admin
                                            (Ctrl+C en la terminal para apagarlo)

Pero el admin solo muestra los modelos que REGISTRES, en libros/admin.py:

    from django.contrib import admin
    from .models import Categoria, Pelicula

    admin.site.register(Categoria)               <- la forma mínima

    @admin.register(Pelicula)                    <- la forma con opciones:
    class PeliculaAdmin(admin.ModelAdmin):
        list_display = ['titulo', 'anio', 'categoria', 'vista']   <- las columnas de la lista
        list_filter = ['categoria', 'vista']                       <- filtros a la derecha
        search_fields = ['titulo']                                 <- un buscador arriba


=======================================================================
PARTE A7 — PROBAR EL ORM EN TU PROYECTO
=======================================================================
Dos formas:

  a) La consola de Django (como la consola de Python, pero con tu proyecto
     cargado). Se escribe una línea por vez, y exit() para salir:

        python manage.py shell
        >>> from libros.models import Libro
        >>> Libro.objects.all()

  b) Un ARCHIVO tuyo al lado de manage.py (por ejemplo practica.py). Tiene
     que "arrancar" Django antes de usar los modelos, con estas líneas
     arriba de todo:

        import os
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')   <- "config" = tu carpeta de settings
        django.setup()

        from libros.models import Libro          <- los import de TUS modelos, DESPUÉS de setup()
        print(Libro.objects.count())

     y se ejecuta desde la carpeta de manage.py:   python practica.py


=======================================================================
PARTE B — EL ORM EN ACCIÓN (desde acá, el archivo se ejecuta)
=======================================================================
"""

# -----------------------------------------------------------------------
# MAQUINARIA DE LA CLASE (no hace falta entenderla ni copiarla)
# Arma un Django mínimo para que este archivo se pueda ejecutar solo, con
# una base en memoria. En tu proyecto esto lo hacen settings.py y manage.py.
# -----------------------------------------------------------------------
import django
from django.apps import AppConfig
from django.conf import settings


class ClaseConfig(AppConfig):
    name = "__main__"
    label = "clase"


settings.configure(
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth", "__main__.ClaseConfig"],
    USE_TZ=True,
    LANGUAGE_CODE="es-ar",
    TIME_ZONE="America/Argentina/Buenos_Aires",
)
django.setup()
# ------------------------- fin de la maquinaria -------------------------

from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import connection, models, transaction
from django.db.models import Avg, Count, F, ProtectedError, Q, Sum
from django.utils import timezone


# =======================================================================
# PARTE B1 — LOS MODELOS (en tu proyecto: libros/models.py)
# =======================================================================
# Los TIPOS DE CAMPO más usados (cada uno es una columna):
#
#   models.CharField(max_length=50)     texto corto (max_length es OBLIGATORIO)
#   models.TextField()                  texto largo, sin límite
#   models.IntegerField()               número entero
#   models.PositiveIntegerField()       número entero que no puede ser negativo
#   models.DecimalField(max_digits=8, decimal_places=2)
#                                       número con decimales EXACTOS: para la PLATA.
#                                       (nunca FloatField para plata: 0.1 + 0.2 = 0.30000000000000004)
#   models.BooleanField(default=False)  sí / no
#   models.DateField()                  una fecha
#   models.DateTimeField()              una fecha con hora
#   models.ForeignKey(OtroModelo, ...)  la relación del paso 1 (categoria_id)
#
# Opciones que sirven para cualquier campo:
#   "año"            el primer texto: el nombre "lindo" que se muestra (admin, formularios)
#   default=90       el valor si no se dice otro
#   unique=True      no se puede repetir
#   blank=True       los formularios dejan dejarlo VACÍO (opcional)
#   null=True        la BASE deja guardarlo vacío (NULL). Para fechas y números
#                    opcionales se usan las dos: null=True, blank=True.
#                    Para textos opcionales alcanza con blank=True (queda "").
#   auto_now_add=True   (en fechas) se pone sola al CREAR
#   auto_now=True       (en fechas) se actualiza sola cada vez que se GUARDA
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["nombre"]                  # el orden por defecto cuando se piden
        verbose_name_plural = "categorías"     # cómo se llama en plural en el admin

    # __str__ = cómo se muestra el objeto (en print, en el admin, en los desplegables)
    def __str__(self):
        return self.nombre


class Pelicula(models.Model):
    titulo = models.CharField(max_length=120)
    sinopsis = models.TextField(blank=True)
    anio = models.PositiveIntegerField("año")
    minutos = models.PositiveIntegerField(default=90)
    precio_alquiler = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    vista = models.BooleanField(default=False)
    fecha_vista = models.DateField(null=True, blank=True)
    creada = models.DateTimeField(auto_now_add=True)
    modificada = models.DateTimeField(auto_now=True)
    # ForeignKey: cada película tiene UNA categoría (en la tabla: categoria_id).
    #   on_delete = qué pasa con las películas si se BORRA su categoría:
    #       models.CASCADE   -> se borran también
    #       models.PROTECT   -> NO deja borrar la categoría mientras tenga películas
    #       models.SET_NULL  -> las películas quedan sin categoría (necesita null=True)
    #   related_name = cómo se llega DESDE la categoría a sus películas:
    #       categoria.peliculas.all()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="peliculas")

    class Meta:
        ordering = ["-anio", "titulo"]     # el "-" = de mayor a menor. Si empatan en el año, por título.

    def __str__(self):
        return f"{self.titulo} ({self.anio})"

    # Un modelo puede tener MÉTODOS propios: la lógica vive junto con los datos.
    def duracion_en_horas(self):
        return f"{self.minutos // 60} h {self.minutos % 60} min"

    def marcar_vista(self):
        self.vista = True
        self.fecha_vista = date.today()
        self.save()                         # save() = guardar los cambios en la base

    # clean() = validaciones TUYAS (las que no se pueden decir con un tipo de
    # campo). Si algo está mal, se provoca un ValidationError con un
    # diccionario {campo: mensaje}. Se ejecuta al validar (PARTE B7).
    def clean(self):
        if self.anio and self.anio < 1888:   # la primera película de la historia es de 1888
            raise ValidationError({"anio": "No hay películas tan viejas."})


# MAQUINARIA DE LA CLASE: crear las tablas (en tu proyecto: makemigrations + migrate)
with connection.schema_editor() as editor:
    editor.create_model(Categoria)
    editor.create_model(Pelicula)


# =======================================================================
# PARTE B2 — CREAR (el INSERT del paso 1)
# =======================================================================
# Modelo.objects es la "puerta" a la tabla: casi todo empieza por ahí.

print()
print("========== PARTE B2: crear ==========")

# Forma 1: armar el objeto y guardarlo con save()
infantil = Categoria(nombre="Infantil")
print("Antes de save() no tiene id:", infantil.id)
# Muestra: Antes de save() no tiene id: None       <- todavía no está en la base
infantil.save()
print("Después de save() sí:", infantil.id)
# Muestra: Después de save() sí: 1                 <- (también se puede decir infantil.pk)

# Forma 2: objects.create() = armar + guardar en un solo paso
accion = Categoria.objects.create(nombre="Acción")
drama = Categoria.objects.create(nombre="Drama")

# La ForeignKey se asigna con el OBJETO (categoria=infantil), no con el número.
Pelicula.objects.create(titulo="Toy Story", anio=1995, minutos=81, categoria=infantil,
                        precio_alquiler=Decimal("1500.00"))
Pelicula.objects.create(titulo="Matrix", anio=1999, minutos=136, categoria=accion, precio_alquiler=2000)
Pelicula.objects.create(titulo="Shrek", anio=2001, minutos=90, categoria=infantil, precio_alquiler=1500)
Pelicula.objects.create(titulo="Gladiador", anio=2000, minutos=155, categoria=accion, precio_alquiler=1800)
Pelicula.objects.create(titulo="Up", anio=2009, minutos=96, categoria=infantil, precio_alquiler=1700, vista=True)
Pelicula.objects.create(titulo="El secreto de sus ojos", anio=2009, minutos=129, categoria=drama,
                        precio_alquiler=2200)

# Muchos de una vez (un solo INSERT): bulk_create, con una lista de objetos
Pelicula.objects.bulk_create([
    Pelicula(titulo="Toy Story 2", anio=1999, minutos=92, categoria=infantil),
    Pelicula(titulo="Duro de matar", anio=1988, minutos=132, categoria=accion),
])

# get_or_create: lo TRAE si existe, y si no, lo CREA.
# Devuelve DOS cosas: (el objeto, True si lo tuvo que crear / False si ya existía)
comedia, se_creo = Categoria.objects.get_or_create(nombre="Comedia")
print("¿Se creó Comedia?", se_creo)
# Muestra: ¿Se creó Comedia? True
comedia, se_creo = Categoria.objects.get_or_create(nombre="Comedia")
print("¿Y la segunda vez?", se_creo)
# Muestra: ¿Y la segunda vez? False          <- ya existía: la trajo, no creó otra


# =======================================================================
# PARTE B3 — LEER (el SELECT del paso 1)
# =======================================================================
# Lo que devuelven all(), filter(), order_by()... se llama QUERYSET: una
# consulta que todavía NO fue a la base. Recién va cuando la USÁS (en un
# for, con list(), len(), print...). Mientras tanto se puede seguir
# encadenando: Pelicula.objects.filter(...).exclude(...).order_by(...)
#
# Cuando se muestra un queryset con list(), cada objeto aparece así:
#     <Pelicula: Matrix (1999)>      <- el modelo, y lo que devuelve su __str__

print()
print("========== PARTE B3: leer ==========")

print("Cuántas:", Pelicula.objects.count())
# Muestra: Cuántas: 8
print("Todas:", list(Pelicula.objects.all()))
# Muestra (en el orden del Meta: año de mayor a menor, y después título):
#   Todas: [<Pelicula: El secreto de sus ojos (2009)>, <Pelicula: Up (2009)>, <Pelicula: Shrek (2001)>,
#           <Pelicula: Gladiador (2000)>, <Pelicula: Matrix (1999)>, <Pelicula: Toy Story 2 (1999)>,
#           <Pelicula: Toy Story (1995)>, <Pelicula: Duro de matar (1988)>]

# get() = traer UNA sola.
#   Si no hay ninguna -> error Modelo.DoesNotExist
#   Si hay más de una -> error Modelo.MultipleObjectsReturned
matrix = Pelicula.objects.get(titulo="Matrix")
print(matrix, "|", matrix.categoria.nombre, "|", matrix.duracion_en_horas())
# Muestra: Matrix (1999) | Acción | 2 h 16 min       <- matrix.categoria es el OBJETO Categoria entero
try:
    Pelicula.objects.get(titulo="No existe")
except Pelicula.DoesNotExist:
    print("get() de algo que no existe -> Pelicula.DoesNotExist")
# Muestra: get() de algo que no existe -> Pelicula.DoesNotExist

# filter() = las que cumplen (pueden ser 0, 1 o muchas). exclude() = las que NO cumplen.
print("Del 2009:", list(Pelicula.objects.filter(anio=2009)))
# Muestra: Del 2009: [<Pelicula: El secreto de sus ojos (2009)>, <Pelicula: Up (2009)>]
print("No vistas:", Pelicula.objects.exclude(vista=True).count())
# Muestra: No vistas: 7

# "LOOKUPS": para condiciones que no son "igual a", se escribe  campo__condición
# (con DOS guiones bajos). Los más usados:
#   __gt  mayor que     __gte  mayor o igual     __lt  menor que     __lte  menor o igual
#   __icontains  contiene el texto (sin importar mayúsculas)    __startswith  empieza con
#   __in  alguno de esta lista      __range  entre dos valores      __isnull  está vacío
print("De 2000 en adelante:", list(Pelicula.objects.filter(anio__gte=2000)))
# Muestra: De 2000 en adelante: [<Pelicula: El secreto de sus ojos (2009)>, <Pelicula: Up (2009)>,
#                                <Pelicula: Shrek (2001)>, <Pelicula: Gladiador (2000)>]
print("Antes de 1995:", list(Pelicula.objects.filter(anio__lt=1995)))
# Muestra: Antes de 1995: [<Pelicula: Duro de matar (1988)>]
print("Que dicen 'toy':", list(Pelicula.objects.filter(titulo__icontains="toy")))
# Muestra: Que dicen 'toy': [<Pelicula: Toy Story 2 (1999)>, <Pelicula: Toy Story (1995)>]
print("Años 1995 o 2001:", list(Pelicula.objects.filter(anio__in=[1995, 2001])))
# Muestra: Años 1995 o 2001: [<Pelicula: Shrek (2001)>, <Pelicula: Toy Story (1995)>]
print("Sin fecha de vista:", Pelicula.objects.filter(fecha_vista__isnull=True).count())
# Muestra: Sin fecha de vista: 8

# Varias condiciones en el mismo filter() = Y (las dos se tienen que cumplir)
print("Infantiles de más de 85 min:", list(Pelicula.objects.filter(categoria=infantil, minutos__gt=85)))
# Muestra: Infantiles de más de 85 min: [<Pelicula: Up (2009)>, <Pelicula: Shrek (2001)>, <Pelicula: Toy Story 2 (1999)>]
# O (alcanza con una): con Q(...) y el símbolo |
print("Del 1995 O de más de 150 min:", list(Pelicula.objects.filter(Q(anio=1995) | Q(minutos__gt=150))))
# Muestra: Del 1995 O de más de 150 min: [<Pelicula: Gladiador (2000)>, <Pelicula: Toy Story (1995)>]

# Filtrar por un campo de la tabla RELACIONADA: relación__campo (Django hace el JOIN solo)
print("De la categoría Acción:", list(Pelicula.objects.filter(categoria__nombre="Acción")))
# Muestra: De la categoría Acción: [<Pelicula: Gladiador (2000)>, <Pelicula: Matrix (1999)>, <Pelicula: Duro de matar (1988)>]

# order_by() cambia el orden ("-" adelante = de mayor a menor).
# [:3] = solo las primeras 3 (es el LIMIT del paso 1).
print("Las 3 más largas:", list(Pelicula.objects.order_by("-minutos")[:3]))
# Muestra: Las 3 más largas: [<Pelicula: Gladiador (2000)>, <Pelicula: Matrix (1999)>, <Pelicula: Duro de matar (1988)>]
print("La más vieja:", Pelicula.objects.order_by("anio").first())
# Muestra: La más vieja: Duro de matar (1988)       <- first(): la primera (o None si no hay)
print("¿Hay alguna de 1980?", Pelicula.objects.filter(anio=1980).exists())
# Muestra: ¿Hay alguna de 1980? False               <- exists(): True o False

# values_list(): traer solo algunos campos, en vez de objetos enteros.
# Con flat=True y un solo campo, da los valores sueltos.
print("Solo títulos:", list(Pelicula.objects.values_list("titulo", flat=True)[:4]))
# Muestra: Solo títulos: ['El secreto de sus ojos', 'Up', 'Shrek', 'Gladiador']

# Desde la categoría hacia sus películas (gracias al related_name="peliculas"):
print("Películas de Infantil:", list(infantil.peliculas.all()))
# Muestra: Películas de Infantil: [<Pelicula: Up (2009)>, <Pelicula: Shrek (2001)>,
#                                  <Pelicula: Toy Story 2 (1999)>, <Pelicula: Toy Story (1995)>]

# ¿Qué SQL escribió Django? .query lo muestra (¡es como el del paso 1!)
print("El SQL:", Pelicula.objects.filter(anio__gte=2000).order_by("titulo").query)
# Muestra: El SQL: SELECT "clase_pelicula"."id", "clase_pelicula"."titulo", ... FROM "clase_pelicula"
#          WHERE "clase_pelicula"."anio" >= 2000 ORDER BY "clase_pelicula"."titulo" ASC

# PROBÁ VOS: traé las películas de la categoría Infantil de menos de 95 minutos.


# =======================================================================
# PARTE B4 — EDITAR (el UPDATE del paso 1)
# =======================================================================
print()
print("========== PARTE B4: editar ==========")

# Forma 1: traer el objeto, cambiarle el atributo, y save()
shrek = Pelicula.objects.get(titulo="Shrek")
shrek.minutos = 92
shrek.save()
shrek.marcar_vista()                     # un método del modelo que cambia y guarda
print("Shrek:", shrek.minutos, "min, vista:", shrek.vista)
# Muestra: Shrek: 92 min, vista: True

# Forma 2: update() sobre un queryset = cambiar MUCHAS de una vez, en una sola
# consulta y sin traerlas. Devuelve CUÁNTAS cambió.
cuantas = Pelicula.objects.filter(categoria=accion).update(precio_alquiler=2100)
print(f"Se cambió el precio de {cuantas} películas de acción.")
# Muestra: Se cambió el precio de 3 películas de acción.

# F("campo") = "el valor que YA tiene ese campo en la base" (como el
# "minutos = minutos + 5" del paso 1). La cuenta la hace la base.
# Acá: subir 10% el alquiler de las infantiles.
Pelicula.objects.filter(categoria=infantil).update(precio_alquiler=F("precio_alquiler") * Decimal("1.10"))
print("Infantiles +10%:", list(Pelicula.objects.filter(categoria=infantil).values_list("titulo", "precio_alquiler")))
# Muestra: Infantiles +10%: [('Up', Decimal('1870.00')), ('Shrek', Decimal('1650.00')),
#                            ('Toy Story 2', Decimal('0.00')), ('Toy Story', Decimal('1650.00'))]
# OJO: precio_alquiler es un DecimalField (plata). Multiplicalo por un
# Decimal, no por un float como 1.10: en un update() Django lo acepta, pero
# en otras consultas (como annotate, PARTE B6) da el error "Cannot infer type
# of '*' expression", y además los float traen el problema de los decimales
# del paso 0 (0.1 + 0.2). Si el porcentaje está en una variable:
#     factor = 1 + Decimal(porcentaje) / 100       (con porcentaje = 10, da 1.1)

# refresh_from_db(): volver a leer un objeto de la base (si cambió "por otro lado",
# como acá, que el update() lo cambió sin tocar la variable matrix)
print("Matrix antes de releer:", matrix.precio_alquiler)
# Muestra: Matrix antes de releer: 2000.00         <- el valor de cuando la trajimos con get(), en la PARTE B3
matrix.refresh_from_db()
print("Matrix, leída de nuevo:", matrix.precio_alquiler)
# Muestra: Matrix, leída de nuevo: 2100.00


# =======================================================================
# PARTE B5 — BORRAR (el DELETE del paso 1)
# =======================================================================
print()
print("========== PARTE B5: borrar ==========")
Pelicula.objects.get(titulo="Toy Story 2").delete()               # borrar UNA
borradas, detalle = Pelicula.objects.filter(anio__lt=1990).delete()      # borrar VARIAS
print("Borradas las anteriores a 1990:", borradas)
# Muestra: Borradas las anteriores a 1990: 1       <- delete() devuelve (cuántas, un detalle por modelo)
print("Quedan:", Pelicula.objects.count())
# Muestra: Quedan: 6

# on_delete=PROTECT: no deja borrar una categoría que todavía tiene películas.
try:
    accion.delete()
except ProtectedError:
    print("No se puede borrar 'Acción': tiene películas (PROTECT).")
# Muestra: No se puede borrar 'Acción': tiene películas (PROTECT).
comedia.delete()     # esta no tiene ninguna: se borra sin problema
print("Comedia borrada (no tenía películas).")
# Muestra: Comedia borrada (no tenía películas).


# =======================================================================
# PARTE B6 — CONTAR Y SUMAR (aggregate y annotate)
# =======================================================================
# Las cuentas las hace la BASE (no un for en Python): es mucho más rápido.
#   aggregate(...) -> UN resultado para todas (el SELECT SUM(...) del paso 1).
#                     Devuelve un DICCIONARIO con los nombres que le pongas.
#   annotate(...)  -> un dato extra POR CADA objeto (el GROUP BY del paso 1).
#                     Cada objeto queda con un atributo nuevo con ese nombre.
# Las funciones: Count (contar), Sum (sumar), Avg (promedio), Min, Max.

print()
print("========== PARTE B6: contar y sumar ==========")
resultado = Pelicula.objects.aggregate(total_min=Sum("minutos"), promedio=Avg("minutos"))
print(resultado)
# Muestra: {'total_min': 689, 'promedio': 114.83333333333333}
print("Solo el promedio:", resultado["promedio"])
# Muestra: Solo el promedio: 114.83333333333333     <- del diccionario se saca con ["nombre"]
print("Promedio de algo vacío:", Pelicula.objects.filter(anio=1900).aggregate(p=Avg("minutos"))["p"])
# Muestra: Promedio de algo vacío: None              <- si no hay ninguna, da None

for categoria in Categoria.objects.annotate(cantidad=Count("peliculas")).order_by("-cantidad"):
    print(" ", categoria.nombre, "tiene", categoria.cantidad, "películas")
# Muestra:
#   Infantil tiene 3 películas
#   Acción tiene 2 películas
#   Drama tiene 1 películas
# (annotate le agregó a cada categoría el atributo "cantidad". Count("peliculas")
#  usa el related_name: cuenta las películas de cada categoría.)

# Contar o sumar SOLO algunas: filter=Q(...) adentro del Count o del Sum.
# Y se puede llegar a un campo de la relación con __: peliculas__precio_alquiler
por_categoria = Categoria.objects.annotate(
    total=Count("peliculas"),
    vistas=Count("peliculas", filter=Q(peliculas__vista=True)),
    plata=Sum("peliculas__precio_alquiler", filter=Q(peliculas__vista=False)),
).order_by("nombre")
for c in por_categoria:
    print(f"  {c.nombre}: {c.vistas} de {c.total} vistas · alquiler de las no vistas: ${(c.plata or 0):.2f}")
# Muestra:
#   Acción: 0 de 2 vistas · alquiler de las no vistas: $4200.00
#   Drama: 0 de 1 vistas · alquiler de las no vistas: $2200.00
#   Infantil: 2 de 3 vistas · alquiler de las no vistas: $1650.00
# Tres detalles:
#   - OJO: con annotate(), Django NO usa el orden del Meta (ordering). Si
#     querés un orden, ponelo vos con .order_by(...), como acá. Sin eso, el
#     orden queda "el que salga" (y la paginación del paso 3 se queja).
#   - Sum de nada da None, por eso el "or 0": "esto, o 0 si está vacío".
#   - {valor:.2f} adentro de un f-string muestra el número con 2 decimales.
#     (SQLite a veces devuelve las sumas con decimales de más, como 1650.00000000000.)

# Fechas: __year, __month, __day, y también __gte / __lte con una fecha
hoy = timezone.localdate()          # la fecha de hoy, en la zona horaria de settings
print("Cargadas este mes:", Pelicula.objects.filter(creada__year=hoy.year, creada__month=hoy.month).count())
# Muestra: Cargadas este mes: 6     <- (todas: se crearon recién, al ejecutar este archivo)
print("Vistas hasta hoy:", Pelicula.objects.filter(fecha_vista__lte=hoy).count())
# Muestra: Vistas hasta hoy: 1      <- Shrek (marcar_vista le puso la fecha de hoy)


# =======================================================================
# PARTE B7 — VALIDAR ANTES DE GUARDAR
# =======================================================================
# OJO: save() NO revisa las reglas (max_length, tu clean(), los validadores...).
# La base frena algunas cosas (NOT NULL, UNIQUE), pero no todas.
# full_clean() revisa TODAS y, si algo está mal, provoca un ValidationError
# con los mensajes de cada campo (en error.message_dict).
# Los FORMULARIOS de Django (paso 3) llaman a full_clean() solos: por eso en
# una página casi nunca lo escribís a mano.

print()
print("========== PARTE B7: validar ==========")
mala = Pelicula(titulo="", anio=1500, categoria=drama)
try:
    mala.full_clean()
except ValidationError as error:
    for campo, mensajes in error.message_dict.items():
        print(f"  {campo}: {mensajes}")
# Muestra:
#   titulo: ['Este campo no puede estar en blanco.']
#   anio: ['No hay películas tan viejas.']          <- el mensaje de NUESTRO clean()


# =======================================================================
# PARTE B8 — TRANSACCIONES: TODO O NADA
# =======================================================================
# with transaction.atomic(): todo lo de adentro se hace ENTERO, o no se hace
# nada (si hay un error, se deshace solo: el rollback del paso 1).

print()
print("========== PARTE B8: transacciones ==========")
try:
    with transaction.atomic():
        Pelicula.objects.create(titulo="Fantasma", anio=2020, categoria=drama)
        raise RuntimeError("algo salió mal")       # simulamos un error después de crear
except RuntimeError:
    pass                                           # "pass" = no hacer nada (ya sabemos que falló)
print("¿Quedó 'Fantasma'?", Pelicula.objects.filter(titulo="Fantasma").exists())
# Muestra: ¿Quedó 'Fantasma'? False                <- se creó, pero se deshizo


# =======================================================================
# RESUMEN: SQL (paso 1)  ->  ORM de Django
# =======================================================================
#  INSERT ...                       Modelo.objects.create(campo=valor)    /  obj.save()
#  SELECT ... WHERE id = 1          Modelo.objects.get(pk=1)
#  SELECT ... WHERE ...             Modelo.objects.filter(campo__lookup=valor)   /  .exclude(...)
#  ... ORDER BY x DESC LIMIT 3      .order_by("-x")[:3]
#  UPDATE ... SET ... WHERE         obj.campo = x; obj.save()   /   queryset.update(campo=x)
#  ... SET n = n + 1                queryset.update(n=F("n") + 1)
#  DELETE ... WHERE                 obj.delete()   /   queryset.delete()
#  JOIN                             filter(categoria__nombre="X")   /   obj.categoria.nombre
#  COUNT / SUM / AVG                aggregate(nombre=Sum("campo"))["nombre"]
#  ... GROUP BY                     annotate(cantidad=Count("relacion"))
#  BEGIN ... COMMIT / ROLLBACK      with transaction.atomic():
#  (validar)                        obj.full_clean()   y   def clean(self) en el modelo

print()
print("Fin de la clase 2. Ahora abrí ejercicio.md (está en esta misma carpeta).")
