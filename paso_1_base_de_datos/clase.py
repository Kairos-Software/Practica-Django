"""
=======================================================================
 PASO 1 — BASES DE DATOS (SQL escrito a mano)
=======================================================================

¿Por qué aprender SQL si Django lo escribe solo? Porque cuando algo falle
(y va a fallar) vas a entender QUÉ le está pidiendo Django a la base.

El ejemplo de toda la clase: una colección de PELÍCULAS.


¿QUÉ NECESITÁS?
---------------
Solo Python (igual que en el paso 0). SQLite, la base de datos que usamos
acá, ya viene incluida en Python: no hay que instalar nada.


CÓMO SE USA ESTE ARCHIVO
------------------------
1. En la terminal de VS Code (menú Terminal → New Terminal), parado en la
   carpeta "Aprender Django", escribí y apretá Enter:

       python paso_1_base_de_datos\\clase.py

2. Van a aparecer resultados separados en PARTES (PARTE 4, PARTE 5...).
   Las partes 1, 2 y 3 son solo explicación: no muestran nada.

3. Leé este archivo de arriba a abajo. Debajo de cada print() está
   anotado lo que muestra (después de "# Muestra:"). Comparalo con la
   terminal.

4. Cambiá cosas y volvé a ejecutar (flecha ↑ en la terminal repite la
   orden). Si rompés algo:   git restore paso_1_base_de_datos\\clase.py


=======================================================================
PARTE 1 — ¿QUÉ ES UNA BASE DE DATOS?
=======================================================================
Es un programa que GUARDA datos ordenados y los mantiene aunque apagues la
compu. Hasta ahora, en el paso 0, los datos vivían en variables: cuando el
programa terminaba, se perdían. En una base quedan guardados.

Los datos van en TABLAS, como una planilla de Excel:

    Tabla "peliculas"
    ┌────┬──────────────────┬──────┬─────────┐
    │ id │ titulo           │ anio │ minutos │   <- las COLUMNAS (cada dato)
    ├────┼──────────────────┼──────┼─────────┤
    │ 1  │ Volver al futuro │ 1985 │ 116     │   <- una FILA (una película)
    │ 2  │ Toy Story        │ 1995 │ 81      │   <- otra FILA
    └────┴──────────────────┴──────┴─────────┘

- Cada COLUMNA tiene un nombre y un TIPO: texto, número entero, número con
  decimales, fecha...
- Cada FILA es una cosa guardada (acá, una película).
- "id" es la CLAVE PRIMARIA (en inglés, primary key): un número único por
  fila, que pone la base sola. Sirve para decir "la película 2" sin
  confusión, aunque haya dos películas con el mismo título.
- NULL quiere decir "vacío, sin dato" (en Python se ve como None).


=======================================================================
PARTE 2 — SQL: EL IDIOMA DE LAS BASES DE DATOS
=======================================================================
Para pedirle cosas a la base se usa SQL, un idioma con órdenes en inglés.
Las cuatro básicas (se las conoce como CRUD):

    Crear   -> INSERT    (guardar una fila nueva)
    Leer    -> SELECT    (buscar y traer filas)
    Editar  -> UPDATE    (cambiar datos de filas que ya existen)
    Borrar  -> DELETE    (sacar filas)

Desde Python, cada orden SQL se escribe como un TEXTO (entre comillas) y se
le manda a la base. Las palabras de SQL se escriben en MAYÚSCULAS por
costumbre (SELECT, WHERE...), así se distinguen de los nombres tuyos.


=======================================================================
PARTE 3 — SQLITE Y POSTGRESQL
=======================================================================
Hay muchas bases de datos. Todas hablan SQL (con pequeñas diferencias).
Lo que cambia es DÓNDE viven los datos:

  SQLite      -> todo en UN archivo (por ejemplo "datos.db"). No hay que
                 instalar nada: viene con Python. Ideal para aprender y
                 para sistemas chicos. Django la usa si no le decís otra.
  PostgreSQL  -> un PROGRAMA aparte (hay que instalarlo) que atiende a
                 muchos usuarios a la vez. Es lo que se usa en sistemas
                 grandes y en servidores (Kairos TV usa PostgreSQL).

Con Django, pasar de una a otra es cambiar UNA configuración (paso 2). Por
eso practicamos con SQLite: el SQL que aprendas sirve igual para las dos.
Al final de este archivo (PARTE 12) está cómo sería con PostgreSQL.
"""

