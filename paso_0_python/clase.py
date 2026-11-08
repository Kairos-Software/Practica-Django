"""
═══════════════════════════════════════════════════════════════════════
 PASO 0 — PYTHON: LO MÍNIMO PARA DJANGO
═══════════════════════════════════════════════════════════════════════

Ejecutalo:   python clase_python.py
(No necesita nada instalado: solo Python.)

Django ES Python. Todo lo que vas a escribir (modelos, vistas, formularios)
son variables, funciones y clases como las de acá. Si esto se entiende,
Django se entiende.

El ejemplo de la clase: un pequeño negocio de PIZZAS.
"""

# ═══════════════════════════════════════════════════════════════════════
# 1) VARIABLES Y TIPOS
# ═══════════════════════════════════════════════════════════════════════
# Una variable es un nombre para un valor. Python adivina el tipo solo.
nombre = "Muzzarella"        # str   = texto (entre comillas)
precio = 9500                # int   = número entero
precio_con_iva = 11495.0     # float = número con decimales
hay_stock = True             # bool  = verdadero (True) o falso (False)
descuento = None             # None  = "nada", "vacío", "sin dato"

print("1) Variables")
print(nombre, precio, precio_con_iva, hay_stock, descuento)
print(type(nombre), type(precio))        # type() dice el tipo

# Texto: f-strings para meter variables adentro (la f antes de las comillas)
print(f"La pizza {nombre} sale ${precio}")
print(f"En mayúsculas: {nombre.upper()} · largo: {len(nombre)} letras")
print("Sin espacios:", "  hola  ".strip())     # strip() saca espacios de los costados

