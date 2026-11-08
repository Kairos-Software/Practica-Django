# Ejercicio paso 1 — La librería de barrio (SQL a mano)

Vas a escribir las funciones de una librería que guarda **autores** y
**libros** en una base de datos SQLite, con SQL escrito por vos. Todo lo que
necesitás está en `clase.py` (el de las películas).

> **Los nombres tienen que ser exactamente estos** (de funciones, tablas y
> columnas). La prueba automática los busca escritos así.

---

## Antes de empezar: dónde está cada cosa en la clase

| Para el punto | Mirá en `clase.py` |
|---|---|
| 1 (tablas) | PARTE 5 (CREATE TABLE y sus reglas) y PARTE 10 (`REFERENCES`) |
| 2 y 3 (guardar) | PARTE 6 (INSERT, `?`, `lastrowid`, `commit`) y PARTE 9 (convertir el error de sqlite en un `ValueError`) |
| 4 (con autor) | PARTE 10 (JOIN) |
| 5, 6 y 7 (leer) | PARTE 7 (SELECT, WHERE, ORDER BY, LIKE, pasar tuplas a una lista de textos) |
| 8 (resumen) | PARTE 10 (LEFT JOIN, GROUP BY, COALESCE) |
| 9 y 10 (modificar) | PARTE 8 (UPDATE, `rowcount`, UPDATE con condición) y la TRAMPA de la división en la PARTE 7 |
| 11 (borrar) | PARTE 9 (DELETE) |
| 12 (todo o nada) | PARTE 11 (transacciones, `with conexion:`) |

---

## Cómo arrancar (la primera vez)

**1. Creá el archivo `mi_solucion.py`** en la carpeta `paso_1_base_de_datos`
(clic derecho sobre la carpeta → **New File**).

**2. Arriba de todo, importá sqlite3**, y escribí la primera función:

```python
import sqlite3


def crear_tablas(conexion):
    pass    # reemplazá "pass" por tu código
```

**3. Corré la prueba** desde la terminal:

```powershell
cd "D:\Desktop\Aprender Django\paso_1_base_de_datos"
python prueba.py
```

Se lee igual que en el paso 0: `ok` está bien; `FAIL` o `ERROR` muestran
abajo qué esperaba la prueba y qué encontró (leé la **última línea** de cada
bloque).

### Algo importante: la conexión te la dan

Todas las funciones reciben como primer dato la **conexión** ya abierta, en
un parámetro llamado `conexion`. **No** la abras vos con `sqlite3.connect`
adentro de las funciones: la prueba crea una base nueva y vacía (en memoria)
para cada punto, y te la pasa. Vos usás esa:

```python
def una_funcion(conexion):
    cursor = conexion.execute("SELECT ...")    # o conexion.cursor() y cursor.execute(...)
```

Las funciones que **cambian** datos (INSERT, UPDATE, DELETE) tienen que
terminar con `conexion.commit()`.

---

## Lo que tenés que hacer

Para los ejemplos, imaginá que la base tiene esto (es lo que carga la prueba):

| Autor | Libro | Precio | Stock |
|---|---|---|---|
| Borges | Ficciones | 15000 | 4 |
| Borges | El Aleph | 14000 | 0 |
| Cortázar | Rayuela | 20000 | 3 |
| Cortázar | Bestiario | 12000 | 5 |
| Quino | (ninguno) | | |

### Las tablas

**1. `crear_tablas(conexion)`** crea dos tablas:
- **`autores`** con las columnas `id` (automático) y `nombre` (obligatorio y
  sin repetir).
- **`libros`** con las columnas `id` (automático), `titulo` (obligatorio),
  `precio` (con decimales, **no negativo**), `stock` (entero, **por defecto 0**)
  y `autor_id` (relacionado con la tabla `autores`: tiene que ser el id de un
  autor que exista).

La prueba revisa que las columnas se llamen así, que un precio negativo sea
rechazado por la tabla, y que un `autor_id` que no existe también.

### Guardar

**2. `agregar_autor(conexion, nombre)`** guarda el autor y **devuelve su id**
(un número). Si ya existe uno con ese nombre, provoca un `ValueError` con un
mensaje entendible (no tiene que salir el error de sqlite, `IntegrityError`).

**3. `agregar_libro(conexion, titulo, precio, stock, autor_id)`** guarda el
libro y **devuelve su id**.

### Leer

**4. `libros_con_autor(conexion)`** devuelve una lista de tuplas
`(titulo, nombre_del_autor)` de todos los libros, ordenada por título.

