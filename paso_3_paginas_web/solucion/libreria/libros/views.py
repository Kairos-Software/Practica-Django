from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import AutorForm, LibroForm, VenderForm
from .models import Autor, Libro

LIBROS_POR_PAGINA = 10


# ── Libros ───────────────────────────────────────────────────────────

def lista(request):
    q = request.GET.get("q", "").strip()
    autor_id = request.GET.get("autor", "")

    libros = Libro.objects.select_related("autor")       # el autor en la MISMA consulta
    if q:
        libros = libros.filter(titulo__icontains=q)
    if autor_id.isdigit():
        libros = libros.filter(autor_id=autor_id)

    # Los filtros de ahora SIN la página, para que los links de las páginas no los pierdan
    filtros = request.GET.copy()
    filtros.pop("pagina", None)
    return render(request, "libros/lista.html", {
        "pagina": Paginator(libros, LIBROS_POR_PAGINA).get_page(request.GET.get("pagina")),
        "q": q,
        "autor_id": autor_id,
        "autores": Autor.objects.all(),
        "filtros": filtros.urlencode(),
    })


def detalle(request, pk):
    libro = get_object_or_404(Libro.objects.select_related("autor"), pk=pk)
    return render(request, "libros/detalle.html", {"libro": libro, "vender_form": VenderForm()})


def crear(request):
    if request.method == "POST":
        form = LibroForm(request.POST)
        if form.is_valid():
            libro = form.save()
            messages.success(request, f"Se guardó «{libro.titulo}».")
            return redirect("libros:detalle", pk=libro.pk)
    else:
        form = LibroForm()
    return render(request, "libros/form.html", {"form": form, "titulo": "Nuevo libro"})


def editar(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == "POST":
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, f"Se guardó «{libro.titulo}».")
            return redirect("libros:detalle", pk=libro.pk)
    else:
        form = LibroForm(instance=libro)
    return render(request, "libros/form.html", {"form": form, "titulo": f"Editar «{libro.titulo}»"})


def borrar(request, pk):
    """GET: la página "¿seguro?". POST (el botón): borra."""
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == "POST":
        libro.delete()
        messages.success(request, f"Se borró «{libro.titulo}».")
        return redirect("libros:lista")
    return render(request, "libros/confirmar_borrar.html", {"libro": libro})


@require_POST
def vender(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    form = VenderForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Poné una cantidad válida (1 o más).")
    else:
        cantidad = form.cleaned_data["cantidad"]
        try:
            libro.vender(cantidad)    # la regla vive en el modelo (paso 2)
        except ValueError as error:
            messages.error(request, str(error))
        else:
            messages.success(request, f"Se vendieron {cantidad}.")
    return redirect("libros:detalle", pk=libro.pk)


# ── Autores ──────────────────────────────────────────────────────────

def autores(request):
    # annotate: la base cuenta los libros de cada autor (no el template)
    lista_de_autores = Autor.objects.annotate(cantidad=Count("libros")).order_by("nombre")
    return render(request, "libros/autores.html", {"autores": lista_de_autores})


def autor(request, pk):
    autor_ = get_object_or_404(Autor, pk=pk)
    return render(request, "libros/autor.html", {"autor": autor_, "libros": autor_.libros.all()})


def crear_autor(request):
    if request.method == "POST":
        form = AutorForm(request.POST)
        if form.is_valid():
            nuevo = form.save()
            messages.success(request, f"Se guardó a {nuevo.nombre}.")
            return redirect("libros:autor", pk=nuevo.pk)
    else:
        form = AutorForm()
    return render(request, "libros/form.html", {"form": form, "titulo": "Nuevo autor"})
