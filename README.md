# API de control de ingresos

Proyecto educativo Django REST Framework para administrar funcionarios, usuarios, ingresos y bitacoras. La base local predeterminada es SQLite (`db.sqlite3`).

## Preparar y ejecutar

En PowerShell, desde la carpeta del proyecto:

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations api
python manage.py migrate
python manage.py check
python manage.py test api
python manage.py runserver
```

Para desarrollo local se usa una clave predeterminada. Antes de desplegar, define `DJANGO_SECRET_KEY` con una clave privada y configura `DEBUG=False`.

Swagger queda disponible en `http://127.0.0.1:8000/api/docs/`; el esquema OpenAPI está en `/api/schema/`. Django Admin está en `/admin/` (crear un administrador con `python manage.py createsuperuser`).

## Recursos y relaciones

- `Funcionario`: datos personales y laborales; `documento` y `correo` son únicos.
- `Usuario`: credenciales, estado, tipo y permisos. Su relación con Funcionario es uno a uno: cada funcionario puede tener como máximo una cuenta.
- `Ingreso`: historial de entradas y salidas. Muchos ingresos pueden pertenecer al mismo usuario (muchos a uno).
- `Bitacora`: acciones del sistema. Muchas acciones pueden pertenecer al mismo usuario (muchos a uno).

Las llaves foráneas `funcionario` y `usuario` guardan el identificador del registro relacionado y garantizan integridad referencial. Django ORM permite navegar, por ejemplo, de un ingreso a su usuario con `ingreso.usuario` y al funcionario con `ingreso.usuario.funcionario`. La API devuelve además `funcionario_detalle` en usuarios y `usuario_detalle` en ingresos y bitácoras. Las relaciones usan `on_delete=models.CASCADE`: borrar el padre también borra sus registros dependientes.

## Rutas CRUD

Todas las rutas usan JSON. `GET` lista o consulta un registro, `POST` crea, `PUT` reemplaza, `PATCH` modifica parcialmente y `DELETE` elimina. El identificador se coloca en la URL y los datos se envían en el cuerpo JSON.

| Recurso | Colección | Detalle |
| --- | --- | --- |
| Funcionarios | `/api/funcionarios/` | `/api/funcionarios/{id}/` |
| Usuarios | `/api/usuarios/` | `/api/usuarios/{id}/` |
| Ingresos | `/api/ingresos/` | `/api/ingresos/{id}/` |
| Bitácoras | `/api/bitacoras/` | `/api/bitacoras/{id}/` |

Orden recomendado para probar en Swagger o Postman:

1. Crear un funcionario y conservar el `id` de la respuesta.
2. Crear un usuario con ese `funcionario` y conservar su `id`.
3. Crear un ingreso y una bitácora con el `usuario`.
4. Listar cada colección y consultar cada detalle por su `id`.
5. Actualizar un campo con `PATCH` y comprobar la respuesta.
6. Eliminar un registro con `DELETE` y consultar de nuevo su detalle (debe responder `404`).

Ejemplo de creación de funcionario:

```json
{
  "nombres": "Ana",
  "apellidos": "Perez",
  "documento": "100200300",
  "cargo": "Analista",
  "telefono": "3001234567",
  "correo": "ana@example.com",
  "estado": true
}
```

Ejemplo de creación de usuario (reemplace `funcionario` por el id real):

```json
{
  "funcionario": 1,
  "username": "ana.perez",
  "password": "ClaveSegura123!",
  "tipo_usuario": "FUNCIONARIO",
  "estado": true,
  "permisos": "consultar"
}
```

En ingresos se envían `usuario` y `fecha_ingreso` en formato ISO 8601; `ip` es opcional. Para registrar la salida se modifica `fecha_salida` con una fecha ISO 8601. En bitácoras se envían `usuario`, `accion` y `descripcion`; `fecha` se genera automáticamente.

## Migraciones y base de datos

Una migración es el historial versionado de cambios en los modelos. `makemigrations` genera instrucciones de esquema y `migrate` las aplica a la base de datos configurada; permiten que el esquema evolucione de forma repetible sin crear tablas manualmente. Para inspeccionar el SQL de una migración: `python manage.py sqlmigrate api 0001` (ajuste el número según el archivo creado).

Para verificar los registros guardados, use `python manage.py shell` y consulte, por ejemplo, `Funcionario.objects.all()` o `Ingreso.objects.select_related('usuario').all()`. También se pueden inspeccionar las tablas de SQLite con un visor compatible con `db.sqlite3`.

## Conceptos para explicar

- **Modelo:** clase Python que describe campos, tipos, restricciones y relaciones; Django ORM traduce sus operaciones a consultas de base de datos.
- **Serializer:** convierte modelos y tipos Python a JSON, recibe los datos de la petición y valida campos y relaciones antes de guardar.
- **ViewSet:** agrupa las acciones de consulta, creación, actualización y eliminación; `ModelViewSet` provee las acciones CRUD estándar.
- **Router y URL:** el router enlaza las rutas de colección/detalle con las acciones del ViewSet. El parámetro `{id}` identifica el registro; el cuerpo JSON lleva los campos a crear o cambiar.
- **Llave primaria:** identifica de manera única cada fila. Django crea `id` automáticamente si no se declara otro campo primario.
- **Pruebas:** `python manage.py test api` verifica creación, listados, detalles, actualización, eliminación, relaciones y que la contraseña no se devuelve en la API y queda cifrada.

## Guion para el video

Muestra la estructura del proyecto, la configuración SQLite, los cuatro modelos y por qué cada relación es uno a uno o muchos a uno. Explica y ejecuta las migraciones; recorre serializers, ViewSets, router y rutas. En Swagger crea funcionario, usuario, ingreso y bitácora; lista y consulta detalles, actualiza y elimina al menos un registro. Al final, comprueba objetos relacionados y datos persistidos en `db.sqlite3` o con el ORM. Explica qué entra en cada petición, cómo valida el serializer y qué representa el id de la URL.

> Este proyecto es una API educativa local, no un sistema listo para producción: no implementa autenticación/autorización y las rutas no deben exponerse públicamente. La contraseña se almacena con hash y no se devuelve en respuestas; para producción se recomienda integrar el modelo de usuario y el sistema de autenticación de Django.