# filters.py
import django_filters
from .models import Producto

class ProductoFilter(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    stock_min = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock_max = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')
    categoria = django_filters.NumberFilter(field_name='categoria__id')  # 🔹 filtra por ID de categoría
    categoria_nombre = django_filters.CharFilter(field_name='categoria__nombre', lookup_expr='icontains')  # 🔹 filtra por nombre

    class Meta:
        model = Producto
        fields = ['precio_min', 'precio_max', 'stock_min', 'stock_max', 'categoria', 'categoria_nombre']
