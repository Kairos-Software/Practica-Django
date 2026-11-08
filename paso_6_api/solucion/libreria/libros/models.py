from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Autor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    pais = models.CharField("país", max_length=50, blank=True)
    nacimiento = models.DateField("fecha de nacimiento", null=True, blank=True)
    foto = models.ImageField(upload_to="autores/", blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "autores"

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField("título", max_length=200)
    # PROTECT: no deja borrar un autor que tiene libros
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT, related_name="libros")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    anio = models.PositiveIntegerField("año de publicación")
    disponible = models.BooleanField(default=True)
    cargado = models.DateTimeField(auto_now_add=True)
    portada = models.ImageField(upload_to="portadas/", blank=True)

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return f"{self.titulo} — {self.autor}"

    def hay_stock(self):
        return self.stock > 0

    def vender(self, cantidad):
        """Resta `cantidad` del stock y guarda. Si no se puede, no cambia nada."""
        if cantidad <= 0:
            raise ValueError("La cantidad tiene que ser mayor que cero.")
        if cantidad > self.stock:
            raise ValueError(f"No alcanza el stock de «{self.titulo}»: hay {self.stock} y pidieron {cantidad}.")
        self.stock -= cantidad
        self.save()

    def clean(self):
        if self.anio and self.anio > date.today().year:
            raise ValidationError({"anio": "El año de publicación no puede ser en el futuro."})


class Resenia(models.Model):
    """La opinión de un usuario sobre un libro (una por usuario y libro)."""
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resenias")
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name="resenias")
    puntaje = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    texto = models.TextField()
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creada", "-id"]
        verbose_name = "reseña"
        constraints = [models.UniqueConstraint(fields=["usuario", "libro"], name="una_resenia_por_usuario_y_libro")]

    def __str__(self):
        return f"{self.usuario} sobre {self.libro.titulo}: {self.puntaje}/5"