import sqlite3

# =======================================================================
# PARTE 4 — CONECTARSE A LA BASE
# =======================================================================
# Para hablar con una base, primero hay que CONECTARSE (como hacer una
# llamada telefónica: mientras está abierta, podés hablar).
#
#   sqlite3.connect("archivo.db")  abre la base guardada en ese archivo (y
#                                  si no existe, lo crea).
#   sqlite3.connect(":memory:")    una base que vive en la memoria y
#                                  desaparece al terminar el programa:
#                                  perfecta para practicar sin dejar basura.
#
# PROBÁ VOS: cambiá ":memory:" por "practica.db" y ejecutá. Va a aparecer
# el archivo practica.db en la carpeta, y lo podés abrir con DBeaver para
# ver las tablas. (Si lo ejecutás DOS veces, falla al crear la tabla porque
# ya existe: borrá practica.db antes de volver a ejecutar.)
conexion = sqlite3.connect(":memory:")

# El CURSOR es el que lleva las órdenes SQL a la base y trae las respuestas.
#   cursor.execute("ORDEN SQL")   manda una orden
cursor = conexion.cursor()
# (Atajo que también vas a ver: conexion.execute("ORDEN SQL") hace lo mismo,
#  sin crear el cursor a mano. Devuelve el cursor, así que podés hacer
#  conexion.execute("SELECT ...").fetchall() en una sola línea.)

# SQLite viene con un control importante APAGADO: el de las relaciones entre
# tablas (lo vas a ver en la PARTE 10). Siempre lo prendemos así:
cursor.execute("PRAGMA foreign_keys = ON")

print()
print("========== PARTE 4: conectarse ==========")
print("Conectado a una base en memoria.")
# Muestra: Conectado a una base en memoria.


# =======================================================================
# PARTE 5 — CREAR UNA TABLA (CREATE TABLE)
# =======================================================================
# Antes de guardar datos hay que crear la tabla: se dice su nombre, y cada
# columna con su TIPO y sus REGLAS. Las piezas que usamos:
#
#   INTEGER PRIMARY KEY AUTOINCREMENT   el id: lo pone la base sola (1, 2, 3...)
#   TEXT                                texto
#   INTEGER                             número entero
#   REAL                                número con decimales (1234.50)
#   NOT NULL                            OBLIGATORIO: no se puede dejar vacío
#   DEFAULT 0                           si no lo mandás, vale 0
#   UNIQUE                              no puede haber dos filas con el mismo valor
#   CHECK (minutos >= 0)                una condición que se tiene que cumplir siempre
#
# Las reglas son una PROTECCIÓN: la base no deja guardar datos que las rompan
# (lo vas a ver en las PARTES 8 y 9).
#
# Las triples comillas """ permiten escribir un texto en varias líneas.

print()
print("========== PARTE 5: crear la tabla ==========")
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
# Muestra: Tabla 'peliculas' creada.
# (Si la tabla ya existiera, daría error. Para evitarlo se escribe
#  CREATE TABLE IF NOT EXISTS peliculas (...): "creala solo si no existe".)


# =======================================================================
# PARTE 6 — GUARDAR (INSERT)
# =======================================================================
# INSERT INTO tabla (columna1, columna2) VALUES (valor1, valor2)
# "Insertá en la tabla, en estas columnas, estos valores."
#
# MUY IMPORTANTE: los valores NO se escriben adentro del texto SQL. Se pone
# un signo ? por cada valor, y los valores van APARTE, en una tupla
# (una lista entre paréntesis):
#
#     cursor.execute("INSERT INTO peliculas (titulo) VALUES (?)", ("Matrix",))
#
# NUNCA armes el SQL pegando textos, así:
#     cursor.execute(f"INSERT INTO peliculas (titulo) VALUES ('{titulo}')")   <- ¡MAL!
# Si alguien escribe como título:   x'); DROP TABLE peliculas; --
# esa "película" BORRA tu tabla. Se llama "inyección SQL" y es uno de los
# ataques más comunes del mundo. Con ? la base trata el valor siempre como
# un DATO, nunca como una orden. (Django lo hace bien solo.)

