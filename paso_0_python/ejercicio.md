# Ejercicio paso 0 — El Kiosquito

Vas a escribir funciones y clases para un kiosco. Todo lo que necesitás
saber está en `clase.py` (el de las pizzas). Acá dice **QUÉ** tiene que hacer
cada cosa, no **CÓMO**: eso lo pensás vos.

> **Los nombres tienen que ser exactamente estos** (de funciones, clases y
> parámetros). La prueba automática los busca escritos así, con las mismas
> mayúsculas y minúsculas.

---

## Antes de empezar: dónde está cada cosa en la clase

| Para el punto | Mirá en `clase.py` |
|---|---|
| Todas las funciones | PARTE 9 (funciones, y la diferencia entre `return` y `print`) |
| 1 (descuento) | PARTE 3 (cuentas y `round`) y PARTE 11 (`raise ValueError`) |
| 2 (mayor de edad) | PARTE 5 (comparar) |
| 3 (carrito) | PARTE 7 (lista de diccionarios) y PARTE 8 (receta 1: sumar) |
| 4 (baratos) | PARTE 8 (receta 2: filtrar) y PARTE 9 (ordenar con `key=`) |
| 5 (buscar) | PARTE 4 (`strip`, `lower`, `in`) y la función `buscar` de la PARTE 9 |
| 6 (contar) | PARTE 8 (receta 3: contar por grupo) |
| 7 (texto a cantidad) | PARTE 4 (convertir) y PARTE 11 (errores) |
| 8 y 9 (las cajas) | PARTE 10 (clases, `__str__`, herencia) y PARTE 11 (`raise`) |

---

## Cómo arrancar (la primera vez)

**1. Creá tu archivo.** En VS Code, en la lista de archivos de la izquierda,
hacé clic derecho sobre la carpeta `paso_0_python` → **New File** → escribí
`mi_solucion.py` y Enter. Tiene que quedar al lado de `clase.py` y `prueba.py`.

**2. Escribí la primera función, aunque sea vacía:**

```python
def es_mayor_de_edad(edad):
    pass    # "pass" quiere decir "todavía nada". Reemplazalo por tu código.
```

**3. Corré la prueba.** En la terminal:

```powershell
cd "D:\Desktop\Aprender Django\paso_0_python"
python prueba.py
```

(Si la terminal ya estaba en `paso_0_python`, alcanza con `python prueba.py`.)

**4. Leé el resultado.** Arriba aparece una línea por cada punto:

```text
1. precio_con_descuento ... FAIL
2. es_mayor_de_edad ... ok
3. total_carrito ... FAIL
```

- `ok` = ese punto está bien.
- `FAIL` = está mal o falta. Más abajo hay un bloque por cada `FAIL`. Leé la
  **última línea** del bloque, que dice qué pasó:

```text
FAIL: test_1_precio_con_descuento
...
AssertionError: ValueError not raised : con porcentaje -5 tiene que dar ValueError
```

  Quiere decir: "con un porcentaje de -5 esperaba un `ValueError`, y tu
  función no lo provocó". Y si dice:

```text
AssertionError: Falta la función o clase 'total_carrito' en mi_solucion.py
```

  es que todavía no la escribiste (o tiene otro nombre).

- `ERROR` = tu código se rompió (por ejemplo, un `TypeError`). Se lee igual:
  la última línea dice qué pasó, y más arriba aparece la línea de **tu** archivo.

Al principio va a fallar casi todo: es normal. **Hacé un punto, corré la
prueba, y pasá al siguiente.** Cuando estén todos bien, al final dice
`✔ ¡Todo bien! Paso 0 aprobado.`

---

## Lo que tenés que hacer

En varios puntos se usa un "producto", que es un diccionario así:
`{"nombre": "Alfajor", "precio": 1200, "categoria": "golosinas"}`

Para los ejemplos, imaginá esta lista (es la misma que usa la prueba):

```python
productos = [
    {"nombre": "Alfajor", "precio": 1200, "categoria": "golosinas"},
    {"nombre": "Coca Cola 500", "precio": 1800, "categoria": "bebidas"},
    {"nombre": "Chicle", "precio": 300, "categoria": "golosinas"},
    {"nombre": "Alfajor triple", "precio": 1900, "categoria": "golosinas"},
]
```

"Devuelve" quiere decir **con `return`**. "Provoca un `ValueError`" quiere
decir **con `raise ValueError("un mensaje")`**.

### Funciones

**1. `precio_con_descuento(precio, porcentaje)`**
Devuelve el precio con ese porcentaje de descuento, redondeado a 2 decimales.
Si el porcentaje es menor que 0 o mayor que 100, provoca un `ValueError`.

| Si la llamás así | Tiene que dar |
|---|---|
| `precio_con_descuento(1000, 15)` | `850` |
| `precio_con_descuento(999, 10)` | `899.1` |
| `precio_con_descuento(500, 0)` | `500` |
| `precio_con_descuento(1000, -5)` | `ValueError` |
| `precio_con_descuento(1000, 120)` | `ValueError` |

**2. `es_mayor_de_edad(edad)`**
Devuelve `True` si la edad es 18 o más; si no, `False`.

| Si la llamás así | Tiene que dar |
|---|---|
| `es_mayor_de_edad(18)` | `True` |
| `es_mayor_de_edad(17)` | `False` |

**3. `total_carrito(carrito)`**
El carrito es una lista de diccionarios así:
`{"producto": "Alfajor", "precio": 1200, "cantidad": 3}`.
Devuelve el total a pagar (precio por cantidad, de cada uno, todo sumado).
Un carrito vacío da `0`.

