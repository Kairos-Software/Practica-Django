"""
=======================================================================
 PASO 0 — PYTHON DESDE CERO
=======================================================================

Django está hecho en Python, y todo lo que vas a escribir en Django
(modelos, vistas, formularios) es Python: variables, funciones y clases
como las de este archivo. Si esto se entiende, Django se entiende.

El ejemplo de toda la clase: una pequeña PIZZERÍA.


¿QUÉ NECESITÁS?
---------------
Solo Python. Todavía NO hace falta Django ni el entorno virtual.
Para saber si tenés Python: en la terminal escribí   python --version
y apretá Enter. Tiene que decir "Python 3.12" o un número más grande.


CÓMO SE USA ESTE ARCHIVO (no te lo saltees)
-------------------------------------------
1. Abrí la carpeta "Aprender Django" en VS Code
   (menú Archivo → Abrir carpeta).

2. Abrí una TERMINAL: menú Terminal → New Terminal. Aparece una ventana
   abajo. La terminal es el lugar donde le das órdenes escritas a la compu.

3. Escribí esta orden y apretá Enter:

       python paso_0_python\\clase.py

   Quiere decir: "Python, ejecutá el archivo clase.py que está en la
   carpeta paso_0_python". (Si la terminal no está parada en la carpeta
   "Aprender Django", antes escribí:   cd "D:\\Desktop\\Aprender Django")

4. En la terminal van a aparecer muchas líneas, separadas en PARTES
   (PARTE 1, PARTE 2...). Eso es lo que hace este archivo.
   AL FINAL el programa te hace una pregunta y se queda esperando:
   escribí un número (por ejemplo 2) y apretá Enter.

5. Ahora LEÉ este archivo de arriba a abajo, de a una parte por vez.
   Debajo de cada print() te dejé anotado lo que muestra en la terminal:

       print(2 + 3)
       # Muestra: 5

   Buscá esa parte en la terminal (podés subir con la ruedita del mouse)
   y comprobá que diga lo mismo.

6. Lo MÁS importante: cambiá cosas. Cambiá un número o un texto, guardá
   el archivo (Ctrl+S) y volvé a ejecutarlo. Para no escribir la orden de
   nuevo: en la terminal, la flecha ↑ del teclado repite la última.
   En cada parte hay ideas para probar, marcadas con "PROBÁ VOS".

   Si rompiste algo y no sabés cómo volver atrás, en la terminal:
       git restore paso_0_python\\clase.py
   y el archivo vuelve a estar como al principio.


OTRA FORMA DE PROBAR: LA CONSOLA DE PYTHON
------------------------------------------
Si en la terminal escribís solo   python   (y Enter), aparece   >>>
Ahí podés escribir UNA línea de Python y ver el resultado al instante:

    >>> 2 + 3
    5
    >>> "hola".upper()
    'HOLA'

Para salir: escribí   exit()   y Enter. Es ideal para probar cosas sueltas.


LAS LÍNEAS QUE EMPIEZAN CON #
-----------------------------
Son COMENTARIOS: notas para las personas. Python las ignora por completo.
Este texto del principio, entre las triples comillas, también lo ignora.
"""


# =======================================================================
# PARTE 1 — print(): MOSTRAR COSAS EN LA PANTALLA
# =======================================================================
# Un programa es una lista de órdenes. Python las ejecuta UNA POR UNA, de
# arriba hacia abajo, como una receta de cocina.
#
# print() es la orden para MOSTRAR algo en la terminal. Lo que querés
# mostrar va adentro de los paréntesis.
#   - Un TEXTO va entre comillas: "hola" (o 'hola', es lo mismo).
#   - Un NÚMERO va sin comillas: 25
#   - Varias cosas separadas por comas se muestran en la misma línea, con
#     un espacio entre cada una.
#   - print() vacío deja una línea en blanco (lo uso para separar las partes).

print()
print("========== PARTE 1: print() ==========")

print("Hola, soy la pizzería")
# Muestra: Hola, soy la pizzería

print(25)
# Muestra: 25

print("Una muzzarella cuesta", 9500, "pesos")
# Muestra: Una muzzarella cuesta 9500 pesos

print(2 + 3)
# Muestra: 5          <- con números, Python HACE la cuenta y muestra el resultado

print("2 + 3")
# Muestra: 2 + 3      <- entre comillas es TEXTO: lo muestra tal cual, no calcula nada

# PROBÁ VOS: cambiá "Hola, soy la pizzería" por tu nombre, guardá y ejecutá.
# OJO: si te olvidás de cerrar una comilla o un paréntesis, Python no
#      ejecuta NADA y muestra un SyntaxError ("error de escritura") con el
#      número de línea donde se confundió. Probalo: borrá una comilla de
#      arriba, ejecutá, mirá el error, y volvé a ponerla.


