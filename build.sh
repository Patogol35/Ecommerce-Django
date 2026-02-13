#!/usr/bin/env bash
# Fail on errors
set -o errexit

# =========================
# Instalar dependencias
# =========================
pip install -r requirements.txt

# =========================
# Recoger archivos estáticos
# =========================
python manage.py collectstatic --noinput

# =========================
# Aplicar migraciones
# =========================
python manage.py migrate

# =========================
# Iniciar servidor con Gunicorn
# =========================
gunicorn tienda_backend.wsgi:application
