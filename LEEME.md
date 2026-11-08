# Aprender Django (sin IA, solo vos)

Un curso para aprender a hacer sistemas web con **Python** y **Django**, desde
cero hasta un sistema completo, de a un paso por vez. Cada paso es un poco más
difícil que el anterior, y cada uno tiene una **prueba automática** que te
dice si lo hiciste bien.

No hace falta saber programar: el paso 0 arranca desde lo más básico.

---

## Si nunca programaste: tres cosas antes de empezar

**1. VS Code** es el programa donde vas a leer y escribir el código. Abrí esta
carpeta con *Archivo → Abrir carpeta* y elegí `Aprender Django`. A la
izquierda vas a ver la lista de archivos y carpetas.

**2. La terminal** es una ventana donde le das órdenes escritas a la
compu: escribís una orden y apretás Enter. En VS Code se abre con el menú
*Terminal → New Terminal* (aparece abajo). Las órdenes de este curso están en
recuadros como este:

```powershell
python --version
```

Escribila tal cual (o copiala) y apretá Enter. Lo que va después de un `#`
es una explicación: no se escribe.

**3. Python** es el lenguaje. Para saber si lo tenés instalado, escribí en la
terminal `python --version`: tiene que decir `Python 3.12` o un número más
grande. Si dice que no lo encuentra, instalalo desde python.org (en el
instalador, tildá **"Add Python to PATH"**) y cerrá y abrí VS Code.

---

## Cómo es cada paso

Cada carpeta `paso_N_...` tiene estos archivos, y se usan en este orden:

| Archivo | Qué es | Qué hacés |
|---|---|---|
| `clase.py` | La **clase**: explicaciones y ejemplos que funcionan. El ejemplo es siempre de **películas** (o pizzas, en el paso 0). | La **ejecutás** (arriba de todo dice cómo) y la **leés** de arriba a abajo. Al lado de cada `print()` está anotado lo que tiene que aparecer en la pantalla, para que compares. |
| `ejercicio.md` | Lo que tenés que hacer **vos**, sobre **otro tema** (una librería), así tenés que pensar y no copiar. Dice QUÉ hacer, no CÓMO, y en qué parte de la clase está cada cosa. | Lo leés y lo hacés de a un punto. Para verlo lindo en VS Code: clic derecho sobre el archivo → *Open Preview*. |
| `prueba.py` o `test_pasoN.py` | La **prueba automática**. | La corrés las veces que quieras mientras avanzás. Te dice qué está bien (`ok`) y qué falta (`FAIL`, con qué esperaba y qué encontró). |
| `solucion/` | Una forma de resolverlo, con un `COMO_USARLA.md` que explica las decisiones importantes. | La mirás **AL FINAL**, para comparar. |

**Si te trabás: volvé a la clase, no a la solución.**

---

## Los pasos

| Carpeta | Qué aprendés | Tu ejercicio |
|---|---|---|
| `paso_0_python` | Python desde cero: mostrar cosas, variables, cuentas, textos, `if`, listas, diccionarios, `for`, funciones, clases, errores | Un kiosco (funciones y clases) |
| `paso_1_base_de_datos` | Qué es una base de datos. SQL escrito a mano: crear tablas, guardar, buscar, editar, borrar, relacionar tablas, transacciones | La librería con SQL |
| `paso_2_django_por_consola` | Un proyecto Django: modelos, migraciones, el ORM (todo lo del paso 1, sin SQL), validaciones, el admin | La librería con Django, desde la consola |
| `paso_3_paginas_web` | HTML básico (`clase_0_html_basico.html`). Direcciones, vistas, templates, formularios, mensajes, paginación | Las páginas de la librería |
| `paso_4_usuarios` | Entrar, salir y registrarse; páginas que piden sesión; que cada usuario vea lo suyo; vistas de clase; "muchos a muchos" | Usuarios y reseñas en la librería |
| `paso_5_imagenes_y_archivos` | Subir imágenes, validarlas, mostrarlas, borrar las viejas. Bajar y subir planillas (CSV) | Portadas, fotos y planillas de la librería |
| `paso_6_api` | Tu propia API en JSON, y usarla desde la página con JavaScript | La API de la librería y un buscador en vivo |
| `proyecto_final` | **Todo junto, de cero, sin ayuda** | Una veterinaria, con pruebas por etapa |

Los pasos 2 a 6 son **el mismo proyecto** (la librería) que va creciendo. Si
un paso no te sale, podés copiar la solución del paso anterior y seguir desde ahí.

---

## Preparar la compu