# =======================================================================
# PARTE 2 — VARIABLES: GUARDAR UN DATO CON UN NOMBRE
# =======================================================================
# Una VARIABLE es como una caja con una etiqueta: adentro guardás un dato,
# y después lo usás llamándolo por la etiqueta.
#
#     precio = 9500
#
# Se lee: "guardá 9500 en una caja que se llama precio".
# OJO: el signo = NO es "igual" como en matemática: es "guardá esto acá".
#
# Reglas para el nombre: sin espacios (se usa el guión bajo: precio_final),
# no puede empezar con un número, y mejor sin acentos ni ñ (anio en vez de
# año). Mayúsculas y minúsculas son distintas: Precio y precio son dos cajas.

print()
print("========== PARTE 2: variables ==========")

nombre = "Muzzarella"
precio = 9500
print(nombre, precio)
# Muestra: Muzzarella 9500       <- muestra lo que hay ADENTRO de cada caja

# Se puede cambiar lo que hay en la caja (el valor viejo se pierde):
precio = 9800
print(precio)
# Muestra: 9800

# Y se puede usar lo que tiene para calcular el valor nuevo:
precio = precio + 200          # "tomá lo que hay en precio, sumale 200 y guardalo en precio"
print(precio)
# Muestra: 10000

# CADA DATO TIENE UN TIPO. Los que vas a usar todo el tiempo:
#
#   Tipo    Qué es                                    Ejemplo
#   ------  ----------------------------------------  ------------
#   str     texto (siempre entre comillas)            "Muzzarella"
#   int     número entero                             9500
#   float   número con decimales (con PUNTO, no coma) 11495.5
#   bool    verdadero o falso (con mayúscula)         True  /  False
#   None    "nada", "sin dato", vacío                 None
#
# type(dato) te dice de qué tipo es un dato.

precio_con_iva = 11495.5
hay_stock = True
descuento = None
print(type(nombre), type(precio), type(precio_con_iva), type(hay_stock), type(descuento))
# Muestra: <class 'str'> <class 'int'> <class 'float'> <class 'bool'> <class 'NoneType'>

# OJO: "9500" (con comillas) es TEXTO, no un número. Se parecen, pero no son lo mismo:
print(type("9500"), type(9500))
# Muestra: <class 'str'> <class 'int'>

# PROBÁ VOS: creá una variable   gusto = "Napolitana"   y mostrala con print.


# =======================================================================
# PARTE 3 — CUENTAS CON NÚMEROS
# =======================================================================
#   +   suma               -   resta              *   multiplicación (no se usa x)
#   /   división (SIEMPRE da un número con decimales, aunque sea exacta)
#   //  división entera (tira los decimales)      %   el resto de la división
#   **  potencia (2 ** 3 es 2 x 2 x 2)
# Se respeta el orden de la matemática: * y / antes que + y -, salvo que
# haya paréntesis.

print()
print("========== PARTE 3: cuentas ==========")

print(2 + 3, 10 - 4, 3 * 4)
# Muestra: 5 6 12

print(7 / 2, 6 / 2)
# Muestra: 3.5 3.0        <- la división con / siempre da decimal (3.0, no 3)

