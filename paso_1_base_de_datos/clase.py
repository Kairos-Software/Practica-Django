"""
═══════════════════════════════════════════════════════════════════════
 PASO 1 — BASES DE DATOS (SQL a mano)
═══════════════════════════════════════════════════════════════════════

Ejecutalo:   python clase.py
Leelo de arriba a abajo: cada parte explica algo y después lo hace.

¿Por qué empezar por acá si Django escribe el SQL solo? Porque cuando algo
falle (y va a fallar) vas a entender QUÉ le está pidiendo Django a la base.


1) ¿QUÉ ES UNA BASE DE DATOS?
─────────────────────────────
Un programa que guarda datos de forma ordenada y los mantiene aunque apagues
la compu. Los datos van en TABLAS, como una planilla de Excel:

    Tabla "peliculas"
    ┌────┬──────────────────────┬──────┬─────────┐
    │ id │ titulo               │ anio │ minutos │   <- COLUMNAS (campos)
    ├────┼──────────────────────┼──────┼─────────┤
    │ 1  │ Volver al futuro     │ 1985 │ 116     │   <- una FILA (un registro)
    │ 2  │ Toy Story            │ 1995 │ 81      │
    └────┴──────────────────────┴──────┴─────────┘

- Cada columna tiene un TIPO: texto, número entero, decimal, fecha, sí/no...
- "id" es la CLAVE PRIMARIA (primary key): un número único por fila, para
  poder decir "la película 2" sin confusión aunque haya dos con el mismo título.

Para hablar con la base se usa SQL, un idioma con 4 operaciones básicas que
se conocen como CRUD:

    Create  -> INSERT   (guardar)
    Read    -> SELECT   (buscar / leer)
    Update  -> UPDATE   (editar)
    Delete  -> DELETE   (borrar)


2) SQLITE vs POSTGRESQL (y MySQL, etc.)
───────────────────────────────────────
Todas hablan SQL (con pequeñas diferencias). Cambia DÓNDE viven los datos:

  SQLite      -> todo en UN archivo (ej: "datos.db"). No hay que instalar
                 nada: viene con Python. Ideal para aprender, prototipos y
                 apps chicas. Django lo usa por defecto.
  PostgreSQL  -> un PROGRAMA servidor aparte (hay que instalarlo). Varios
                 usuarios y programas a la vez, más robusto, lo que se usa en
                 producción (Kairos TV usa PostgreSQL).

Con Django pasar de una a otra es cambiar UNA configuración (lo vemos en el
paso 2). Por eso acá practicamos con SQLite: el SQL que aprendas sirve igual.
Al final de este archivo está cómo sería lo mismo con PostgreSQL.
"""

import sqlite3

# ═══════════════════════════════════════════════════════════════════════
# 3) CONECTARSE
# ═══════════════════════════════════════════════════════════════════════
# connect() abre (o crea, si no existe) el archivo de la base.
# ":memory:" = una base en la memoria, que desaparece al terminar: perfecta
# para practicar sin dejar basura. Cambialo por "practica.db" y vas a ver
# que aparece el archivo (y que los datos siguen ahí la próxima vez).
conexion = sqlite3.connect(":memory:")

# El "cursor" es el que manda las órdenes SQL y trae los resultados.
cursor = conexion.cursor()

# SQLite viene con las claves foráneas apagadas (cosa rara de SQLite).
# Las prendemos para que nos proteja (ver punto 9).
cursor.execute("PRAGMA foreign_keys = ON")


def titulo(texto):
    print("\n" + "─" * 60 + f"\n {texto}\n" + "─" * 60)


# ═══════════════════════════════════════════════════════════════════════
# 4) CREAR UNA TABLA  (CREATE TABLE)
# ═══════════════════════════════════════════════════════════════════════
# Se dice el nombre de la tabla y cada columna con su tipo y sus reglas:
#   INTEGER PRIMARY KEY AUTOINCREMENT -> el id lo pone la base solo (1, 2, 3...)
#   TEXT NOT NULL   -> texto obligatorio (NULL = "vacío / sin dato")
#   INTEGER         -> número entero (puede quedar vacío)
#   REAL            -> número con decimales (precios, promedios: 1234.50)
#   DEFAULT 0       -> si no lo mandás, vale 0
#   UNIQUE          -> no puede haber dos filas con el mismo valor
#   CHECK (...)     -> una condición que tiene que cumplirse (ej: no negativo)
titulo("4) Crear la tabla")
cursor.execute("""
    CREATE TABLE peliculas (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo   TEXT    NOT NULL,
        anio     INTEGER,
        minutos  INTEGER DEFAULT 0 CHECK (minutos >= 0),
        codigo   TEXT    UNIQUE,
        puntaje  REAL
    )
""")
print("Tabla 'peliculas' creada.")


