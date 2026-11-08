import re

from django import forms

from .models import Duenio, Mascota, Visita

FECHA = forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")


class DuenioForm(forms.ModelForm):
    class Meta:
        model = Duenio
        fields = ["nombre", "telefono", "email", "direccion"]

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"].strip()
        # Un "+" opcional al principio y después solo números, espacios y guiones
        if not re.fullmatch(r"\+?[0-9 \-]+", telefono):
            raise forms.ValidationError("Solo números, espacios, guiones y un + al principio.")
        return telefono


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ["nombre", "especie", "raza", "nacimiento", "duenio", "vacunas", "foto"]
        widgets = {"nacimiento": FECHA, "vacunas": forms.CheckboxSelectMultiple}


class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        # Sin "mascota" ni "atendida_por": los pone la vista
        fields = ["fecha", "motivo", "diagnostico", "costo", "pagada"]
        widgets = {"fecha": FECHA, "diagnostico": forms.Textarea(attrs={"rows": 2})}
