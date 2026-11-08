# Ejercicio paso 3 — La librería, ahora con páginas

Seguí con **tu** proyecto `libreria` del paso 2. (Si no lo terminaste, copiá
`paso_2_django_por_consola\solucion\libreria` a `mis_proyectos\` y arrancá de ahí.)

Hasta ahora todo se hacía desde el admin o la consola. Ahora hacé páginas
para que las use un empleado de la librería. **El diseño no importa**: HTML
simple alcanza (el CSS es opcional).

**Los nombres tienen que ser exactamente estos** (la prueba los busca así).

## Estructura

1. Las direcciones de la app van en **`libros/urls.py`**, con
   `app_name = "libros"`, y `config/urls.py` las incluye en la raíz (`""`).
2. Un template base con un menú (Libros, Autores, + Libro, + Autor), los
   **mensajes** y un bloque para el contenido. Todas las páginas lo heredan.

## Páginas de libros

| Nombre (`name=`) | Dirección | Qué hace |
|---|---|---|
| `lista` | `""` | Tabla con todos los libros: título (link al detalle), autor, precio y stock. Si el stock es 0, en vez del número dice **`Sin stock`**. |
| `detalle` | `libros/<id>/` | Todos los datos del libro, links a editar y borrar, y el formulario de vender. Si no existe: 404. |
| `crear` | `libros/nuevo/` | Formulario de libro. Al guardar: ir al **detalle** con el mensaje **`Se guardó «título».`** |
| `editar` | `libros/<id>/editar/` | El mismo formulario con los datos. Al guardar: al **detalle** con **`Se guardó «título».`** |
| `borrar` | `libros/<id>/borrar/` | Con GET: una página "¿Seguro que querés borrar…?" con un botón. Con POST (el botón): borra y va a la **lista** con **`Se borró «título».`** Nunca borra con GET. |
| `vender` | `libros/<id>/vender/` | Solo POST (con GET: error 405). Recibe el campo **`cantidad`** y usa `vender()` del modelo. Siempre vuelve al **detalle**: si salió bien, mensaje **`Se vendieron N.`**; si no, un mensaje de error con el texto del error (ej: "No alcanza el stock…"). |

3. En la **lista**:
   - un buscador por título (campo **`q`**) y un desplegable para filtrar por
     autor (campo **`autor`**, con el id). Funcionan juntos y después de buscar
     el texto sigue escrito en el buscador.
   - de a **10** libros por página, con links "Anterior / Siguiente" (campo
     **`pagina`**) que no pierdan la búsqueda.
4. En el formulario de libro: además de las validaciones del modelo, el precio
   tiene que ser **mayor a 0** (el error tiene que decir "mayor a 0").

## Páginas de autores

| Nombre | Dirección | Qué hace |
|---|---|---|
| `autores` | `autores/` | Cada autor (link a su detalle) con cuántos libros tiene, escrito así: `2 libros` o `1 libro` (lo cuenta la base, no el template). |
| `autor` | `autores/<id>/` | Sus datos y la lista de SUS libros, cada uno con link a su detalle. |
| `crear_autor` | `autores/nuevo/` | Formulario de autor. Al guardar: al detalle del autor. |

---

## Cómo ejecutarlo

```powershell
cd "D:\Desktop\Aprender Django"
.\entorno\Scripts\activate
cd mis_proyectos\libreria
python manage.py runserver        # dejalo prendido en ESTA terminal
```

- Abrí http://127.0.0.1:8000 en el navegador.
- Mientras programás: guardás el archivo y apretás F5. El servidor se reinicia
  solo cuando cambia un `.py`. Si hay un error, lo muestra en la terminal o en
  la página: arreglalo, guardá y F5.
- Para lo demás (pruebas, migraciones) abrí **otra** terminal, activá el
  entorno y andá a la misma carpeta.
- En este paso no cambiás `models.py`, así que no hace falta migrar.

## Cómo comprobar que está bien

1. Copiá **`test_paso3.py`** (de esta carpeta) a tu carpeta `libros`.
2. En la otra terminal:

```powershell
python manage.py test libros.test_paso3     # solo el paso 3
python manage.py test libros                # el 2 y el 3 juntos (el 2 tiene que seguir andando)
```

La solución está en `solucion/libreria/` (con su `COMO_USARLA.md`).
