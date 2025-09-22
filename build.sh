#!/usr/bin/env bash
# fail on errors
set -o errexit

echo "🔹 Instalando dependencias..."
pip install -r requirements.txt

echo "🔹 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "🔹 Eliminando migraciones viejas..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

echo "🔹 Generando nuevas migraciones..."
python manage.py makemigrations

echo "🔹 Aplicando migraciones..."
python manage.py migrate --fake-initial

echo "🔹 Creando superusuario si no existe..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin1234")
    print("✅ Superusuario creado: admin / admin1234")
else:
    print("ℹ️ Superusuario ya existe, no se creó otro.")
END

echo "✅ Deploy terminado con éxito"
