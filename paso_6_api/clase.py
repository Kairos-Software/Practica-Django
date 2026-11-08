"""
=======================================================================
 PASO 6 — TU PROPIA API (JSON) Y USARLA DESDE LA PÁGINA CON JAVASCRIPT
=======================================================================

Hasta ahora tus páginas eran para que las LEA UNA PERSONA. Ahora vas a hacer
que tu sistema también entregue y reciba DATOS para que los use OTRO
PROGRAMA. Y vas a usar esos datos desde tu propia página, con JavaScript,
para hacer un buscador que filtra mientras escribís, sin recargar.

Acá NO nos conectamos con nada de afuera: todo pasa dentro de tu sistema.

El ejemplo de toda la clase: una lista de películas, con un buscador en vivo
y un botón "Me gusta".


¿QUÉ NECESITÁS?
---------------
El entorno virtual activado, con Django instalado.


CÓMO SE USA ESTE ARCHIVO
------------------------
Igual que en los pasos 3 a 5 (parado en "Aprender Django"):

  1) SIMULACIÓN:   python paso_6_api\\clase.py
     Le hace pedidos a la API (buscar, ver una, crear, puntuar, borrar...)
     y muestra cada respuesta. Lo que muestra está anotado en la PARTE 11.

  2) DE VERDAD:    python paso_6_api\\clase.py runserver
     Abrí http://127.0.0.1:8000: escribí en el buscador y mirá cómo se
     filtra la lista sin recargar la página. Apretá F12 (las herramientas
     del navegador) y andá a la pestaña "Red" (o "Network"): vas a ver cada
     pedido que hace la página a la API, y su respuesta.
     También abrí http://127.0.0.1:8000/api/peliculas/ : es la API "pelada",
     los datos en JSON.
     Ctrl+C en la terminal para apagar el servidor. (Crea clase6.sqlite3 al
     lado de este archivo: se puede borrar.)

Las PARTES 1 a 9 explican; la PARTE 10 es el código que se ejecuta. Lo
marcado como MAQUINARIA DE LA CLASE no hace falta entenderlo ni copiarlo.


=======================================================================
PARTE 1 — ¿QUÉ ES UNA API?
=======================================================================
Hasta ahora tus vistas devolvían HTML: una página, para que la lea una
persona. Una API ("interfaz de programación") devuelve DATOS, para que los
use otro programa:
  - una app de celular (así funciona, por ejemplo, la app de Kairos TV:
    le pide los canales a una API),
  - otro sistema,
  - o el JavaScript de tu propia página, para actualizar una parte sin
    recargar todo (el buscador en vivo de esta clase).

Los datos van en JSON, un formato de texto casi igual a los diccionarios y
listas de Python:

    {"id": 1, "titulo": "Matrix", "anio": 1999, "generos": ["Acción"], "vista": true, "nota": null}

Las diferencias con Python: true / false / null (en minúscula) en vez de
True / False / None, y los textos siempre con comillas DOBLES.


=======================================================================
PARTE 2 — DEVOLVER JSON
=======================================================================
    from django.http import JsonResponse

    def api_peliculas(request):
        peliculas = Pelicula.objects.all()
        q = request.GET.get('q', '')                         <- los filtros, igual que en una página
        if q:
            peliculas = peliculas.filter(titulo__icontains=q)
        datos = [{'id': p.id, 'titulo': p.titulo, 'anio': p.anio} for p in peliculas]
        return JsonResponse({'peliculas': datos})            <- un diccionario de Python -> JSON

  - El diccionario de cada objeto se arma A MANO. Así decidís qué datos se
    muestran (nunca mandes contraseñas ni datos privados). Conviene una
    función que lo haga, para usarla en todos lados (pelicula_a_dict, en
    la PARTE 10).
  - JSON solo entiende textos, números, true/false, null, listas y
    diccionarios. Lo demás hay que convertirlo:
        plata (Decimal)    ->  str(p.precio)                    "15000.00"
        una fecha          ->  p.fecha.isoformat()              "2026-10-08"
        una imagen         ->  p.poster.url if p.poster else None
        un objeto relacionado  ->  {'id': p.autor.id, 'nombre': p.autor.nombre}
  - En el navegador, los acentos pueden verse como \\u00ed ("\\u00ed" = í). Es
    normal en JSON: el programa que lo recibe lo lee bien. Para que salgan
    tal cual:  JsonResponse(datos, json_dumps_params={'ensure_ascii': False})


=======================================================================
PARTE 3 — LOS CÓDIGOS DE RESPUESTA (status)
=======================================================================
El programa que llama a tu API mira el NÚMERO para saber cómo le fue
(ya los viste en el paso 3):

    200 OK            todo bien (el que va si no decís otro)
    201 Created       se CREÓ algo nuevo
    204 No Content    salió bien y no hay nada que devolver (ej: después de borrar)
    400 Bad Request   los datos que mandaste están mal
    401 Unauthorized  tenés que iniciar sesión
    403 Forbidden     iniciaste sesión, pero eso no te corresponde
    404 Not Found     no existe
    405 Method Not Allowed   ese método (GET, POST...) no se puede en esta dirección

    return JsonResponse({'error': 'No existe esa película.'}, status=404)
    return HttpResponse(status=204)                  <- sin contenido

  OJO: get_object_or_404 responde una página HTML de error. En una API
  conviene que el error también sea JSON:
        try:
            pelicula = Pelicula.objects.get(pk=pk)
        except Pelicula.DoesNotExist:
            return JsonResponse({'error': 'No existe esa película.'}, status=404)


=======================================================================
PARTE 4 — LOS MÉTODOS: LA MISMA DIRECCIÓN HACE COSAS DISTINTAS
=======================================================================
    GET     /api/peliculas/       -> la lista          GET     /api/peliculas/5/  -> una
    POST    /api/peliculas/       -> crear una nueva   DELETE  /api/peliculas/5/  -> borrarla
    (también existen PUT y PATCH, para editar: mismo estilo)

  En la vista:   if request.method == 'GET': ...   elif request.method == 'POST': ...
  Y para que cualquier otro método dé 405 solo:
        from django.views.decorators.http import require_http_methods

        @require_http_methods(['GET', 'POST'])
        def api_peliculas(request): ...


=======================================================================
PARTE 5 — RECIBIR JSON
=======================================================================
Otro programa te manda los datos como JSON, en el "cuerpo" del pedido (no
como un formulario). Llegan como texto, en request.body, y se convierten:

        import json
        try:
            datos = json.loads(request.body)              <- texto JSON -> diccionario de Python
        except json.JSONDecodeError:                      <- si el texto no es JSON válido
            return JsonResponse({'error': 'El JSON está mal escrito.'}, status=400)

  ¡Y se VALIDAN igual que siempre! Un ModelForm sirve aunque no haya HTML:
        form = PeliculaForm(datos)
        if not form.is_valid():
            return JsonResponse({'errores': form.errors}, status=400)   <- {"anio": ["Introduzca un número entero."]}
        pelicula = form.save()
        return JsonResponse(pelicula_a_dict(pelicula), status=201)

  OJO con las casillas (BooleanField): en un formulario HTML, una casilla
  sin tildar NO se manda, y Django entiende "no". Con JSON pasa lo mismo:
  si el JSON no trae "disponible", el formulario lo toma como False. Si
  querés que por defecto sea True:   datos.setdefault('disponible', True)


=======================================================================
PARTE 6 — REVISAR EL TIPO DE UN DATO SUELTO DEL JSON
=======================================================================
Cuando un dato NO pasa por un formulario (ej: {"estrellas": 4}), hay que
revisarlo a mano. Lo que puede llegar:

    {"estrellas": 4}         <- bien: un int
    {"estrellas": "cuatro"}  <- un texto
    {"estrellas": 4.5}       <- un float (¡int(4.5) da 4 sin avisar!)
    {"estrellas": true}      <- un bool
    {}                       <- no vino: datos.get('estrellas') da None (¡int(None) da TypeError!)

  Por eso no alcanza con int(...). Se pregunta el TIPO con isinstance:
        isinstance(valor, int)       -> True si valor es un número entero

        estrellas = datos.get('estrellas')
        if not isinstance(estrellas, int) or isinstance(estrellas, bool):
            return JsonResponse({'error': 'Las estrellas tienen que ser un número entero.'}, status=400)

  ¿Por qué también "isinstance(estrellas, bool)"? Porque en Python True y
  False SON números enteros por dentro (True vale 1): isinstance(True, int)
  da True. Así que los bool hay que descartarlos aparte.
  Mirá la vista api_puntuar en la PARTE 10, y su simulación en la PARTE 11.


=======================================================================
PARTE 7 — ¿QUIÉN ES? (la sesión) Y LA PROTECCIÓN CSRF
=======================================================================
Si el pedido viene de TU página, el navegador manda solo la cookie de la
sesión: request.user funciona igual que en una página (paso 4). Pero
@login_required redirige al login (una página HTML): en una API conviene
responder 401 en JSON:
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Tenés que iniciar sesión.'}, status=401)
  (Para que una app de celular u otro sistema se identifique sin navegador
  se usan "tokens": es lo que hace Django REST Framework. Ese es el paso
  siguiente, cuando domines esto.)

La protección CSRF ({% csrf_token %}, paso 3) también cuida a los POST y
DELETE de la API. Desde TU página, el JavaScript manda el token en un
encabezado (ver la PARTE 8). Nunca la desactives "porque molesta": es lo
que impide que otra página de internet haga cosas en tu sistema con la
sesión de tu usuario.


=======================================================================
PARTE 8 — USAR LA API DESDE LA PÁGINA (JavaScript, lo mínimo)
=======================================================================
JavaScript es el lenguaje que corre ADENTRO DEL NAVEGADOR (Python corre en
el servidor). Lo usamos para: cada vez que el usuario escribe, pedirle datos
a la API y mostrar el resultado SIN recargar la página. Va adentro de
<script> ... </script>, al final del HTML.

Lo justo y necesario, explicado línea por línea:

    const cuadro = document.getElementById('buscar');        // agarrar el elemento que tiene id="buscar"
    cuadro.addEventListener('input', async () => {           // "cada vez que escriben en él, hacé esto:"
        const respuesta = await fetch('/api/peliculas/?q=' + encodeURIComponent(cuadro.value));
                                                             // pedirle a la API (await = "esperá la respuesta")
        const datos = await respuesta.json();                // el JSON -> un objeto de JavaScript
        const lista = document.getElementById('resultados');
        lista.innerHTML = '';                                // vaciar la lista
        for (const p of datos.peliculas) {                   // un for, como en Python
            const li = document.createElement('li');         // crear un <li>
            li.textContent = p.titulo + ' (' + p.anio + ')'; // su texto (textContent: seguro, no interpreta HTML)
            lista.appendChild(li);                           // agregarlo a la lista
        }
    });

  - En JavaScript las líneas terminan con ; y los bloques van entre { }.
    Los comentarios empiezan con //. "const" crea una variable.
  - encodeURIComponent(texto) prepara el texto para ir en una dirección
    (espacios, acentos, &...).
  - Un link: const a = document.createElement('a'); a.href = '/libros/' + p.id + '/';

  Para un POST (ej: el botón "Me gusta"), con el token CSRF y datos en JSON:
    const respuesta = await fetch('/api/peliculas/5/me-gusta/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': TOKEN},
        body: JSON.stringify({cantidad: 1}),                 // objeto de JavaScript -> texto JSON
    });
    if (respuesta.ok) { ... } else { const error = await respuesta.json(); alert(error.error); }
  (TOKEN se escribe desde Django en el template:   const TOKEN = '{{ csrf_token }}';)

  Para ver qué pasa: en el navegador, F12 → pestaña "Consola" (los errores
  de JavaScript, en rojo) y pestaña "Red" / "Network" (cada pedido a la API
  y su respuesta).


=======================================================================
PARTE 9 — PROBAR UNA API
=======================================================================
  - Los GET, en el navegador: abrí /api/peliculas/?q=toy y vas a ver el JSON.
  - En las pruebas automáticas, con el Client de siempre:
        respuesta = self.client.get('/api/peliculas/', {'q': 'toy'})
        datos = respuesta.json()                                     <- el JSON ya convertido a diccionario
        respuesta = self.client.post('/api/peliculas/', json.dumps({'titulo': 'Up', 'anio': 2009}),
                                     content_type='application/json')
        self.assertEqual(respuesta.status_code, 201)


=======================================================================
PARTE 10 — EN ACCIÓN (desde acá, el archivo se ejecuta)
=======================================================================
"""

