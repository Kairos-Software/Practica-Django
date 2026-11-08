# Ejercicio paso 5 — La librería con portadas y planillas

Seguí con **tu** proyecto `libreria`. (Si no terminaste el paso 4, copiá
`paso_4_usuarios\solucion\libreria` a `mis_proyectos\`.)

Antes de empezar: `pip install pillow` (con el entorno activado).

**Los nombres tienen que ser exactamente estos.**

## Configuración

1. Los archivos subidos se guardan en la carpeta `media/` del proyecto y se
   piden con la dirección `/media/`. En desarrollo, que se puedan ver.

## Imágenes

2. `Libro` tiene una **`portada`** (imagen, opcional, en la subcarpeta
   `portadas/`) y `Autor` una **`foto`** (imagen, opcional, en `autores/`).
3. Los formularios de libro y de autor permiten subirlas (crear y editar).
4. La portada **no puede pesar más de 2 MB**: el error tiene que decir
   **`La imagen no puede pesar más de 2 MB.`** Lo que no es una imagen tampoco
   se acepta.
5. El **detalle** del libro muestra la portada si tiene, y el detalle del autor
   su foto. La **lista** de libros muestra la portada chiquita.
6. Al **cambiar** la portada de un libro, el archivo viejo se **borra** del
   disco. Al **borrar** un libro, se borra también su portada.

## Planillas (CSV separado por `;`)

7. **Bajar la planilla de libros**: dirección `libros/exportar/`,
   **`name="exportar"`**. Cualquiera puede bajarla. Descarga un archivo
   **`libros.csv`** con una fila de títulos **`titulo;autor;precio;stock`** y
   después un libro por fila, ordenados por título. Un link en la lista: "Bajar planilla".
8. **Importar libros**: dirección `libros/importar/`, **`name="importar"`**,
   solo con sesión iniciada. Una página con un formulario para subir el archivo
   (campo **`archivo`**). La planilla tiene las columnas
   **`titulo;autor;precio;stock;anio`**:
   - si el autor no existe, se crea; si existe, se usa ese
   - las filas con algún dato mal (precio con letras, falta una columna...) se
     saltean y se sigue con las demás
   - después vuelve a la **lista** con el mensaje **`Se importaron N libros.`**
     y, si hubo filas malas, otro mensaje que diga cuáles (por número de fila)
   - si el archivo no es un CSV de texto (por ejemplo, una foto), el mensaje de
     error **`El archivo no es una planilla CSV.`** y no se importa nada
   - un link en la lista: "Importar planilla"

Para probar el punto 8, armá la planilla con Excel (Guardar como → "CSV
delimitado por punto y coma") o con el Bloc de notas:

```
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

Las imágenes que subas aparecen en la carpeta `media\portadas\` del proyecto:
mirala mientras probás cambiar y borrar.

## Cómo comprobar que está bien

1. Copiá **`test_paso5.py`** a tu carpeta `libros`.
2. `python manage.py test libros.test_paso5` (o `python manage.py test libros` para todos).

La prueba usa una carpeta temporal para las imágenes: no toca tu `media/`.

La solución está en `solucion/libreria/` (con su `COMO_USARLA.md`).
