from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, ProtectedError, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import DuenioForm, MascotaForm, VisitaForm
from .models import Duenio, Mascota, Visita

# Lo que debe un dueño: la suma de los costos de las visitas SIN pagar de sus mascotas
DEUDA = Sum("mascotas__visitas__costo", filter=Q(mascotas__visitas__pagada=False))


# ── Inicio ───────────────────────────────────────────────────────────

@login_required
def inicio(request):
    hoy = timezone.localdate()
    del_mes = Visita.objects.filter(fecha__year=hoy.year, fecha__month=hoy.month)
    especies = dict(Mascota.Especie.choices)
    return render(request, "clinica/inicio.html", {
        "total_mascotas": Mascota.objects.count(),
        "por_especie": [(especies[fila["especie"]], fila["cantidad"]) for fila in
                        Mascota.objects.values("especie").annotate(cantidad=Count("id")).order_by("-cantidad")],
        "visitas_del_mes": del_mes.count(),
        "cobrado_del_mes": del_mes.filter(pagada=True).aggregate(total=Sum("costo"))["total"] or 0,
        "deuda_total": Visita.objects.filter(pagada=False).aggregate(total=Sum("costo"))["total"] or 0,
        "ultimas": Visita.objects.select_related("mascota", "mascota__duenio")[:5],
    })


# ── Dueños (vistas de CLASE) ─────────────────────────────────────────

class Duenios(LoginRequiredMixin, ListView):
    model = Duenio
    paginate_by = 20

    def get_queryset(self):
        # distinct=True: al atravesar dos relaciones (mascotas y visitas) se repetirían filas
        # order_by: con totales (annotate) Django no usa el orden de Meta, hay que pedirlo
        duenios = Duenio.objects.annotate(cantidad=Count("mascotas", distinct=True), deuda=DEUDA).order_by("nombre")
        q = self.request.GET.get("q", "").strip()
        if q:
            duenios = duenios.filter(Q(nombre__icontains=q) | Q(telefono__icontains=q))
        return duenios

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), "q": self.request.GET.get("q", "")}


class DetalleDuenio(LoginRequiredMixin, DetailView):
    model = Duenio

    def get_queryset(self):
        return Duenio.objects.annotate(deuda=DEUDA)


