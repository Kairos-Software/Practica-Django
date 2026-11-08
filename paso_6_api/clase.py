"""
═══════════════════════════════════════════════════════════════════════
 PASO 6 — TU PROPIA API (JSON) Y USARLA DESDE LA PÁGINA CON JAVASCRIPT
═══════════════════════════════════════════════════════════════════════

Ejecutalo (con el entorno activado):
    python clase.py              -> simula pedidos a la API y te muestra las respuestas
    python clase.py runserver    -> abrí http://127.0.0.1:8000 (el buscador en vivo y el botón "Me gusta")
                                    y http://127.0.0.1:8000/api/peliculas/ (la API "pelada")

Acá NO nos conectamos con nada de afuera: hacemos que TU sistema entregue y
reciba datos en JSON, y los usamos desde tu propia página.


═══════════════════════════════════════════════════════════════════════
 PARTE 1 — LA EXPLICACIÓN
═══════════════════════════════════════════════════════════════════════

1) ¿QUÉ ES UNA API?
───────────────────
Hasta ahora tus vistas devolvían HTML: una página para que la LEA UNA PERSONA.
Una API devuelve DATOS para que los use OTRO PROGRAMA: una app de celular, otro
sistema, o el JavaScript de tu propia página (para actualizar una parte sin
recargar todo). Así funciona la app de Kairos TV: pide los canales a una API.

Los datos van en JSON, que es casi igual a los diccionarios y listas de Python:
    {"id": 1, "titulo": "Matrix", "anio": 1999, "generos": ["Acción"], "vista": true, "nota": null}
(true/false/null en vez de True/False/None, y siempre comillas dobles)

2) DEVOLVER JSON
────────────────
    from django.http import JsonResponse

    def api_peliculas(request):
        peliculas = Pelicula.objects.all()
        q = request.GET.get('q', '')                         <- los filtros, igual que en una página
        if q:
            peliculas = peliculas.filter(titulo__icontains=q)
        datos = [{'id': p.id, 'titulo': p.titulo, 'anio': p.anio} for p in peliculas]
        return JsonResponse({'peliculas': datos})            <- un diccionario -> JSON
  - Se arma A MANO qué datos van (un diccionario por objeto). Así decidís qué
    se muestra (nunca mandes contraseñas ni datos privados).
  - Decimal (plata) y fechas: pasalos a texto -> str(precio), fecha.isoformat()
  - Una imagen: su dirección -> p.poster.url if p.poster else None
  - Los acentos salen como \u00e1 ("\u00e1" = á): es normal en JSON y el que lo
    recibe lo lee bien. Para verlos tal cual: JsonResponse(datos, json_dumps_params={'ensure_ascii': False})

3) LOS CÓDIGOS DE RESPUESTA (status)
────────────────────────────────────
El programa que te llama mira el NÚMERO para saber cómo le fue:
    200 OK            todo bien (el que va por defecto)
    201 Created       se creó algo nuevo
    204 No Content    salió bien y no hay nada que devolver (ej: después de borrar)
    400 Bad Request   los datos que mandaste están mal
    401 Unauthorized  tenés que iniciar sesión
    403 Forbidden     iniciaste sesión, pero eso no te corresponde
    404 Not Found     no existe
    405 Method Not Allowed   ese método (GET/POST...) no se puede acá
    return JsonResponse({'error': 'No existe esa película.'}, status=404)
  OJO: get_object_or_404 devuelve una página HTML de error. En una API
  conviene responder el error en JSON:
        try:
            pelicula = Pelicula.objects.get(pk=pk)
        except Pelicula.DoesNotExist:
            return JsonResponse({'error': 'No existe esa película.'}, status=404)

4) LOS MÉTODOS: la MISMA dirección hace cosas distintas
───────────────────────────────────────────────────────
    GET     /api/peliculas/        -> la lista            GET    /api/peliculas/5/  -> una
    POST    /api/peliculas/        -> crear una nueva     DELETE /api/peliculas/5/  -> borrarla
    (también PUT/PATCH para editar: mismo estilo)
  En la vista:  if request.method == 'GET': ...  elif request.method == 'POST': ...
  Y para que otro método dé 405:  from django.views.decorators.http import require_http_methods
                                  @require_http_methods(['GET', 'POST'])

5) RECIBIR JSON
───────────────
Otro programa te manda los datos como JSON en el "cuerpo" del pedido (no como
un formulario). Se leen así:
        import json
        try:
            datos = json.loads(request.body)              <- texto JSON -> diccionario
        except json.JSONDecodeError:
            return JsonResponse({'error': 'El JSON está mal escrito.'}, status=400)
  ¡Y se validan igual que siempre! Un ModelForm sirve aunque no haya HTML:
        form = PeliculaForm(datos)
        if not form.is_valid():
            return JsonResponse({'errores': form.errors}, status=400)   <- {"anio": ["Introduzca un número entero."]}
        pelicula = form.save()
        return JsonResponse(pelicula_a_dict(pelicula), status=201)

6) ¿QUIÉN ES? (sesión)
──────────────────────
Si el pedido viene de TU página, el navegador manda la cookie de sesión sola:
request.user funciona igual que en una página. Pero @login_required redirige
al login (HTML): en una API conviene responder 401 en JSON:
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Tenés que iniciar sesión.'}, status=401)
  (Para que una app de celular u otro sistema se identifique sin navegador se
  usan "tokens": es lo que hace Django REST Framework. Eso es el paso
  siguiente cuando domines esto.)

7) CSRF EN LA API
─────────────────
La protección CSRF ({% csrf_token %}) también cuida a los POST de la API.
Desde TU página, el JavaScript manda el token en un encabezado (ver punto 8).
Nunca la desactives "porque molesta": es lo que impide que otra página haga
cosas en tu sistema con la sesión de tu usuario.

8) USAR LA API DESDE LA PÁGINA (JavaScript, lo mínimo)
──────────────────────────────────────────────────────
JavaScript es el lenguaje que corre EN EL NAVEGADOR. Lo usamos para: cuando
el usuario escribe, pedir datos a la API y mostrar el resultado SIN recargar.
Va dentro de <script> ... </script> al final del HTML. Lo justo y necesario:

    const cuadro = document.getElementById('buscar');       // agarrar un elemento por su id
    cuadro.addEventListener('input', async () => {          // "cada vez que escriben..."
        const respuesta = await fetch('/api/peliculas/?q=' + encodeURIComponent(cuadro.value));   // pedirle a la API
        const datos = await respuesta.json();               // el JSON -> un objeto de JavaScript
        const lista = document.getElementById('resultados');
        lista.innerHTML = '';                               // vaciar la lista
        for (const p of datos.peliculas) {                  // un for, como en Python
            const li = document.createElement('li');        // crear un <li>
            li.textContent = p.titulo + ' (' + p.anio + ')';   // su texto (textContent: seguro, no interpreta HTML)
            lista.appendChild(li);                          // agregarlo a la lista
        }
    });

  Para un POST (ej: "Me gusta"), con el token CSRF y datos en JSON:
    const respuesta = await fetch('/api/peliculas/5/me-gusta/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': TOKEN},
        body: JSON.stringify({cantidad: 1}),                // objeto -> texto JSON
    });
    if (respuesta.ok) { ... } else { const error = await respuesta.json(); alert(error.error); }
  (TOKEN se pone desde Django en el template: const TOKEN = '{{ csrf_token }}';)

  Para ver qué pasa: en el navegador, F12 -> pestaña "Consola" (los errores
  de JavaScript) y pestaña "Red" / "Network" (cada pedido a la API y su respuesta).

9) PROBAR UNA API
─────────────────
  - Los GET, en el navegador: abrí /api/peliculas/?q=toy y vas a ver el JSON.
  - En las pruebas automáticas, con el Client de siempre:
        respuesta = self.client.get('/api/peliculas/', {'q': 'toy'})
        datos = respuesta.json()                                     <- el JSON ya convertido
        respuesta = self.client.post('/api/peliculas/', json.dumps({'titulo': 'Up', 'anio': 2009}),
                                     content_type='application/json')
        self.assertEqual(respuesta.status_code, 201)


═══════════════════════════════════════════════════════════════════════
 PARTE 2 — EN ACCIÓN (desde acá se ejecuta)
═══════════════════════════════════════════════════════════════════════
"""