# Cuentas
print("Suma:", 2 + 3, "· resta:", 10 - 4, "· por:", 3 * 4, "· dividido:", 7 / 2)
print("División entera:", 7 // 2, "· resto:", 7 % 2, "· potencia:", 2 ** 3)

# Convertir entre tipos (MUY común: lo que llega de un formulario web es SIEMPRE texto)
cantidad_texto = "3"
cantidad = int(cantidad_texto)                # "3" -> 3
print("Texto a número y cuenta:", cantidad * precio)
print("Número a texto:", str(precio) + " pesos")


# ═══════════════════════════════════════════════════════════════════════
# 2) DECIDIR: if / elif / else
# ═══════════════════════════════════════════════════════════════════════
# OJO con la SANGRÍA (los espacios al principio): en Python marca qué
# código está "adentro" del if. Siempre 4 espacios.
print("\n2) Decisiones")
total = 25000
if total >= 30000:
    print("Envío gratis")
elif total >= 20000:                          # "si no, si..."
    print("Envío con 50% de descuento")
else:                                         # "si no"
    print("Envío normal")

# Comparar:  ==  (igual)   !=  (distinto)   <  >  <=  >=
# Combinar:  and (las dos)   or (alguna)   not (lo contrario)
es_socio = True
if total > 20000 and es_socio:
    print("Socio con compra grande: 10% off")
if not hay_stock:
    print("No hay stock")                     # no se imprime: hay_stock es True

# Lo "vacío" cuenta como falso: "", 0, None, [], {}
comentario = ""
if not comentario:
    print("El cliente no dejó comentario")


# ═══════════════════════════════════════════════════════════════════════
# 3) LISTAS: varias cosas en orden
# ═══════════════════════════════════════════════════════════════════════
print("\n3) Listas")
gustos = ["Muzzarella", "Napolitana", "Fugazzeta"]
print(gustos, "· hay", len(gustos))
print("La primera:", gustos[0], "· la última:", gustos[-1])   # se cuenta desde 0
gustos.append("Calabresa")                    # agregar al final
gustos.remove("Napolitana")                   # sacar
print("Después de agregar y sacar:", gustos)
print("¿Hay Fugazzeta?", "Fugazzeta" in gustos)
print("Ordenada:", sorted(gustos))
print("Las 2 primeras:", gustos[:2])          # "rebanadas": [desde:hasta]


# ═══════════════════════════════════════════════════════════════════════
# 4) DICCIONARIOS: datos con nombre (clave -> valor)
# ═══════════════════════════════════════════════════════════════════════
# Es como una ficha. En Django los vas a ver TODO el tiempo (el "contexto"
# que se manda a un template es un diccionario).
print("\n4) Diccionarios")
pizza = {"nombre": "Muzzarella", "precio": 9500, "porciones": 8}
print(pizza["nombre"], "cuesta", pizza["precio"])
pizza["precio"] = 9800                        # cambiar
pizza["vegetariana"] = True                   # agregar una clave nueva
print(pizza)
print("¿Tiene 'picante'?", pizza.get("picante", "no dice"))   # get: sin error si no existe
for clave, valor in pizza.items():            # recorrer clave y valor
    print(f"  {clave}: {valor}")

# Una lista de diccionarios = una "tabla" en memoria
menu = [
    {"nombre": "Muzzarella", "precio": 9800},
    {"nombre": "Napolitana", "precio": 11000},
    {"nombre": "Fugazzeta", "precio": 12000},
]


# ═══════════════════════════════════════════════════════════════════════
# 5) REPETIR: for y while
# ═══════════════════════════════════════════════════════════════════════
print("\n5) Repetir")
for item in menu:                             # "para cada item del menú..."
    print(f"  {item['nombre']}: ${item['precio']}")

for numero in range(1, 4):                    # range(1, 4) = 1, 2, 3
    print("  Pizza número", numero)

for posicion, item in enumerate(menu, start=1):   # con su número de orden
    print(f"  {posicion}. {item['nombre']}")

# Juntar, filtrar y sumar mientras se recorre
caras = []
for item in menu:
    if item["precio"] > 10000:
        caras.append(item["nombre"])
print("Las de más de $10.000:", caras)

# Lo mismo en una línea ("comprensión de lista"): muy usado
print("Igual, en una línea:", [item["nombre"] for item in menu if item["precio"] > 10000])
print("Suma de todos los precios:", sum(item["precio"] for item in menu))

# while: repetir MIENTRAS se cumpla algo
porciones = 8
while porciones > 5:
    porciones -= 1                            # es lo mismo que: porciones = porciones - 1
print("Quedan", porciones, "porciones")


# ═══════════════════════════════════════════════════════════════════════
# 6) FUNCIONES: un pedazo de código con nombre, que se reusa
# ═══════════════════════════════════════════════════════════════════════
# Recibe datos (parámetros), hace algo y DEVUELVE un resultado (return).
# En Django cada página es una función (una "vista").
print("\n6) Funciones")


def precio_final(precio, cantidad=1, descuento=0):
    """Lo que hay que cobrar. (Este texto entre comillas triples explica la función.)"""
    subtotal = precio * cantidad
    return subtotal - subtotal * descuento / 100


print("1 pizza:", precio_final(9800))                       # usa los valores por defecto
print("3 pizzas:", precio_final(9800, 3))
print("3 con 10% off:", precio_final(9800, 3, descuento=10))   # parámetro por nombre


def buscar(menu, texto):
    """Las pizzas cuyo nombre contiene el texto (sin importar mayúsculas)."""
    texto = texto.lower()
    return [item for item in menu if texto in item["nombre"].lower()]


print("Buscar 'zza':", buscar(menu, "zza"))
# Una variable creada ADENTRO de la función (subtotal) no existe afuera.


# ═══════════════════════════════════════════════════════════════════════
# 7) CLASES Y OBJETOS: los "moldes"
# ═══════════════════════════════════════════════════════════════════════
# Una CLASE es un molde; un OBJETO es una cosa hecha con ese molde.
# Los MODELOS de Django son clases: "class Pizza(models.Model)".
print("\n7) Clases")


class Pedido:
    def __init__(self, cliente):              # __init__ = lo que pasa al CREAR un objeto
        self.cliente = cliente                # self = "este objeto": sus datos (atributos)
        self.items = []

    def agregar(self, nombre, precio, cantidad=1):    # un MÉTODO = una función del objeto
        self.items.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})

    def total(self):
        return sum(item["precio"] * item["cantidad"] for item in self.items)

    def __str__(self):                        # cómo se muestra con print()
        return f"Pedido de {self.cliente} ({len(self.items)} ítems, ${self.total()})"


