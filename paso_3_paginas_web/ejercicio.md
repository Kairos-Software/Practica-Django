# Ejercicio paso 3 — La librería, ahora con páginas

Seguí con **tu** proyecto `libreria` del paso 2. (Si no lo terminaste, copiá
la carpeta `paso_2_django_por_consola\solucion\libreria` adentro de
`mis_proyectos\` y arrancá desde ahí.)

Hasta ahora todo se hacía desde el admin o la consola. Ahora vas a hacer
páginas para que las use un empleado de la librería. **El diseño no
importa**: HTML simple alcanza (el CSS es opcional).

> **Los nombres tienen que ser exactamente estos** (de direcciones, `name=`,
> campos y mensajes). La prueba automática los busca escritos así.

---

## Antes de empezar: dónde está cada cosa en la clase

| Para | Mirá en `clase.py` (y en la PARTE 9, el código que funciona) |
|---|---|
| Cómo funciona una página | PARTE 1 |
| `libros/urls.py` y `config/urls.py` | PARTE 2 |
| Las vistas | PARTE 3 |
| Los templates y el `base.html` | PARTE 4 |
| Los formularios (crear, editar, borrar, vender) | PARTE 5 |
| Los mensajes | PARTE 6 |
| La paginación (sin perder la búsqueda) | PARTE 7 |
| El HTML (formularios, tablas, links) | `clase_0_html_basico.html` |
| Contar los libros de cada autor | Paso 2, PARTE B6 (`annotate`), y el filtro `pluralize` (PARTE 4) |

---

## Dónde va cada archivo

```text
mis_proyectos\libreria\
├── config\
│   └── urls.py                  <- incluís las urls de la app
└── libros\
    ├── urls.py                  <- NUEVO: las direcciones de la app (app_name = "libros")
    ├── views.py                 <- las vistas
    ├── forms.py                 <- NUEVO: los formularios
    └── templates\
        └── libros\              <- sí, "libros" dos veces
            ├── base.html        <- el menú y los mensajes
            ├── lista.html
            ├── detalle.html
            └── ...
```

---

## Un orden para hacerlo (de a poco, probando cada vez)

1. **Una página que diga "Hola"**: `libros/urls.py` con la dirección `""`,
   una vista `lista` que haga `render` de un `lista.html` con un `<h1>`, y el
   `include` en `config/urls.py`. Prendé el servidor y abrí
   http://127.0.0.1:8000. Si ves tu "Hola", lo más difícil ya está.
2. **La lista de verdad**: la vista le manda los libros al template, y el
   template los muestra en una tabla.
3. **`base.html`** con el menú y los mensajes, y que `lista.html` lo herede.
4. **El detalle** de un libro.
5. **Crear y editar** (el formulario, con el "baile" de la PARTE 5).
6. **Borrar**, después **vender**.
7. **Buscador, filtro y paginación** en la lista.
8. **Las páginas de autores.**

Después de cada paso, recargá el navegador (F5). Y corré la prueba seguido.

---

## Estructura

**1.** Las direcciones de la app van en **`libros/urls.py`**, con
`app_name = "libros"`, y `config/urls.py` las incluye en la raíz (`""`).
Por el `app_name`, en los templates y en `redirect` los nombres llevan el
apellido: `{% url 'libros:detalle' libro.pk %}`, `redirect("libros:lista")`.

**2.** Un template base con un menú (links a: Libros, Autores, + Libro,
+ Autor), los **mensajes** y un bloque para el contenido. Todas las páginas
lo heredan.

---

## Páginas de libros

| Nombre (`name=`) | Dirección | Qué hace |
|---|---|---|
| `lista` | `""` | Tabla con todos los libros: título (link al detalle), autor, precio y stock. Si el stock es 0, en vez del número dice **`Sin stock`**. |
| `detalle` | `libros/<id>/` | Todos los datos del libro, links a editar y borrar, y el formulario de vender. Si no existe: 404. |
| `crear` | `libros/nuevo/` | Formulario de libro. Al guardar: va al **detalle** con el mensaje **`Se guardó «título».`** |
| `editar` | `libros/<id>/editar/` | El mismo formulario, con los datos del libro. Al guardar: va al **detalle** con **`Se guardó «título».`** |
| `borrar` | `libros/<id>/borrar/` | Con GET: una página "¿Seguro que querés borrar…?" con un botón. Con POST (el botón): borra y va a la **lista** con **`Se borró «título».`** Nunca borra con GET. |
| `vender` | `libros/<id>/vender/` | Solo POST (con GET: error 405). Recibe el campo **`cantidad`** y usa el `vender()` del modelo (paso 2). Siempre vuelve al **detalle**: si salió bien, con el mensaje **`Se vendieron N.`** (N es la cantidad); si no, con un mensaje de error que sea el texto del `ValueError` (si no alcanza el stock, el que pide el paso 2: empieza con **`No alcanza el stock`**). |

En los mensajes, «título» es el título del libro, entre esas comillas
angulares: por ejemplo `Se guardó «Rayuela».`

**3.** En la **lista**:
- un buscador por título (campo **`q`**) y un desplegable para filtrar por
  autor (campo **`autor`**, que manda el id). Funcionan juntos, y después de
  buscar, el texto sigue escrito en el buscador.
- de a **10** libros por página, con links "Anterior" y "Siguiente" (campo
  **`pagina`**) que no pierdan la búsqueda (PARTE 7 de la clase).

**4.** En el formulario de libro: además de las validaciones del modelo, el
precio tiene que ser **mayor a 0** (el mensaje de error tiene que decir
"mayor a 0").

---

## Páginas de autores

| Nombre | Dirección | Qué hace |
|---|---|---|
| `autores` | `autores/` | Cada autor (link a su detalle) con cuántos libros tiene, escrito así: `2 libros` o `1 libro`. Lo cuenta la base (con `annotate`), no el template. |
| `autor` | `autores/<id>/` | Sus datos y la lista de SUS libros, cada uno con link a su detalle. |
| `crear_autor` | `autores/nuevo/` | Formulario de autor. Al guardar: va al detalle del autor. |

---

## Cómo ejecutarlo

```powershell
cd "D:\Desktop\Aprender Django"
.\entorno\Scripts\activate
cd mis_proyectos\libreria
python manage.py runserver        # dejalo prendido en ESTA terminal
```

- Abrí http://127.0.0.1:8000 en el navegador.
- Mientras programás: guardás el archivo y apretás F5 en el navegador. El
  servidor se reinicia solo cuando cambia un `.py`. Si hay un error, aparece
  en la página (pantalla amarilla) o en la terminal: leelo de abajo hacia
  arriba, arreglalo, guardá y F5.
- Para lo demás (pruebas, migraciones) abrí **otra** terminal (el **+** de la
  terminal de VS Code), activá el entorno y andá a la misma carpeta.
- En este paso no cambiás `models.py`, así que no hace falta migrar.

### Si algo no anda

| Lo que ves | Qué pasa | Qué hacer |
|---|---|---|
| `TemplateDoesNotExist` | El template no está donde Django lo busca | Tiene que estar en `libros/templates/libros/archivo.html`, y en la vista se pide como `"libros/archivo.html"` |
| `NoReverseMatch` | Un `{% url %}` o un `redirect` con un nombre que no existe, o sin el número que necesita | Revisá el `name=` en `urls.py`, el `libros:` adelante, y que le pases el id (`{% url 'libros:detalle' libro.pk %}`) |
| `Page not found (404)` con una lista de direcciones | Ninguna dirección coincide | ¿Falta la barra final `/`? ¿Está el `include` en `config/urls.py`? |
| `CSRF verification failed` | Un formulario POST sin `{% csrf_token %}` | Agregalo adentro del `<form>` |
| La página no cambia | El navegador guardó la versión vieja | Ctrl+F5 |

---

## Cómo comprobar que está bien

1. Copiá **`test_paso3.py`** a tu carpeta `libros`:

   ```powershell
   cd "D:\Desktop\Aprender Django\mis_proyectos\libreria"
   copy "..\..\paso_3_paginas_web\test_paso3.py" libros\
   ```

2. En la otra terminal (la del servidor puede seguir prendida):

   ```powershell
   python manage.py test libros.test_paso3     # solo el paso 3
   python manage.py test libros                # el 2 y el 3 juntos (el 2 tiene que seguir andando)
   ```

Cada prueba dice qué punto revisa ("1. La lista muestra los libros...").
Si falla, la última línea del bloque `FAIL` dice qué esperaba encontrar en la
página y no encontró.

La solución está en `solucion/libreria/` (con su `COMO_USARLA.md`). Mirala
recién cuando termines.