print()
print("========== PARTE 6: guardar (INSERT) ==========")
cursor.execute(
    "INSERT INTO peliculas (titulo, anio, minutos, codigo) VALUES (?, ?, ?, ?)",
    ("Volver al futuro", 1985, 116, "VAF"),
)
print("Guardada. Su id es:", cursor.lastrowid)
# Muestra: Guardada. Su id es: 1      <- lastrowid: el id que le puso la base a la fila recién guardada

# Muchas filas de una vez: executemany, con una LISTA de tuplas
cursor.executemany(
    "INSERT INTO peliculas (titulo, anio, minutos, codigo) VALUES (?, ?, ?, ?)",
    [
        ("Toy Story", 1995, 81, "TS1"),
        ("Matrix", 1999, 136, "MTX"),
        ("Shrek", 2001, 90, "SHR"),
        ("Toy Story 2", 1999, 92, "TS2"),
    ],
)

# commit() = CONFIRMAR los cambios. Hasta que no hacés commit(), los cambios
# están "en borrador": si el programa se corta, se pierden. Cada vez que
# guardás, editás o borrás algo, al final va un commit(). (Más en la PARTE 11.)
conexion.commit()
print("Guardadas 4 más y confirmadas con commit().")
# Muestra: Guardadas 4 más y confirmadas con commit().

# OJO: una tupla de UN SOLO valor lleva una coma al final: ("Matrix",)
#      Sin la coma, ("Matrix") es solo un texto entre paréntesis, y da error.


# =======================================================================
# PARTE 7 — LEER (SELECT)
# =======================================================================
# SELECT columnas FROM tabla WHERE condición ORDER BY columna
# "Traeme estas columnas, de esta tabla, de las filas que cumplan esto,
#  ordenadas así."
#
# Después del execute, la respuesta se trae con:
#   cursor.fetchall()   -> una LISTA con TODAS las filas
#   cursor.fetchone()   -> UNA sola fila (o None si no hay ninguna)
# Cada fila llega como una TUPLA: los valores en el orden de las columnas.

print()
print("========== PARTE 7: leer (SELECT) ==========")

# * quiere decir "todas las columnas"
cursor.execute("SELECT * FROM peliculas")
for fila in cursor.fetchall():
    print(fila)
# Muestra (una tupla por fila: id, titulo, anio, minutos, codigo, puntaje):
#   (1, 'Volver al futuro', 1985, 116, 'VAF', None)
#   (2, 'Toy Story', 1995, 81, 'TS1', None)
#   (3, 'Matrix', 1999, 136, 'MTX', None)
#   (4, 'Shrek', 2001, 90, 'SHR', None)
#   (5, 'Toy Story 2', 1999, 92, 'TS2', None)
# (puntaje es None porque no lo guardamos: quedó vacío, NULL)

# Solo algunas columnas, con condición (WHERE) y orden (ORDER BY).
#   ORDER BY anio DESC  -> de mayor a menor (DESC = descendente; sin nada, de menor a mayor)
#   ORDER BY anio DESC, titulo   -> si empatan en el año, por título
print("De 1999 o después, de la más nueva a la más vieja:")
cursor.execute(
    "SELECT titulo, anio FROM peliculas WHERE anio >= ? ORDER BY anio DESC, titulo",
    (1999,),
)
for titulo, anio in cursor.fetchall():       # cada tupla se "desarma" en dos variables
    print(" ", titulo, anio)
# Muestra:
#   De 1999 o después, de la más nueva a la más vieja:
#     Shrek 2001
#     Matrix 1999
#     Toy Story 2 1999

# Una sola fila: fetchone()
cursor.execute("SELECT * FROM peliculas WHERE codigo = ?", ("MTX",))
print("La de código MTX:", cursor.fetchone())
# Muestra: La de código MTX: (3, 'Matrix', 1999, 136, 'MTX', None)
cursor.execute("SELECT * FROM peliculas WHERE codigo = ?", ("NOEXISTE",))
print("Una que no existe:", cursor.fetchone())
# Muestra: Una que no existe: None

# Pasar de "lista de tuplas" a "lista de textos": con una comprensión de
# lista (paso 0, PARTE 8). fila[0] es el primer valor de cada tupla.
cursor.execute("SELECT titulo FROM peliculas ORDER BY titulo")
filas = cursor.fetchall()
print(filas)
# Muestra: [('Matrix',), ('Shrek',), ('Toy Story',), ('Toy Story 2',), ('Volver al futuro',)]
print([fila[0] for fila in filas])
# Muestra: ['Matrix', 'Shrek', 'Toy Story', 'Toy Story 2', 'Volver al futuro']

