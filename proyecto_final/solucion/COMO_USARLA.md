# Solución del proyecto final — Veterinaria "Patitas"

## Para probarla

Con el entorno activado (y `pip install pillow` hecho):

```powershell
cd "D:\Desktop\Aprender Django\proyecto_final\solucion\veterinaria_proyecto"
python manage.py migrate             # crea db.sqlite3 con todas las tablas
python cargar_ejemplos.py            # 4 dueños, 7 mascotas, vacunas, visitas y el usuario recepcion
python manage.py createsuperuser     # (opcional) tu usuario para /admin
python manage.py runserver           # http://127.0.0.1:8000
```

Entrá con **recepcion / patitas-2026**. Para las pruebas automáticas, en otra
terminal: `python manage.py test clinica` (son las 39 pruebas de `pruebas\`, ya copiadas en `clinica\`).

## Dónde está cada cosa del enunciado

| Etapa | Dónde mirar |
|---|---|
| 1. Proyecto | `config/settings.py`: app, idioma, hora, `DIRS` de templates, `MEDIA_*`, `LOGIN_*` |
| 2. Modelos | `clinica/models.py`: `PROTECT` (dueño), `CASCADE` (visitas), `SET_NULL` (quién atendió), choices, ManyToMany, `ImageField`, validadores, `clean()`, `edad()` |
| 3. Admin | `clinica/admin.py`: inlines, `filter_horizontal`, `list_editable` |
| 4. Usuarios | `config/urls.py` (`auth.urls`, sin registro), `templates/registration/login.html`, `LoginRequiredMixin` y `@login_required` en todas las vistas |
| 5. Páginas y API | `clinica/views.py` (de función Y de clase), `clinica/urls.py`, `clinica/forms.py`, `clinica/templates/clinica/`, `clinica/static/clinica/estilo.css` |
| Pruebas | `clinica/test_etapa*.py` (las mismas de la carpeta `pruebas\`) |

## Decisiones para mirar con atención

- **`DEUDA`** (arriba de `views.py`): una suma CON condición
  (`filter=Q(...)`) que atraviesa dos relaciones (dueño → mascotas → visitas).
  Se define una vez y se usa en la lista y en el detalle del dueño.
- **`Count("mascotas", distinct=True)`**: al juntar con las visitas, cada
  mascota aparecería una vez por visita. `distinct` la cuenta una sola vez.
- **`.order_by("nombre")` después de `annotate`**: con totales, Django NO usa
  el `ordering` de `Meta`. Sin esto la paginación avisa que el orden no es fijo.
- **`FormularioDeDuenio`**: un mixin propio con lo común de crear y editar.
  **Ojo con esta trampa:** hacer `class EditarDuenio(CrearDuenio, UpdateView)`
  parece lógico, pero `CreateView` gana y al "editar" se guardaría un dueño
  NUEVO. Por eso las dos heredan del mixin y cada una de SU vista.
- **`_campos.html` con `{% include %}`**: el mismo pedazo de formulario sirve
  para dueños, mascotas y visitas.
- **`marcar_pagada` no redirige a "cualquier lado"**: solo a dos destinos
  conocidos. Redirigir a una dirección que manda el navegador permite armar
  links engañosos (se llama "open redirect").
- **`fecha = models.DateField(default=date.today)`** sin paréntesis: así se
  calcula en cada visita nueva. Con `date.today()` quedaría fijo el día en
  que arrancó el servidor.
- **`visita.atendida_por = request.user`**: lo pone la vista, no el formulario.
- **La validación del teléfono** usa una expresión regular (`re.fullmatch`).
  Si no las conocés, se puede hacer recorriendo el texto con un `for`: las dos
  formas valen.

## Una alternativa moderna para "todo exige sesión"

Desde Django 5.1, en vez de poner `@login_required` y `LoginRequiredMixin` en
cada vista, se puede agregar en `settings.py`, en `MIDDLEWARE` (al final):

```python
"django.contrib.auth.middleware.LoginRequiredMiddleware",
```

Y TODAS las páginas piden sesión (las de login quedan libres solas). Las que
quieras públicas se marcan con `@login_not_required`. Para aprender está bien
hacerlo vista por vista, como en la solución.

## Extras (pistas)

- **PostgreSQL**: igual que en la fase 2 (`DATABASES` con `os.environ[...]`).
- **CSV**: `response = HttpResponse(content_type="text/csv")`, el encabezado
  `Content-Disposition: attachment; filename="visitas.csv"`, y `csv.writer(response)`.
- **Sin antirrábica**: `if not mascota.vacunas.filter(nombre="Antirrábica").exists()`.
- **`.gitignore`**: `entorno/`, `db.sqlite3`, `media/`, `__pycache__/`.
