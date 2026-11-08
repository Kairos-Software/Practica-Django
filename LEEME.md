# Aprender Django (sin IA, solo vos)

De lo más básico (Python) hasta un sistema completo, de a un paso por vez.
Cada paso es un poco más difícil que el anterior, y en cada uno hay una
**prueba automática** que te dice si lo hiciste bien.

## Cómo se usa cada paso

1. **`clase.py`**: leelo de arriba a abajo (está todo explicado en los
   comentarios) y **ejecutalo** para ver qué pasa. El ejemplo de las clases es
   siempre de **películas**.
2. **`ejercicio.md`**: lo que tenés que hacer vos. Es de **otro tema** (una
   **librería** que vas construyendo paso a paso), así tenés que pensar y no
   copiar. Dice QUÉ hacer, no CÓMO, y al final explica **cómo ejecutarlo**.
3. **La prueba** (`prueba.py` o `test_pasoN.py`): la corrés las veces que
   quieras mientras avanzás. Te dice qué está bien (`ok`) y qué falta
   (`FAIL`, con qué esperaba y qué encontró).
4. **`solucion/`**: una forma de resolverlo, para comparar AL FINAL, con un
   `COMO_USARLA.md` que explica las decisiones importantes.

Si te trabás: volvé a la clase, no a la solución.

## Los pasos

| Carpeta | Qué aprendés | Tu ejercicio |
|---|---|---|
| `paso_0_python` | Variables, listas, diccionarios, `if`, `for`, funciones, clases, errores | Un kiosco (funciones y clases) |
| `paso_1_base_de_datos` | Qué es una base de datos. SQL a mano: crear tablas, guardar, buscar, editar, borrar, relacionar, transacciones. SQLite y PostgreSQL | La librería con SQL |
| `paso_2_django_por_consola` | Proyecto Django, modelos, migraciones, el ORM (todo lo del paso 1 sin SQL), validaciones, admin | La librería con Django, desde la consola |
| `paso_3_paginas_web` | HTML básico (`clase_0_html_basico.html`). URLs, vistas, templates, formularios, mensajes, paginación | Las páginas de la librería |
| `paso_4_usuarios` | Login, logout, registro, "solo con sesión", cada usuario ve lo suyo, vistas de clase, muchos a muchos | Usuarios y reseñas en la librería |
| `paso_5_imagenes_y_archivos` | Subir imágenes, validarlas, mostrarlas, borrar las viejas. Descargar (exportar a Excel/CSV) e importar planillas | Portadas, fotos y planillas de la librería |
| `paso_6_api` | Tu propia API en JSON (leer, crear, borrar, errores, códigos), y usarla desde la página con JavaScript | La API de la librería y un buscador en vivo |
| `proyecto_final` | **Todo junto, de cero, sin ayuda** | Una veterinaria, con pruebas por etapa |

Los pasos 2 a 6 son **el mismo proyecto** (la librería) que va creciendo. Si
un paso no te sale, podés copiar la solución del paso anterior y seguir desde ahí.

## ⚙️ Antes de empezar: `COMANDOS.md`

**Cómo se ejecuta todo**: crear el entorno, instalar Django, cada comando de
`manage.py` explicado, el ciclo de trabajo de todos los días, cómo ver la base
con DBeaver y los errores más comunes con su arreglo. Leelo primero y tenelo a
mano.

## Preparar la compu (una sola vez)

Abrí PowerShell en esta carpeta (o en VS Code: *Archivo → Abrir carpeta* y
*Terminal → New Terminal*):

```powershell
python --version                 # tiene que decir 3.12 o más nuevo
python -m venv entorno           # crea el entorno
.\entorno\Scripts\activate       # entrar (aparece "(entorno)" al principio)
pip install django pillow        # Django, y Pillow para las imágenes (paso 5)
mkdir mis_proyectos              # acá van TUS proyectos (la librería y la veterinaria)
```

## Cómo se ejecuta cada clase

```powershell
cd "D:\Desktop\Aprender Django"
.\entorno\Scripts\activate
python paso_0_python\clase.py
python paso_1_base_de_datos\clase.py
python paso_2_django_por_consola\clase.py
#   paso 3: primero abrí paso_3_paginas_web\clase_0_html_basico.html con doble clic
python paso_3_paginas_web\clase.py              # simula visitas a las páginas
python paso_3_paginas_web\clase.py runserver    # y abrís http://127.0.0.1:8000
python paso_4_usuarios\clase.py                 # (y con runserver: usuario ana / clave-de-ana-123)
python paso_5_imagenes_y_archivos\clase.py      # (y con runserver)
python paso_6_api\clase.py                      # (y con runserver: el buscador en vivo)
```

El servidor se apaga con **Ctrl+C**. Las clases 3 a 6 crean una base (y una
carpeta de imágenes) temporal al lado del archivo; se pueden borrar sin problema.

## Cómo se corren las pruebas

- **Pasos 0 y 1**: tu archivo se llama `mi_solucion.py` y va en la carpeta del
  paso. Ahí mismo: `python prueba.py`
- **Pasos 2 a 6**: copiás `test_pasoN.py` adentro de tu carpeta `libros` y,
  desde la carpeta de `manage.py`: `python manage.py test libros.test_pasoN`.
  Al final, `python manage.py test libros` corre todos juntos.
- **Proyecto final**: copiás las pruebas de `proyecto_final\pruebas\` a tu
  carpeta `clinica` a medida que terminás cada etapa (el enunciado dice cuál).

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
6. La documentación oficial (docs.djangoproject.com, tiene un tutorial) es tu
   amiga. Buscar en la documentación NO es hacer trampa.
