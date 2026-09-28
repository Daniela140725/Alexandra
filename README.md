# Consultas Directas API

API en Django para gestionar proveedores y compras con operaciones CRUD, búsqueda y filtros.

## Requisitos
- Python 3.10+
- Virtualenv

## Instalación
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Endpoints principales
- Proveedores: `/api/proveedores/`
- Compras: `/api/compras/`
- Swagger: `/swagger/`
- Redoc: `/redoc/`

## Funcionalidades
- Registrar, listar, consultar, actualizar y eliminar proveedores.
- Buscar proveedores por nombre.
- Registrar, listar, consultar, actualizar y eliminar compras.
- Filtrar compras por fecha, proveedor, valor mínimo y máximo.
