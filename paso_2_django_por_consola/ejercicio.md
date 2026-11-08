# Ejercicio paso 2 — La librería con Django (por consola)

Es la librería del paso 1, ahora **sin escribir SQL**. Este proyecto lo vas a
seguir agrandando en los pasos 3, 4, 5 y 6: hacelo con cariño.

**Los nombres tienen que ser exactamente estos**, porque la prueba automática
los busca así.

## Parte A — El proyecto

1. En `D:\Desktop\Aprender Django\mis_proyectos\` creá la carpeta `libreria`, y
   adentro un proyecto cuya configuración se llame **`config`** y una app que se
   llame **`libros`**.
2. Registrá la app. Idioma `es-ar` y zona horaria `America/Argentina/Buenos_Aires`.

## Parte B — Los modelos (en `libros/models.py`)

3. **`Autor`**:
   - `nombre` (texto, sin repetir)
   - `pais` (texto, opcional)
   - `nacimiento` (fecha, opcional)
   - se muestra por su nombre y se ordena por nombre
4. **`Libro`**:
   - `titulo` (texto)
   - `autor` (relacionado con Autor; si se intenta borrar un autor con libros,
     que **no** lo deje; desde un autor, sus libros se piden con `autor.libros`)
   - `precio` (plata, 2 decimales)
   - `stock` (entero no negativo, por defecto 0)
   - `anio` (año de publicación, entero no negativo)
   - `disponible` (sí/no, por defecto sí)
   - `cargado` (fecha y hora, se pone sola al crearlo)
   - se muestra como `Título — Autor` (con ese guión largo: —) y se ordena por título
5. Métodos de `Libro`:
   - `hay_stock()` → verdadero si el stock es mayor que 0
   - `vender(cantidad)` → resta y guarda. Si la cantidad es 0 o menos, o si no
     alcanza el stock, provoca un `ValueError` y no cambia nada.
   - validación (`clean`): el año no puede ser mayor que el año actual.
6. Creá las tablas en la base.

## Parte C — El admin

7. Creá tu superusuario. Registrá los dos modelos. En la lista de libros: las
   columnas `titulo`, `autor`, `precio`, `stock` y `disponible`; filtros por
   `autor` y `disponible`; buscador por `titulo`.
8. Entrá al admin y cargá algunos autores y libros a mano.

## Parte D — Las consultas (en un archivo nuevo: `libros/consultas.py`)

Funciones que usan el ORM (nada de SQL a mano):

9. `sin_stock()` → los libros con stock 0, ordenados por título.
10. `mas_baratos_que(precio)` → los libros que cuestan menos, del más barato al más caro.
11. `buscar(texto)` → los libros cuyo título contiene el texto (sin importar
    mayúsculas), ordenados por título.
12. `de_autor(nombre)` → los libros del autor que se llama así, en **una sola
    consulta** (sin buscar primero al autor).
13. `subir_precios(autor, porcentaje)` → sube el precio de todos los libros de
    ese autor (un objeto `Autor`) en **una sola consulta**, sin recorrerlos uno
    por uno. Devuelve cuántos cambió.
14. `marcar_no_disponibles_sin_stock()` → los que no tienen stock pasan a no
    disponibles (una sola consulta). Devuelve cuántos cambió.
15. `resumen_por_autor()` → todos los autores, cada uno con dos datos extra
    calculados por la base: `cantidad` (cuántos libros tiene) y `stock_total`
    (la suma de su stock; si no tiene libros puede quedar vacío).
16. `precio_promedio()` → el precio promedio de todos los libros (o `None` si no hay).
17. `borrar_no_disponibles()` → borra los libros no disponibles y devuelve cuántos borró.

## Parte E — Probarlo a mano (opcional pero recomendado)

18. Un archivo `practica.py` al lado de `manage.py` que cree algunos autores y
    libros y use tus funciones con `print()`. (La clase explica cómo un script
    "arranca" Django.)

---

## Cómo ejecutar cada cosa (en orden)

```powershell
cd "D:\Desktop\Aprender Django"
.\entorno\Scripts\activate
mkdir mis_proyectos                       # si no existe
cd mis_proyectos
mkdir libreria
cd libreria
django-admin startproject config .        # ¡con el punto!
python manage.py startapp libros
#   ...config/settings.py y libros/models.py...
python manage.py makemigrations           # escribe el plan de las tablas
python manage.py migrate                  # crea las tablas
python manage.py createsuperuser
#   ...libros/admin.py...
python manage.py runserver                # http://127.0.0.1:8000/admin   (Ctrl+C para apagarlo)
#   ...libros/consultas.py...
python practica.py                        # tu prueba a mano
```

## Cómo comprobar que está bien (la prueba automática)

1. Copiá el archivo **`test_paso2.py`** (de esta carpeta) adentro de tu carpeta
   **`libros`**, al lado de `models.py`.
2. Desde la carpeta de `manage.py`:

```powershell
python manage.py test libros.test_paso2
```

- Cada prueba dice qué revisa. `OK` al final = todo bien.
- Si dice `FAILED`, arriba está cuál y por qué ("esperaba X y encontró Y").
- Las pruebas usan una base **aparte**: no tocan tus datos.
- La podés correr todas las veces que quieras mientras avanzás.

La solución está en `solucion/libreria/` (con su `COMO_USARLA.md`).
