# Solución paso 2

`libreria/` es el proyecto completo hasta el paso 2. Se armó con:

```powershell
django-admin startproject config .
python manage.py startapp libros
```

y después se tocaron solo estos archivos (compará con los tuyos):

| Archivo | Qué tiene |
|---|---|
| `config/settings.py` | `'libros'` en `INSTALLED_APPS`, idioma y zona horaria |
| `libros/models.py` | `Autor` y `Libro`, con `hay_stock()`, `vender()` y `clean()` |
| `libros/admin.py` | los dos modelos con columnas, filtros y buscador |
| `libros/consultas.py` | las 9 funciones de la parte D |
| `libros/migrations/0001_initial.py` | lo escribió `makemigrations` (no se escribe a mano) |
| `libros/test_paso2.py` | la prueba automática, copiada donde va |
| `practica.py` | la parte E |

(Se borró el `libros/tests.py` vacío que crea `startapp`: no hace falta.)

## Para probarla

```powershell
cd "D:\Desktop\Aprender Django\paso_2_django_por_consola\solucion\libreria"
python manage.py migrate
python practica.py
python manage.py test libros.test_paso2
python manage.py createsuperuser
python manage.py runserver          # http://127.0.0.1:8000/admin
```

## Para mirar con atención

- **`subir_precios` usa `Decimal(porcentaje)`**: el precio es `DecimalField`
  (plata exacta). Multiplicarlo por un `float` como `1.1` daría error o
  decimales raros.
- **`vender()` vive en el modelo**: cualquier parte del sistema que venda (el
  admin, una página, la API del paso 6) usa la misma regla.
- **`Libro.objects.all().delete()` antes que `Autor...`** en `practica.py`: por
  el `PROTECT` no se puede borrar un autor con libros.
- **Las funciones de `consultas.py` devuelven QuerySets**: se pueden seguir
  filtrando (`buscar("a").filter(stock__gt=0)`) y no van a la base hasta que se usan.
