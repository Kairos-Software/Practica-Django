"""Solución del paso 0 — El Kiosquito. (Es UNA forma de hacerlo.)"""


def precio_con_descuento(precio, porcentaje):
    if porcentaje < 0 or porcentaje > 100:
        raise ValueError("El porcentaje tiene que estar entre 0 y 100.")
    return round(precio - precio * porcentaje / 100, 2)


def es_mayor_de_edad(edad):
    return edad >= 18


def total_carrito(carrito):
    total = 0
    for item in carrito:
        total += item["precio"] * item["cantidad"]
    return total


def productos_baratos(productos, tope):
    baratos = [p for p in productos if p["precio"] < tope]
    baratos.sort(key=lambda p: p["precio"])     # ordenar por el precio
    return [p["nombre"] for p in baratos]


def buscar_producto(productos, texto):
    texto = texto.strip().lower()
    return [p for p in productos if texto in p["nombre"].lower()]


def contar_por_categoria(productos):
    cuantos = {}
    for p in productos:
        cuantos[p["categoria"]] = cuantos.get(p["categoria"], 0) + 1
    return cuantos


def texto_a_cantidad(texto):
    texto = texto.strip()
    if not texto.isdigit():       # isdigit: solo dígitos (sin signo, sin coma, sin letras)
        raise ValueError(f"'{texto}' no es una cantidad válida.")
    cantidad = int(texto)
    if cantidad < 1:
        raise ValueError("La cantidad tiene que ser mayor que 0.")
    return cantidad


class Caja:
    def __init__(self, cajero):
        self.cajero = cajero
        self.saldo = 0
        self.ventas = []

    def importe(self, precio, cantidad):
        """Cuánto suma una venta (CajaConRecargo lo cambia)."""
        return precio * cantidad

    def vender(self, producto, precio, cantidad=1):
        if cantidad < 1:
            raise ValueError("La cantidad tiene que ser al menos 1.")
        self.saldo += self.importe(precio, cantidad)
        self.ventas.append({"producto": producto, "precio": precio, "cantidad": cantidad})

    def retirar(self, monto):
        if monto > self.saldo:
            raise ValueError(f"No alcanza: hay ${self.saldo}.")
        self.saldo -= monto

    def cantidad_de_ventas(self):
        return len(self.ventas)

    def __str__(self):
        return f"Caja de {self.cajero}: ${self.saldo}"


class CajaConRecargo(Caja):
    def importe(self, precio, cantidad):
        return super().importe(precio, cantidad) * 1.10


if __name__ == "__main__":
    caja = Caja("Marcos")
    caja.vender("Alfajor", 1200, 3)
    print(caja)