import json
import logging
import os
import sys

import django
from django.apps import AppConfig
from django.conf import settings

BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DB = os.path.join(BASE, "clase6.sqlite3")


class ClaseConfig(AppConfig):            # MAQUINARIA DE LA CLASE
    name = "__main__"
    label = "clase"


# La página con el buscador en vivo y el botón "Me gusta"
# (→ en tu proyecto: un .html en templates/, que herede de tu base.html)
PAGINA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Buscador en vivo</title>
<style>body{font-family:sans-serif;max-width:700px;margin:2rem auto;padding:0 1rem} li{margin:.4rem 0}</style>
</head><body>
<h1>Películas</h1>
<p>Escribí y mirá cómo filtra SIN recargar la página (abrí F12 → Red para ver cada pedido a la API).</p>
<input id="buscar" placeholder="Buscar..." autocomplete="off">
<ul id="resultados"></ul>

<script>
const TOKEN = '{{ csrf_token }}';                       // el token CSRF, para los POST

async function buscar() {
    const texto = document.getElementById('buscar').value;
    const respuesta = await fetch('/api/peliculas/?q=' + encodeURIComponent(texto));
    const datos = await respuesta.json();
    const lista = document.getElementById('resultados');
    lista.innerHTML = '';
    for (const p of datos.peliculas) {
        const li = document.createElement('li');
        li.textContent = p.titulo + ' (' + p.anio + ') · ' + p.likes + ' me gusta ';
        const boton = document.createElement('button');
        boton.textContent = '👍';
        boton.addEventListener('click', () => meGusta(p.id));
        li.appendChild(boton);
        lista.appendChild(li);
    }
}