print(7 // 2, 7 % 2)
# Muestra: 3 1            <- 7 dividido 2 da 3, y sobra 1

print(2 ** 3)
# Muestra: 8

print(2 + 3 * 4, (2 + 3) * 4)
# Muestra: 14 20          <- primero la multiplicación, salvo que haya paréntesis

# Una cuenta con variables: 3 pizzas con 10% de descuento
precio = 9500
cantidad = 3
subtotal = precio * cantidad
total = subtotal - subtotal * 10 / 100
print(subtotal, total)
# Muestra: 28500 25650.0  <- total tiene ".0" porque en la cuenta hay una división con /

# round(numero, decimales) REDONDEA. Muy útil con plata:
print(round(10 / 3, 2), round(1234.5678, 1))
# Muestra: 3.33 1234.6

# ATAJOS para cambiar una variable usando su propio valor (los vas a ver mucho):
#   x += 5    es lo mismo que    x = x + 5
#   x -= 5    es lo mismo que    x = x - 5
porciones = 8
porciones -= 3             # se comieron 3
print(porciones)
# Muestra: 5
porciones += 8             # llegó otra pizza entera
print(porciones)
# Muestra: 13

# PROBÁ VOS: calculá cuánto salen 4 pizzas de 9500 con 15% de descuento.
#            (Te tiene que dar 32300.0)


# =======================================================================
# PARTE 4 — TEXTO (str)
# =======================================================================
print()
print("========== PARTE 4: texto ==========")

# Juntar textos con +  (solo texto con texto)
saludo = "Hola, " + "Ana"
print(saludo)
# Muestra: Hola, Ana

# f-strings: la forma cómoda de meter variables ADENTRO de un texto.
# Se pone una f pegada antes de las comillas, y cada variable entre llaves { }.
nombre = "Muzzarella"
precio = 9500
print(f"La pizza {nombre} sale ${precio}")
# Muestra: La pizza Muzzarella sale $9500
print(f"Dos salen ${precio * 2}")
# Muestra: Dos salen $19000          <- adentro de las llaves también se puede calcular

# MÉTODOS: herramientas que trae cada dato. Se usan con un punto:  dato.herramienta()
print(nombre.upper())
# Muestra: MUZZARELLA                 <- upper(): todo en mayúsculas
print(nombre.lower())
# Muestra: muzzarella                 <- lower(): todo en minúsculas
print("[" + "   hola   ".strip() + "]")
# Muestra: [hola]                     <- strip(): saca los espacios de los costados
#                                        (los corchetes son para que veas que no quedan espacios)

# len() cuenta cuántas letras tiene un texto (los espacios también cuentan)
print(len(nombre), len("a b"))
# Muestra: 10 3

# "in" pregunta si un texto está ADENTRO de otro. Responde True o False.
print("zza" in nombre, "ZZA" in nombre)
# Muestra: True False                 <- distingue mayúsculas de minúsculas
print("ZZA".lower() in nombre.lower())
# Muestra: True                       <- truco: pasar los dos a minúsculas antes de comparar

# OJO: los métodos NO cambian la variable: devuelven un texto NUEVO.
nombre.upper()
print(nombre)
# Muestra: Muzzarella                 <- sigue igual. Para cambiarla: nombre = nombre.upper()

# CONVERTIR de un tipo a otro. Es MUY común, porque lo que escribe una
# persona (en la terminal o en una página web) llega SIEMPRE como texto.
#   int("3")       texto -> número entero
#   float("2.5")   texto -> número con decimales
#   str(9500)      número -> texto
cantidad_texto = "3"
print(cantidad_texto * 2)
# Muestra: 33          <- ¡OJO! un TEXTO por 2 es el texto repetido dos veces
cantidad = int(cantidad_texto)
print(cantidad * 2)
# Muestra: 6           <- ahora sí es un número
print(int(" 7 "))
# Muestra: 7           <- int() acepta espacios a los costados
print(str(precio) + " pesos")
# Muestra: 9500 pesos  <- para pegar con + hay que pasar el número a texto.
#                         Sin el str() daría un error (TypeError: no se puede sumar texto y número)
# Si el texto no es un número, como int("tres"), Python da un ERROR
# (ValueError). En la PARTE 11 vas a ver cómo atajarlo.

# PROBÁ VOS: mostrá tu nombre en mayúsculas y cuántas letras tiene.


# =======================================================================
# PARTE 5 — DECIDIR: if / elif / else
# =======================================================================
# "if" significa "si". Sirve para hacer algo SOLO si se cumple una condición.
#
#     if total >= 30000:              <- la condición, y al final DOS PUNTOS
#         print("Envío gratis")       <- lo de ADENTRO va corrido 4 espacios
#     print("Gracias")                <- esto ya está AFUERA: se hace siempre
#
# Esos 4 espacios al principio se llaman SANGRÍA y en Python son
# obligatorios: así sabe qué está "adentro" del if.
# (En VS Code, la tecla Tab pone los 4 espacios.)
#
#   elif = "si no, si..."  (otra condición: se mira solo si la de arriba no se cumplió)
#   else = "si no"         (cuando no se cumplió ninguna)
# Python revisa de arriba a abajo y hace SOLO la primera que se cumple.

print()
print("========== PARTE 5: if / elif / else ==========")

total = 25000
if total >= 30000:
    print("Envío gratis")
elif total >= 20000:
    print("Envío con 50% de descuento")
else:
    print("Envío normal")
# Muestra: Envío con 50% de descuento     <- 25000 no llega a 30000, pero sí a 20000

# Para COMPARAR (cada comparación da True o False):
#   ==  igual (¡DOS signos! uno solo es "guardar")     !=  distinto
#   <   menor      >   mayor      <=  menor o igual    >=  mayor o igual
print(5 == 5, 5 != 5, 3 < 10, "Ana" == "ana")
# Muestra: True False True False     <- "Ana" y "ana" no son iguales (por la mayúscula)

# Para COMBINAR condiciones:
#   and  -> se tienen que cumplir LAS DOS
#   or   -> alcanza con que se cumpla UNA
#   not  -> da vuelta: True pasa a ser False, y al revés
es_socio = True
if total > 20000 and es_socio:
    print("Socio con compra grande: 10% de descuento")
# Muestra: Socio con compra grande: 10% de descuento

hay_stock = True
if not hay_stock:
    print("No hay stock")
# No muestra nada: hay_stock es True, y "not True" es False.

# Lo "vacío" cuenta como falso: el texto vacío "", el número 0, None, la
# lista vacía [] y el diccionario vacío {}. Todo lo demás cuenta como verdadero.
comentario = ""
if not comentario:
    print("El cliente no dejó comentario")
# Muestra: El cliente no dejó comentario

# PROBÁ VOS: cambiá  total = 25000  por 35000, y después por 5000.
#            ¿Qué muestra cada vez? ¿Por qué?


# =======================================================================
# PARTE 6 — LISTAS: VARIAS COSAS EN ORDEN
# =======================================================================
# Una LISTA guarda varios datos en orden, entre corchetes [ ] y separados
# por comas. Cada dato tiene una POSICIÓN, que se cuenta DESDE CERO:
#
#     gustos = ["Muzzarella", "Napolitana", "Fugazzeta"]
#     posición:      0             1             2

print()
print("========== PARTE 6: listas ==========")

gustos = ["Muzzarella", "Napolitana", "Fugazzeta"]
print(gustos)
# Muestra: ['Muzzarella', 'Napolitana', 'Fugazzeta']
print(len(gustos))
# Muestra: 3                       <- len() en una lista: cuántos elementos tiene
print(gustos[0], gustos[2])
# Muestra: Muzzarella Fugazzeta    <- el primero es el [0], no el [1]
print(gustos[-1])
# Muestra: Fugazzeta               <- con números negativos se cuenta desde el final

gustos.append("Calabresa")         # append = agregar al final
gustos.remove("Napolitana")        # remove = sacar ese valor
print(gustos)
# Muestra: ['Muzzarella', 'Fugazzeta', 'Calabresa']

print("Fugazzeta" in gustos, "Anchoas" in gustos)
# Muestra: True False              <- "in" pregunta si está en la lista

print(sorted(gustos))
# Muestra: ['Calabresa', 'Fugazzeta', 'Muzzarella']     <- sorted(): una copia ordenada (de la A a la Z)
print(sorted([30, 5, 12]), sorted([30, 5, 12], reverse=True))
# Muestra: [5, 12, 30] [30, 12, 5]                      <- reverse=True: de mayor a menor

print(gustos[0:2])
# Muestra: ['Muzzarella', 'Fugazzeta']   <- "rebanada" [desde:hasta]: el "hasta" NO se incluye
print(sum([100, 200, 300]))
# Muestra: 600                           <- sum(): suma todos los números de una lista

# OJO: si pedís una posición que no existe, como gustos[10], da IndexError.
# PROBÁ VOS: agregá tu gusto favorito con append y mostrá la lista.


# =======================================================================
# PARTE 7 — DICCIONARIOS: DATOS CON NOMBRE
# =======================================================================
# Un DICCIONARIO es como una FICHA: cada dato tiene un nombre (la CLAVE) y
# un valor. Va entre llaves { }, con  clave: valor  separados por comas.
#
#     pizza = {"nombre": "Muzzarella", "precio": 9500}
#               clave      valor         clave   valor
#
# En una lista se busca por POSICIÓN (0, 1, 2...); en un diccionario, por
# CLAVE. En Django los vas a usar TODO el tiempo.

print()
print("========== PARTE 7: diccionarios ==========")

pizza = {"nombre": "Muzzarella", "precio": 9500, "porciones": 8}
print(pizza["nombre"], pizza["precio"])
# Muestra: Muzzarella 9500

pizza["precio"] = 9800             # si la clave ya existe: cambia el valor
pizza["vegetariana"] = True        # si no existe: la agrega
print(pizza)
# Muestra: {'nombre': 'Muzzarella', 'precio': 9800, 'porciones': 8, 'vegetariana': True}

# Pedir con [ ] una clave que no existe da ERROR (KeyError).
# .get(clave, por_defecto) no da error: si la clave no está, devuelve el "por defecto".
print(pizza.get("precio", 0), pizza.get("picante", "no dice"))
# Muestra: 9800 no dice

print("picante" in pizza)
# Muestra: False                   <- "in" en un diccionario pregunta por las CLAVES

# Una LISTA de DICCIONARIOS es como una tabla: cada diccionario es una fila.
# (Esto se usa muchísimo, y está en el ejercicio.)
menu = [
    {"nombre": "Muzzarella", "precio": 9800},
    {"nombre": "Napolitana", "precio": 11000},
    {"nombre": "Fugazzeta", "precio": 12000},
]
print(menu[1]["nombre"])
# Muestra: Napolitana              <- el diccionario de la posición 1, y de ese, la clave "nombre"

# PROBÁ VOS: agregale a pizza la clave "tamanio" con el valor "grande" y mostrala.


# =======================================================================
# PARTE 8 — REPETIR: for y while
# =======================================================================
# "for" repite algo UNA VEZ POR CADA elemento de una lista:
#
#     for item in menu:          <- "para cada item del menú..." (y DOS PUNTOS)
#         print(item)            <- "...hacé esto" (con sangría, como en el if)
#
# "item" es un nombre que inventás vos. En cada vuelta vale el elemento que
# toca: en la 1ra vuelta, el 1ro de la lista; en la 2da, el 2do; etc.

print()
print("========== PARTE 8: for y while ==========")

for item in menu:
    print(item["nombre"], "cuesta", item["precio"])
# Muestra (3 líneas, una por vuelta):
#   Muzzarella cuesta 9800
#   Napolitana cuesta 11000
#   Fugazzeta cuesta 12000

# range(desde, hasta): una serie de números. El "hasta" NO se incluye.
for numero in range(1, 4):
    print("Pizza número", numero)
# Muestra:
#   Pizza número 1
#   Pizza número 2
#   Pizza número 3

# enumerate(): para tener también el NÚMERO de vuelta (start=1: empezar a contar en 1)
for numero, item in enumerate(menu, start=1):
    print(numero, item["nombre"])
# Muestra:
#   1 Muzzarella
#   2 Napolitana
#   3 Fugazzeta

# Recorrer un DICCIONARIO: .items() da cada clave junto con su valor
for clave, valor in pizza.items():
    print(clave, "=", valor)
# Muestra:
#   nombre = Muzzarella
#   precio = 9800
#   porciones = 8
#   vegetariana = True

# --- Tres "RECETAS" con for que vas a usar TODO el tiempo ---

# RECETA 1 — SUMAR: una variable que arranca en 0, y en cada vuelta se le suma algo.
total = 0
for item in menu:
    total += item["precio"]
print("Suma de los precios:", total)
# Muestra: Suma de los precios: 32800

# RECETA 2 — FILTRAR: una lista que arranca vacía, y en cada vuelta, SI se
# cumple algo, se le agrega el elemento.
caras = []
for item in menu:
    if item["precio"] > 10000:
        caras.append(item["nombre"])
print("Las de más de $10000:", caras)
# Muestra: Las de más de $10000: ['Napolitana', 'Fugazzeta']

# RECETA 3 — CONTAR POR GRUPO: un diccionario que arranca vacío. En cada
# vuelta, a la clave del grupo se le suma 1. Se usa .get(clave, 0) porque la
# primera vez que aparece un grupo, todavía no está en el diccionario.
pedidos = ["Muzzarella", "Fugazzeta", "Muzzarella", "Napolitana", "Muzzarella"]
cuantas = {}
for gusto in pedidos:
    cuantas[gusto] = cuantas.get(gusto, 0) + 1
print(cuantas)
# Muestra: {'Muzzarella': 3, 'Fugazzeta': 1, 'Napolitana': 1}

# LO MISMO EN UNA LÍNEA: la "comprensión de lista". Se lee así:
#     [ QUÉ guardar   for CADA COSA in LA LISTA   if CONDICIÓN ]
print([item["nombre"] for item in menu if item["precio"] > 10000])
# Muestra: ['Napolitana', 'Fugazzeta']       <- igual que la receta 2
print(sum(item["precio"] for item in menu))
# Muestra: 32800                              <- igual que la receta 1
# (No es obligatorio usarla: el for "largo" hace lo mismo y al principio
#  es más fácil de leer.)

# "while" repite MIENTRAS se cumpla una condición. Sirve cuando no sabés de
# antemano cuántas vueltas va a dar.
porciones = 8
while porciones > 5:
    porciones -= 1
    print("Me como una, quedan", porciones)
# Muestra:
#   Me como una, quedan 7
#   Me como una, quedan 6
#   Me como una, quedan 5
# OJO: si la condición nunca deja de cumplirse, repite PARA SIEMPRE.
#      Si te pasa, cortalo apretando Ctrl+C en la terminal.

# PROBÁ VOS: con la receta 2, armá la lista de las pizzas de MENOS de $11500.


# =======================================================================
# PARTE 9 — FUNCIONES: UN PEDAZO DE CÓDIGO CON NOMBRE
# =======================================================================
# Una FUNCIÓN es como una máquina: le das datos (los PARÁMETROS), hace algo
# y te DEVUELVE un resultado (con return). Se escribe una vez y se usa muchas.
# Ya usaste varias que trae Python: print(), len(), sorted(), round()...
# Ahora vas a hacer las tuyas. En Django, cada PÁGINA es una función.
#
#     def doble(numero):          <- def + el nombre + (los parámetros) + DOS PUNTOS
#         return numero * 2       <- adentro, con sangría: lo que hace
#
# "def" solo la DEFINE (arma la máquina): todavía no hace nada.
# Se EJECUTA cuando la LLAMÁS por su nombre, con los datos:   doble(5)

print()
print("========== PARTE 9: funciones ==========")


def precio_final(precio, cantidad=1, descuento=0):
    """Lo que hay que cobrar. (Este texto entre triples comillas explica qué hace la función.)"""
    subtotal = precio * cantidad
    return subtotal - subtotal * descuento / 100


print(precio_final(9800, 3))
# Muestra: 29400.0        <- precio=9800, cantidad=3, y descuento=0 (su valor por defecto)
print(precio_final(9800))
# Muestra: 9800.0         <- los parámetros con = tienen un valor por defecto: cantidad=1, descuento=0
print(precio_final(9800, 3, descuento=10))
# Muestra: 26460.0        <- un parámetro también se puede pasar por su NOMBRE

# Lo que devuelve se puede guardar en una variable y seguir usando:
a_cobrar = precio_final(9800, 2)
print("Con envío:", a_cobrar + 1500)
# Muestra: Con envío: 21100.0

# MUY IMPORTANTE: return NO es lo mismo que print.
#   print  -> MUESTRA algo en la terminal (para que lo lea una persona).
#   return -> DEVUELVE el resultado a quien llamó a la función (para usarlo en el código).
# Una función sin return devuelve None ("nada"). Mirá la diferencia:


def mostrar_doble(numero):
    print(numero * 2)          # lo muestra, pero NO lo devuelve


def doble(numero):
    return numero * 2          # lo devuelve, sin mostrar nada


resultado_1 = mostrar_doble(5)
# Muestra: 10             <- lo mostró el print de adentro de mostrar_doble
resultado_2 = doble(5)
print(resultado_1, resultado_2)
# Muestra: None 10        <- mostrar_doble NO devolvió nada (None); doble sí devolvió 10
# En los ejercicios, las pruebas automáticas miran lo que DEVUELVE tu
# función (el return), no lo que muestra.


# Una función que usa una lista, un for y un if (la receta 2 de la PARTE 8):
def buscar(menu, texto):
    """Las pizzas cuyo nombre contiene el texto, sin importar mayúsculas."""
    texto = texto.lower()
    encontradas = []
    for item in menu:
        if texto in item["nombre"].lower():
            encontradas.append(item)
    return encontradas


print(buscar(menu, "ZZ"))
# Muestra: [{'nombre': 'Muzzarella', 'precio': 9800}, {'nombre': 'Fugazzeta', 'precio': 12000}]
# (Encontró "zz" en muZZarella y en fugaZZeta, aunque lo buscamos en mayúsculas.)
# (Las variables creadas ADENTRO de una función, como "encontradas", solo
#  existen adentro: afuera Python no las conoce y daría NameError.)


# ORDENAR UNA LISTA DE DICCIONARIOS POR UNO DE SUS DATOS:
# sorted() sabe ordenar números y textos, pero no sabe por qué dato ordenar
# fichas. Se lo decís con  key=  y una FUNCIÓN que, para cada elemento,
# devuelve el dato por el que querés ordenar.
def precio_de(item):
    return item["precio"]


ofertas = [
    {"nombre": "Fugazzeta", "precio": 12000},
    {"nombre": "Muzzarella", "precio": 9800},
    {"nombre": "Napolitana", "precio": 11000},
]
for item in sorted(ofertas, key=precio_de):        # OJO: precio_de SIN paréntesis (se pasa la función, no se llama)
    print(item["nombre"], item["precio"])
# Muestra (de la más barata a la más cara):
#   Muzzarella 9800
#   Napolitana 11000
#   Fugazzeta 12000
# Con  sorted(ofertas, key=precio_de, reverse=True)  sería de la más cara a la más barata.

# Forma corta que vas a ver mucho: "lambda" es una función chiquita, sin
# nombre, escrita en el mismo lugar donde se usa. Esto hace LO MISMO:
#     sorted(ofertas, key=lambda item: item["precio"])
# Y si en vez de una lista nueva querés ordenar ESA misma lista:
#     ofertas.sort(key=precio_de)

# PROBÁ VOS: escribí una función  es_cara(item)  que devuelva True si el
#            precio es mayor a 10000, y probala con  print(es_cara(menu[0])).


# =======================================================================
# PARTE 10 — CLASES Y OBJETOS: LOS MOLDES
# =======================================================================
# Una CLASE es un MOLDE; un OBJETO es una cosa hecha con ese molde.
# Pensalo como un molde de galletitas: el molde es uno solo, pero con él
# hacés muchas galletitas, y cada una tiene su propio relleno.
#
# Un objeto junta DATOS (se llaman ATRIBUTOS) y las COSAS QUE SABE HACER
# (se llaman MÉTODOS: son funciones que viven adentro de la clase).
#
# En Django vas a escribir clases todo el tiempo: cada tabla de la base de
# datos es una clase, por ejemplo  class Libro(models.Model).
#
# Las piezas de una clase:
#   class Pedido:              <- el nombre del molde (con Mayúscula, por costumbre)
#   def __init__(self, ...):   <- lo que pasa al CREAR un objeto: prepara sus datos
#   self                       <- quiere decir "este objeto".
#                                 self.cliente = "el cliente de ESTE pedido"
#   def total(self):           <- un método: siempre recibe self primero
#   def __str__(self):         <- cómo se muestra el objeto con print()

print()
print("========== PARTE 10: clases y objetos ==========")


class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente        # cada pedido guarda SU cliente...
        self.items = []               # ...y SU lista de cosas pedidas (arranca vacía)

    def agregar(self, nombre, precio, cantidad=1):
        self.items.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})

    def total(self):
        suma = 0
        for item in self.items:
            suma += item["precio"] * item["cantidad"]
        return suma

    def __str__(self):
        return f"Pedido de {self.cliente}: ${self.total()}"


