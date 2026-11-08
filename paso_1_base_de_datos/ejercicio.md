# Ejercicio paso 1 — La librería de barrio (SQL a mano)

Escribí **`mi_solucion.py`** en esta carpeta con las funciones de abajo,
usando `sqlite3` y SQL escrito por vos. **Los nombres tienen que ser exactamente
estos** (la prueba los busca así).

Todas las funciones reciben como primer dato la **conexión** ya abierta
(`conexion`), así la prueba puede usar una base en memoria. Las que cambian
datos tienen que hacer `commit()`.

## Las tablas

1. `crear_tablas(conexion)` crea:
   - **autores**: id automático, nombre (obligatorio y sin repetir)
   - **libros**: id automático, titulo (obligatorio), precio (con decimales,
     no negativo), stock (entero, por defecto 0), autor_id (relacionado con
     autores)

## Guardar

2. `agregar_autor(conexion, nombre)` → guarda el autor y **devuelve su id**.
   Si ya existe uno con ese nombre, que provoque un `ValueError` con un
   mensaje entendible (no el error de sqlite).
3. `agregar_libro(conexion, titulo, precio, stock, autor_id)` → guarda el
   libro y devuelve su id.

## Leer

4. `libros_con_autor(conexion)` → lista de tuplas `(titulo, nombre_del_autor)`
   de todos los libros, ordenada por título.
5. `libros_sin_stock(conexion)` → lista con los **títulos** de los libros con
   stock 0, ordenada por título.
6. `libros_mas_baratos_que(conexion, precio)` → lista de tuplas
   `(titulo, precio)` de los que cuestan menos, del más barato al más caro.
7. `buscar_libros(conexion, texto)` → lista de títulos que contienen el texto
   (sin importar mayúsculas), ordenada. Tiene que ser **segura**: si el texto es
   `"x'; DROP TABLE libros; --"` no tiene que romper nada.
8. `resumen_por_autor(conexion)` → lista de tuplas
   `(nombre, cantidad_de_libros, valor_del_stock)` de **todos** los autores
   (también los que no tienen libros, con 0 y 0), ordenada por nombre. El valor
   del stock es la suma de precio × stock.

## Modificar

9. `vender(conexion, libro_id, cantidad)` → resta la cantidad al stock (la
   resta la hace la base). Si no alcanza el stock, `ValueError` y no cambia nada.
10. `subir_precios_de_autor(conexion, autor_id, porcentaje)` → sube el precio
    de todos los libros de ese autor y devuelve **cuántos** cambió.
11. `borrar_sin_stock(conexion)` → borra los libros con stock 0 y devuelve
    cuántos borró.

## Transacción

12. `agregar_libros_juntos(conexion, libros)` → recibe una lista de tuplas
    `(titulo, precio, stock, autor_id)` y las guarda **todas o ninguna**: si
    alguna falla (por ejemplo, un precio negativo), no queda guardada ninguna,
    y la función provoca un `ValueError`.

## Cómo ejecutarlo y comprobarlo

```powershell
cd "D:\Desktop\Aprender Django"
.\entorno\Scripts\activate
cd paso_1_base_de_datos
python prueba.py               # prueba tu mi_solucion.py
python prueba.py solucion      # (al final) la solución
```

Para probar a mano mientras programás, al final de tu archivo:

```python
if __name__ == "__main__":
    import sqlite3
    conexion = sqlite3.connect("libreria.db")      # un archivo: lo podés abrir con DBeaver
    conexion.execute("PRAGMA foreign_keys = ON")
    crear_tablas(conexion)
    borges = agregar_autor(conexion, "Borges")
    print(libros_con_autor(conexion))
```

y `python mi_solucion.py`. (Si lo ejecutás dos veces, el `CREATE TABLE` va a
fallar porque la tabla ya existe: borrá `libreria.db` o usá
`CREATE TABLE IF NOT EXISTS`.)
