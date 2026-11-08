# Ejercicio paso 4 — La librería con usuarios y reseñas

Seguí con **tu** proyecto `libreria`. (Si no terminaste el paso 3, copiá
`paso_3_paginas_web\solucion\libreria` a `mis_proyectos\`.)

Ahora: cualquiera puede **mirar** los libros, pero para **cambiar** algo hay que
iniciar sesión. Y los usuarios pueden dejar una **reseña** (opinión con
puntaje) de cada libro. **Los nombres tienen que ser exactamente estos.**

## Login, logout y registro

1. Las páginas de login y logout de Django en `cuentas/` (o sea
   `cuentas/login/` y `cuentas/logout/`), con tu template de login.
2. En la configuración: si hace falta iniciar sesión se va a la página de
   login; después de entrar y después de salir, a la **lista de libros**.
3. Registrarse: dirección `cuentas/registro/` con **`name="registro"`** (sin
   `libros:` adelante). Con el formulario de usuario que trae Django. Al
   registrarse queda con la sesión iniciada y va a la lista de libros.
4. En el menú: si inició sesión, **`Hola, (usuario)`** y un botón **Salir**; si
   no, links **Entrar** y **Registrarme**.

## Quién puede qué

5. **Mirar** (lista, detalle, autores, detalle de autor): cualquiera, con o sin sesión.
6. **Crear, editar, borrar y vender libros, y crear autores**: solo con sesión
   iniciada. Sin sesión, te manda al login (y después de entrar, vuelve a donde
   querías ir).

## Reseñas

7. Modelo **`Resenia`**:
   - `usuario` (quién la escribió; si se borra el usuario, se borran sus
     reseñas; desde un usuario: `usuario.resenias`)
   - `libro` (de qué libro; si se borra el libro, se borran; desde un libro:
     `libro.resenias`)
   - `puntaje` (entero del 1 al 5)
   - `texto`
   - `creada` (fecha y hora, sola)
   - ordenadas de la más nueva a la más vieja
   - un usuario puede escribir **una sola** reseña por libro (que la base no deje dos)
8. En el **detalle del libro**: las reseñas (quién, puntaje y texto) y el
   **puntaje promedio**. Si iniciaste sesión y todavía no opinaste: un
   formulario para dejar tu reseña. Si no iniciaste sesión: un link "Entrá para opinar".
9. **Guardar la reseña**: dirección `libros/<id>/resenia/`,
   **`name="resenia"`**. Solo POST y solo con sesión. El usuario lo pone la vista
   (no el formulario). Siempre vuelve al detalle del libro: si salió bien, con el
   mensaje **`¡Gracias por tu reseña!`**; si ya habías opinado, con el error
   **`Ya opinaste sobre este libro.`**; si el puntaje no es del 1 al 5, no se guarda.
10. **Borrar una reseña**: dirección `resenias/<id>/borrar/`,
    **`name="borrar_resenia"`**. Solo POST, solo con sesión y **solo tus propias
    reseñas** (la de otro: 404). Vuelve al detalle del libro.
11. **Mis reseñas**: dirección `mis-resenias/`, **`name="mis_resenias"`**, solo
    con sesión: la lista de TUS reseñas (libro con link, puntaje, texto). Hacela
    con una **vista de clase** (`ListView`).
12. `Resenia` en el admin.

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

Para probar con **dos usuarios a la vez**: uno en una ventana normal y otro en
una ventana de incógnito (Ctrl+Shift+N). Registrá uno nuevo desde la página.

## Cómo comprobar que está bien

1. Copiá **`test_paso4.py`** a tu carpeta `libros`.
2. `python manage.py test libros.test_paso4` (o `python manage.py test libros`
   para ver que los pasos 2 y 3 siguen andando).

La solución está en `solucion/libreria/` (con su `COMO_USARLA.md`).