import json
import os
import sys

import django
from django.apps import AppConfig
from django.conf import settings

BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DB = os.path.join(BASE, "clase6.sqlite3")


class ClaseConfig(AppConfig):
    name = "__main__"
    label = "clase"


# La página con el buscador en vivo y el botón "Me gusta" (→ en tu proyecto: un .html en templates/)
PAGINA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Buscador en vivo</title>
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

from django import forms  # noqa: E402
from django.db import models  # noqa: E402
from django.db.models import F  # noqa: E402
from django.http import HttpResponse, JsonResponse  # noqa: E402
from django.shortcuts import render  # noqa: E402
from django.urls import path  # noqa: E402
from django.views.decorators.http import require_http_methods, require_POST  # noqa: E402


class Pelicula(models.Model):
    titulo = models.CharField("título", max_length=120)
    anio = models.PositiveIntegerField("año")
    likes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["titulo"]


class PeliculaForm(forms.ModelForm):          # el MISMO tipo de formulario de siempre, para validar el JSON
    class Meta:
        model = Pelicula
        fields = ["titulo", "anio"]


def pelicula_a_dict(p):
    """Qué datos de una película se muestran en la API (los decidís vos)."""
    return {"id": p.id, "titulo": p.titulo, "anio": p.anio, "likes": p.likes}