```python
total_carrito([{"producto": "Alfajor", "precio": 1200, "cantidad": 3},
               {"producto": "Chicle", "precio": 300, "cantidad": 1}])     # tiene que dar 3900
total_carrito([])                                                          # tiene que dar 0
```

**4. `productos_baratos(productos, tope)`**
Devuelve una lista con los **nombres** (solo el texto, no el diccionario
entero) de los productos que cuestan **menos** que el tope, ordenados del más
barato al más caro.

| Si la llamás así | Tiene que dar |
|---|---|
| `productos_baratos(productos, 1850)` | `["Chicle", "Alfajor", "Coca Cola 500"]` |
| `productos_baratos(productos, 1200)` | `["Chicle"]` ← el Alfajor cuesta 1200 justo: "menos que" no lo incluye |
| `productos_baratos(productos, 100)` | `[]` |

**5. `buscar_producto(productos, texto)`**
Devuelve la lista de productos (los **diccionarios enteros**) cuyo nombre
**contiene** el texto, sin importar mayúsculas ni los espacios que el texto
tenga al principio o al final.

```python
buscar_producto(productos, "  ALFA ")   # los diccionarios de "Alfajor" y de "Alfajor triple"
buscar_producto(productos, "helado")    # []
```

**6. `contar_por_categoria(productos)`**
Devuelve un diccionario con cuántos productos hay de cada categoría.

```python
contar_por_categoria(productos)    # {"golosinas": 3, "bebidas": 1}
```

**7. `texto_a_cantidad(texto)`**
Convierte un texto como `" 3 "` en el número `3`. Si no es un número entero
mayor que 0, provoca un `ValueError`.

| Si la llamás así | Tiene que dar |
|---|---|
| `texto_a_cantidad(" 3 ")` | `3` |
| `texto_a_cantidad("12")` | `12` |
| `texto_a_cantidad("tres")`, `("0")`, `("-2")`, `("")`, `("2.5")` | `ValueError` (cada uno) |

> Pista: probá en la consola de Python (`python` en la terminal, ver el
> principio de la clase) qué hace `int()` con cada uno de esos textos. Con
> algunos ya da `ValueError` solo; con otros no, y ahí lo tenés que provocar vos.

### Clases

**8. Clase `Caja`**
- Se crea con el nombre de quien atiende: `Caja("Marcos")`.
- Empieza con el atributo `saldo` en `0` y el atributo `ventas` como una lista vacía.
- Método `vender(producto, precio, cantidad=1)`: suma `precio * cantidad` al
  saldo, y agrega a `ventas` un diccionario así:
  `{"producto": "Alfajor", "precio": 1200, "cantidad": 3}`.
  Si la cantidad es menor que 1, provoca un `ValueError` **y no cambia nada**
  (ni el saldo ni las ventas).
- Método `retirar(monto)`: resta el monto del saldo. Si el saldo no alcanza,
  provoca un `ValueError` **y no cambia nada**.
- Método `cantidad_de_ventas()`: devuelve cuántas ventas se hicieron.
- Al hacer `print(caja)` (o `str(caja)`) se ve así: `Caja de Marcos: $3600`

Lo que revisa la prueba, en orden:

```python
caja = Caja("Marcos")
caja.saldo                       # 0
caja.ventas                      # []
caja.vender("Alfajor", 1200, 3)
caja.saldo                       # 3600
caja.ventas                      # [{"producto": "Alfajor", "precio": 1200, "cantidad": 3}]
str(caja)                        # "Caja de Marcos: $3600"
caja.vender("Chicle", 300, 0)    # ValueError (cantidad 0)...
caja.saldo                       # ...y sigue en 3600
caja.cantidad_de_ventas()        # 1  (la venta mal no se contó)
caja.retirar(600)
caja.saldo                       # 3000
caja.retirar(5000)               # ValueError (no alcanza)...
caja.saldo                       # ...y sigue en 3000
```

> Pista para "no cambia nada": revisá **antes** de cambiar (PARTE 11, la
> función `cobrar`).

**9. Clase `CajaConRecargo`, que hereda de `Caja`**
Es igual a `Caja`, pero cada venta cobra un 10% más. Usá **herencia**
(`class CajaConRecargo(Caja):`) y cambiá solo lo necesario.

```python
caja = CajaConRecargo("Ana")
caja.vender("Gaseosa", 1000)
caja.saldo                       # 1100
caja.cantidad_de_ventas()        # 1
```

---

## Probar tus funciones a mano (opcional)

Además de la prueba, podés ver qué devuelven tus funciones. Al **final** de
`mi_solucion.py` agregá:

```python
if __name__ == "__main__":
    print(precio_con_descuento(1000, 15))
    caja = Caja("Marcos")
    caja.vender("Alfajor", 1200, 3)
    print(caja)
```

Y ejecutalo con `python mi_solucion.py`.

`if __name__ == "__main__":` quiere decir "solo si ejecuto ESTE archivo".
Cuando la prueba usa tu archivo, eso no se ejecuta, así que no molesta.

---

## Cuando terminaste

- `python prueba.py` tiene que terminar con `✔ ¡Todo bien! Paso 0 aprobado.`
- Recién ahí, compará con `solucion.py`. No tiene que ser igual: hay muchas
  formas correctas. Para ver la prueba pasando con la solución:
  `python prueba.py solucion`.

Tu `mi_solucion.py` es tuyo: no se sube al repositorio (está en el `.gitignore`).