# ═══════════════════════════════════════════════════════════════════════
# 5) GUARDAR  (INSERT)
# ═══════════════════════════════════════════════════════════════════════
# MUY IMPORTANTE: los valores van con "?" y aparte, en una tupla. NUNCA
# armes el SQL pegando texto, así:
#     f"INSERT ... VALUES ('{titulo}')"       <- ¡MAL!
# Si alguien escribe como título:   x'); DROP TABLE peliculas; --
# te borra la tabla. Eso se llama "inyección SQL" y es uno de los ataques más
# comunes. Con "?" la base trata el valor como dato, nunca como orden.
# (Django lo hace bien solo: otro motivo para usar su ORM.)
titulo("5) Guardar (INSERT)")
cursor.execute(
    "INSERT INTO peliculas (titulo, anio, minutos, codigo) VALUES (?, ?, ?, ?)",
    ("Volver al futuro", 1985, 116, "VAF"),
)
print("Guardada. Su id es:", cursor.lastrowid)

# Muchas de una vez: executemany
cursor.executemany(
    "INSERT INTO peliculas (titulo, anio, minutos, codigo) VALUES (?, ?, ?, ?)",
    [
        ("Toy Story", 1995, 81, "TS1"),
        ("Matrix", 1999, 136, "MTX"),
        ("Shrek", 2001, 90, "SHR"),
        ("Toy Story 2", 1999, 92, "TS2"),
    ],
)

# commit() = "confirmar". Hasta que no hacés commit, los cambios están en
# borrador: si el programa se corta, se pierden. (Ver punto 10, transacciones.)
conexion.commit()
print("Guardadas 4 más y confirmadas con commit().")


# ═══════════════════════════════════════════════════════════════════════
# 6) BUSCAR / LEER  (SELECT)
# ═══════════════════════════════════════════════════════════════════════
titulo("6) Leer (SELECT)")

# Todas las columnas (*) de todas las filas
cursor.execute("SELECT * FROM peliculas")
for fila in cursor.fetchall():          # fetchall() = traer TODAS las filas
    print(fila)                         # cada fila es una tupla

# Solo algunas columnas, con condición (WHERE) y orden (ORDER BY)
print("\nDe 1999 o después, de la más nueva a la más vieja:")
cursor.execute(
    "SELECT titulo, anio FROM peliculas WHERE anio >= ? ORDER BY anio DESC, titulo",
    (1999,),        # ojo: una tupla de UN elemento lleva la coma
)
for titulo_, anio in cursor.fetchall():   # se puede "desarmar" la tupla
    print(f"  {titulo_} ({anio})")

# Una sola fila: fetchone() (None si no hay)
cursor.execute("SELECT * FROM peliculas WHERE codigo = ?", ("MTX",))
print("\nLa de código MTX:", cursor.fetchone())
cursor.execute("SELECT * FROM peliculas WHERE codigo = ?", ("NOEXISTE",))
print("Una que no existe:", cursor.fetchone())

# Buscar por parte del texto: LIKE con % ("cualquier cosa").
# En SQLite, LIKE no distingue mayúsculas ("toy" encuentra "Toy"); en
# PostgreSQL sí: ahí se usa ILIKE. El % se pega al valor, NO al SQL.
buscado = "toy"
cursor.execute("SELECT titulo FROM peliculas WHERE titulo LIKE ?", (f"%{buscado}%",))
print("Las que dicen 'toy':", [f[0] for f in cursor.fetchall()])

# Cuentas en el SQL: la base puede calcular (ej: pasar minutos a horas)
cursor.execute("SELECT titulo, minutos / 60.0 FROM peliculas WHERE minutos > 100")
print("En horas:", [(t, round(h, 1)) for t, h in cursor.fetchall()])

# Contar, sumar, promediar (funciones de agregación)
cursor.execute("SELECT COUNT(*), SUM(minutos), AVG(minutos) FROM peliculas")
cantidad, total, promedio = cursor.fetchone()
print(f"Hay {cantidad} películas, {total} minutos en total, {promedio:.1f} de promedio.")

# LIMIT: solo las primeras N (para paginar)
cursor.execute("SELECT titulo FROM peliculas ORDER BY minutos DESC LIMIT 2")
print("Las 2 más largas:", [f[0] for f in cursor.fetchall()])


# ═══════════════════════════════════════════════════════════════════════
# 7) EDITAR  (UPDATE)
# ═══════════════════════════════════════════════════════════════════════
# ¡SIEMPRE con WHERE! Un UPDATE sin WHERE cambia TODAS las filas.
titulo("7) Editar (UPDATE)")
cursor.execute("UPDATE peliculas SET minutos = ? WHERE codigo = ?", (88, "SHR"))
print("Filas cambiadas:", cursor.rowcount)     # rowcount = cuántas tocó
conexion.commit()
cursor.execute("SELECT titulo, minutos FROM peliculas WHERE codigo = 'SHR'")
print("Shrek ahora:", cursor.fetchone())