pedido = Pedido("Marcos")             # CREAR un objeto: el nombre de la clase con ( ). Ahí se ejecuta __init__
pedido.agregar("Muzzarella", 9800, 2)
pedido.agregar("Fugazzeta", 12000)    # no le pasamos cantidad: vale 1
print(pedido.cliente)
# Muestra: Marcos                     <- un atributo: objeto.dato (sin paréntesis)
print(pedido.total())
# Muestra: 31600                      <- un método: objeto.metodo() (con paréntesis)
print(pedido)
# Muestra: Pedido de Marcos: $31600   <- print() usa el __str__
print(len(pedido.items))
# Muestra: 2

otro = Pedido("Ana")                  # otro objeto del mismo molde, con SUS propios datos
print(otro)
# Muestra: Pedido de Ana: $0          <- el pedido de Ana está vacío: no comparte nada con el de Marcos


# HERENCIA: una clase NUEVA que parte de otra y le cambia o agrega cosas.
#     class PedidoDelivery(Pedido):     <- entre paréntesis, la clase "madre"
# PedidoDelivery tiene TODO lo de Pedido (agregar, total, __str__...) sin
# escribirlo de nuevo, y cambia SOLO lo que es distinto: el total suma el envío.
# super() quiere decir "la clase madre": super().total() es "el total como
# lo calculaba Pedido".
#
# Django usa herencia en todos lados: tu modelo hereda de models.Model, y
# por eso ya sabe guardarse en la base, borrarse, etc., sin que lo programes.
class PedidoDelivery(Pedido):
    COSTO_ENVIO = 1500

    def total(self):
        return super().total() + self.COSTO_ENVIO