pedido = Pedido("Marcos")                     # crear un objeto
pedido.agregar("Muzzarella", 9800, 2)
pedido.agregar("Fugazzeta", 12000)
print(pedido)
print("Cliente:", pedido.cliente, "· total:", pedido.total())

otro = Pedido("Ana")                          # otro objeto, con SUS propios datos
print(otro)


# HERENCIA: una clase que parte de otra y le agrega o cambia cosas.
# Django lo usa en todos lados: tu modelo hereda de models.Model y por eso
# ya sabe guardarse, borrarse, etc., sin que lo programes.
class PedidoDelivery(Pedido):
    COSTO_ENVIO = 1500

    def total(self):
        return super().total() + self.COSTO_ENVIO   # super() = "lo que hacía la clase de arriba"


delivery = PedidoDelivery("Beto")
delivery.agregar("Napolitana", 11000)
print(delivery, "(incluye envío)")


# ═══════════════════════════════════════════════════════════════════════
# 8) ERRORES: try / except
# ═══════════════════════════════════════════════════════════════════════
# Cuando algo puede salir mal (el usuario escribe letras donde va un
# número), se "ataja" el error para que el programa no explote.
print("\n8) Errores")
for escrito in ["4", "cuatro"]:
    try:
        cantidad = int(escrito)
        print(f"'{escrito}' -> {cantidad} pizzas")
    except ValueError:                        # el tipo de error que se ataja
        print(f"'{escrito}' no es un número: pedile que lo escriba de nuevo")


def cobrar(pedido, pago):
    if pago < pedido.total():
        raise ValueError(f"Faltan ${pedido.total() - pago}")   # raise = PROVOCAR un error a propósito
    return pago - pedido.total()                                  # el vuelto


try:
    print("Vuelto:", cobrar(pedido, 40000))
    print("Vuelto:", cobrar(pedido, 10000))
except ValueError as error:
    print("No se pudo cobrar:", error)


# ═══════════════════════════════════════════════════════════════════════
# 9) IMPORTAR: usar código de otro lado
# ═══════════════════════════════════════════════════════════════════════
# Python trae muchas herramientas; se "importan" para usarlas.
# En Django vas a ver muchos: from django.db import models
print("\n9) Importar")
from datetime import date, timedelta   # noqa: E402  (normalmente los import van arriba de todo)
from decimal import Decimal            # noqa: E402

hoy = date.today()
print("Hoy:", hoy, "· en una semana:", hoy + timedelta(days=7))
print("Formato argentino:", hoy.strftime("%d/%m/%Y"))
print("Plata exacta con Decimal:", Decimal("0.10") + Decimal("0.20"), "(con float: ", 0.1 + 0.2, ")")


# ═══════════════════════════════════════════════════════════════════════
# 10) PEDIRLE DATOS AL USUARIO (en la consola)
# ═══════════════════════════════════════════════════════════════════════
# input() espera que el usuario escriba y apriete Enter. Devuelve TEXTO.
# (En la web, en vez de input(), los datos llegan de un formulario HTML:
#  lo ves en el paso 3.)
print("\n10) input()")
respuesta = input("¿Cuántas pizzas querés? ")
try:
    print("Son $", precio_final(9800, int(respuesta)))
except ValueError:
    print("Eso no es un número.")

print("\nFin de la clase 0. Ahora: ejercicio.md")
