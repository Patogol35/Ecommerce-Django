#!/usr/bin/env bash
set -o errexit

# Instala dependencias
pip install -r requirements.txt

# Archivos estáticos
python manage.py collectstatic --noinput

# Migraciones
python manage.py migrate

# Crear superusuario solo si no existe
python - <<END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "Gabycobo12")
    print("Superusuario creado ✅")
else:
    print("El superusuario ya existe ⚠️")
END
