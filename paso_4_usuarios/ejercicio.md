# Ejercicio paso 4 — La librería con usuarios y reseñas

Seguí con **tu** proyecto `libreria`. (Si no terminaste el paso 3, copiá
`paso_3_paginas_web\solucion\libreria` adentro de `mis_proyectos\`.)

Ahora: cualquiera puede **mirar** los libros, pero para **cambiar** algo hay
que iniciar sesión. Y los usuarios pueden dejar una **reseña** (una opinión
con puntaje del 1 al 5) de cada libro.

> **Los nombres y los mensajes tienen que ser exactamente estos.** La prueba
> automática los busca escritos así.

---

## Antes de empezar: dónde está cada cosa en la clase

| Para los puntos | Mirá en `clase.py` |
|---|---|
| 1 a 4 (login, logout, registro, menú) | PARTE 3 (a, b, c, d, f, g) y los templates `base.html` y `registration/login.html` de la PARTE 10 |
| 5 y 6 (quién puede qué) | PARTE 3e (`@login_required`) |
| 7 (el modelo `Resenia`) | Paso 2: PARTE A4 (a y b: una sola por usuario y libro, puntaje del 1 al 5). Acá: PARTE 4 y PARTE 8a (el desempate) |
| 8 y 9 (mostrar y guardar reseñas) | Paso 3: PARTE 5 (`save(commit=False)`) y PARTE 6 (mensajes). Paso 2: PARTE B6 (el promedio con `aggregate`) |
| 10 (borrar solo las propias) | PARTE 4 (`get_object_or_404(..., usuario=request.user)`) |
| 11 (Mis reseñas) | PARTE 5 (`ListView`, `get_queryset`, `LoginRequiredMixin`) |
| 12 (admin) | Paso 2: PARTE A6 |

---

## Dónde va cada cosa nueva

```text
mis_proyectos\libreria\
├── config\
│   ├── settings.py       <- LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL (y 'DIRS' si usás una carpeta templates en la raíz)
│   └── urls.py           <- path('cuentas/', include('django.contrib.auth.urls')) y la dirección del registro
└── libros\
    ├── models.py         <- el modelo Resenia
    ├── forms.py          <- el formulario de la reseña
    ├── views.py          <- @login_required, las vistas de reseñas y la ListView
    └── templates\
        ├── registration\
        │   ├── login.html      <- el login de Django lo busca acá, con este nombre exacto
        │   └── registro.html   <- (este nombre lo elegís vos)
        └── libros\
            └── ...
```

(Un template en `libros/templates/registration/login.html` funciona: Django
busca en las carpetas `templates` de todas las apps. También podés hacer una
carpeta `templates` en la raíz del proyecto, con `'DIRS'` en settings: PARTE 3a.)

---

## Login, logout y registro

**1.** Las páginas de login y logout de Django en `cuentas/` (o sea,
`cuentas/login/` y `cuentas/logout/`), con tu template de login.

**2.** En la configuración: si hace falta iniciar sesión, se va a la página de
login. Después de entrar, y después de salir, se va a la **lista de libros**.

**3.** Registrarse: dirección `cuentas/registro/` con **`name="registro"`** (sin
`libros:` adelante: va en `config/urls.py`, ver la PARTE 3g de la clase). Usá
el formulario de usuario que trae Django. Al registrarse, el usuario queda
con la sesión iniciada y va a la lista de libros.

**4.** En el menú: si inició sesión, **`Hola, (usuario)`** (por ejemplo
`Hola, ana`) y un botón **Salir**. Si no, links **Entrar** y **Registrarme**.

---

## Quién puede qué

**5.** **Mirar** (la lista, el detalle de un libro, los autores, el detalle de
un autor): cualquiera, con o sin sesión.

**6.** **Crear, editar, borrar y vender libros, y crear autores**: solo con
sesión iniciada. Sin sesión, te manda al login (y después de entrar, vuelve
a donde querías ir: eso lo hace solo el `?next=`).

---

## Reseñas

**7.** Un modelo nuevo, **`Resenia`** (sin ñ, como `anio`):
- `usuario`: quién la escribió. Si se borra el usuario, se borran sus
  reseñas. Desde un usuario: `usuario.resenias`.
- `libro`: de qué libro. Si se borra el libro, se borran sus reseñas. Desde
  un libro: `libro.resenias`.
- `puntaje`: un entero del 1 al 5.
- `texto`.
- `creada`: fecha y hora, que se pone sola.
- ordenadas de la más nueva a la más vieja (pensá en el desempate: PARTE 8a).
- un usuario puede escribir **una sola** reseña por libro: que **la base**
  no deje guardar dos (no alcanza con revisarlo en la vista).

Es un modelo nuevo: `makemigrations` y `migrate`.

**8.** En el **detalle del libro**:
- las reseñas: quién, el puntaje y el texto
- el **puntaje promedio** (por ejemplo, con un 5 y un 2, `3,5`)
- si iniciaste sesión y todavía no opinaste sobre ese libro: un formulario
  para dejar tu reseña (que se manda a la dirección del punto 9)
- si no iniciaste sesión: un link que diga **`Entrá para opinar`** (al login)

**9.** **Guardar la reseña**: dirección `libros/<id>/resenia/`, con
**`name="resenia"`**. Solo POST y solo con sesión. El usuario y el libro los
pone la vista (no vienen en el formulario). Siempre vuelve al detalle del libro:
- si salió bien, con el mensaje **`¡Gracias por tu reseña!`**
- si ya habías opinado sobre ese libro, con el error **`Ya opinaste sobre este libro.`**
- si el puntaje no es del 1 al 5, no se guarda

**10.** **Borrar una reseña**: dirección `resenias/<id>/borrar/`, con
**`name="borrar_resenia"`**. Solo POST, solo con sesión y **solo tus propias
reseñas** (si intentás borrar la de otro: 404). Vuelve al detalle del libro.

**11.** **Mis reseñas**: dirección `mis-resenias/`, con
**`name="mis_resenias"`**, solo con sesión: la lista de TUS reseñas (cada una
con el libro, con link a su detalle, el puntaje y el texto). Hacela con una
**vista de clase** (`ListView`). Su template, si no le decís otro nombre, es
`libros/resenia_list.html` (PARTE 5 de la clase).

**12.** `Resenia` en el admin.

---

## Cómo ejecutarlo

```powershell
cd "D:\Desktop\Aprender Django"
.\entorno\Scripts\activate
cd mis_proyectos\libreria
python manage.py makemigrations       # por el modelo nuevo
python manage.py migrate
python manage.py runserver
```

Para probar con **dos usuarios a la vez**: uno en una ventana normal y otro
en una ventana de incógnito (Ctrl+Shift+N). Registrá uno nuevo desde tu
página. Probá entrar a la dirección de borrar una reseña de otro: tiene que
dar 404.

---

## Cómo comprobar que está bien

1. Copiá **`test_paso4.py`** a tu carpeta `libros`:

   ```powershell
   copy "..\..\paso_4_usuarios\test_paso4.py" libros\
   ```

2. Corré la prueba:

   ```powershell
   python manage.py test libros.test_paso4     # solo el paso 4
   python manage.py test libros                # los pasos 2, 3 y 4 juntos (los anteriores tienen que seguir andando)
   ```

**Ojo con las pruebas del paso 3:** ahora crear, editar, borrar y vender piden
sesión, y la prueba del paso 3 entra con un usuario antes de probarlos. Si
una del paso 3 falla porque la manda al login, revisá que sea solo lo que
el punto 6 dice que pide sesión (mirar tiene que seguir siendo libre).

La solución está en `solucion/libreria/` (con su `COMO_USARLA.md`). Mirala
recién cuando termines.
