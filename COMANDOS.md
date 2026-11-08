# Guía de comandos: cómo se ejecuta TODO

Todo esto se escribe en una **terminal**. En Windows: PowerShell (o la
terminal de VS Code: menú *Terminal → New Terminal*). Lo que va después de
`#` es una explicación, no se escribe.

---

## 0. Moverse entre carpetas

```powershell
pwd                                   # ¿en qué carpeta estoy?
ls                                    # ¿qué hay acá?
cd "D:\Desktop\Aprender Django"       # ir a una carpeta (comillas si tiene espacios)
cd paso_1_base_de_datos               # entrar a una subcarpeta
cd ..                                 # volver a la carpeta de arriba
mkdir mis_proyectos                   # crear una carpeta
```

Truco: escribí las primeras letras y apretá **Tab**: completa el nombre solo.

---

## 1. El entorno virtual (una vez por carpeta de trabajo)

Un **entorno virtual** es una "caja" con su propio Python y sus paquetes
(Django, etc.). Así cada proyecto tiene sus versiones y no se mezclan.
**Los pasos 0 y 1 no lo necesitan** (alcanza con Python); hace falta desde el paso 2.

```powershell
cd "D:\Desktop\Aprender Django"
python -m venv entorno                # crea la caja (una carpeta "entorno")
.\entorno\Scripts\activate            # ENTRAR a la caja
pip install django                    # instalar Django adentro
pip install pillow                    # para subir imágenes (paso 5 y proyecto final)
pip install "psycopg[binary]"         # solo si vas a usar PostgreSQL
pip list                              # ver qué hay instalado
deactivate                            # salir de la caja (cuando termines)
```

- Sabés que estás adentro porque la línea empieza con **(entorno)**.
- **Cada terminal nueva arranca afuera**: volvé a hacer `.\entorno\Scripts\activate`.
- Si al activar sale *"la ejecución de scripts está deshabilitada"*, una sola vez:
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (y respondé S).
- Si dice *"No module named django"*: no activaste el entorno.
- En VS Code: `Ctrl+Shift+P` → *Python: Select Interpreter* → elegí el de
  `entorno`. Así el editor también "ve" Django y te autocompleta.

Para pasarle a alguien tu proyecto con sus paquetes:
```powershell
pip freeze > requirements.txt         # anota los paquetes y versiones
pip install -r requirements.txt       # (en la otra compu) los instala todos
```

---

## 2. Ejecutar un archivo de Python suelto

```powershell
python clase.py                       # ejecuta el archivo
python solucion.py
```
Si el programa pide algo con `input()`, escribilo y apretá Enter.
Para cortar un programa que no termina: **Ctrl+C**.

---

## 3. Crear un proyecto Django

```powershell
mkdir mi_proyecto
cd mi_proyecto
django-admin startproject config .    # crea manage.py y la carpeta config (¡el punto!)
python manage.py startapp nombreapp   # crea una app (después agregala en settings.py)
```

Sin el punto, `startproject` crea una carpeta de más adentro (`config/config/`)
y es un lío. Si te pasó, borrá todo y empezá de nuevo.

---

## 4. Los comandos de `manage.py`

Todos se escriben **en la carpeta donde está `manage.py`** y con el entorno activado.

| Comando | Qué hace | Cuándo |
|---|---|---|
| `python manage.py runserver` | Prende el servidor de desarrollo. Abrí **http://127.0.0.1:8000** en el navegador. Se corta con **Ctrl+C**. Se reinicia solo cuando guardás un `.py`. | Para ver tus páginas |
| `python manage.py runserver 8080` | Lo mismo en otro puerto (si el 8000 está ocupado) | |
| `python manage.py makemigrations` | Escribe el "plan" de cambios de tus modelos (no toca la base) | Cada vez que cambiás `models.py` |
| `python manage.py migrate` | Aplica los planes: crea o cambia las tablas | Después de `makemigrations`, y la primera vez en un proyecto nuevo |
| `python manage.py showmigrations` | Lista las migraciones: `[X]` aplicada, `[ ]` pendiente | Si algo de la base no cuadra |
| `python manage.py sqlmigrate app 0001` | Muestra el SQL que ejecutaría esa migración | Para aprender / curiosear |
| `python manage.py createsuperuser` | Crea un usuario administrador (para `/admin`). La contraseña no se ve mientras la escribís: es normal. | Una vez por base |
| `python manage.py changepassword usuario` | Cambia la contraseña de un usuario | Si te la olvidaste |
| `python manage.py shell` | Una consola de Python con tu proyecto cargado, para probar el ORM. Se sale con `exit()` | Para probar consultas |
| `python manage.py test` | Ejecuta las pruebas automáticas (`tests.py`) en una base aparte | Antes de dar algo por terminado |
| `python manage.py test nombreapp` | Solo las pruebas de una app | |
| `python manage.py check` | Busca errores de configuración sin prender nada | Si algo no arranca |
| `python manage.py dbshell` | Abre la consola SQL de la base (necesita el programa de la base instalado) | |
| `python manage.py flush` | **Borra TODOS los datos** (deja las tablas vacías). Cuidado. | Para empezar de cero |

### Un script propio que usa tus modelos
Un archivo al lado de `manage.py` que empieza con:
```python
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
```
y se ejecuta con `python mi_script.py` (desde la carpeta de `manage.py`).

---

## 5. El ciclo de trabajo de todos los días

