# Ejercicio paso 2 — La librería con Django (por consola)

Es la librería del paso 1 (autores y libros), ahora con Django y **sin
escribir SQL**. Este proyecto lo vas a seguir agrandando en los pasos 3, 4,
5 y 6: hacelo con cariño.

> **Los nombres tienen que ser exactamente estos** (de carpetas, archivos,
> modelos, campos y funciones). La prueba automática los busca escritos así.

---

## Antes de empezar: dónde está cada cosa en la clase

| Para la parte | Mirá en `clase.py` |
|---|---|
| A (el proyecto) | PARTES A2 y A3 |
| B (los modelos) | PARTE A4, y la PARTE B1 (cada tipo de campo explicado) |
| B5 (`vender`, `clean`) | PARTE B1 (métodos y `clean`), y en el paso 0 la función `cobrar` (revisar antes de cambiar) |
| B6 (crear las tablas) | PARTE A5 (migraciones) |
| C (el admin) | PARTE A6 |
| D (las consultas) | PARTES B3 (leer), B4 (`update` y `F`), B5 (borrar) y B6 (`annotate` y `aggregate`) |
| E (probar a mano) | PARTE A7 |

---

## Parte A — El proyecto (paso a paso)

Todo esto va en la terminal, **con el entorno activado** (la línea empieza
con `(entorno)`; si no, mirá la PARTE "¿Qué necesitás?" de la clase).

```powershell
cd "D:\Desktop\Aprender Django"
.\entorno\Scripts\activate
mkdir mis_proyectos                       # la carpeta para TUS proyectos (si ya existe, da un aviso: no pasa nada)
cd mis_proyectos
mkdir libreria
cd libreria
django-admin startproject config .        # ¡con el punto al final!
python manage.py startapp libros
```

Comprobá que quedó así (con `ls` en la terminal, o mirando en VS Code):

```text
mis_proyectos\libreria\
├── manage.py
├── config\        (settings.py, urls.py...)
└── libros\        (models.py, admin.py, views.py...)
```