# Se puede usar el valor que ya tiene: "sumale 5 a lo que haya" (sin leerlo antes)
cursor.execute("UPDATE peliculas SET minutos = minutos + 5 WHERE anio < 1990")
cursor.execute("UPDATE peliculas SET puntaje = 8.5 WHERE puntaje IS NULL")   # IS NULL = "está vacío"
conexion.commit()
cursor.execute("SELECT titulo, minutos, puntaje FROM peliculas WHERE anio < 1990")
print("Las de antes de 1990, con 5 minutos más:", cursor.fetchall())

# CHECK no deja guardar un valor que no cumple la condición
try:
    cursor.execute("UPDATE peliculas SET minutos = -10 WHERE codigo = 'SHR'")
except sqlite3.IntegrityError as error:
    print("CHECK no dejó poner minutos negativos:", error)


# ═══════════════════════════════════════════════════════════════════════
# 8) BORRAR  (DELETE)
# ═══════════════════════════════════════════════════════════════════════
# Igual: ¡SIEMPRE con WHERE! "DELETE FROM peliculas" vacía la tabla entera.
titulo("8) Borrar (DELETE)")
cursor.execute("DELETE FROM peliculas WHERE codigo = ?", ("TS2",))
print("Filas borradas:", cursor.rowcount)
conexion.commit()
cursor.execute("SELECT COUNT(*) FROM peliculas")
print("Quedan:", cursor.fetchone()[0])

# Las reglas de la tabla te protegen: UNIQUE no deja repetir el código
try:
    cursor.execute("INSERT INTO peliculas (titulo, codigo) VALUES (?, ?)", ("Otra Matrix", "MTX"))
except sqlite3.IntegrityError as error:
    print("No dejó repetir el código:", error)

# y NOT NULL no deja guardar sin título
try:
    cursor.execute("INSERT INTO peliculas (anio) VALUES (?)", (2020,))
except sqlite3.IntegrityError as error:
    print("No dejó guardar sin título:", error)


# ═══════════════════════════════════════════════════════════════════════
# 9) RELACIONAR TABLAS  (FOREIGN KEY y JOIN)
# ═══════════════════════════════════════════════════════════════════════
# Cada película tiene UNA categoría; cada categoría tiene MUCHAS películas.
# Eso es una relación "uno a muchos". NO se repite el nombre de la categoría
# en cada película: se guarda el id de la categoría (una CLAVE FORÁNEA).
#
#   categorias              peliculas
#   ┌────┬──────────┐       ┌────┬────────────┬──────────────┐
#   │ id │ nombre   │       │ id │ titulo     │ categoria_id │
#   ├────┼──────────┤       ├────┼────────────┼──────────────┤
#   │ 1  │ Infantil │ <──── │ 2  │ Toy Story  │ 1            │
#   │ 2  │ Acción   │ <──── │ 3  │ Matrix     │ 2            │
#   └────┴──────────┘       └────┴────────────┴──────────────┘
#
# Ventaja: si "Infantil" pasa a llamarse "Para chicos", se cambia en UN lugar.
titulo("9) Relaciones (FOREIGN KEY y JOIN)")
cursor.execute("""
    CREATE TABLE categorias (
        id     INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    )
""")
# ALTER TABLE = cambiarle algo a una tabla que ya existe (agregar una columna)
# REFERENCES = "este número tiene que ser un id que exista en categorias"
cursor.execute("ALTER TABLE peliculas ADD COLUMN categoria_id INTEGER REFERENCES categorias(id)")
cursor.executemany("INSERT INTO categorias (nombre) VALUES (?)", [("Infantil",), ("Acción",)])
cursor.execute("UPDATE peliculas SET categoria_id = 1 WHERE codigo IN ('TS1', 'SHR')")
cursor.execute("UPDATE peliculas SET categoria_id = 2 WHERE codigo IN ('MTX', 'VAF')")
conexion.commit()

# JOIN: juntar las dos tablas por la relación para leer el nombre de la categoría
cursor.execute("""
    SELECT peliculas.titulo, categorias.nombre
    FROM peliculas
    JOIN categorias ON categorias.id = peliculas.categoria_id
    ORDER BY categorias.nombre, peliculas.titulo
""")
for titulo_, categoria in cursor.fetchall():
    print(f"  {titulo_:20} -> {categoria}")