async function meGusta(id) {
    const respuesta = await fetch('/api/peliculas/' + id + '/me-gusta/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': TOKEN},
        body: JSON.stringify({}),
    });
    if (respuesta.ok) {
        buscar();                                        // volver a pedir la lista (con el número nuevo)
    } else {
        const error = await respuesta.json();
        alert(error.error);
    }
}

document.getElementById('buscar').addEventListener('input', buscar);
buscar();                                                // la primera vez, todas
</script>
</body></html>"""

# ── MAQUINARIA DE LA CLASE: la configuración (→ en tu proyecto: config/settings.py) ──
settings.configure(
    DEBUG=True,
    SECRET_KEY="solo-para-la-clase-6",
    ALLOWED_HOSTS=["*"],
    ROOT_URLCONF="__main__",
    INSTALLED_APPS=["django.contrib.contenttypes", "__main__.ClaseConfig"],
    MIDDLEWARE=["django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware"],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ARCHIVO_DB}},
    TEMPLATES=[{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {"loaders": [("django.template.loaders.locmem.Loader", {"pagina.html": PAGINA})]},
    }],
    LANGUAGE_CODE="es-ar",
    TIME_ZONE="America/Argentina/Buenos_Aires",
    USE_TZ=True,
    DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
)
django.setup()

from django import forms
from django.db import models
from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import path
from django.views.decorators.http import require_http_methods, require_POST


# ── El MODELO (→ models.py) ──
class Pelicula(models.Model):
    titulo = models.CharField("título", max_length=120)
    anio = models.PositiveIntegerField("año")
    likes = models.PositiveIntegerField(default=0)
    estrellas = models.PositiveSmallIntegerField(null=True, blank=True)      # de 1 a 5, o vacío

    class Meta:
        ordering = ["titulo"]


# ── El FORMULARIO (→ forms.py): el MISMO tipo de siempre, para validar el JSON ──
class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ["titulo", "anio"]


# ── Las VISTAS (→ views.py, o un archivo aparte, api.py) ──
def pelicula_a_dict(p):
    """Qué datos de una película muestra la API (los decidís vos). PARTE 2."""
    return {"id": p.id, "titulo": p.titulo, "anio": p.anio, "likes": p.likes, "estrellas": p.estrellas}


def no_existe():
    return JsonResponse({"error": "No existe esa película."}, status=404)       # PARTE 3


def pagina(request):
    return render(request, "pagina.html")


@require_http_methods(["GET", "POST"])                                  # PARTE 4: otro método -> 405
def api_peliculas(request):
    if request.method == "GET":                                         # la lista (con el filtro ?q=)
        peliculas = Pelicula.objects.all()
        q = request.GET.get("q", "").strip()
        if q:
            peliculas = peliculas.filter(titulo__icontains=q)
        return JsonResponse({"cantidad": peliculas.count(), "peliculas": [pelicula_a_dict(p) for p in peliculas]})

    try:                                                                # POST: crear, con JSON (PARTE 5)
        datos = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "El JSON está mal escrito."}, status=400)
    form = PeliculaForm(datos)
    if not form.is_valid():
        return JsonResponse({"errores": form.errors}, status=400)
    return JsonResponse(pelicula_a_dict(form.save()), status=201)


@require_http_methods(["GET", "DELETE"])
def api_pelicula(request, pk):
    try:
        pelicula = Pelicula.objects.get(pk=pk)
    except Pelicula.DoesNotExist:
        return no_existe()                                              # 404 en JSON
    if request.method == "DELETE":
        pelicula.delete()
        return HttpResponse(status=204)                                 # borrada: nada que devolver
    return JsonResponse(pelicula_a_dict(pelicula))


@require_POST
def api_me_gusta(request, pk):
    cuantos = Pelicula.objects.filter(pk=pk).update(likes=F("likes") + 1)   # la suma la hace la base (paso 2)
    if not cuantos:
        return no_existe()
    return JsonResponse({"likes": Pelicula.objects.get(pk=pk).likes})


@require_POST
def api_puntuar(request, pk):                                           # PARTE 6
    try:
        pelicula = Pelicula.objects.get(pk=pk)
    except Pelicula.DoesNotExist:
        return no_existe()
    try:
        datos = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "El JSON está mal escrito."}, status=400)
    estrellas = datos.get("estrellas")
    if not isinstance(estrellas, int) or isinstance(estrellas, bool):   # ¿es un número entero (y no True/False)?
        return JsonResponse({"error": "Las estrellas tienen que ser un número entero."}, status=400)
    if not 1 <= estrellas <= 5:                                         # "entre 1 y 5", escrito como en matemática
        return JsonResponse({"error": "Tienen que ser de 1 a 5 estrellas."}, status=400)
    pelicula.estrellas = estrellas
    pelicula.save()
    return JsonResponse({"estrellas": pelicula.estrellas})


# ── Las URLS (→ urls.py) ──
urlpatterns = [
    path("", pagina),
    path("api/peliculas/", api_peliculas),
    path("api/peliculas/<int:pk>/", api_pelicula),
    path("api/peliculas/<int:pk>/me-gusta/", api_me_gusta),
    path("api/peliculas/<int:pk>/puntuar/", api_puntuar),
]


def preparar_base():
    """MAQUINARIA: crear la tabla (en tu proyecto: migrate) y 4 películas de ejemplo."""
    from django.db import connection
    if Pelicula._meta.db_table not in connection.introspection.table_names():
        with connection.schema_editor() as editor:
            editor.create_model(Pelicula)
    if not Pelicula.objects.exists():
        for titulo, anio in (("Matrix", 1999), ("Toy Story", 1995), ("Toy Story 2", 1999), ("Up", 2009)):
            Pelicula.objects.create(titulo=titulo, anio=anio)


# =======================================================================
# PARTE 11 — LA SIMULACIÓN
# =======================================================================
# Hay 4 películas: Matrix (id 1), Toy Story (id 2), Toy Story 2 (id 3) y Up (id 4).
# Debajo de cada pedido está anotado lo que muestra.

def simular():
    from django.test import Client

    logging.getLogger("django.request").setLevel(logging.ERROR)    # MAQUINARIA: sin avisos de cada 404/400
    navegador = Client()

    def mostrar(que, respuesta):
        """Muestra el pedido, el código y el JSON que respondió (con los acentos legibles)."""
        if respuesta.content:
            cuerpo = json.dumps(respuesta.json(), ensure_ascii=False)
        else:
            cuerpo = "(vacío)"
        print()
        print(que)
        print("   código", respuesta.status_code, "·", cuerpo)

    def post_json(direccion, datos):
        """Un POST con datos en JSON (como el fetch de la PARTE 8)."""
        return navegador.post(direccion, json.dumps(datos), content_type="application/json")

    print()
    print("========== PARTE 11: la simulación ==========")

    mostrar("GET /api/peliculas/?q=toy   (buscar)", navegador.get("/api/peliculas/", {"q": "toy"}))
    # Muestra:
    #   GET /api/peliculas/?q=toy   (buscar)
    #      código 200 · {"cantidad": 2, "peliculas": [{"id": 2, "titulo": "Toy Story", "anio": 1995, "likes": 0,
    #                    "estrellas": null}, {"id": 3, "titulo": "Toy Story 2", "anio": 1999, "likes": 0, "estrellas": null}]}

    mostrar("GET /api/peliculas/1/   (una)", navegador.get("/api/peliculas/1/"))
    # Muestra:
    #   GET /api/peliculas/1/   (una)
    #      código 200 · {"id": 1, "titulo": "Matrix", "anio": 1999, "likes": 0, "estrellas": null}

    mostrar("GET /api/peliculas/99/   (no existe)", navegador.get("/api/peliculas/99/"))
    # Muestra:
    #   GET /api/peliculas/99/   (no existe)
    #      código 404 · {"error": "No existe esa película."}

    mostrar("POST /api/peliculas/   con JSON bien (crear)", post_json("/api/peliculas/", {"titulo": "Coco", "anio": 2017}))
    # Muestra:
    #   POST /api/peliculas/   con JSON bien (crear)
    #      código 201 · {"id": 5, "titulo": "Coco", "anio": 2017, "likes": 0, "estrellas": null}

    mostrar("POST /api/peliculas/   con datos mal", post_json("/api/peliculas/", {"titulo": "", "anio": "dos mil"}))
    # Muestra:
    #   POST /api/peliculas/   con datos mal
    #      código 400 · {"errores": {"titulo": ["Este campo es obligatorio."], "anio": ["Introduzca un número entero."]}}
    # Los errores del formulario, igual que en una página.

    mostrar("POST /api/peliculas/   con JSON mal escrito",
            navegador.post("/api/peliculas/", "{esto no es json", content_type="application/json"))
    # Muestra:
    #   POST /api/peliculas/   con JSON mal escrito
    #      código 400 · {"error": "El JSON está mal escrito."}

    mostrar("POST /api/peliculas/1/me-gusta/", navegador.post("/api/peliculas/1/me-gusta/"))
    # Muestra:
    #   POST /api/peliculas/1/me-gusta/
    #      código 200 · {"likes": 1}

    mostrar("GET /api/peliculas/1/me-gusta/   (solo acepta POST)", navegador.get("/api/peliculas/1/me-gusta/"))
    # Muestra:
    #   GET /api/peliculas/1/me-gusta/   (solo acepta POST)
    #      código 405 · (vacío)

    # PARTE 6: revisar el tipo de un dato suelto
    mostrar('POST /api/peliculas/1/puntuar/   {"estrellas": 4}', post_json("/api/peliculas/1/puntuar/", {"estrellas": 4}))
    mostrar('POST /api/peliculas/1/puntuar/   {"estrellas": "cuatro"}',
            post_json("/api/peliculas/1/puntuar/", {"estrellas": "cuatro"}))
    mostrar('POST /api/peliculas/1/puntuar/   {"estrellas": 4.5}', post_json("/api/peliculas/1/puntuar/", {"estrellas": 4.5}))
    mostrar('POST /api/peliculas/1/puntuar/   {}   (sin estrellas)', post_json("/api/peliculas/1/puntuar/", {}))
    mostrar('POST /api/peliculas/1/puntuar/   {"estrellas": 9}', post_json("/api/peliculas/1/puntuar/", {"estrellas": 9}))
    # Muestra:
    #   POST /api/peliculas/1/puntuar/   {"estrellas": 4}
    #      código 200 · {"estrellas": 4}
    #   POST /api/peliculas/1/puntuar/   {"estrellas": "cuatro"}
    #      código 400 · {"error": "Las estrellas tienen que ser un número entero."}
    #   POST /api/peliculas/1/puntuar/   {"estrellas": 4.5}
    #      código 400 · {"error": "Las estrellas tienen que ser un número entero."}
    #   POST /api/peliculas/1/puntuar/   {}   (sin estrellas)
    #      código 400 · {"error": "Las estrellas tienen que ser un número entero."}
    #   POST /api/peliculas/1/puntuar/   {"estrellas": 9}
    #      código 400 · {"error": "Tienen que ser de 1 a 5 estrellas."}

    mostrar("DELETE /api/peliculas/4/   (borrar Up)", navegador.delete("/api/peliculas/4/"))
    # Muestra:
    #   DELETE /api/peliculas/4/   (borrar Up)
    #      código 204 · (vacío)

    print()
    print("Ahora probala de verdad:   python paso_6_api\\clase.py runserver")
    print("y abrí http://127.0.0.1:8000 (Ctrl+C en la terminal para apagarlo).")


def limpiar():
    """MAQUINARIA: borrar la base de la clase."""
    from django.db import connection
    connection.close()
    if os.path.exists(ARCHIVO_DB):
        os.remove(ARCHIVO_DB)


# =======================================================================
# RESUMEN
# =======================================================================
#  devolver JSON     return JsonResponse({...}, status=200)       (Decimal -> str, fecha -> isoformat)
#  sin contenido     return HttpResponse(status=204)
#  qué métodos       @require_http_methods(['GET', 'POST'])  /  @require_POST       (lo demás: 405)
#  no existe         try: Modelo.objects.get(pk=pk) except Modelo.DoesNotExist: ... status=404
#  recibir JSON      datos = json.loads(request.body)   (json.JSONDecodeError -> 400)
#  validar           form = MiForm(datos); form.is_valid(); form.errors   (400 con los errores)
#  un dato suelto    isinstance(valor, int) and not isinstance(valor, bool)
#  sin sesión        if not request.user.is_authenticated: ... status=401
#  JavaScript        fetch(direccion)  ->  await respuesta.json()  ->  createElement / textContent
#  POST desde JS     fetch(..., {method: 'POST', headers: {'X-CSRFToken': TOKEN, ...}, body: JSON.stringify(...)})


# MAQUINARIA: arrancar en modo simulación o en modo servidor
if __name__ == "__main__":
    if len(sys.argv) == 1:
        limpiar()
        preparar_base()
        simular()
        limpiar()
        print()
        print("Fin de la clase 6. Ahora abrí ejercicio.md (está en esta misma carpeta).")
    else:
        preparar_base()
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