delivery = PedidoDelivery("Beto")
delivery.agregar("Napolitana", 11000)     # agregar() viene de Pedido: no hubo que escribirlo
print(delivery)
# Muestra: Pedido de Beto: $12500
# (El __str__ está escrito en Pedido, pero usa el total() NUEVO: self es un
#  PedidoDelivery, así que self.total() es el de PedidoDelivery.)

# PROBÁ VOS: creá tu propio pedido con 3 pizzas distintas y mostralo con print.


# =======================================================================
# PARTE 11 — ERRORES: try / except y raise
# =======================================================================
# Cuando algo sale mal, Python frena el programa y muestra un ERROR así:
#
#     Traceback (most recent call last):
#       File "clase.py", line 12, in <module>
#         cantidad = int("cuatro")
#     ValueError: invalid literal for int() with base 10: 'cuatro'
#
# Se lee DE ABAJO HACIA ARRIBA:
#   - La ÚLTIMA línea dice QUÉ pasó: ValueError (un valor que no sirve) y el detalle.
#   - Más arriba dice DÓNDE: el archivo y el número de línea (line 12).
#
# Los errores más comunes al empezar:
#   SyntaxError       escribiste algo mal (falta una comilla, un paréntesis, los dos puntos)
#   IndentationError  la sangría (los espacios del principio) está mal
#   NameError         usaste una variable que no existe (¿la escribiste distinto?)
#   TypeError         mezclaste tipos que no van juntos:  "Edad: " + 5
#   ValueError        el tipo está bien pero el valor no sirve:  int("cuatro")
#   KeyError          pediste una clave que el diccionario no tiene
#   IndexError        pediste una posición que la lista no tiene
#
# ATAJAR un error: try / except
#   try:          "intentá hacer esto..."
#   except X:     "...y si da el error X, en vez de frenar todo, hacé esto otro"

