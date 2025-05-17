#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Colectar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones
python manage.py migrate

# Crear superusuario usando el comando personalizado
python manage.py create_superuser