# GROUP BY: cuántas películas hay por categoría
cursor.execute("""
    SELECT categorias.nombre, COUNT(peliculas.id)
    FROM categorias
    LEFT JOIN peliculas ON peliculas.categoria_id = categorias.id
    GROUP BY categorias.id
""")
print("Por categoría:", cursor.fetchall())
# (LEFT JOIN = traer TODAS las categorías, aunque no tengan películas)
# Y si una categoría no tiene películas, SUM(...) da NULL (vacío). Para que dé 0:
#     COALESCE(SUM(peliculas.minutos), 0)     <- "esto, o 0 si está vacío"
cursor.execute("""
    SELECT categorias.nombre, COALESCE(SUM(peliculas.minutos), 0)
    FROM categorias LEFT JOIN peliculas ON peliculas.categoria_id = categorias.id
    GROUP BY categorias.id
""")
print("Minutos por categoría:", cursor.fetchall())

# La clave foránea protege: no deja apuntar a una categoría que no existe
try:
    cursor.execute("UPDATE peliculas SET categoria_id = 99 WHERE codigo = 'MTX'")
except sqlite3.IntegrityError as error:
    print("No dejó usar una categoría inexistente:", error)


# ═══════════════════════════════════════════════════════════════════════
# 10) TRANSACCIONES: todo o nada
# ═══════════════════════════════════════════════════════════════════════
# Si hacés varios cambios que van JUNTOS (ej: pasar plata de una cuenta a
# otra: restar en una y sumar en otra), o se hacen todos, o ninguno.
# rollback() = deshacer todo lo que no se confirmó con commit().
titulo("10) Transacciones (commit / rollback)")
try:
    cursor.execute("UPDATE peliculas SET minutos = 0")         # cambio 1 (¡sin WHERE: todas!)
    raise RuntimeError("se cortó la luz a la mitad")           # simulamos un error
except RuntimeError as error:
    conexion.rollback()                                        # se deshace el cambio 1
    print("Hubo un error:", error, "-> rollback, no quedó nada a medias.")
cursor.execute("SELECT SUM(minutos) FROM peliculas")
print("Los minutos siguen intactos:", cursor.fetchone()[0])

# Forma cómoda: "with conexion:" hace commit si todo sale bien y rollback si hay error
with conexion:
    conexion.execute("INSERT INTO peliculas (titulo, anio, codigo) VALUES (?, ?, ?)", ("Up", 2009, "UP1"))
print("Guardada 'Up' con 'with' (commit automático).")

conexion.close()     # siempre cerrar al terminar


# ═══════════════════════════════════════════════════════════════════════
# 11) LO MISMO CON POSTGRESQL
# ═══════════════════════════════════════════════════════════════════════
# 1. Instalar PostgreSQL (postgresql.org) y crear una base, por ejemplo con
#    la terminal "psql":
#        CREATE DATABASE practica;
#    (o con DBeaver / pgAdmin, que tenés: botón derecho -> Crear base de datos)
# 2. pip install "psycopg[binary]"
# 3. El código es CASI igual. Diferencias:
#      - los parámetros van con %s en vez de ?
#      - el id automático se escribe:  id SERIAL PRIMARY KEY
#        (o  id INTEGER GENERATED ALWAYS AS IDENTITY)
#
#   import psycopg
#   with psycopg.connect("dbname=practica user=postgres password=TU_CLAVE host=localhost") as conexion:
#       with conexion.cursor() as cursor:
#           cursor.execute("CREATE TABLE peliculas (id SERIAL PRIMARY KEY, titulo TEXT NOT NULL)")
#           cursor.execute("INSERT INTO peliculas (titulo) VALUES (%s)", ("Matrix",))
#           cursor.execute("SELECT * FROM peliculas")
#           print(cursor.fetchall())
#       # al salir del "with" hace commit solo
#
# En Django NI SIQUIERA eso cambia: escribís el mismo código y él traduce.


# ═══════════════════════════════════════════════════════════════════════
# RESUMEN (para repasar antes del ejercicio)
# ═══════════════════════════════════════════════════════════════════════
#  CREATE TABLE t (col TIPO reglas, ...)       crear una tabla
#  INSERT INTO t (a, b) VALUES (?, ?)          guardar
#  SELECT a, b FROM t WHERE ... ORDER BY ...   buscar   (fetchall / fetchone)
#  UPDATE t SET a = ? WHERE ...                editar   ¡con WHERE!
#  DELETE FROM t WHERE ...                     borrar   ¡con WHERE!
#  JOIN otra ON otra.id = t.otra_id            leer de dos tablas relacionadas
#  COUNT / SUM / AVG + GROUP BY                contar y sumar por grupo
#  commit() confirma, rollback() deshace, "?" siempre para los valores.
print("\nFin de la clase 1. Ahora: ejercicio.md")