def no_existe():
    return JsonResponse({"error": "No existe esa película."}, status=404)


def pagina(request):
    return render(request, "pagina.html")


@require_http_methods(["GET", "POST"])
def api_peliculas(request):
    if request.method == "GET":                                         # 2) la lista
        peliculas = Pelicula.objects.all()
        q = request.GET.get("q", "").strip()
        if q:
            peliculas = peliculas.filter(titulo__icontains=q)
        return JsonResponse({"cantidad": peliculas.count(), "peliculas": [pelicula_a_dict(p) for p in peliculas]})

    try:                                                                # 5) POST: crear con JSON
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
        return no_existe()                                              # 3) 404 en JSON
    if request.method == "DELETE":
        pelicula.delete()
        return HttpResponse(status=204)                                 # 3) borrado, nada que devolver
    return JsonResponse(pelicula_a_dict(pelicula))


@require_POST
def api_me_gusta(request, pk):
    cuantos = Pelicula.objects.filter(pk=pk).update(likes=F("likes") + 1)   # la suma la hace la base
    if not cuantos:
        return no_existe()
    return JsonResponse({"likes": Pelicula.objects.get(pk=pk).likes})


urlpatterns = [
    path("", pagina),
    path("api/peliculas/", api_peliculas),
    path("api/peliculas/<int:pk>/", api_pelicula),
    path("api/peliculas/<int:pk>/me-gusta/", api_me_gusta),
]


def preparar_base():
    from django.db import connection
    if Pelicula._meta.db_table not in connection.introspection.table_names():
        with connection.schema_editor() as editor:
            editor.create_model(Pelicula)
    if not Pelicula.objects.exists():
        for titulo, anio in (("Matrix", 1999), ("Toy Story", 1995), ("Toy Story 2", 1999), ("Up", 2009)):
            Pelicula.objects.create(titulo=titulo, anio=anio)


def simular():
    from django.test import Client
    navegador = Client()

    def mostrar(que, respuesta):
        cuerpo = respuesta.content.decode() or "(vacío)"
        print(f"\n{que}\n   código {respuesta.status_code} · {cuerpo}")

    mostrar("GET /api/peliculas/?q=toy", navegador.get("/api/peliculas/", {"q": "toy"}))
    mostrar("GET /api/peliculas/1/", navegador.get("/api/peliculas/1/"))
    mostrar("GET /api/peliculas/99/  (no existe: 404 en JSON)", navegador.get("/api/peliculas/99/"))
    mostrar("POST /api/peliculas/  con JSON bien (crear: 201)",
            navegador.post("/api/peliculas/", json.dumps({"titulo": "Coco", "anio": 2017}),
                           content_type="application/json"))
    mostrar("POST /api/peliculas/  con datos mal (400 con los errores)",
            navegador.post("/api/peliculas/", json.dumps({"titulo": "", "anio": "dos mil"}),
                           content_type="application/json"))
    mostrar("POST /api/peliculas/  con JSON mal escrito (400)",
            navegador.post("/api/peliculas/", "{esto no es json", content_type="application/json"))
    mostrar("POST /api/peliculas/1/me-gusta/", navegador.post("/api/peliculas/1/me-gusta/"))
    mostrar("GET /api/peliculas/1/me-gusta/  (solo POST: 405)", navegador.get("/api/peliculas/1/me-gusta/"))
    mostrar("DELETE /api/peliculas/4/  (204: borrada)", navegador.delete("/api/peliculas/4/"))
    print("\nAhora probalo de verdad:  python clase.py runserver   y abrí http://127.0.0.1:8000")


def limpiar():
    from django.db import connection
    connection.close()
    if os.path.exists(ARCHIVO_DB):
        os.remove(ARCHIVO_DB)


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
