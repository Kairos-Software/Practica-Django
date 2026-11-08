"""
Carga datos de ejemplo (dueños, mascotas, vacunas y visitas) para probar.
Desde esta carpeta:   python cargar_ejemplos.py
Crea también el usuario  recepcion / patitas-2026  para entrar.
(Solo agrega lo que falta: se puede ejecutar varias veces.)
"""

import os
from datetime import date, timedelta

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User  # noqa: E402

from clinica.models import Duenio, Mascota, Vacuna, Visita  # noqa: E402

if not User.objects.filter(username="recepcion").exists():
    User.objects.create_user("recepcion", password="patitas-2026", first_name="Vero")
    print("Usuario creado: recepcion / patitas-2026")
recepcion = User.objects.get(username="recepcion")

vacunas = {n: Vacuna.objects.get_or_create(nombre=n)[0] for n in ("Antirrábica", "Séxtuple", "Triple felina")}
hoy = date.today()

DATOS = [
    # dueño, teléfono, [(mascota, especie, raza, nacimiento, vacunas, [(días atrás, motivo, costo, pagada)])]
    ("Lucía Pérez", "+54 9 11 5555-1234", [
        ("Toby", "perro", "Caniche", date(2020, 3, 15), ["Antirrábica", "Séxtuple"],
         [(2, "Control anual", 8000, False), (200, "Vacunas", 12000, True)]),
        ("Michi", "gato", "Siamés", date(2023, 8, 1), ["Triple felina"], [(5, "Castración", 45000, True)]),
    ]),
    ("Carlos Gómez", "011 4444-9876", [
        ("Rocco", "perro", "Ovejero", date(2018, 1, 20), ["Antirrábica"], [(1, "Renguea de una pata", 15000, False)]),
    ]),
    ("Marta Sosa", "3624-445566", [
        ("Piolín", "ave", "Canario", None, [], [(30, "No canta", 5000, True)]),
        ("Copito", "conejo", "", date(2025, 12, 1), [], []),
    ]),
    ("Familia Romero", "+54 362 400-1122", [
        ("Luna", "gato", "Común europeo", date(2021, 6, 6), ["Triple felina", "Antirrábica"],
         [(0, "Vómitos", 18000, False)]),
        ("Thor", "perro", "Labrador", date(2019, 11, 2), [], []),
    ]),
]

for nombre, telefono, mascotas in DATOS:
    duenio, _ = Duenio.objects.get_or_create(nombre=nombre, defaults={"telefono": telefono})
    for m_nombre, especie, raza, nacimiento, sus_vacunas, visitas in mascotas:
        mascota, creada = Mascota.objects.get_or_create(
            nombre=m_nombre, duenio=duenio, defaults={"especie": especie, "raza": raza, "nacimiento": nacimiento})
        if not creada:
            continue
        mascota.vacunas.set([vacunas[v] for v in sus_vacunas])
        for dias, motivo, costo, pagada in visitas:
            Visita.objects.create(mascota=mascota, fecha=hoy - timedelta(days=dias), motivo=motivo, costo=costo,
                                  pagada=pagada, atendida_por=recepcion)
        print(f"Agregada: {m_nombre} ({duenio})")
