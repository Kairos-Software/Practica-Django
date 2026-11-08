import csv
import io

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Avg, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import AutorForm, ImportarForm, LibroForm, ReseniaForm, VenderForm
from .models import Autor, Libro, Resenia

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
    resenias = libro.resenias.select_related("usuario")
    ya_opino = request.user.is_authenticated and resenias.filter(usuario=request.user).exists()
    return render(request, "libros/detalle.html", {
        "libro": libro,
        "vender_form": VenderForm(),
        "resenias": resenias,
        "promedio": resenias.aggregate(promedio=Avg("puntaje"))["promedio"],
        "ya_opino": ya_opino,
        "resenia_form": ReseniaForm(),
    })


@login_required
def crear(request):
    if request.method == "POST":
        form = LibroForm(request.POST, request.FILES)       # request.FILES: la portada
        if form.is_valid():
            libro = form.save()
            messages.success(request, f"Se guardó «{libro.titulo}».")
            return redirect("libros:detalle", pk=libro.pk)
    else:
        form = LibroForm()
    return render(request, "libros/form.html", {"form": form, "titulo": "Nuevo libro"})


@login_required
def editar(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    vieja = libro.portada                       # la que tenía antes de cambiar nada
    if request.method == "POST":
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            if vieja and vieja != libro.portada:    # cambió (o la sacaron): el archivo viejo se borra
                vieja.delete(save=False)
            messages.success(request, f"Se guardó «{libro.titulo}».")
            return redirect("libros:detalle", pk=libro.pk)
    else:
        form = LibroForm(instance=libro)
    return render(request, "libros/form.html", {"form": form, "titulo": f"Editar «{libro.titulo}»"})


@login_required
def borrar(request, pk):
    """GET: la página "¿seguro?". POST (el botón): borra."""
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == "POST":
        if libro.portada:
            libro.portada.delete(save=False)    # primero el archivo...
        libro.delete()                          # ...después el registro
        messages.success(request, f"Se borró «{libro.titulo}».")
        return redirect("libros:lista")
    return render(request, "libros/confirmar_borrar.html", {"libro": libro})


@login_required        # primero login_required: sin sesión manda al login (y no da 405)
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


@login_required
def crear_autor(request):
    if request.method == "POST":
        form = AutorForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo = form.save()
            messages.success(request, f"Se guardó a {nuevo.nombre}.")
            return redirect("libros:autor", pk=nuevo.pk)
    else:
        form = AutorForm()
    return render(request, "libros/form.html", {"form": form, "titulo": "Nuevo autor"})


# ── Reseñas ──────────────────────────────────────────────────────────

@login_required
@require_POST
def resenia(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if libro.resenias.filter(usuario=request.user).exists():
        messages.error(request, "Ya opinaste sobre este libro.")
        return redirect("libros:detalle", pk=pk)
    form = ReseniaForm(request.POST)
    if form.is_valid():
        nueva = form.save(commit=False)     # todavía sin guardar...
        nueva.usuario = request.user        # ...le completamos lo que no viene del formulario
        nueva.libro = libro
        nueva.save()
        messages.success(request, "¡Gracias por tu reseña!")
    else:
        messages.error(request, "La reseña no se guardó: el puntaje va del 1 al 5 y el texto es obligatorio.")
    return redirect("libros:detalle", pk=pk)


@login_required
@require_POST
def borrar_resenia(request, pk):
    # usuario=request.user: si la reseña es de otro, no la encuentra (404)
    resenia_ = get_object_or_404(Resenia, pk=pk, usuario=request.user)
    resenia_.delete()
    messages.success(request, "Se borró tu reseña.")
    return redirect("libros:detalle", pk=resenia_.libro_id)


class MisResenias(LoginRequiredMixin, ListView):
    """Una vista de CLASE: la lista de mis reseñas. Usa el template libros/resenia_list.html"""
    model = Resenia

    def get_queryset(self):
        return Resenia.objects.filter(usuario=self.request.user).select_related("libro")


# ── Registro ─────────────────────────────────────────────────────────

def registro(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        login(request, usuario)             # queda con la sesión iniciada
        messages.success(request, f"¡Bienvenido/a, {usuario.username}!")
        return redirect("libros:lista")
    return render(request, "registration/registro.html", {"form": form})


# ── Planillas ────────────────────────────────────────────────────────

def exportar(request):
    """Descarga libros.csv (separado por ; para que Excel en castellano lo abra bien)."""
    respuesta = HttpResponse(content_type="text/csv; charset=utf-8")
    respuesta["Content-Disposition"] = 'attachment; filename="libros.csv"'
    respuesta.write("\ufeff")                   # para que Excel lea bien los acentos
    escritor = csv.writer(respuesta, delimiter=";")
    escritor.writerow(["titulo", "autor", "precio", "stock"])
    for libro in Libro.objects.select_related("autor").order_by("titulo"):
        escritor.writerow([libro.titulo, libro.autor.nombre, libro.precio, libro.stock])
    return respuesta


@login_required
def importar(request):
    form = ImportarForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        try:
            texto = form.cleaned_data["archivo"].read().decode("utf-8-sig")
        except UnicodeDecodeError:
            messages.error(request, "El archivo no es una planilla CSV.")
            return redirect("libros:importar")
        importados, errores = 0, []
        for numero, fila in enumerate(csv.DictReader(io.StringIO(texto), delimiter=";"), start=2):
            # Cada fila se valida con el MISMO formulario de las páginas (todas sus reglas:
            # precio mayor a 0, stock no negativo, año que no sea futuro...) y adentro de una
            # transacción: si la fila está mal, se deshace todo lo de esa fila, incluido el
            # autor que se haya creado para ella.
            try:
                nombre_autor = fila["autor"].strip()
                if not nombre_autor:
                    raise ValueError("Falta el autor.")
                with transaction.atomic():
                    autor, _ = Autor.objects.get_or_create(nombre=nombre_autor)
                    form = LibroForm({"titulo": fila["titulo"], "autor": autor.pk, "precio": fila["precio"],
                                      "stock": fila["stock"], "anio": fila["anio"], "disponible": True})
                    if not form.is_valid():
                        raise ValueError("La fila tiene datos mal.")    # sale del atomic: se deshace el autor
                    form.save()
                importados += 1
            except (KeyError, AttributeError, ValueError):
                # KeyError: falta una columna en los títulos de la planilla.
                # AttributeError: la fila tiene columnas de menos (el dato llega como None).
                # ValueError: falta el autor, o el formulario rechazó algún dato.
                errores.append(numero)
        messages.success(request, f"Se importaron {importados} libros.")
        if errores:
            messages.error(request, f"Estas filas tenían errores y no se cargaron: {', '.join(map(str, errores))}.")
        return redirect("libros:lista")
    return render(request, "libros/importar.html", {"form": form})