```python
[("Bestiario", "Cortázar"), ("El Aleph", "Borges"), ("Ficciones", "Borges"), ("Rayuela", "Cortázar")]
```

**5. `libros_sin_stock(conexion)`** devuelve una lista con los **títulos**
(textos, no tuplas) de los libros con stock 0, ordenada por título.

```python
["El Aleph"]
```

**6. `libros_mas_baratos_que(conexion, precio)`** devuelve una lista de
tuplas `(titulo, precio)` de los libros que cuestan **menos** que ese precio,
del más barato al más caro.

```python
libros_mas_baratos_que(conexion, 15000)    # [("Bestiario", 12000.0), ("El Aleph", 14000.0)]
```

**7. `buscar_libros(conexion, texto)`** devuelve una lista de títulos que
contienen el texto (sin importar mayúsculas), ordenada por título. Tiene que
ser **segura**: si el texto es `"x'; DROP TABLE libros; --"` no tiene que
romper nada (la prueba lo intenta y después cuenta que sigan estando los libros).

```python
buscar_libros(conexion, "AL")     # ["El Aleph"]
buscar_libros(conexion, "ray")    # ["Rayuela"]
```

**8. `resumen_por_autor(conexion)`** devuelve una lista de tuplas
`(nombre, cantidad_de_libros, valor_del_stock)` de **todos** los autores
(también los que no tienen libros, con 0 y 0), ordenada por nombre. El valor
del stock es la suma de precio × stock de sus libros.

```python
[("Borges", 2, 60000.0), ("Cortázar", 2, 120000.0), ("Quino", 0, 0)]
```

(Borges: 15000 × 4 + 14000 × 0 = 60000. Quino no tiene libros, pero tiene que aparecer.)

### Modificar

**9. `vender(conexion, libro_id, cantidad)`** le resta la cantidad al stock
de ese libro (la resta la hace la base, con un UPDATE). Si no alcanza el
stock, provoca un `ValueError` **y no cambia nada**.

```python
vender(conexion, id_de_ficciones, 3)    # Ficciones pasa de 4 a 1
vender(conexion, id_de_ficciones, 5)    # ValueError: solo queda 1. Y sigue en 1.
```

**10. `subir_precios_de_autor(conexion, autor_id, porcentaje)`** sube el
precio de todos los libros de ese autor en ese porcentaje y **devuelve
cuántos libros cambió**.

```python
subir_precios_de_autor(conexion, id_de_cortazar, 10)   # devuelve 2
# Bestiario pasa a 13200 y Rayuela a 22000
```

**11. `borrar_sin_stock(conexion)`** borra los libros con stock 0 y
**devuelve cuántos borró**.

```python
borrar_sin_stock(conexion)    # devuelve 1 (El Aleph). Quedan 3 libros.
```

### Transacción

**12. `agregar_libros_juntos(conexion, libros)`** recibe una lista de tuplas
`(titulo, precio, stock, autor_id)` y las guarda **todas o ninguna**: si
alguna falla (por ejemplo, un precio negativo), no queda guardada ninguna, y
la función provoca un `ValueError`.

```python
agregar_libros_juntos(conexion, [("Mafalda 1", 8000, 2, quino), ("Mafalda 2", 8000, 1, quino)])
# guarda las dos
agregar_libros_juntos(conexion, [("Mafalda 3", 8000, 1, quino), ("Mal", -50, 1, quino)])
# ValueError, y "Mafalda 3" TAMPOCO queda guardada
```

---

## Probar a mano mientras programás (opcional)

Al **final** de tu archivo:

```python
if __name__ == "__main__":
    conexion = sqlite3.connect("libreria.db")      # un archivo: lo podés abrir con DBeaver
    conexion.execute("PRAGMA foreign_keys = ON")
    crear_tablas(conexion)
    borges = agregar_autor(conexion, "Borges")
    agregar_libro(conexion, "Ficciones", 15000, 4, borges)
    print(libros_con_autor(conexion))
```

y ejecutalo con `python mi_solucion.py`.

Si lo ejecutás dos veces, va a fallar: la primera vez se creó el archivo
`libreria.db` con las tablas y con Borges, y la segunda vez las tablas ya
existen (y Borges también). Antes de volver a ejecutarlo, borrá `libreria.db`.
También podés usar `CREATE TABLE IF NOT EXISTS` (ver la PARTE 5 de la clase).
El archivo `libreria.db` no se sube al repositorio (está en el `.gitignore`).

---

## Cuando terminaste

- `python prueba.py` tiene que terminar con `✔ ¡Todo bien! Paso 1 aprobado.`
- Recién ahí, compará con `solucion.py` (y `python prueba.py solucion`).