# Buscar por PARTE de un texto: LIKE, con % que quiere decir "cualquier cosa".
#   LIKE '%toy%'  -> que tenga "toy" en cualquier lugar
#   LIKE 'toy%'   -> que EMPIECE con "toy"
# En SQLite, LIKE no distingue mayúsculas ("toy" encuentra "Toy"). (En
# PostgreSQL sí distingue: ahí se usa ILIKE.) OJO: los % se pegan al VALOR,
# no al texto SQL, así el ? sigue protegiéndote.
buscado = "toy"
cursor.execute("SELECT titulo FROM peliculas WHERE titulo LIKE ?", (f"%{buscado}%",))
print("Las que dicen 'toy':", [fila[0] for fila in cursor.fetchall()])
# Muestra: Las que dicen 'toy': ['Toy Story', 'Toy Story 2']

# La base también puede hacer CUENTAS (acá: pasar minutos a horas)
cursor.execute("SELECT titulo, minutos / 60.0 FROM peliculas WHERE minutos > 100")
print("En horas:", [(titulo, round(horas, 1)) for titulo, horas in cursor.fetchall()])
# Muestra: En horas: [('Volver al futuro', 1.9), ('Matrix', 2.3)]

# OJO, TRAMPA: en SQL, un número ENTERO dividido otro ENTERO da un ENTERO
# (tira los decimales). En Python 7 / 2 da 3.5, pero en SQL da 3.
# Para que dé con decimales, escribí uno de los dos con punto: 7 / 2.0
cursor.execute("SELECT 7 / 2, 7 / 2.0, 10 / 100, 10 / 100.0")
print("Divisiones en SQL:", cursor.fetchone())
# Muestra: Divisiones en SQL: (3, 3.5, 0, 0.1)      <- ¡10 / 100 da 0! (útil para porcentajes)

# Contar, sumar y promediar ("funciones de agregación"): dan UN resultado
# para todas las filas.
#   COUNT(*)  cuántas filas     SUM(col)  la suma     AVG(col)  el promedio
#   MIN(col)  el menor          MAX(col)  el mayor
cursor.execute("SELECT COUNT(*), SUM(minutos), AVG(minutos) FROM peliculas")
cantidad, total, promedio = cursor.fetchone()
print(f"Hay {cantidad} películas, {total} minutos en total, {promedio} de promedio.")
# Muestra: Hay 5 películas, 515 minutos en total, 103.0 de promedio.

# LIMIT: solo las primeras N
cursor.execute("SELECT titulo FROM peliculas ORDER BY minutos DESC LIMIT 2")
print("Las 2 más largas:", [fila[0] for fila in cursor.fetchall()])
# Muestra: Las 2 más largas: ['Matrix', 'Volver al futuro']

# PROBÁ VOS: traé las películas de menos de 100 minutos, ordenadas por título.


# =======================================================================
# PARTE 8 — EDITAR (UPDATE)
# =======================================================================
# UPDATE tabla SET columna = valor WHERE condición
# "En esta tabla, poné este valor en esta columna, en las filas que cumplan esto."
#
# ¡SIEMPRE con WHERE! Un UPDATE sin WHERE cambia TODAS las filas de la tabla.
#
# cursor.rowcount dice CUÁNTAS filas tocó el último UPDATE o DELETE.
# Si da 0, es que ninguna fila cumplía la condición.

print()
print("========== PARTE 8: editar (UPDATE) ==========")
cursor.execute("UPDATE peliculas SET minutos = ? WHERE codigo = ?", (88, "SHR"))
print("Filas cambiadas:", cursor.rowcount)
# Muestra: Filas cambiadas: 1
conexion.commit()
cursor.execute("SELECT titulo, minutos FROM peliculas WHERE codigo = 'SHR'")
print("Shrek ahora:", cursor.fetchone())
# Muestra: Shrek ahora: ('Shrek', 88)

# Usar el valor que YA tiene la columna: "sumale 5 a lo que haya", sin leerlo
# antes. La cuenta la hace la base.
cursor.execute("UPDATE peliculas SET minutos = minutos + 5 WHERE anio < 1990")
# IS NULL quiere decir "está vacío" (OJO: no se escribe "= NULL", no funciona)
cursor.execute("UPDATE peliculas SET puntaje = 8.5 WHERE puntaje IS NULL")
conexion.commit()
cursor.execute("SELECT titulo, minutos, puntaje FROM peliculas WHERE anio < 1990")
print("Las de antes de 1990:", cursor.fetchall())
# Muestra: Las de antes de 1990: [('Volver al futuro', 121, 8.5)]     <- tenía 116, ahora 121

