"""
Prueba automática del paso 1.
    python prueba.py              -> prueba tu mi_solucion.py
    python prueba.py solucion     -> prueba la solución (para comparar)
"""

import importlib
import sqlite3
import sys
import unittest

NOMBRE = sys.argv[1] if len(sys.argv) > 1 else "mi_solucion"
try:
    m = importlib.import_module(NOMBRE)
except ModuleNotFoundError:
    sys.exit(f"No encontré {NOMBRE}.py en esta carpeta. Crealo y volvé a probar.")


def f(nombre):
    if not hasattr(m, nombre):
        raise AssertionError(f"Falta la función '{nombre}' en {NOMBRE}.py")
    return getattr(m, nombre)


class Paso1(unittest.TestCase):

    def setUp(self):
        # Una base nueva y vacía (en memoria) para cada prueba
        self.con = sqlite3.connect(":memory:")
        self.con.execute("PRAGMA foreign_keys = ON")
        f("crear_tablas")(self.con)

    def tearDown(self):
        self.con.close()

    def cargar(self):
        agregar_autor, agregar_libro = f("agregar_autor"), f("agregar_libro")
        self.borges = agregar_autor(self.con, "Borges")
        self.cortazar = agregar_autor(self.con, "Cortázar")
        self.quino = agregar_autor(self.con, "Quino")
        self.ficciones = agregar_libro(self.con, "Ficciones", 15000, 4, self.borges)
        agregar_libro(self.con, "El Aleph", 14000, 0, self.borges)
        agregar_libro(self.con, "Rayuela", 20000, 3, self.cortazar)
        agregar_libro(self.con, "Bestiario", 12000, 5, self.cortazar)

    def columnas(self, tabla):
        return {fila[1] for fila in self.con.execute(f"PRAGMA table_info({tabla})")}

    def test_01_crear_tablas(self):
        """1. crear_tablas: autores y libros con sus columnas"""
        self.assertEqual(self.columnas("autores"), {"id", "nombre"})
        self.assertEqual(self.columnas("libros"), {"id", "titulo", "precio", "stock", "autor_id"})

    def test_02_agregar_autor(self):
        """2. agregar_autor: devuelve el id y no deja repetir"""
        primero = f("agregar_autor")(self.con, "Borges")
        segundo = f("agregar_autor")(self.con, "Quino")
        self.assertIsInstance(primero, int)
        self.assertNotEqual(primero, segundo)
        with self.assertRaises(ValueError, msg="un autor repetido tiene que dar ValueError (no sqlite3.IntegrityError)"):
            f("agregar_autor")(self.con, "Borges")

    def test_03_agregar_libro_y_reglas(self):
        """3. agregar_libro: devuelve el id; stock por defecto 0; precio no negativo; autor existente"""
        autor = f("agregar_autor")(self.con, "Borges")
        libro = f("agregar_libro")(self.con, "Ficciones", 15000, 4, autor)
        self.assertEqual(self.con.execute("SELECT titulo, stock FROM libros WHERE id = ?", (libro,)).fetchone(),
                         ("Ficciones", 4))
        self.con.execute("INSERT INTO libros (titulo, precio, autor_id) VALUES ('Sin stock', 1, ?)", (autor,))
        self.assertEqual(self.con.execute("SELECT stock FROM libros WHERE titulo = 'Sin stock'").fetchone(), (0,))
        with self.assertRaises(sqlite3.IntegrityError, msg="la tabla tiene que rechazar un precio negativo (CHECK)"):
            self.con.execute("INSERT INTO libros (titulo, precio, autor_id) VALUES ('X', -1, ?)", (autor,))
        with self.assertRaises(sqlite3.IntegrityError, msg="autor_id tiene que ser un autor que exista (REFERENCES)"):
            self.con.execute("INSERT INTO libros (titulo, precio, autor_id) VALUES ('X', 1, 999)")

    def test_04_libros_con_autor(self):
        """4. libros_con_autor"""
        self.cargar()
        self.assertEqual(f("libros_con_autor")(self.con), [
            ("Bestiario", "Cortázar"), ("El Aleph", "Borges"), ("Ficciones", "Borges"), ("Rayuela", "Cortázar")])

    def test_05_libros_sin_stock(self):
        """5. libros_sin_stock"""
        self.cargar()
        self.assertEqual(f("libros_sin_stock")(self.con), ["El Aleph"])

    def test_06_libros_mas_baratos_que(self):
        """6. libros_mas_baratos_que"""
        self.cargar()
        self.assertEqual([(t, float(p)) for t, p in f("libros_mas_baratos_que")(self.con, 15000)],
                         [("Bestiario", 12000.0), ("El Aleph", 14000.0)])

    def test_07_buscar_libros_seguro(self):
        """7. buscar_libros (y que no se pueda hacer inyección SQL)"""
        self.cargar()
        self.assertEqual(f("buscar_libros")(self.con, "AL"), ["El Aleph"])
        self.assertEqual(f("buscar_libros")(self.con, "ray"), ["Rayuela"])
        f("buscar_libros")(self.con, "x'; DROP TABLE libros; --")
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM libros").fetchone(), (4,), "¡se borró la tabla!")

    def test_08_resumen_por_autor(self):
        """8. resumen_por_autor (también autores sin libros)"""
        self.cargar()
        self.assertEqual([(n, c, float(v)) for n, c, v in f("resumen_por_autor")(self.con)], [
            ("Borges", 2, 60000.0), ("Cortázar", 2, 120000.0), ("Quino", 0, 0.0)])

    def test_09_vender(self):
        """9. vender: resta, y si no alcanza no cambia nada"""
        self.cargar()
        f("vender")(self.con, self.ficciones, 3)
        self.assertEqual(self.con.execute("SELECT stock FROM libros WHERE id = ?", (self.ficciones,)).fetchone(), (1,))
        with self.assertRaises(ValueError):
            f("vender")(self.con, self.ficciones, 5)
        self.assertEqual(self.con.execute("SELECT stock FROM libros WHERE id = ?", (self.ficciones,)).fetchone(), (1,))

    def test_10_subir_precios_de_autor(self):
        """10. subir_precios_de_autor"""
        self.cargar()
        self.assertEqual(f("subir_precios_de_autor")(self.con, self.cortazar, 10), 2)
        precios = [round(p) for (p,) in self.con.execute(
            "SELECT precio FROM libros WHERE autor_id = ? ORDER BY titulo", (self.cortazar,))]
        self.assertEqual(precios, [13200, 22000])

    def test_11_borrar_sin_stock(self):
        """11. borrar_sin_stock"""
        self.cargar()
        self.assertEqual(f("borrar_sin_stock")(self.con), 1)
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM libros").fetchone(), (3,))

    def test_12_transaccion(self):
        """12. agregar_libros_juntos: todos o ninguno"""
        autor = f("agregar_autor")(self.con, "Quino")
        f("agregar_libros_juntos")(self.con, [("Mafalda 1", 8000, 2, autor), ("Mafalda 2", 8000, 1, autor)])
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM libros").fetchone(), (2,))
        with self.assertRaises(ValueError):
            f("agregar_libros_juntos")(self.con, [("Mafalda 3", 8000, 1, autor), ("Mal", -50, 1, autor)])
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM libros").fetchone(), (2,),
                         "si uno falla, no tiene que quedar guardado ninguno")


if __name__ == "__main__":
    print(f"Probando {NOMBRE}.py ...\n")
    resultado = unittest.main(argv=[sys.argv[0]], verbosity=2, exit=False).result
    print("\n✔ ¡Todo bien! Paso 1 aprobado." if resultado.wasSuccessful()
          else "\n✘ Hay puntos para revisar: mirá los FAIL/ERROR de arriba.")
