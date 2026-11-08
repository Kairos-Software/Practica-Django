# Ejercicio paso 5 — La librería con portadas y planillas

Seguí con **tu** proyecto `libreria`. (Si no terminaste el paso 4, copiá
`paso_4_usuarios\solucion\libreria` adentro de `mis_proyectos\`.)

Antes de empezar, con el entorno activado: `pip install pillow` (la librería
que entiende imágenes; sin ella, `ImageField` no funciona).

> **Los nombres y los mensajes tienen que ser exactamente estos.** La prueba
> automática los busca escritos así.

---

## Antes de empezar: dónde está cada cosa en la clase

| Para los puntos | Mirá en `clase.py` |
|---|---|
| 1 (configurar `media/`) | PARTE 2 |
| 2 (los campos de imagen) | PARTE 3 |
| 3 (subirlas desde los formularios) | PARTE 4 (`enctype` y `request.FILES`) |
| 4 (validar) | PARTE 6 |
| 5 (mostrarlas) | PARTE 5 |
| 6 (borrar los archivos viejos) | PARTE 7 |
| 7 (bajar la planilla) | PARTE 8a |
| 8 (importar la planilla) | PARTE 8b (y el paso 2, PARTE B8, para `transaction.atomic`) |

---

## Configuración

**1.** Los archivos subidos se guardan en la carpeta `media/` del proyecto y
se piden con la dirección `/media/`. En desarrollo, que se puedan ver (el
`static(...)` en `config/urls.py`).

---

## Imágenes

**2.** `Libro` tiene una **`portada`** (imagen, opcional, en la subcarpeta
`portadas/`) y `Autor` una **`foto`** (imagen, opcional, en `autores/`). Son
campos nuevos: `makemigrations` y `migrate`.

**3.** Los formularios de libro y de autor permiten subirlas, al crear y al
editar. (Acordate del `enctype` en el `<form>` y del `request.FILES` en la
vista: sin eso la imagen llega vacía **sin dar ningún error**.)

**4.** La portada **no puede pesar más de 2 MB**: el error tiene que decir
**`La imagen no puede pesar más de 2 MB.`** Lo que no es una imagen tampoco
se acepta (eso ya lo hace `ImageField` solo).

**5.** El **detalle** del libro muestra la portada (si tiene), y el detalle
del autor, su foto. La **lista** de libros muestra la portada chiquita (con
`width` en el `<img>`, o con CSS).

**6.** Al **cambiar** la portada de un libro, el archivo viejo se **borra**
de la carpeta. Al **borrar** un libro, se borra también su portada.

Mientras probás, mirá la carpeta `media\portadas\` de tu proyecto: tiene que
haber un archivo por libro con portada, nunca de más.

---

## Planillas (CSV separado por `;`)

**7. Bajar la planilla de libros**: dirección `libros/exportar/`, con
**`name="exportar"`**. Cualquiera puede bajarla (no pide sesión). Descarga un
archivo **`libros.csv`** con una fila de títulos **`titulo;autor;precio;stock`**
y después un libro por fila, ordenados por título. En la lista, un link
"Bajar planilla". Por ejemplo:

```text
titulo;autor;precio;stock
Bestiario;Cortázar;12000.00;5
El Aleph;Borges;14000.00;0
```

**8. Importar libros**: dirección `libros/importar/`, con
**`name="importar"`**, solo con sesión iniciada. Una página con un formulario
para subir el archivo (el campo se llama **`archivo`**). La planilla tiene las
columnas **`titulo;autor;precio;stock;anio`**:
- si el autor no existe, se crea; si existe, se usa ese
- las filas con algún dato mal (precio con letras, una columna de menos, un
  stock negativo...) se saltean, y se sigue con las demás
- después vuelve a la **lista** con el mensaje **`Se importaron N libros.`**
  y, si hubo filas malas, otro mensaje que diga cuáles (por su número de fila;
  la de los títulos es la fila 1)
- si el archivo no es un CSV de texto (por ejemplo, una foto), el mensaje de
  error **`El archivo no es una planilla CSV.`** y no se importa nada
- en la lista, un link "Importar planilla"

Lo que hace la prueba, para que sepas qué esperar:

```text
titulo;autor;precio;stock;anio      <- fila 1: títulos
Rayuela;Cortázar;20000;3;1963       <- fila 2: bien
El Aleph;Borges;14000;0;1949        <- fila 3: bien (stock 0 vale)
Mal;Quino;caro;1;1966               <- fila 4: el precio tiene letras
Mafalda 1;Quino;8000;10;1966        <- fila 5: bien
```

Mensajes esperados: `Se importaron 3 libros.` y otro que mencione la fila 4.

> **Pistas para importar (PARTE 8b de la clase):**
> - Lo más seguro es validar cada fila con **tu `LibroForm`**: así la
>   planilla cumple las mismas reglas que las páginas (precio mayor a 0, año
>   que no sea futuro...). OJO: si el formulario tiene la casilla
>   `disponible` y no se la pasás, queda en **no** (una casilla que no se
>   manda vale "no"). Pasale `"disponible": True`.
> - El formulario necesita el **id** del autor, así que el autor se crea
>   antes de validar el libro. Para que una fila mala no deje un autor creado
>   de más, hacé todo lo de la fila adentro de un `with transaction.atomic():`
>   y, si la fila está mal, provocá un error **adentro** del `with`.
> - Una fila con columnas de menos trae `None` en las que faltan:
>   `None.strip()` da `AttributeError`.

Para probar el punto 8 a mano, armá la planilla con Excel (Guardar como →
"CSV delimitado por punto y coma") o con el Bloc de notas, guardándola como
`libros.csv`:

```text
titulo;autor;precio;stock;anio
Rayuela;Cortázar;20000;3;1963
Mafalda 1;Quino;8000;10;1966
```

---

## Cómo ejecutarlo

```powershell
cd "D:\Desktop\Aprender Django"
.\entorno\Scripts\activate
pip install pillow
cd mis_proyectos\libreria
python manage.py makemigrations       # por los campos nuevos
python manage.py migrate
python manage.py runserver
```

Las imágenes que subas aparecen en la carpeta `media\portadas\` del
proyecto. La carpeta `media` no se sube al repositorio (está en el `.gitignore`).

---

## Cómo comprobar que está bien

1. Copiá **`test_paso5.py`** a tu carpeta `libros`:

   ```powershell
   copy "..\..\paso_5_imagenes_y_archivos\test_paso5.py" libros\
   ```

2. Corré la prueba:

   ```powershell
   python manage.py test libros.test_paso5     # solo el paso 5
   python manage.py test libros                # los pasos 2 a 5 juntos
   ```

La prueba usa una carpeta temporal para las imágenes: no toca tu `media/`.

La solución está en `solucion/libreria/` (con su `COMO_USARLA.md`). Mirala
recién cuando termines.
