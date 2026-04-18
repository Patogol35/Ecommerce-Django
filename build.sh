#!/usr/bin/env bash
set -o errexit

echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo "🗂️ Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "🛠️ Aplicando migraciones..."
python manage.py migrate --noinput

echo "🧹 Limpiando datos antiguos sin variantes..."
python manage.py shell << END
from tienda.models import ItemCarrito, ItemPedido

ItemCarrito.objects.filter(variante__isnull=True).delete()
ItemPedido.objects.filter(variante__isnull=True).delete()

print("✅ Datos antiguos eliminados correctamente")
END

echo "👤 Creando superusuario si no existe..."
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
    print("✅ Superusuario creado")
else:
    print("ℹ️ El superusuario ya existe")
END

echo "🚀 Build completado correctamente"
