# Solución paso 3

`libreria/` es el proyecto del paso 2 con la parte web agregada.

## Qué se agregó (compará con lo tuyo)

| Archivo | Qué tiene |
|---|---|
| `config/urls.py` | `include("libros.urls")` en la raíz |
| `libros/urls.py` (nuevo) | `app_name = "libros"` y las 9 direcciones con nombre |
| `libros/forms.py` (nuevo) | `LibroForm` (con `clean_precio`), `AutorForm` y `VenderForm` (un `forms.Form`: no es de un modelo) |
| `libros/views.py` | las 9 vistas |
| `libros/templates/libros/` | `base.html` y una página por vista. `form.html` sirve para crear y editar libros y crear autores |
| `libros/static/libros/estilo.css` | CSS mínimo (opcional) |
| `libros/test_paso3.py` | la prueba |

## Para probarla

```powershell
cd "D:\Desktop\Aprender Django\paso_3_paginas_web\solucion\libreria"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver          # http://127.0.0.1:8000
python manage.py test libros        # (en otra terminal) pasos 2 y 3
```

La base arranca vacía: cargá autores y libros desde las páginas (o desde `/admin`).

## Cosas para mirar con atención

- **`borrar`**: la misma vista hace dos cosas. Con GET muestra "¿Seguro?" y
  con POST borra. Un link nunca borra.
- **`vender`**: `@require_POST` y vuelve SIEMPRE al detalle. Si algo sale mal,
  vuelve con un mensaje de error (`messages.error`), no con una pantalla de
  error. La regla del stock no está en la vista: está en `Libro.vender()`.
- **El filtro por autor en `lista.html`**: `autor_id` llega como texto ("3") y
  `a.pk` es un número (3). Para compararlos, el número se pasa a texto con
  `|stringformat:"d"`. Si no, el desplegable nunca queda "seleccionado".
- **La paginación conserva los filtros**: `filtros` es la búsqueda actual sin
  la página (`request.GET.copy()` + `pop("pagina")` + `urlencode()`).
- **`select_related("autor")`** en la lista: una consulta en vez de una por libro.
- **`Count("libros")`** en autores, y `|pluralize` para "1 libro / 2 libros".
