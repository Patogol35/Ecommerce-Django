#!/usr/bin/env bash
set -o errexit

echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo "🗂️ Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "🛠️ Aplicando migraciones..."
python manage.py migrate --noinput

echo "🧹 Limpiando datos antiguos sin variantes..."
python manage.py shell -c "from tienda.models import ItemCarrito, ItemPedido; ItemCarrito.objects.filter(variante__isnull=True).delete(); ItemPedido.objects.filter(variante__isnull=True).delete(); print('OK limpieza')"

echo "👤 Creando superusuario si no existe..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); username='admin'; User.objects.filter(username=username).exists() or User.objects.create_superuser(username=username, email='patogol3535@gmail.com', password='jorgepatricio26'); print('OK superuser')"

echo "🚀 Build completado correctamente"
