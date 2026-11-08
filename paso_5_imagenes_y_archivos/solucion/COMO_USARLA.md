# Solución paso 5

`libreria/` es el proyecto del paso 4 con portadas, fotos y planillas.

## Qué se agregó (compará con lo tuyo)

| Archivo | Qué tiene |
|---|---|
| `config/settings.py` | `MEDIA_URL` y `MEDIA_ROOT` (al final) |
| `config/urls.py` | `static(...)` para ver las imágenes en desarrollo |
| `libros/models.py` | `Autor.foto` y `Libro.portada` (`ImageField`) |
| `libros/migrations/0003_...py` | lo escribió `makemigrations` |
| `libros/forms.py` | `portada` y `foto` en los formularios, `clean_portada` (2 MB), `ImportarForm` |
| `libros/views.py` | `request.FILES` en crear/editar/crear autor; borrar la portada vieja al editar y al borrar; `exportar` e `importar` |
| `libros/urls.py` | `libros/exportar/` y `libros/importar/` |
| `libros/templates/libros/` | `enctype` en `form.html`; imágenes en `detalle`, `lista` y `autor`; `importar.html` |
| `libros/test_paso5.py` | la prueba |

## Para probarla

```powershell
pip install pillow
cd "D:\Desktop\Aprender Django\paso_5_imagenes_y_archivos\solucion\libreria"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py test libros        # pasos 2 a 5 (55 pruebas)
```

## Para mirar con atención

- **`vieja = libro.portada` ANTES de armar el formulario**: después de
  `form.save()`, `libro.portada` ya es la nueva. Hay que guardar la vieja
  antes para poder borrarla.
- **`vieja != libro.portada`**: si editás el título sin tocar la imagen, la
  portada es la misma y NO se borra.
- **`delete(save=False)`**: borra el archivo sin volver a guardar el libro.
- **`"\ufeff"` y `utf-8-sig`**: una marca invisible al principio del archivo
  para que Excel lea bien los acentos. Al leer, `utf-8-sig` la descarta.
- **Separador `;`**: Excel en castellano usa `;` porque la `,` es la coma de
  los decimales.
- **`get_or_create`** en importar: si el autor ya existe lo usa; si no, lo crea.
- **Cada fila en su `try`**: una fila mala no frena las demás. Los errores se
  juntan y se muestran todos juntos al final.
- **`Decimal(fila["precio"])`** y no `float`: es plata. Si el texto no es un
  número, da `InvalidOperation`, que también se ataja.