```text
1. Abrir la terminal en la carpeta del proyecto
2. .\entorno\Scripts\activate            (o el entorno de tu carpeta)
3. python manage.py runserver            (y lo dejás corriendo)
4. Abrir OTRA terminal (botón + en VS Code) para los demás comandos
5. ¿Cambiaste models.py?  ->  makemigrations  ->  migrate
6. ¿Cambiaste views/urls/templates?  ->  solo recargá el navegador (F5)
7. ¿Agregaste un archivo .css/.js?  ->  F5 (si no cambia: Ctrl+F5, el navegador lo tenía guardado)
8. Antes de cerrar:  python manage.py test
```

---

## 5b. Las pruebas automáticas de los ejercicios

**Pasos 0 y 1** (Python suelto): tu archivo `mi_solucion.py` va en la carpeta del paso.

```powershell
cd "D:\Desktop\Aprender Django\paso_0_python"
python prueba.py                 # prueba tu mi_solucion.py
python prueba.py solucion        # (al final) la solución
```

**Pasos 2 a 6** (la librería): la prueba se copia ADENTRO de tu app y se corre con `manage.py`.

```powershell
cd "D:\Desktop\Aprender Django\mis_proyectos\libreria"
copy "..\..\paso_2_django_por_consola\test_paso2.py" libros\      # copiar la prueba a tu app
python manage.py test libros.test_paso2                            # solo esa
python manage.py test libros                                       # todas las que copiaste
python manage.py test libros -v 2                                  # con el nombre de cada prueba
```

**Proyecto final**: igual, con las de `proyecto_final\pruebas\` y tu app `clinica`:

```powershell
cd "D:\Desktop\Aprender Django\mis_proyectos\veterinaria"
copy "..\..\proyecto_final\pruebas\test_etapa1_proyecto.py" clinica\
python manage.py test clinica.test_etapa1_proyecto
```

Cómo leer el resultado:
- `OK` al final = todo bien.
- `FAILED (failures=2)` = 2 pruebas fallaron. Arriba de eso, cada `FAIL:` dice
  cuál, con su explicación, y un `AssertionError` con lo que esperaba y lo que
  encontró (por ejemplo, `'Sin stock' not found in ...`).
- `ERROR:` = tu código tiró un error (el detalle está igual que cuando falla
  una página: leelo de abajo hacia arriba).
- Las pruebas usan una base de datos APARTE y vacía: no tocan tus datos.

---

## 6. Ver la base de datos con tus ojos

- **SQLite**: el archivo `db.sqlite3` se abre con **DBeaver** (lo tenés):
  *Nueva conexión → SQLite → Path: el archivo `db.sqlite3`*. Ahí ves las tablas.
- **PostgreSQL**: en DBeaver, *Nueva conexión → PostgreSQL*, con host
  `localhost`, puerto `5432`, tu usuario y clave.
- Las tablas de Django se llaman `app_modelo` (ej: `libros_libro`).

---

## 7. Cuando algo falla (los errores más comunes)

| Mensaje | Qué significa | Arreglo |
|---|---|---|
| `No module named 'django'` | Entorno no activado | `.\entorno\Scripts\activate` |
| `no such table: app_modelo` | No hiciste las migraciones | `makemigrations` + `migrate` |
| `You have N unapplied migration(s)` | Falta `migrate` | `python manage.py migrate` |
| `TemplateDoesNotExist` | El template no está donde Django lo busca | `app/templates/app/archivo.html` y la app en `INSTALLED_APPS` |
| `NoReverseMatch` | Un `{% url %}` o `redirect` con un nombre que no existe o le faltan datos | Revisá `name=` en urls.py y el `app_name:` |
| `Page not found (404)` | Ninguna URL coincide | Mirá la lista que muestra Django: ¿falta la barra final `/`? ¿el `include`? |
| `CSRF verification failed` | Formulario POST sin `{% csrf_token %}` | Agregalo adentro del `<form>` |
| `That port is already in use` | Ya hay un `runserver` prendido (quizás en otra terminal) | Cerralo con Ctrl+C o usá otro puerto |
| `IntegrityError ... UNIQUE` / `NOT NULL` | Rompiste una regla de la tabla | Revisá los datos que mandás |
| `ProtectedError` | Querés borrar algo que tiene cosas relacionadas con `PROTECT` | Borrá primero lo relacionado |
| Cambié el modelo y "no pasa nada" | Falta migrar | `makemigrations` + `migrate` |
| La página no cambia | El navegador guardó la versión vieja | Ctrl+F5 |

Leé el error **de abajo hacia arriba**: la última línea dice qué pasó. Más
arriba, buscá la primera línea que sea de TU código (no de `site-packages`):
ahí está el problema.

---

## 8. Volver atrás un archivo del curso (git)

El curso está guardado en git. Tu trabajo (`mis_proyectos/`, los
`mi_solucion.py`, el `entorno`, las bases) **no** se guarda ahí: está en el
`.gitignore` y queda solo en tu compu.

```powershell
cd "D:\Desktop\Aprender Django"
git status                                  # ¿toqué algún archivo del curso? (si no dice nada, no)
git restore paso_0_python\clase.py          # deja ESE archivo como era originalmente
git restore .                               # deja TODOS los archivos del curso como eran
                                            # (tu trabajo no se toca: git lo ignora)
git pull                                    # trae las correcciones nuevas del curso, si las hay
```

Para empezar de cero en otra compu: `git clone` con la dirección del
repositorio, y después "Preparar la compu" del `LEEME.md`.