**Para los pasos 0 y 1 alcanza con Python.** No hace falta nada más.

**Desde el paso 2 necesitás Django**, instalado en un *entorno virtual* (una
carpeta con su propio Python y sus paquetes, para que no se mezclen con los
de otros proyectos). Una sola vez, en la terminal, parado en `Aprender Django`:

```powershell
python -m venv entorno           # crea el entorno (una carpeta "entorno")
.\entorno\Scripts\activate       # lo activa: la línea empieza con "(entorno)"
pip install django pillow        # instala Django, y Pillow para las imágenes (paso 5)
mkdir mis_proyectos              # acá van TUS proyectos (la librería y la veterinaria)
```

Cada vez que abras una terminal nueva, el entorno arranca **desactivado**:
volvé a escribir `.\entorno\Scripts\activate`. Si al activarlo sale *"la
ejecución de scripts está deshabilitada"*, mirá `COMANDOS.md`, punto 1.

**`COMANDOS.md`** explica cómo se ejecuta todo: el entorno, cada comando de
Django, el ciclo de trabajo de todos los días, cómo ver la base de datos y
los errores más comunes con su arreglo. Tenelo a mano.

---

## Cómo se ejecuta cada clase

Desde la carpeta `Aprender Django` (y desde el paso 2, con el entorno activado):

```powershell
python paso_0_python\clase.py                   # al final te pregunta algo: escribí un número y Enter
python paso_1_base_de_datos\clase.py
python paso_2_django_por_consola\clase.py
#   paso 3: primero abrí paso_3_paginas_web\clase_0_html_basico.html en el navegador
python paso_3_paginas_web\clase.py              # simula visitas a las páginas
python paso_3_paginas_web\clase.py runserver    # y la página de verdad: abrí http://127.0.0.1:8000
python paso_4_usuarios\clase.py                 # (y con runserver: usuario ana / clave-de-ana-123)
python paso_5_imagenes_y_archivos\clase.py      # (y con runserver)
python paso_6_api\clase.py                      # (y con runserver: el buscador en vivo)
```

Cuando una clase se ejecuta con `runserver`, la terminal queda ocupada
mientras el servidor está prendido. Se apaga con **Ctrl+C**. Las clases 3 a 6
crean una base (y una carpeta de imágenes) temporal al lado del archivo; se
pueden borrar sin problema.

---

## Cómo se corren las pruebas

- **Pasos 0 y 1**: tu archivo se llama `mi_solucion.py` y va en la carpeta del
  paso. Desde esa carpeta: `python prueba.py`
- **Pasos 2 a 6**: copiás `test_pasoN.py` adentro de tu carpeta `libros` y,
  desde la carpeta de `manage.py`: `python manage.py test libros.test_pasoN`.
  Al final, `python manage.py test libros` corre todas juntas.
- **Proyecto final**: copiás las pruebas de `proyecto_final\pruebas\` a tu
  carpeta `clinica` a medida que terminás cada etapa (el enunciado dice cuál).

Cada `ejercicio.md` explica con ejemplos cómo leer el resultado.

---

## Tu trabajo y este repositorio

Este curso está guardado en git (un sistema que guarda las versiones de los
archivos). Tu trabajo **no** se guarda en el repositorio: `mis_proyectos/`,
los `mi_solucion.py`, el `entorno` y las bases de datos están en el
`.gitignore`, así que quedan solo en tu compu.

- Si cambiaste un archivo **del curso** sin querer (una clase, una prueba) y
  querés que vuelva a estar como era:
  `git restore paso_0_python\clase.py` (con el archivo que sea).
- `git status` te muestra si tocaste algún archivo del curso.
- Para empezar de cero en otra compu: `git clone` del repositorio, y listo.

---

## Consejos para aprender de verdad

1. **Escribí el código a mano**, no copies y pegues. Los dedos también aprenden.
2. **Rompé cosas a propósito**: borrá una línea y mirá qué error sale. Leer
   errores es la mitad del trabajo de un programador.
3. **Los errores se leen de abajo hacia arriba**: la última línea dice QUÉ
   pasó; más arriba, la primera línea de TU código dice DÓNDE.
4. Cuando algo no anda: `print()` de lo que creés que vale una variable. Casi
   siempre vale otra cosa.
5. Avanzá **de a un punto** y corré la prueba seguido: es más fácil arreglar
   un error recién hecho que diez juntos.
6. La documentación oficial (docs.djangoproject.com, que tiene un tutorial)
   es tu amiga. Buscar en la documentación NO es hacer trampa.
