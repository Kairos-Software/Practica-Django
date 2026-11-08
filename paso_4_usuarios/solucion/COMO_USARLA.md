# Solución paso 4

`libreria/` es el proyecto del paso 3 con usuarios y reseñas.

## Qué se agregó (compará con lo tuyo)

| Archivo | Qué tiene |
|---|---|
| `config/settings.py` | `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` (al final) |
| `config/urls.py` | `cuentas/` (login y logout de Django) y `cuentas/registro/` |
| `libros/models.py` | `Resenia` con validadores 1 a 5 y `UniqueConstraint` (una por usuario y libro) |
| `libros/migrations/0002_resenia.py` | lo escribió `makemigrations` |
| `libros/forms.py` | `ReseniaForm` (sin usuario ni libro) |
| `libros/views.py` | `@login_required` en lo que cambia datos; `resenia`, `borrar_resenia`, `MisResenias` (vista de clase) y `registro` |
| `libros/urls.py` | las 3 direcciones de reseñas |
| `libros/templates/registration/` | `login.html` y `registro.html` |
| `libros/templates/libros/` | `base.html` (menú con usuario), `detalle.html` (reseñas), `resenia_list.html` (mis reseñas) |
| `libros/test_paso4.py` | la prueba |

## Para probarla

```powershell
cd "D:\Desktop\Aprender Django\paso_4_usuarios\solucion\libreria"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py test libros        # pasos 2, 3 y 4 (44 pruebas)
```

## Para mirar con atención

- **El orden de los decoradores en `vender`**: primero `@login_required` y
  después `@require_POST`. Al revés, alguien sin sesión que entra con GET
  recibiría "405" en vez de ir al login.
- **`get_object_or_404(Resenia, pk=pk, usuario=request.user)`**: así nadie
  borra la reseña de otro cambiando el número en la dirección. Para Django, la
  de otro "no existe".
- **`form.save(commit=False)`** en `resenia`: el formulario no trae ni el
  usuario ni el libro, así que se completan antes de guardar.
- **"Ya opinaste" se revisa ANTES de guardar**, para mostrar un mensaje lindo.
  Igual la `UniqueConstraint` de la base es la última defensa (si dos pedidos
  llegan juntos).
- **`?next={{ request.path }}`** en "Entrá para opinar": después de entrar, te
  devuelve al libro.
- **`MisResenias`** es una vista de clase: no tiene `render` ni template
  elegido, porque usa `libros/resenia_list.html` por convención y le pasa la
  lista como `object_list`.
