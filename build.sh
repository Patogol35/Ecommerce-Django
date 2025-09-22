#!/usr/bin/env bash
set -o errexit

# Instala dependencias
pip install -r requirements.txt

# Recoge archivos estáticos
python manage.py collectstatic --noinput

# ⚠️ En PRODUCCIÓN solo se APLICAN migraciones
# NUNCA se generan en el servidor
python manage.py migrate --noinput

# Crear superusuario si no existe
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin1234")
END
