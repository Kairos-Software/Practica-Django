"""
La API de la librería: las mismas cosas que las páginas, pero en JSON, para
que las use otro programa o el JavaScript de nuestras páginas (el buscador).

    GET    api/libros/                 la lista (?q= y ?autor=)
    POST   api/libros/                 crear un libro (con sesión)
    GET    api/libros/<id>/            un libro, con sus reseñas
    DELETE api/libros/<id>/            borrarlo (con sesión)
    POST   api/libros/<id>/vender/     vender {"cantidad": 2} (con sesión)
"""

import json

from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods, require_POST

from .forms import LibroForm
from .models import Libro

SIN_SESION = {"error": "Tenés que iniciar sesión."}
NO_EXISTE = {"error": "No existe ese libro."}


# ── Cómo se ve un libro en JSON (lo decidimos nosotros) ──────────────

def libro_en_lista(libro):
    return {
        "id": libro.id,
        "titulo": libro.titulo,
        "autor": libro.autor.nombre,
        "precio": str(libro.precio),        # Decimal -> texto ("15000.00"): JSON no tiene Decimal
        "stock": libro.stock,
        "disponible": libro.disponible,
    }


def libro_completo(libro):
    resenias = libro.resenias.select_related("usuario")
    return {
        "id": libro.id,
        "titulo": libro.titulo,
        "autor": {"id": libro.autor.id, "nombre": libro.autor.nombre},
        "precio": str(libro.precio),
        "stock": libro.stock,
        "anio": libro.anio,
        "disponible": libro.disponible,
        "portada": libro.portada.url if libro.portada else None,
        "promedio": resenias.aggregate(promedio=Avg("puntaje"))["promedio"],
        "resenias": [{"usuario": r.usuario.username, "puntaje": r.puntaje, "texto": r.texto} for r in resenias],
    }


def leer_json(request):
    """El JSON que mandaron, como diccionario. None si está mal escrito."""
    try:
        datos = json.loads(request.body)
    except json.JSONDecodeError:
        return None
    return datos if isinstance(datos, dict) else None


def json_mal_escrito():
    return JsonResponse({"error": "El JSON está mal escrito."}, status=400)


# ── Las vistas ───────────────────────────────────────────────────────

@require_http_methods(["GET", "POST"])
def libros(request):
    if request.method == "GET":
        lista = Libro.objects.select_related("autor").order_by("titulo")
        q = request.GET.get("q", "").strip()
        autor = request.GET.get("autor", "")
        if q:
            lista = lista.filter(titulo__icontains=q)
        if autor.isdigit():
            lista = lista.filter(autor_id=autor)
        return JsonResponse({"cantidad": lista.count(), "libros": [libro_en_lista(l) for l in lista]})

    # POST: crear
    if not request.user.is_authenticated:
        return JsonResponse(SIN_SESION, status=401)
    datos = leer_json(request)
    if datos is None:
        return json_mal_escrito()
    datos.setdefault("disponible", True)     # en un formulario, una casilla que no viene = False
    form = LibroForm(datos)                  # ¡el mismo formulario de las páginas, con todas sus reglas!
    if not form.is_valid():
        return JsonResponse({"errores": form.errors}, status=400)
    return JsonResponse(libro_completo(form.save()), status=201)


@require_http_methods(["GET", "DELETE"])
def libro(request, pk):
    try:
        libro_ = Libro.objects.select_related("autor").get(pk=pk)
    except Libro.DoesNotExist:
        return JsonResponse(NO_EXISTE, status=404)
    if request.method == "DELETE":
        if not request.user.is_authenticated:
            return JsonResponse(SIN_SESION, status=401)
        if libro_.portada:
            libro_.portada.delete(save=False)
        libro_.delete()
        return HttpResponse(status=204)       # borrado: nada que devolver
    return JsonResponse(libro_completo(libro_))


@require_POST
def vender(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse(SIN_SESION, status=401)
    try:
        libro_ = Libro.objects.get(pk=pk)
    except Libro.DoesNotExist:
        return JsonResponse(NO_EXISTE, status=404)
    datos = leer_json(request)
    if datos is None:
        return json_mal_escrito()
    cantidad = datos.get("cantidad")
    # isinstance(cantidad, bool): en Python True también es un int, y no queremos "vender True"
    if not isinstance(cantidad, int) or isinstance(cantidad, bool):
        return JsonResponse({"error": "La cantidad tiene que ser un número entero."}, status=400)
    try:
        libro_.vender(cantidad)              # la regla de siempre, en el modelo
    except ValueError as error:
        return JsonResponse({"error": str(error)}, status=400)
    return JsonResponse({"stock": libro_.stock})