# Se puede condicionar el cambio, y mirar rowcount para saber si se hizo:
# "restale 200 minutos a Matrix, SOLO SI tiene 200 o más".
cursor.execute("UPDATE peliculas SET minutos = minutos - 200 WHERE codigo = 'MTX' AND minutos >= 200")
print("¿Se pudo restar?", cursor.rowcount == 1)
# Muestra: ¿Se pudo restar? False      <- Matrix tiene 136: la condición no se cumplió y no cambió nada

# Las REGLAS de la tabla te protegen: CHECK (minutos >= 0) no deja poner un negativo.
# Cuando una regla se rompe, sqlite3 da un error IntegrityError, que se ataja
# con try/except (paso 0, PARTE 11).
try:
    cursor.execute("UPDATE peliculas SET minutos = -10 WHERE codigo = 'SHR'")
except sqlite3.IntegrityError as error:
    print("CHECK no dejó poner minutos negativos:", error)
# Muestra: CHECK no dejó poner minutos negativos: CHECK constraint failed: minutos >= 0


# =======================================================================
# PARTE 9 — BORRAR (DELETE)
# =======================================================================
# DELETE FROM tabla WHERE condición
# ¡SIEMPRE con WHERE! "DELETE FROM peliculas" sin WHERE vacía la tabla entera.

print()
print("========== PARTE 9: borrar (DELETE) ==========")
cursor.execute("DELETE FROM peliculas WHERE codigo = ?", ("TS2",))
print("Filas borradas:", cursor.rowcount)
# Muestra: Filas borradas: 1
conexion.commit()
cursor.execute("SELECT COUNT(*) FROM peliculas")
print("Quedan:", cursor.fetchone()[0])
# Muestra: Quedan: 4         <- fetchone() da la tupla (4,), y [0] saca el 4

# Más reglas que protegen: UNIQUE no deja repetir el código...
try:
    cursor.execute("INSERT INTO peliculas (titulo, codigo) VALUES (?, ?)", ("Otra Matrix", "MTX"))
except sqlite3.IntegrityError as error:
    print("No dejó repetir el código:", error)
# Muestra: No dejó repetir el código: UNIQUE constraint failed: peliculas.codigo

# ...y NOT NULL no deja guardar sin título.
try:
    cursor.execute("INSERT INTO peliculas (anio) VALUES (?)", (2020,))
except sqlite3.IntegrityError as error:
    print("No dejó guardar sin título:", error)
# Muestra: No dejó guardar sin título: NOT NULL constraint failed: peliculas.titulo


# El mensaje de sqlite ("UNIQUE constraint failed...") está en inglés y es
# técnico. Una costumbre muy común: ATAJAR el error de la base y PROVOCAR
# uno propio, con un mensaje que entienda cualquiera:
def guardar_pelicula(titulo, codigo):
    try:
        cursor.execute("INSERT INTO peliculas (titulo, codigo) VALUES (?, ?)", (titulo, codigo))
    except sqlite3.IntegrityError:
        raise ValueError(f"Ya hay una película con el código {codigo}.")
    conexion.commit()
    return cursor.lastrowid


try:
    guardar_pelicula("Matrix 2", "MTX")
except ValueError as error:
    print("Error entendible:", error)
# Muestra: Error entendible: Ya hay una película con el código MTX.


# =======================================================================
# PARTE 10 — RELACIONAR TABLAS (FOREIGN KEY y JOIN)
# =======================================================================
# Cada película tiene UNA categoría, y cada categoría tiene MUCHAS películas.
# Eso se llama una relación "uno a muchos".
#
# En vez de escribir el nombre de la categoría en cada película, se hace una
# tabla de categorías, y cada película guarda el ID de su categoría. Esa
# columna se llama CLAVE FORÁNEA (foreign key): "un id de OTRA tabla".
#
#   categorias              peliculas
#   ┌────┬──────────┐       ┌────┬────────────┬──────────────┐
#   │ id │ nombre   │       │ id │ titulo     │ categoria_id │
#   ├────┼──────────┤       ├────┼────────────┼──────────────┤
#   │ 1  │ Infantil │ <──── │ 2  │ Toy Story  │ 1            │
#   │ 2  │ Acción   │ <──── │ 3  │ Matrix     │ 2            │
#   │ 3  │ Terror   │       └────┴────────────┴──────────────┘
#   └────┴──────────┘       (Terror todavía no tiene películas)
#
# Ventaja: si "Infantil" pasa a llamarse "Para chicos", se cambia en UN lugar.

