"""Solución del paso 1 — La librería de barrio con SQL a mano. (Es UNA forma de hacerlo.)"""

import sqlite3


def crear_tablas(conexion):
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS autores (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    """)
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo    TEXT NOT NULL,
            precio    REAL NOT NULL CHECK (precio >= 0),
            stock     INTEGER NOT NULL DEFAULT 0,
            autor_id  INTEGER NOT NULL REFERENCES autores(id)
        )
    """)
    conexion.commit()


def agregar_autor(conexion, nombre):
    try:
        cursor = conexion.execute("INSERT INTO autores (nombre) VALUES (?)", (nombre,))
    except sqlite3.IntegrityError:
        conexion.rollback()
        raise ValueError(f"Ya existe un autor llamado {nombre}.") from None
    conexion.commit()
    return cursor.lastrowid


def agregar_libro(conexion, titulo, precio, stock, autor_id):
    cursor = conexion.execute("INSERT INTO libros (titulo, precio, stock, autor_id) VALUES (?, ?, ?, ?)",
                              (titulo, precio, stock, autor_id))
    conexion.commit()
    return cursor.lastrowid


def libros_con_autor(conexion):
    return conexion.execute("""
        SELECT libros.titulo, autores.nombre
        FROM libros JOIN autores ON autores.id = libros.autor_id
        ORDER BY libros.titulo
    """).fetchall()


def libros_sin_stock(conexion):
    filas = conexion.execute("SELECT titulo FROM libros WHERE stock = 0 ORDER BY titulo").fetchall()
    return [titulo for (titulo,) in filas]


def libros_mas_baratos_que(conexion, precio):
    return conexion.execute("SELECT titulo, precio FROM libros WHERE precio < ? ORDER BY precio",
                            (precio,)).fetchall()


def buscar_libros(conexion, texto):
    # El % se pega al VALOR; el SQL queda fijo con "?": así no hay inyección posible
    filas = conexion.execute("SELECT titulo FROM libros WHERE titulo LIKE ? ORDER BY titulo", (f"%{texto}%",))
    return [titulo for (titulo,) in filas]


def resumen_por_autor(conexion):
    return conexion.execute("""
        SELECT autores.nombre,
               COUNT(libros.id),
               COALESCE(SUM(libros.precio * libros.stock), 0)
        FROM autores
        LEFT JOIN libros ON libros.autor_id = autores.id
        GROUP BY autores.id
        ORDER BY autores.nombre
    """).fetchall()


def vender(conexion, libro_id, cantidad):
    # La condición "stock >= ?" hace que la base solo reste si alcanza
    cursor = conexion.execute("UPDATE libros SET stock = stock - ? WHERE id = ? AND stock >= ?",
                              (cantidad, libro_id, cantidad))
    if cursor.rowcount == 0:
        conexion.rollback()
        raise ValueError("No alcanza el stock (o el libro no existe).")
    conexion.commit()


def subir_precios_de_autor(conexion, autor_id, porcentaje):
    cursor = conexion.execute("UPDATE libros SET precio = precio * (1 + ? / 100.0) WHERE autor_id = ?",
                              (porcentaje, autor_id))
    conexion.commit()
    return cursor.rowcount


def borrar_sin_stock(conexion):
    cursor = conexion.execute("DELETE FROM libros WHERE stock = 0")
    conexion.commit()
    return cursor.rowcount


def agregar_libros_juntos(conexion, libros):
    try:
        with conexion:      # commit si todo sale bien; rollback si algo falla
            conexion.executemany("INSERT INTO libros (titulo, precio, stock, autor_id) VALUES (?, ?, ?, ?)", libros)
    except sqlite3.IntegrityError as error:
        raise ValueError(f"No se guardó ninguno: {error}") from None


if __name__ == "__main__":
    conexion = sqlite3.connect(":memory:")
    conexion.execute("PRAGMA foreign_keys = ON")
    crear_tablas(conexion)
    borges = agregar_autor(conexion, "Borges")
    agregar_libro(conexion, "Ficciones", 15000, 4, borges)
    print(libros_con_autor(conexion))
    print(resumen_por_autor(conexion))