print()
print("========== PARTE 11: errores ==========")

for escrito in ["4", "cuatro"]:
    try:
        cantidad = int(escrito)
        print(f"'{escrito}' se convirtió en el número {cantidad}")
    except ValueError:
        print(f"'{escrito}' no es un número: hay que pedirlo de nuevo")
# Muestra:
#   '4' se convirtió en el número 4
#   'cuatro' no es un número: hay que pedirlo de nuevo


# PROVOCAR un error a propósito: raise
# Sirve para avisar "esto no se puede hacer" desde TU código. Es lo que
# piden los ejercicios cuando dicen "que provoque un ValueError":
#
#     raise ValueError("El mensaje que explica qué pasó")
#
# Cuando se ejecuta un raise, la función se corta AHÍ: lo que sigue no se hace.
# Por eso la costumbre es: PRIMERO revisar, DESPUÉS cambiar. Así, si hay un
# error, no queda nada cambiado a medias.
def cobrar(pedido, pago):
    """Devuelve el vuelto. Si el pago no alcanza, provoca un ValueError."""
    if pago < pedido.total():                                  # 1) primero revisar...
        raise ValueError(f"Faltan ${pedido.total() - pago}")   # ...si no alcanza: error, y se corta acá
    return pago - pedido.total()                               # 2) después, hacer