print()
print("========== PARTE 10: relaciones (FOREIGN KEY y JOIN) ==========")
cursor.execute("""
    CREATE TABLE categorias (
        id     INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    )
""")
# ALTER TABLE = cambiarle algo a una tabla que ya existe (acá: agregar una columna).
# REFERENCES categorias(id) = "este número tiene que ser un id que exista en categorias".
cursor.execute("ALTER TABLE peliculas ADD COLUMN categoria_id INTEGER REFERENCES categorias(id)")
cursor.executemany("INSERT INTO categorias (nombre) VALUES (?)", [("Infantil",), ("Acción",), ("Terror",)])
cursor.execute("UPDATE peliculas SET categoria_id = 1 WHERE codigo IN ('TS1', 'SHR')")   # IN = "alguno de estos"
cursor.execute("UPDATE peliculas SET categoria_id = 2 WHERE codigo IN ('MTX', 'VAF')")
conexion.commit()

# JOIN: juntar las dos tablas siguiendo la relación, para poder leer el
# NOMBRE de la categoría de cada película. Se lee:
#   "de peliculas, unida con categorias donde el id de la categoría
#    es igual al categoria_id de la película"
# Como hay dos tablas, cada columna se escribe con su tabla: peliculas.titulo
cursor.execute("""
    SELECT peliculas.titulo, categorias.nombre
    FROM peliculas
    JOIN categorias ON categorias.id = peliculas.categoria_id
    ORDER BY categorias.nombre, peliculas.titulo
""")
for titulo, categoria in cursor.fetchall():
    print(" ", titulo, "->", categoria)
# Muestra:
#   Matrix -> Acción
#   Volver al futuro -> Acción
#   Shrek -> Infantil
#   Toy Story -> Infantil

# GROUP BY: hacer un COUNT (o SUM...) POR CADA grupo, en vez de uno para todo.
# Con JOIN común, una categoría SIN películas no aparece (no tiene con quién juntarse):
cursor.execute("""
    SELECT categorias.nombre, COUNT(peliculas.id)
    FROM categorias
    JOIN peliculas ON peliculas.categoria_id = categorias.id
    GROUP BY categorias.id
""")
print("Con JOIN:", cursor.fetchall())
# Muestra: Con JOIN: [('Infantil', 2), ('Acción', 2)]       <- falta Terror

# LEFT JOIN: trae TODAS las filas de la tabla de la izquierda (categorias),
# aunque no tengan nada relacionado.
cursor.execute("""
    SELECT categorias.nombre, COUNT(peliculas.id)
    FROM categorias
    LEFT JOIN peliculas ON peliculas.categoria_id = categorias.id
    GROUP BY categorias.id
""")
print("Con LEFT JOIN:", cursor.fetchall())
# Muestra: Con LEFT JOIN: [('Infantil', 2), ('Acción', 2), ('Terror', 0)]

# Con SUM pasa algo: la suma de "nada" da NULL (None), no 0.
# COALESCE(algo, 0) quiere decir "algo, o 0 si está vacío".
cursor.execute("""
    SELECT categorias.nombre, SUM(peliculas.minutos), COALESCE(SUM(peliculas.minutos), 0)
    FROM categorias
    LEFT JOIN peliculas ON peliculas.categoria_id = categorias.id
    GROUP BY categorias.id
""")
print("Minutos (sin y con COALESCE):", cursor.fetchall())
# Muestra: Minutos (sin y con COALESCE): [('Infantil', 169, 169), ('Acción', 257, 257), ('Terror', None, 0)]

# La clave foránea protege: no deja apuntar a una categoría que no existe.
try:
    cursor.execute("UPDATE peliculas SET categoria_id = 99 WHERE codigo = 'MTX'")
except sqlite3.IntegrityError as error:
    print("No dejó usar una categoría inexistente:", error)
# Muestra: No dejó usar una categoría inexistente: FOREIGN KEY constraint failed


