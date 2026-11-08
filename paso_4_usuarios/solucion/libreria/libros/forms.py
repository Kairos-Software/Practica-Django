from django import forms

from .models import Autor, Libro, Resenia


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ["titulo", "autor", "precio", "stock", "anio", "disponible"]

    def clean_precio(self):
        precio = self.cleaned_data["precio"]
        if precio <= 0:
            raise forms.ValidationError("El precio tiene que ser mayor a 0.")
        return precio


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ["nombre", "pais", "nacimiento"]
        # Para que el navegador muestre un calendario en la fecha
        widgets = {"nacimiento": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}


class VenderForm(forms.Form):
    """Un formulario que NO es de un modelo: solo pide un número."""
    cantidad = forms.IntegerField(min_value=1, initial=1)


class ReseniaForm(forms.ModelForm):
    class Meta:
        model = Resenia
        fields = ["puntaje", "texto"]          # ¡sin usuario ni libro: los pone la vista!
        widgets = {
            "puntaje": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "texto": forms.Textarea(attrs={"rows": 3}),
        }
