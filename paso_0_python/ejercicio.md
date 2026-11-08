# Ejercicio paso 0 — El Kiosquito

Escribí un archivo **`mi_solucion.py`** en esta carpeta, con las funciones y
clases de abajo. Los **nombres tienen que ser exactamente estos** (la prueba
automática los busca así). Cómo hacerlas, lo decidís vos.

En todos los puntos, un "producto" es un diccionario así:
`{"nombre": "Alfajor", "precio": 1200, "categoria": "golosinas"}`

## Funciones

1. `precio_con_descuento(precio, porcentaje)` → el precio con ese % de
   descuento, redondeado a 2 decimales. Si el porcentaje es menor que 0 o
   mayor que 100, que provoque un `ValueError`.
2. `es_mayor_de_edad(edad)` → `True` si tiene 18 o más, si no `False`.
3. `total_carrito(carrito)` → el total a pagar. El carrito es una lista de
   diccionarios `{"producto": "Alfajor", "precio": 1200, "cantidad": 3}`.
   Un carrito vacío da 0.
4. `productos_baratos(productos, tope)` → una lista con los **nombres** de los
   productos que cuestan **menos** que el tope, del más barato al más caro.
5. `buscar_producto(productos, texto)` → la lista de productos (los
   diccionarios enteros) cuyo nombre **contiene** el texto, sin importar
   mayúsculas ni los espacios que el texto tenga al principio o al final.
6. `contar_por_categoria(productos)` → un diccionario con cuántos productos
   hay de cada categoría. Ej: `{"golosinas": 2, "bebidas": 1}`.
7. `texto_a_cantidad(texto)` → convierte un texto como `" 3 "` en el número
   `3`. Si no es un número entero mayor que 0 (ej: `"tres"`, `"0"`, `"-2"`),
   que provoque un `ValueError`.

## Clases

8. Clase **`Caja`**:
   - se crea con el nombre de quien atiende: `Caja("Marcos")`
   - empieza con `saldo` en 0 y una lista `ventas` vacía
   - `vender(producto, precio, cantidad=1)`: suma `precio * cantidad` al saldo
     y agrega a `ventas` un diccionario con producto, precio y cantidad. Si la
     cantidad es menor que 1, `ValueError` (y no cambia nada).
   - `retirar(monto)`: resta del saldo. Si no alcanza, `ValueError` (y no
     cambia nada).
   - `cantidad_de_ventas()`: cuántas ventas se hicieron.
   - al hacer `print()` de la caja (o `str(caja)`) se ve:
     `Caja de Marcos: $3600`
9. Clase **`CajaConRecargo`**, que **hereda** de `Caja`: igual, pero cada venta
   cobra un 10% más (una venta de $1000 suma $1100 al saldo).

## Cómo ejecutarlo y comprobarlo

```powershell
cd "D:\Desktop\Aprender Django"
.\entorno\Scripts\activate
cd paso_0_python
python prueba.py                # prueba TU archivo: mi_solucion.py
```

La prueba muestra cada punto con **ok** (bien) o **FAIL** / **ERROR** (mal), y
abajo el detalle de qué esperaba y qué encontró. Podés ejecutarla todas las
veces que quieras mientras avanzás: al principio va a fallar casi todo.

Para ver la prueba pasando con la solución: `python prueba.py solucion`
(mirala recién cuando termines).

Si querés probar tus funciones a mano, al final de tu archivo:

```python
if __name__ == "__main__":
    print(precio_con_descuento(1000, 15))
```

(`if __name__ == "__main__":` = "solo si ejecuto ESTE archivo"; cuando la
prueba lo importa, eso no se ejecuta.)