# =======================================================================
# PARTE 11 — TRANSACCIONES: TODO O NADA
# =======================================================================
# A veces varios cambios van JUNTOS. Ejemplo: pasar plata de una cuenta a
# otra es "restar en una" y "sumar en la otra". Si el programa se corta en
# el medio, la plata desaparecería. La regla: o se hacen TODOS, o NINGUNO.
#
#   commit()    confirma todos los cambios desde el último commit
#   rollback()  DESHACE todos los cambios desde el último commit

print()
print("========== PARTE 11: transacciones (commit / rollback) ==========")
try:
    cursor.execute("UPDATE peliculas SET minutos = 0")         # cambio 1 (¡sin WHERE: todas!)
    raise RuntimeError("se cortó la luz a la mitad")           # simulamos que algo falla
except RuntimeError as error:
    conexion.rollback()                                        # se deshace el cambio 1
    print("Hubo un error:", error, "-> rollback, no quedó nada a medias.")
# Muestra: Hubo un error: se cortó la luz a la mitad -> rollback, no quedó nada a medias.
cursor.execute("SELECT SUM(minutos) FROM peliculas")
print("Los minutos siguen intactos:", cursor.fetchone()[0])
# Muestra: Los minutos siguen intactos: 426

# Forma cómoda: "with conexion:" hace commit() solo si todo lo de adentro
# sale bien, y rollback() solo si algo da error (y el error sigue de largo,
# para que lo atajes vos).
try:
    with conexion:
        conexion.execute("INSERT INTO peliculas (titulo, codigo) VALUES (?, ?)", ("Up", "UP1"))
        conexion.execute("INSERT INTO peliculas (titulo, codigo) VALUES (?, ?)", ("Coco", "MTX"))   # código repetido: falla
except sqlite3.IntegrityError:
    print("Falló la segunda: tampoco quedó guardada la primera.")
# Muestra: Falló la segunda: tampoco quedó guardada la primera.
cursor.execute("SELECT COUNT(*) FROM peliculas WHERE titulo = 'Up'")
print("¿Quedó 'Up'?", cursor.fetchone()[0] == 1)
# Muestra: ¿Quedó 'Up'? False

conexion.close()     # al terminar, se cierra la conexión ("cortar la llamada")


# =======================================================================
# PARTE 12 — LO MISMO CON POSTGRESQL (solo para leer)
# =======================================================================
# 1. Instalar PostgreSQL (postgresql.org) y crear una base, por ejemplo con
#    DBeaver o pgAdmin: botón derecho → Crear base de datos → "practica".
# 2. Con el entorno activado:   pip install "psycopg[binary]"
# 3. El código es CASI igual. Las diferencias:
#      - los valores van con %s en vez de ?
#      - el id automático se escribe:   id SERIAL PRIMARY KEY
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
# En Django NI SIQUIERA eso cambia: escribís el mismo código para las dos.


# =======================================================================
# RESUMEN (para tener a mano mientras hacés el ejercicio)
# =======================================================================
#  conexion = sqlite3.connect(":memory:")       conectarse
#  conexion.execute("PRAGMA foreign_keys = ON") prender el control de relaciones
#  CREATE TABLE t (col TIPO reglas, ...)        crear una tabla
#  INSERT INTO t (a, b) VALUES (?, ?)           guardar      -> cursor.lastrowid = el id nuevo
#  SELECT a, b FROM t WHERE ... ORDER BY ...    buscar       -> fetchall() / fetchone()
#  UPDATE t SET a = ? WHERE ...                 editar  ¡con WHERE!  -> cursor.rowcount
#  DELETE FROM t WHERE ...                      borrar  ¡con WHERE!  -> cursor.rowcount
#  LIKE ?  con  f"%{texto}%"                    buscar parte de un texto
#  JOIN otra ON otra.id = t.otra_id             leer de dos tablas relacionadas
#  LEFT JOIN                                    ...incluyendo las que no tienen nada relacionado
#  COUNT / SUM / AVG  +  GROUP BY               contar y sumar por grupo
#  COALESCE(SUM(...), 0)                        0 en vez de vacío
#  commit() confirma, rollback() deshace, "with conexion:" hace las dos solo
#  sqlite3.IntegrityError                       el error cuando se rompe una regla
#  ¡Siempre ? para los valores, nunca f-strings en el SQL!

print()
print("Fin de la clase 1. Ahora abrí ejercicio.md (está en esta misma carpeta).")
