#!/usr/bin/env bash
# Fail on errors
set -o errexit

# Instala dependencias
pip install -r requirements.txt

# Recoge archivos estáticos
python manage.py collectstatic --noinput

# Aplica migraciones
python manage.py migrate

# Crear superusuario solo si no existe
python - <<END
import os
import django

# Ajusta esto al nombre de tu proyecto (el que contiene settings.py)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tiendaback.settings")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin1234")
    print("Superusuario creado ✅")
else:
    print("El superusuario ya existe ⚠️")
END