Si te quedó `config\config\`, te olvidaste del punto: borrá la carpeta
`libreria` y empezá de nuevo.

**A1.** En `config/settings.py`, registrá la app `libros` en `INSTALLED_APPS`.

**A2.** En el mismo archivo: idioma `es-ar` y zona horaria
`America/Argentina/Buenos_Aires`.

---

## Parte B — Los modelos (en `libros/models.py`)

**B3. `Autor`**
- `nombre`: texto, sin repetir
- `pais`: texto, opcional
- `nacimiento`: fecha, opcional
- se muestra por su nombre (`print(autor)` → `Borges`) y se ordena por nombre

**B4. `Libro`**
- `titulo`: texto
- `autor`: relacionado con `Autor`. Si se intenta borrar un autor que tiene
  libros, que **no** lo deje. Desde un autor, sus libros se piden con
  `autor.libros` (por ejemplo `borges.libros.all()`).
- `precio`: plata, con 2 decimales
- `stock`: entero no negativo, por defecto 0
- `anio`: año de publicación, entero no negativo
- `disponible`: sí/no, por defecto sí
- `cargado`: fecha y hora, que se pone sola al crearlo
- se muestra como `Título — Autor` (con ese guion largo: —), por ejemplo
  `Ficciones — Borges`, y se ordena por título

**B5. Métodos de `Libro`**
- `hay_stock()`: devuelve `True` si el stock es mayor que 0.
- `vender(cantidad)`: le resta la cantidad al stock y **guarda**. Si la
  cantidad es 0 o menos, o si no alcanza el stock, provoca un `ValueError`
  **y no cambia nada**. Cuando no alcanza el stock, el mensaje del error
  tiene que **empezar con `No alcanza el stock`** (por ejemplo:
  `No alcanza el stock de «Ficciones»: hay 3 y pidieron 10.`). Las páginas
  del paso 3 y la API del paso 6 muestran ese mensaje, y sus pruebas lo buscan.

  ```python
  libro.stock        # 5
  libro.vender(2)    # ahora 3, y guardado en la base
  libro.vender(10)   # ValueError("No alcanza el stock..."). Sigue en 3.
  libro.vender(0)    # ValueError (cantidad mala, el mensaje lo elegís vos). Sigue en 3.
  ```

- validación (`clean`): el año no puede ser mayor que el año actual. (Un
  libro de este año sí vale; uno del año que viene, no.)

**B6. Creá las tablas en la base** (desde la carpeta de `manage.py`):

```powershell
python manage.py makemigrations       # escribe el plano: tiene que decir "Create model Autor" y "Create model Libro"
python manage.py migrate              # crea las tablas: muchas líneas que terminan en "OK"
```

Cada vez que cambies algo en `models.py`, repetí esos dos comandos.

---

## Parte C — El admin

**C7.** Creá tu superusuario:

```powershell
python manage.py createsuperuser      # usuario, email (podés dejarlo vacío) y contraseña dos veces
```

En `libros/admin.py`, registrá los dos modelos. En la lista de libros:
- las columnas `titulo`, `autor`, `precio`, `stock` y `disponible`
- filtros por `autor` y `disponible`
- buscador por `titulo`

**C8.** Prendé el servidor y cargá algunos autores y libros a mano:

```powershell
python manage.py runserver            # dejalo prendido. Abrí http://127.0.0.1:8000/admin
```

Entrá con tu superusuario. Para apagar el servidor: **Ctrl+C** en la terminal.
(Mientras está prendido, esa terminal queda ocupada: para otros comandos,
abrí otra con el **+** de la terminal de VS Code, y activá el entorno ahí también.)

---

## Parte D — Las consultas (en un archivo nuevo: `libros/consultas.py`)

Creá el archivo `consultas.py` adentro de la carpeta `libros`, al lado de
`models.py`. Arriba de todo va el import de tus modelos:

```python
from .models import Autor, Libro       # el punto = "de esta misma app"
```

Son funciones que usan el ORM (nada de SQL a mano). Para los ejemplos,
imaginá estos datos (son los que carga la prueba):

| Autor | Libro | Precio | Stock |
|---|---|---|---|
| Borges | Ficciones | 15000 | 4 |
| Borges | El Aleph | 14000 | 0 |
| Cortázar | Rayuela | 20000 | 3 |
| Cortázar | Bestiario | 12000 | 5 |
| Quino | (ninguno) | | |

| Función | Qué devuelve | Ejemplo |
|---|---|---|
| **D9.** `sin_stock()` | Los libros con stock 0, ordenados por título | El Aleph |
| **D10.** `mas_baratos_que(precio)` | Los libros que cuestan menos, del más barato al más caro | `mas_baratos_que(15000)` → Bestiario, El Aleph |
| **D11.** `buscar(texto)` | Los libros cuyo título contiene el texto (sin importar mayúsculas), ordenados por título | `buscar("AL")` → El Aleph. `buscar("ray")` → Rayuela |
| **D12.** `de_autor(nombre)` | Los libros del autor que se llama así, en **una sola consulta** (sin buscar primero al autor) | `de_autor("Cortázar")` → Bestiario, Rayuela |
| **D13.** `subir_precios(autor, porcentaje)` | Sube el precio de todos los libros de ese autor (`autor` es un objeto `Autor`) en **una sola consulta**, sin recorrerlos uno por uno. Devuelve **cuántos** cambió | `subir_precios(cortazar, 10)` → `2`. Bestiario pasa a 13200 y Rayuela a 22000 |
| **D14.** `marcar_no_disponibles_sin_stock()` | Los que no tienen stock pasan a no disponibles (una sola consulta). Devuelve cuántos cambió | → `1` (El Aleph) |
| **D15.** `resumen_por_autor()` | Todos los autores, cada uno con dos datos extra calculados por la base: `cantidad` (cuántos libros tiene) y `stock_total` (la suma de su stock; si no tiene libros puede quedar `None`) | Borges: cantidad 2, stock_total 4. Quino: 0 y `None` |
| **D16.** `precio_promedio()` | El precio promedio de todos los libros (o `None` si no hay ninguno) | → `15250` |
| **D17.** `borrar_no_disponibles()` | Borra los libros no disponibles y devuelve cuántos borró | |

"**Una sola consulta**" quiere decir que la función le habla **una sola vez**
a la base. La prueba lo cuenta. Por ejemplo, para D12, hacer primero
`Autor.objects.get(...)` y después buscar sus libros son **dos** consultas:
mirá en la PARTE B3 de la clase cómo filtrar por un campo de la tabla
relacionada.

---

## Parte E — Probarlo a mano (opcional, pero recomendado)

**E18.** Un archivo `practica.py` al lado de `manage.py`, que cree algunos
autores y libros y use tus funciones con `print()`. En la PARTE A7 de la clase
están las líneas para que un archivo suelto "arranque" Django. Se ejecuta con
`python practica.py`, desde la carpeta de `manage.py`.

---

## Cómo comprobar que está bien (la prueba automática)

1. Copiá el archivo **`test_paso2.py`** (de la carpeta del paso 2) adentro de
   tu carpeta **`libros`**, al lado de `models.py`:

   ```powershell
   cd "D:\Desktop\Aprender Django\mis_proyectos\libreria"
   copy "..\..\paso_2_django_por_consola\test_paso2.py" libros\
   ```

2. Desde la carpeta de `manage.py`:

   ```powershell
   python manage.py test libros.test_paso2
   ```

3. Cómo leer el resultado:
   - Arriba aparece una línea por cada prueba, con su punto (B3, D12...).
   - `OK` al final = todo bien.
   - `FAILED (failures=2)` = dos pruebas fallaron. Para cada una hay un bloque
     `FAIL:` con una explicación y, en la **última línea**, qué esperaba y qué
     encontró.
   - Las pruebas usan una base de datos **aparte** y vacía: no tocan tus datos.
   - La podés correr todas las veces que quieras mientras avanzás.

### Si algo no anda

| Lo que ves | Qué pasa | Qué hacer |
|---|---|---|
| `No module named 'django'` | El entorno no está activado | `.\entorno\Scripts\activate` (desde `Aprender Django`) |
| `ImportError: cannot import name 'Autor' from 'libros.models'` (al correr la prueba) | Todavía no escribiste ese modelo, o tiene otro nombre | Mientras no existan `Autor` y `Libro`, la prueba no puede ni arrancar: escribilos primero |
| `Falta el archivo libros/consultas.py` | No creaste `consultas.py`, o no está adentro de `libros` | Crealo al lado de `models.py` |
| `no such table: libros_libro` | Faltan las migraciones | `makemigrations` y `migrate` |
| `You have N unapplied migration(s)` | Falta `migrate` | `python manage.py migrate` |
| `That port is already in use` | Ya hay un `runserver` prendido | Cerralo con Ctrl+C (o buscá la otra terminal) |

Más errores comunes en `COMANDOS.md`, punto 7.

La solución está en `solucion/libreria/` (con su `COMO_USARLA.md`). Mirala
recién cuando termines.
