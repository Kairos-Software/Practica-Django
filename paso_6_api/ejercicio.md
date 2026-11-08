# Ejercicio paso 6 — La API de la librería

Seguí con **tu** proyecto `libreria`. (Si no terminaste el paso 5, copiá
`paso_5_imagenes_y_archivos\solucion\libreria` a `mis_proyectos\`.)

Hacé que la librería entregue y reciba datos en JSON, y usala desde una
página con un buscador en vivo. **Los nombres y las respuestas tienen que ser
exactamente estos** (la prueba los revisa).

Todas las direcciones van en `libros/urls.py` (con `app_name = "libros"`).

## 1. La lista de libros — `api/libros/`, `name="api_libros"`

**GET** (cualquiera) → código 200 y:

```json
{"cantidad": 2,
 "libros": [{"id": 3, "titulo": "El Aleph", "autor": "Borges", "precio": "14000.00", "stock": 0, "disponible": true},
            ...]}
```

- ordenados por título
- `precio` como **texto** con 2 decimales (es un Decimal: `str(libro.precio)`)
- filtros opcionales en la dirección: `?q=` (parte del título, sin importar
  mayúsculas) y `?autor=` (el id del autor). Se pueden usar juntos.

**POST** (crear un libro) → solo con sesión iniciada. Recibe un JSON:

```json
{"titulo": "Bestiario", "autor": 2, "precio": "12000", "stock": 5, "anio": 1951}
```

- sin sesión: código **401** y `{"error": "Tenés que iniciar sesión."}`
- JSON mal escrito: código **400** y `{"error": "El JSON está mal escrito."}`
- datos mal (validalos con tu formulario de libro, con todas sus reglas):
  código **400** y `{"errores": {...}}` (los errores del formulario)
- bien: código **201** y el libro creado **en el formato del detalle** (punto 2)

Cualquier otro método (PUT, DELETE...) → 405.

## 2. Un libro — `api/libros/<id>/`, `name="api_libro"`

**GET** (cualquiera) → código 200 y:

```json
{"id": 1, "titulo": "Ficciones", "autor": {"id": 1, "nombre": "Borges"},
 "precio": "15000.00", "stock": 4, "anio": 1944, "disponible": true,
 "portada": "/media/portadas/ficciones.png",
 "promedio": 4.5,
 "resenias": [{"usuario": "ana", "puntaje": 5, "texto": "Genial"}, ...]}
```

- `portada`: la dirección de la imagen, o `null` si no tiene
- `promedio`: el promedio de las reseñas, o `null` si no tiene
- `resenias`: de la más nueva a la más vieja

**DELETE** → solo con sesión: borra el libro (y su portada) y responde
código **204** sin contenido. Sin sesión: 401 con el mismo error del punto 1.

Si el libro no existe (cualquier método): código **404** y
`{"error": "No existe ese libro."}`.

## 3. Vender — `api/libros/<id>/vender/`, `name="api_vender"`

Solo **POST** (con GET: 405) y solo con sesión (sin sesión: 401). Recibe
`{"cantidad": 2}` y usa `vender()` del modelo:

- bien: código 200 y `{"stock": 2}` (el stock que quedó)
- no alcanza, o la cantidad es mala: código **400** y `{"error": "..."}` con
  el mensaje del error
- la cantidad no es un número entero o falta: código **400** y
  `{"error": "La cantidad tiene que ser un número entero."}`
- el libro no existe: 404 como en el punto 2

## 4. El buscador en vivo — `buscador/`, `name="buscador"`

Una página (que herede de tu template base) con:
- un cuadro de texto con **`id="buscar"`**
- una lista vacía con **`id="resultados"`**
- JavaScript que, **cada vez que se escribe**, pide la lista a tu API (punto 1)
  con `?q=` y muestra cada libro (título, autor y precio) **sin recargar la
  página**. Cada resultado es un link al detalle del libro (`/libros/<id>/`).
- un link "Buscador" en el menú

---

## Cómo ejecutarlo

```powershell
cd "D:\Desktop\Aprender Django"
.\entorno\Scripts\activate
cd mis_proyectos\libreria
python manage.py runserver
```

- Los GET se prueban en el navegador: http://127.0.0.1:8000/api/libros/?q=a
- El buscador: http://127.0.0.1:8000/buscador/ con **F12** abierto, en las
  pestañas **Consola** (errores de JavaScript) y **Red** (cada pedido a la API).
- POST y DELETE no se pueden probar escribiendo la dirección: para eso está la
  prueba automática (o el JavaScript de tu página).
- En este paso no cambiás modelos: no hace falta migrar.

## Cómo comprobar que está bien

1. Copiá **`test_paso6.py`** a tu carpeta `libros`.
2. `python manage.py test libros.test_paso6`, y al final `python manage.py test libros`:
   **toda la librería** (pasos 2 a 6) tiene que dar OK.

La solución está en `solucion/libreria/` (con su `COMO_USARLA.md`).
