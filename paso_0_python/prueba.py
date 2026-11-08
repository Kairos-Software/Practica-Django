"""
Prueba automática del paso 0.
    python prueba.py              -> prueba tu mi_solucion.py
    python prueba.py solucion     -> prueba la solución (para comparar)
"""

import importlib
import sys
import unittest

NOMBRE = sys.argv[1] if len(sys.argv) > 1 else "mi_solucion"
try:
    m = importlib.import_module(NOMBRE)
except ModuleNotFoundError:
    sys.exit(f"No encontré {NOMBRE}.py en esta carpeta. Crealo y volvé a probar.")

PRODUCTOS = [
    {"nombre": "Alfajor", "precio": 1200, "categoria": "golosinas"},
    {"nombre": "Coca Cola 500", "precio": 1800, "categoria": "bebidas"},
    {"nombre": "Chicle", "precio": 300, "categoria": "golosinas"},
    {"nombre": "Alfajor triple", "precio": 1900, "categoria": "golosinas"},
]


def funcion(nombre):
    if not hasattr(m, nombre):
        raise AssertionError(f"Falta la función o clase '{nombre}' en {NOMBRE}.py")
    return getattr(m, nombre)


class Paso0(unittest.TestCase):

    def test_1_precio_con_descuento(self):
        """1. precio_con_descuento"""
        f = funcion("precio_con_descuento")
        self.assertEqual(f(1000, 15), 850)
        self.assertEqual(f(999, 10), 899.1)
        self.assertEqual(f(500, 0), 500)
        for malo in (-5, 120):
            with self.assertRaises(ValueError, msg=f"con porcentaje {malo} tiene que dar ValueError"):
                f(1000, malo)

    def test_2_es_mayor_de_edad(self):
        """2. es_mayor_de_edad"""
        f = funcion("es_mayor_de_edad")
        self.assertIs(f(18), True)
        self.assertIs(f(40), True)
        self.assertIs(f(17), False)

    def test_3_total_carrito(self):
        """3. total_carrito"""
        f = funcion("total_carrito")
        carrito = [{"producto": "Alfajor", "precio": 1200, "cantidad": 3},
                   {"producto": "Chicle", "precio": 300, "cantidad": 1}]
        self.assertEqual(f(carrito), 3900)
        self.assertEqual(f([]), 0)

    def test_4_productos_baratos(self):
        """4. productos_baratos"""
        f = funcion("productos_baratos")
        self.assertEqual(f(PRODUCTOS, 1850), ["Chicle", "Alfajor", "Coca Cola 500"])
        self.assertEqual(f(PRODUCTOS, 100), [])
        self.assertEqual(f(PRODUCTOS, 1200), ["Chicle"], "'menos que' el tope: el de 1200 no entra")

    def test_5_buscar_producto(self):
        """5. buscar_producto"""
        f = funcion("buscar_producto")
        self.assertEqual([p["nombre"] for p in f(PRODUCTOS, "  ALFA ")], ["Alfajor", "Alfajor triple"])
        self.assertEqual(f(PRODUCTOS, "helado"), [])

    def test_6_contar_por_categoria(self):
        """6. contar_por_categoria"""
        self.assertEqual(funcion("contar_por_categoria")(PRODUCTOS), {"golosinas": 3, "bebidas": 1})

    def test_7_texto_a_cantidad(self):
        """7. texto_a_cantidad"""
        f = funcion("texto_a_cantidad")
        self.assertEqual(f(" 3 "), 3)
        self.assertEqual(f("12"), 12)
        for malo in ("tres", "0", "-2", "", "2.5"):
            with self.assertRaises(ValueError, msg=f"'{malo}' tiene que dar ValueError"):
                f(malo)

    def test_8_caja(self):
        """8. Caja"""
        caja = funcion("Caja")("Marcos")
        self.assertEqual((caja.saldo, caja.ventas), (0, []))
        caja.vender("Alfajor", 1200, 3)
        self.assertEqual(caja.saldo, 3600)
        self.assertEqual(caja.ventas, [{"producto": "Alfajor", "precio": 1200, "cantidad": 3}])
        self.assertEqual(str(caja), "Caja de Marcos: $3600")
        with self.assertRaises(ValueError):
            caja.vender("Chicle", 300, 0)
        self.assertEqual((caja.saldo, caja.cantidad_de_ventas()), (3600, 1), "una venta mal no cambia nada")
        caja.retirar(600)
        self.assertEqual(caja.saldo, 3000)
        with self.assertRaises(ValueError):
            caja.retirar(5000)
        self.assertEqual(caja.saldo, 3000, "un retiro que no alcanza no cambia nada")

    def test_9_caja_con_recargo(self):
        """9. CajaConRecargo (hereda de Caja)"""
        Caja, ConRecargo = funcion("Caja"), funcion("CajaConRecargo")
        self.assertTrue(issubclass(ConRecargo, Caja), "CajaConRecargo tiene que heredar de Caja")
        caja = ConRecargo("Ana")
        caja.vender("Gaseosa", 1000)
        self.assertEqual(caja.saldo, 1100)
        self.assertEqual(caja.cantidad_de_ventas(), 1)


if __name__ == "__main__":
    print(f"Probando {NOMBRE}.py ...\n")
    resultado = unittest.main(argv=[sys.argv[0]], verbosity=2, exit=False).result
    if resultado.wasSuccessful():
        print("\n✔ ¡Todo bien! Paso 0 aprobado.")
    else:
        print("\n✘ Hay puntos para revisar: mirá los FAIL/ERROR de arriba.")
