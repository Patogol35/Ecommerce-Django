#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

# ⚠️ QUITA makemigrations en producción
python manage.py migrate --noinput

# Crear superusuario automático
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

username = "admin"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email="patogol3535@gmail.com",
        password="jorgepatricio26"
    )
END
