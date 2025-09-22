#!/usr/bin/env bash
# fail on errors
set -o errexit

# Instala dependencias
pip install -r requirements.txt

# Recoge archivos estáticos
python manage.py collectstatic --noinput

# Genera migraciones (muy importante cuando cambias modelos)
python manage.py makemigrations --noinput

# Aplica migraciones
python manage.py migrate --noinput

# Crear superusuario automático si no existe
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin1234")
END
