# Solución paso 6 — la librería completa

`libreria/` es el proyecto terminado: pasos 2 a 6.

## Qué se agregó en este paso

| Archivo | Qué tiene |
|---|---|
| `libros/api.py` (nuevo) | las 3 vistas de la API y cómo se convierte un libro a JSON |
| `libros/urls.py` | `api/libros/`, `api/libros/<id>/`, `api/libros/<id>/vender/` y `buscador/` |
| `libros/views.py` | `buscador` (solo muestra la página) |
| `libros/templates/libros/buscador.html` | la página con el JavaScript |
| `libros/templates/libros/base.html` | el link "Buscador" |
| `libros/test_paso6.py` | la prueba |

## Para probarla

```powershell
cd "D:\Desktop\Aprender Django\paso_6_api\solucion\libreria"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py test libros        # TODA la librería: 65 pruebas
```

- http://127.0.0.1:8000/api/libros/ → el JSON (cargá algunos libros antes).
- http://127.0.0.1:8000/buscador/ → el buscador en vivo, con F12 → Red abierto.

## Para mirar con atención

- **`libro_en_lista` y `libro_completo`**: vos decidís qué datos salen.
  `str(libro.precio)` porque JSON no tiene Decimal. `portada.url if
  portada else None`, porque `.url` de una imagen vacía da error.
- **`LibroForm(datos)` en la API**: el MISMO formulario de las páginas. Las
  reglas (precio mayor a 0, año no futuro) valen igual en la página y en la
  API, sin escribirlas dos veces.
- **`datos.setdefault("disponible", True)`**: en un formulario HTML, una
  casilla sin tildar no se manda y vale `False`. En la API, si no la mandan,
  queremos el valor por defecto.
- **401 en JSON y no `@login_required`**: `login_required` redirige al login
  (una página HTML). A un programa le sirve más un 401 con el error.
- **`isinstance(cantidad, bool)`**: en Python `True` cuenta como el número 1.
  Sin este control, `{"cantidad": true}` vendería 1.
- **En el JavaScript, `{% url %}` arma las direcciones** (`API` y `DETALLE`):
  si cambiás `urls.py`, el buscador sigue andando.
- **`textContent` y no `innerHTML`** para los títulos: si alguien carga un
  libro con `<script>` en el título, se muestra como texto y no se ejecuta.
- **CSRF**: el buscador solo hace GET (no lo necesita). Si agregás un POST desde
  JavaScript, mandá el token en el encabezado `X-CSRFToken`, como en la clase.