print("Vuelto:", cobrar(pedido, 40000))
# Muestra: Vuelto: 8400
try:
    print("Vuelto:", cobrar(pedido, 10000))
except ValueError as error:                  # "as error": guarda el error para poder leer su mensaje
    print("No se pudo cobrar:", error)
# Muestra: No se pudo cobrar: Faltan $21600
# (El print("Vuelto:", ...) de adentro del try no llega a mostrar nada:
#  cobrar() se cortó con el raise antes de devolver algo.)


# =======================================================================
# PARTE 12 — IMPORTAR: USAR HERRAMIENTAS QUE NO VIENEN "A MANO"
# =======================================================================
# Python trae muchísimas herramientas guardadas en MÓDULOS (archivos de
# código). Para usar una, primero se IMPORTA:
#     from datetime import date        <- "del módulo datetime, traeme date"
# Normalmente los import van arriba de todo del archivo. Acá están en esta
# parte para que los veas junto con su explicación.
# En Django vas a ver muchos, por ejemplo:  from django.db import models

print()
print("========== PARTE 12: importar ==========")

from datetime import date, timedelta     # fechas
from decimal import Decimal              # plata con decimales exactos

hoy = date.today()
print("Hoy es", hoy)
# Muestra la fecha de HOY en formato año-mes-día. Por ejemplo: Hoy es 2026-11-08
print("En una semana:", hoy + timedelta(days=7))
# Muestra la fecha de dentro de 7 días. Por ejemplo: En una semana: 2026-11-15
print("Formato argentino:", hoy.strftime("%d/%m/%Y"))
# Por ejemplo: Formato argentino: 08/11/2026
print("Año:", hoy.year)
# Por ejemplo: Año: 2026

