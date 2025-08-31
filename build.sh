#!/usr/bin/env bash
set -o errexit

# Instala dependencias
pip install -r requirements.txt

# Archivos estáticos
python manage.py collectstatic --noinput

# Migraciones
python manage.py migrate