class FormularioDeDuenio(LoginRequiredMixin):
    """Lo que tienen en común crear y editar un dueño (un mixin propio)."""
    model = Duenio
    form_class = DuenioForm

    def form_valid(self, form):
        messages.success(self.request, f"Se guardó a {form.instance.nombre}.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("clinica:duenio", args=[self.object.pk])


class CrearDuenio(FormularioDeDuenio, CreateView):
    pass


class EditarDuenio(FormularioDeDuenio, UpdateView):
    pass


@login_required
def borrar_duenio(request, pk):
    duenio = get_object_or_404(Duenio, pk=pk)
    if request.method == "POST":
        try:
            duenio.delete()
        except ProtectedError:
            messages.error(request, f"No se puede borrar a {duenio}: tiene mascotas. Borralas o pasalas a otro dueño antes.")
            return redirect("clinica:duenio", pk=pk)
        messages.success(request, f"Se borró a {duenio}.")
        return redirect("clinica:duenios")
    return render(request, "clinica/confirmar.html", {
        "pregunta": f"¿Borrar a {duenio}?", "volver": reverse("clinica:duenio", args=[pk]),
    })


# ── Mascotas (vistas de FUNCIÓN y de clase) ──────────────────────────

@login_required
def mascotas(request):
    q = request.GET.get("q", "").strip()
    especie = request.GET.get("especie", "")
    lista = Mascota.objects.select_related("duenio")
    if q:
        # El nombre de la mascota O el de su dueño
        lista = lista.filter(Q(nombre__icontains=q) | Q(duenio__nombre__icontains=q))
    if especie in Mascota.Especie.values:
        lista = lista.filter(especie=especie)
    filtros = request.GET.copy()
    filtros.pop("pagina", None)
    return render(request, "clinica/mascotas.html", {
        "pagina": Paginator(lista, 12).get_page(request.GET.get("pagina")),
        "q": q, "especie": especie, "especies": Mascota.Especie.choices, "filtros": filtros.urlencode(),
    })


@login_required
def mascota(request, pk):
    """La ficha, y el formulario de visita nueva (que se manda a esta misma página)."""
    mascota_ = get_object_or_404(Mascota.objects.select_related("duenio"), pk=pk)
    form = VisitaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        visita = form.save(commit=False)
        visita.mascota = mascota_
        visita.atendida_por = request.user
        visita.save()
        messages.success(request, "Visita cargada.")
        return redirect("clinica:mascota", pk=pk)
    visitas = mascota_.visitas.select_related("atendida_por")
    return render(request, "clinica/mascota.html", {
        "mascota": mascota_, "visitas": visitas, "form": form,
        "total_gastado": visitas.aggregate(total=Sum("costo"))["total"] or 0,
    })


@login_required
def crear_mascota(request):
    if request.method == "POST":
        form = MascotaForm(request.POST, request.FILES)      # request.FILES: la foto
        if form.is_valid():
            nueva = form.save()                             # guarda también las vacunas (ManyToMany)
            messages.success(request, f"Se agregó a {nueva.nombre}.")
            return redirect("clinica:mascota", pk=nueva.pk)
    else:
        # Desde la ficha de un dueño: ?duenio=5 -> el formulario arranca con ese dueño elegido
        form = MascotaForm(initial={"duenio": request.GET.get("duenio")})
    return render(request, "clinica/form.html", {"form": form, "titulo": "Nueva mascota", "con_archivos": True})


class EditarMascota(LoginRequiredMixin, UpdateView):
    model = Mascota
    form_class = MascotaForm
    template_name = "clinica/form.html"                     # en vez del nombre por defecto
    extra_context = {"titulo": "Editar mascota", "con_archivos": True}

    def get_success_url(self):
        messages.success(self.request, "Cambios guardados.")
        return reverse("clinica:mascota", args=[self.object.pk])


class BorrarMascota(LoginRequiredMixin, DeleteView):
    model = Mascota
    template_name = "clinica/confirmar.html"
    success_url = reverse_lazy("clinica:mascotas")

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs),
                "pregunta": f"¿Borrar a {self.object.nombre} y todas sus visitas?",
                "volver": reverse("clinica:mascota", args=[self.object.pk])}


# ── Visitas ──────────────────────────────────────────────────────────

@login_required
@require_POST
def marcar_pagada(request, pk):
    visita = get_object_or_404(Visita, pk=pk)
    visita.pagada = True
    visita.save()
    messages.success(request, f"Visita del {visita.fecha:%d/%m} marcada como pagada.")
    # Vuelve a la página de donde vino: la de deudas o la ficha de la mascota.
    # (Nunca redirigir a una dirección cualquiera que mande el navegador)
    if request.POST.get("desde") == "deudas":
        return redirect("clinica:deudas")
    return redirect("clinica:mascota", pk=visita.mascota_id)


@login_required
def deudas(request):
    sin_pagar = Visita.objects.filter(pagada=False).select_related("mascota", "mascota__duenio")
    return render(request, "clinica/deudas.html", {
        "visitas": sin_pagar, "total": sin_pagar.aggregate(total=Sum("costo"))["total"] or 0,
    })


# ── API ──────────────────────────────────────────────────────────────

@login_required
def api_mascota(request, pk):
    try:
        m = Mascota.objects.select_related("duenio").get(pk=pk)
    except Mascota.DoesNotExist:
        # En una API, el error también en JSON (get_object_or_404 devolvería una página HTML)
        return JsonResponse({"error": "No existe esa mascota."}, status=404)
    return JsonResponse({
        "id": m.id,
        "nombre": m.nombre,
        "especie": m.get_especie_display(),
        "edad": m.edad(),
        "duenio": {"nombre": m.duenio.nombre, "telefono": m.duenio.telefono},
        "vacunas": [v.nombre for v in m.vacunas.all()],
        "visitas": [{"fecha": v.fecha.isoformat(), "motivo": v.motivo, "costo": str(v.costo), "pagada": v.pagada}
                    for v in m.visitas.all()],
    })
