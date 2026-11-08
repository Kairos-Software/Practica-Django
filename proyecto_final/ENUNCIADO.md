# Proyecto final — Veterinaria "Patitas"

Un sistema para una veterinaria de barrio: los dueños, sus mascotas, las
vacunas y cada visita (con lo que se cobró). **De cero, solo vos.** Sin IA y
sin mirar la solución. Tenés las clases de los pasos 0 a 6, `COMANDOS.md` y la
documentación de Django.

Hacelo **por etapas**. Al terminar cada una, corré su prueba (ver "Cómo
comprobar", al final) y no sigas hasta que dé OK.

> Los **nombres** (de archivos, modelos, campos, direcciones) y los
> **mensajes** marcados en `código` tienen que ser exactamente esos: las
> pruebas los buscan así. El CÓMO hacerlo lo decidís vos.

---

## Etapa 1 — El proyecto

- Carpeta `mis_proyectos\veterinaria`, configuración en **`config`**, una app **`clinica`**.
- Idioma `es-ar`, zona horaria `America/Argentina/Buenos_Aires`, SQLite.
- Una carpeta **`templates`** en la raíz del proyecto, que Django use.
- Los archivos subidos en la carpeta `media`, con la dirección **`/media/`**.

## Etapa 2 — Los modelos (`clinica/models.py`)

**`Duenio`**: `nombre`, `telefono`, `email` (opcional), `direccion` (opcional).
Ordenados por nombre.

**`Vacuna`**: `nombre` (sin repetir). Ordenadas por nombre.

**`Mascota`**:
- `nombre`
- `especie`: opciones fijas, con estos valores guardados y textos:
  `perro` "Perro", `gato` "Gato", `ave` "Ave", `conejo` "Conejo", `otro` "Otro"
- `raza` (opcional)
- `nacimiento` (fecha, opcional; no puede ser en el futuro)
- `foto` (imagen, opcional, en la subcarpeta `mascotas/`)
- `duenio`: si un dueño tiene mascotas, **no se lo puede borrar**. Desde un dueño: `duenio.mascotas`.
- `vacunas`: varias. Desde una vacuna: `vacuna.mascotas`.
- ordenadas por nombre
- un método **`edad(hoy=None)`** que devuelve un texto. `hoy` es la fecha
  contra la que se calcula; si no se la pasan, es la de hoy.
  - sin fecha de nacimiento: `Edad desconocida`
  - menos de 1 mes: `Recién nacido`
  - de 1 a 11 meses: `1 mes`, `7 meses`...
  - 12 meses o más: `1 año`, `3 años`...
  - (un mes se cumple el mismo día del mes: del 11/2 al 10/10 son 7 meses, no 8)

**`Visita`**:
- `mascota`: si se borra la mascota, se borran sus visitas. Desde una mascota: `mascota.visitas`.
- `fecha`: por defecto la de hoy; no puede ser en el futuro
- `motivo`, `diagnostico` (opcional)
- `costo`: plata, con 2 decimales, no negativo
- `pagada`: por defecto no
- `atendida_por`: el usuario que la cargó. Si se borra el usuario, la visita
  queda (sin ese dato).
- ordenadas de la más nueva a la más vieja

Mensajes de validación:
- `La fecha de nacimiento no puede ser en el futuro.`
- `La visita no puede ser en el futuro.`

## Etapa 3 — El admin

- Todo en el admin.
- **Dueño**: sus mascotas editables adentro (inline).
- **Mascota**: sus visitas adentro (inline); filtro por `especie`; buscador por
  `nombre` y por el nombre del dueño; el selector cómodo para `vacunas`.
- **Visita**: `pagada` editable desde la lista.
- Cargá datos de prueba (o hacé un script `cargar_ejemplos.py`).

## Etapa 4 — Usuarios

- **Todas** las páginas de la app (y la API) piden haber iniciado sesión.
- Login y logout de Django en **`cuentas/`**. **No** hay página de registro: los
  usuarios los crea el administrador desde el admin.
- En el menú: el nombre de quien está trabajando y el botón para salir.
- Después de entrar: el inicio. Después de salir: el login.

## Etapa 5 — Las páginas

Todas heredan de un template base con menú y mensajes. El diseño es libre (con
HTML simple alcanza). Usá vistas de función Y de clase (de las dos).
Direcciones en `clinica/urls.py` con **`app_name = "clinica"`**:

| `name` | Dirección | Qué hace |
|---|---|---|
| `inicio` | `""` | Total de mascotas y cuántas de cada especie; visitas de este mes; lo **cobrado este mes** (visitas pagadas del mes); la **deuda total** (visitas sin pagar); las últimas 5 visitas. |
| `duenios` | `duenios/` | Lista con buscador (`q`: nombre o teléfono), cuántas mascotas tiene cada uno y **cuánto debe** (calculado por la base). |
| `duenio` | `duenios/<id>/` | Datos, sus mascotas, su deuda, y un botón "Agregar mascota" que abre el formulario de mascota **con ese dueño ya elegido**. |
| `crear_duenio` | `duenios/nuevo/` | Formulario. El teléfono solo puede tener números, espacios, guiones y un `+` al principio; si no: `Solo números, espacios, guiones y un + al principio.` |
| `editar_duenio` | `duenios/<id>/editar/` | Igual que crear, sobre uno existente. |
| `borrar_duenio` | `duenios/<id>/borrar/` | GET: confirmación. POST: borra. Si tiene mascotas no se borra y vuelve a su detalle con un mensaje que diga `tiene mascotas`. |
| `mascotas` | `mascotas/` | Buscador (`q`) que encuentra por nombre de la mascota **o** del dueño; filtro por `especie`; de a 12 por página (`pagina`) sin perder los filtros; la foto chiquita si tiene. |
| `mascota` | `mascotas/<id>/` | Todo: datos, edad, dueño (link), vacunas, foto, historial de visitas con el total gastado, y un **formulario para cargar una visita ahí mismo** (POST a esta misma dirección; quien la atiende = el usuario con sesión). Cada visita sin pagar con un botón "Marcar pagada". |
| `crear_mascota` | `mascotas/nueva/` | Formulario con foto y vacunas con casillas. Con `?duenio=<id>` arranca con ese dueño elegido. |
| `editar_mascota` | `mascotas/<id>/editar/` | Igual, sobre una existente. |
| `borrar_mascota` | `mascotas/<id>/borrar/` | GET: confirmación. POST: borra (con sus visitas). |
| `pagada` | `visitas/<id>/pagada/` | Solo POST: marca la visita como pagada y vuelve a la ficha de la mascota (o a la página de deudas, si vino de ahí). |
| `deudas` | `deudas/` | Todas las visitas sin pagar (mascota, dueño, teléfono, fecha, costo), el total, y el botón "Marcar pagada". |
| `api_mascota` | `api/mascotas/<id>/` | JSON (abajo). |

Todo lo que no existe da 404. Cada acción muestra un mensaje.

**La API** (`api_mascota`, con sesión) devuelve:

```json
{"id": 1, "nombre": "Toby", "especie": "Perro", "edad": "6 años",
 "duenio": {"nombre": "Lucía Pérez", "telefono": "+54 9 11 5555-1234"},
 "vacunas": ["Antirrábica", "Séxtuple"],
 "visitas": [{"fecha": "2026-10-08", "motivo": "Control anual", "costo": "8000.00", "pagada": false}]}
```

(`especie` con el texto lindo; `costo` como texto; `fecha` como `año-mes-día`;
las visitas en su orden: la más nueva primero. Si no existe: 404 en JSON
`{"error": "No existe esa mascota."}`.)

## Etapa 6 — Terminarlo bien

- Tus propias pruebas en `clinica/tests.py` (aunque ya tengas las nuestras: escribir
  pruebas también se aprende).
- Que se pueda usar desde el celular sin que se rompa (alcanza con la línea
  `<meta name="viewport" ...>` del HTML básico).

## Extras (si querés ir más lejos)

- Pasarlo a **PostgreSQL**, con la clave de la base en una variable de entorno.
- Un botón que **descargue las visitas del mes en CSV** (como en el paso 5).
- En la ficha, avisar si la mascota **no tiene la Antirrábica**.
- Subirlo a GitHub con un `.gitignore` (afuera: la base, `media/` y el entorno).

---

## Cómo ejecutar cada cosa

```powershell
cd "D:\Desktop\Aprender Django"
.\entorno\Scripts\activate
cd mis_proyectos
mkdir veterinaria
cd veterinaria
django-admin startproject config .
python manage.py startapp clinica
#   etapa 2:
python manage.py makemigrations
python manage.py migrate
#   etapa 3:
python manage.py createsuperuser
python manage.py runserver           # http://127.0.0.1:8000/admin
#   etapas 4 y 5: con el servidor prendido, guardás y F5
```

Cada vez que toques `models.py`: `makemigrations` + `migrate`.

## Cómo comprobar (las pruebas por etapa)

En la carpeta `pruebas\` hay una prueba por etapa. Copiá la de la etapa que
terminaste a tu carpeta `clinica` y corréla (desde la carpeta de `manage.py`):

| Al terminar la etapa | Copiá | Y corré |
|---|---|---|
| 1 | `test_etapa1_proyecto.py` | `python manage.py test clinica.test_etapa1_proyecto` |
| 2 | `test_etapa2_modelos.py` | `python manage.py test clinica.test_etapa2_modelos` |
| 3 | `test_etapa3_admin.py` | `python manage.py test clinica.test_etapa3_admin` |
| 4 | `test_etapa4_usuarios.py` | `python manage.py test clinica.test_etapa4_usuarios` (necesita las URLs de la etapa 5 escritas, aunque las vistas estén vacías) |
| 5 | `test_etapa5_paginas.py` y `test_etapa5_api.py` | `python manage.py test clinica` (todas juntas) |

Al final, `python manage.py test clinica` tiene que dar **OK** con todas.

**Cuando termines**, compará con `solucion/`. No tiene que ser igual: si pasa
todas las pruebas y lo entendés, está aprobado. 🐾