# Plata: los float a veces hacen cuentas con un error chiquito (es por cómo
# la compu guarda los decimales por dentro). Decimal hace las cuentas exactas.
print(0.1 + 0.2)
# Muestra: 0.30000000000000004          <- ¡no da 0.3!
print(Decimal("0.10") + Decimal("0.20"))
# Muestra: 0.30


# =======================================================================
# PARTE 13 — PEDIRLE DATOS A LA PERSONA: input()
# =======================================================================
# input("pregunta") muestra la pregunta y DETIENE el programa hasta que la
# persona escriba algo y apriete Enter. Lo que escribió llega SIEMPRE como
# TEXTO (aunque sea un número): por eso se convierte con int().
# (En una página web los datos no llegan con input() sino desde un
#  formulario: lo ves en el paso 3. Pero también llegan como texto.)

print()
print("========== PARTE 13: input() ==========")

respuesta = input("¿Cuántas pizzas querés? ")
# El programa se queda esperando acá. Escribí un número y apretá Enter.
try:
    cantidad = int(respuesta)
    print(f"Son ${precio_final(9800, cantidad)}")
except ValueError:
    print(f"'{respuesta}' no es un número.")
# Si escribiste 2, muestra:      Son $19600.0
# Si escribiste dos, muestra:    'dos' no es un número.


# =======================================================================
# RESUMEN (para tener a mano mientras hacés el ejercicio)
# =======================================================================
#   print("texto", variable)              mostrar en la terminal
#   x = 5                                 guardar un dato en una variable
#   x += 1                                sumarle 1 a lo que ya tiene
#   int("3")   str(3)   float("2.5")      convertir entre tipos
#   round(x, 2)                           redondear a 2 decimales
#   f"Hola {nombre}"                      meter variables adentro de un texto
#   texto.strip()  .lower()  .upper()     sacar espacios / minúsculas / mayúsculas
#   "a" in "casa"     x in lista          ¿está adentro?
#   if ...: / elif ...: / else:           decidir (con DOS PUNTOS y sangría)
#   ==  !=  <  >  <=  >=    and  or  not  comparar y combinar
#   lista = [1, 2]   lista[0]   lista.append(x)   len(lista)   sorted(lista)
#   ficha = {"a": 1}   ficha["a"]   ficha.get("b", 0)   ficha.items()
#   for x in lista:     for n in range(1, 4):     while condicion:
#   def funcion(a, b=0): return ...       (return DEVUELVE; print solo muestra)
#   sorted(lista, key=funcion)            ordenar por un dato
#   class Molde:  __init__(self)  self.dato  def metodo(self)  __str__(self)
#   class Hija(Madre):   super().metodo() herencia
#   try: ... except ValueError: ...       atajar un error
#   raise ValueError("mensaje")           provocar un error a propósito

print()
print("Fin de la clase 0. Ahora abrí ejercicio.md (está en esta misma carpeta).")
