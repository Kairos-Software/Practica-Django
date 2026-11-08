from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Duenio(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField("teléfono", max_length=30)
    email = models.EmailField(blank=True)
    direccion = models.CharField("dirección", max_length=150, blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "dueño"

    def __str__(self):
        return self.nombre


class Vacuna(models.Model):
    nombre = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Mascota(models.Model):
    class Especie(models.TextChoices):
        PERRO = "perro", "Perro"
        GATO = "gato", "Gato"
        AVE = "ave", "Ave"
        CONEJO = "conejo", "Conejo"
        OTRO = "otro", "Otro"

    nombre = models.CharField(max_length=60)
    especie = models.CharField(max_length=10, choices=Especie.choices)
    raza = models.CharField(max_length=60, blank=True)
    nacimiento = models.DateField("fecha de nacimiento", null=True, blank=True)
    foto = models.ImageField(upload_to="mascotas/", blank=True)
    # PROTECT: un dueño con mascotas no se puede borrar
    duenio = models.ForeignKey(Duenio, on_delete=models.PROTECT, related_name="mascotas", verbose_name="dueño")
    vacunas = models.ManyToManyField(Vacuna, blank=True, related_name="mascotas")

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.get_especie_display()})"

    def clean(self):
        if self.nacimiento and self.nacimiento > date.today():
            raise ValidationError({"nacimiento": "La fecha de nacimiento no puede ser en el futuro."})

    def edad(self, hoy=None):
        """ "3 años", "1 año", "8 meses", "Recién nacido" o "Edad desconocida". """
        if not self.nacimiento:
            return "Edad desconocida"
        hoy = hoy or date.today()
        meses = (hoy.year - self.nacimiento.year) * 12 + hoy.month - self.nacimiento.month
        if hoy.day < self.nacimiento.day:
            meses -= 1          # todavía no cumplió el mes
        if meses < 1:
            return "Recién nacido"
        if meses < 12:
            return f"{meses} mes{'es' if meses > 1 else ''}"
        anios = meses // 12
        return f"{anios} año{'s' if anios > 1 else ''}"


class Visita(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name="visitas")
    fecha = models.DateField(default=date.today)          # sin paréntesis: se calcula en cada visita nueva
    motivo = models.CharField(max_length=150)
    diagnostico = models.TextField("diagnóstico", blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    pagada = models.BooleanField(default=False)
    atendida_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="visitas_atendidas")

    class Meta:
        ordering = ["-fecha", "-id"]

    def __str__(self):
        return f"{self.mascota.nombre} · {self.fecha:%d/%m/%Y} · {self.motivo}"

    def clean(self):
        if self.fecha and self.fecha > date.today():
            raise ValidationError({"fecha": "La visita no puede ser en el futuro."})
