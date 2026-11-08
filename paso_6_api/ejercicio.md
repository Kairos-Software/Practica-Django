# Ejercicio paso 6 — La API de la librería

Seguí con **tu** proyecto `libreria`. (Si no terminaste el paso 5, copiá
`paso_5_imagenes_y_archivos\solucion\libreria` adentro de `mis_proyectos\`.)

Vas a hacer que la librería entregue y reciba datos en JSON, y a usarla desde
una página con un buscador que filtra mientras escribís.

> **Los nombres y las respuestas tienen que ser exactamente estos** (la
> prueba revisa cada JSON y cada código).

Todas las direcciones van en `libros/urls.py` (con `app_name = "libros"`).
Si querés, las vistas de la API pueden ir en un archivo aparte,
`libros/api.py` (en `urls.py`: `from . import api` y `api.libros`, etc.).

---

## Antes de empezar: dónde está cada cosa en la clase

| Para | Mirá en `clase.py` |
|---|---|
| Qué es una API y qué es JSON | PARTE 1 |
| Devolver JSON (y pasar plata, imágenes y relaciones a JSON) | PARTE 2 |
| Los códigos 200, 201, 204, 400, 401, 404, 405 | PARTE 3 |
| Que una dirección acepte GET y POST (y lo demás dé 405) | PARTE 4 |
| Recibir JSON y validarlo con tu formulario | PARTE 5 (¡y el OJO de las casillas!) |
| Revisar que la cantidad sea un número entero | PARTE 6 |
| Sin sesión: 401 | PARTE 7 |
| El buscador con JavaScript | PARTE 8 y la página `PAGINA` de la PARTE 10 |
| El promedio de las reseñas | Paso 2, PARTE B6 (`aggregate` y `Avg`) |

Un orden posible: primero los GET (1 y 2), que se prueban en el navegador;
después el buscador (4), que usa el GET; y al final los POST y DELETE.

---

## 1. La lista de libros — `api/libros/`, con `name="api_libros"`

**GET** (cualquiera, con o sin sesión) → código 200 y:

```json
{"cantidad": 2,
 "libros": [{"id": 3, "titulo": "El Aleph", "autor": "Borges", "precio": "14000.00", "stock": 0, "disponible": true},
            ...]}
```

- ordenados por título
- `autor`: el **nombre** del autor (un texto)
- `precio` como **texto** con 2 decimales (es un Decimal: `str(libro.precio)`)
- filtros opcionales en la dirección: `?q=` (parte del título, sin importar
  mayúsculas) y `?autor=` (el id del autor). Se pueden usar juntos:
  `api/libros/?q=a&autor=1`

**POST** (crear un libro) → solo con sesión iniciada. Recibe un JSON así:

```json
{"titulo": "Bestiario", "autor": 2, "precio": "12000", "stock": 5, "anio": 1951}
```

(acá `autor` es el **id** del autor, como en el formulario)

- sin sesión: código **401** y `{"error": "Tenés que iniciar sesión."}`
- JSON mal escrito: código **400** y `{"error": "El JSON está mal escrito."}`
- datos mal (validalos con **tu formulario de libro**, con todas sus reglas):
  código **400** y `{"errores": {...}}` (los errores del formulario)
- bien: código **201** y el libro creado **en el formato del detalle** (punto 2)

Cualquier otro método (PUT, DELETE...) → 405.

> OJO (PARTE 5 de la clase): si tu formulario tiene la casilla `disponible`
> y el JSON no la trae, el formulario la toma como **no**. Un libro creado
> por la API tiene que quedar disponible si no se dice otra cosa.

---

## 2. Un libro — `api/libros/<id>/`, con `name="api_libro"`

**GET** (cualquiera) → código 200 y:

```json
{"id": 1, "titulo": "Ficciones", "autor": {"id": 1, "nombre": "Borges"},
 "precio": "15000.00", "stock": 4, "anio": 1944, "disponible": true,
 "portada": "/media/portadas/ficciones.png",
 "promedio": 4.5,
 "resenias": [{"usuario": "ana", "puntaje": 5, "texto": "Genial"}, ...]}
```

- `autor`: acá es un diccionario con su `id` y su `nombre`
- `portada`: la dirección de la imagen, o `null` si no tiene
- `promedio`: el promedio de los puntajes de las reseñas, o `null` si no tiene reseñas
- `resenias`: de la más nueva a la más vieja (`usuario` es el nombre de usuario)

**DELETE** → solo con sesión: borra el libro (y su portada) y responde
código **204**, sin contenido. Sin sesión: 401 con el mismo error del punto 1.

Si el libro no existe (con cualquier método): código **404** y
`{"error": "No existe ese libro."}`.

---

## 3. Vender — `api/libros/<id>/vender/`, con `name="api_vender"`

Solo **POST** (con GET: 405) y solo con sesión (sin sesión: 401). Recibe
`{"cantidad": 2}` y usa el `vender()` del modelo:

- bien: código 200 y `{"stock": 2}` (el stock que quedó)
- no alcanza el stock, o la cantidad es 0 o negativa: código **400** y
  `{"error": "..."}` con el mensaje del `ValueError` de `vender()` (si no
  alcanza, empieza con `No alcanza el stock`, como pide el paso 2)
- la cantidad no es un número entero, o no vino: código **400** y
  `{"error": "La cantidad tiene que ser un número entero."}`.
  La prueba manda `{"cantidad": "dos"}`, `{}` y `{"cantidad": 1.5}`: los tres
  tienen que dar este error (PARTE 6 de la clase: `int(1.5)` da 1 sin avisar).
- el libro no existe: 404, como en el punto 2

---

## 4. El buscador en vivo — `buscador/`, con `name="buscador"`

Una página (que herede de tu template base) con:
- un cuadro de texto con **`id="buscar"`**
- una lista vacía con **`id="resultados"`**
- JavaScript que, **cada vez que se escribe**, le pide la lista a tu API
  (punto 1) con `?q=` y muestra cada libro (título, autor y precio) **sin
  recargar la página**. Cada resultado es un link al detalle del libro
  (`/libros/<id>/`).
- un link "Buscador" en el menú

> El JavaScript va **adentro de la misma página**, en un `<script>` al final
> del template (como en la clase), y no en un archivo `.js` aparte: la prueba
> lee el HTML de la página y busca ahí `fetch(` y la dirección de tu API
> (`/api/libros/`). Para escribir esa dirección podés usar
> `{% url 'libros:api_libros' %}` adentro del `<script>`.

---

## Cómo ejecutarlo y probarlo

```powershell
cd "D:\Desktop\Aprender Django"
.\entorno\Scripts\activate
cd mis_proyectos\libreria
python manage.py runserver
```

- Los GET se prueban escribiendo la dirección en el navegador:
  http://127.0.0.1:8000/api/libros/?q=a y http://127.0.0.1:8000/api/libros/1/
  (Si los acentos se ven como `\u00ed`, es normal: PARTE 2 de la clase.)
- El buscador: http://127.0.0.1:8000/buscador/ con **F12** abierto, en las
  pestañas **Consola** (los errores de JavaScript, en rojo) y **Red** (cada
  pedido a la API y su respuesta).
- POST y DELETE no se pueden probar escribiendo la dirección: para eso está
  la prueba automática (o el JavaScript de tu página).
- En este paso no cambiás modelos: no hace falta migrar.

---

## Cómo comprobar que está bien

1. Copiá **`test_paso6.py`** a tu carpeta `libros`:

   ```powershell
   copy "..\..\paso_6_api\test_paso6.py" libros\
   ```

2. Corré la prueba:

   ```powershell
   python manage.py test libros.test_paso6     # solo el paso 6
   python manage.py test libros                # TODA la librería (pasos 2 a 6): tiene que dar OK
   ```

Si una prueba de la API falla, la última línea del bloque `FAIL` muestra el
JSON que esperaba y el que devolvió tu API: compará campo por campo.

La solución está en `solucion/libreria/` (con su `COMO_USARLA.md`). Mirala
recién cuando termines. ¡Y después, el proyecto final!
