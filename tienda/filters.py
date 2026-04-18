import django_filters
from .models import Producto


class ProductoFilter(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(method='filter_precio_min')
    precio_max = django_filters.NumberFilter(method='filter_precio_max')
    stock_min = django_filters.NumberFilter(method='filter_stock_min')
    stock_max = django_filters.NumberFilter(method='filter_stock_max')
    categoria = django_filters.NumberFilter(field_name='categoria__id')

    class Meta:
        model = Producto
        fields = ['precio_min', 'precio_max', 'stock_min', 'stock_max', 'categoria']

    def filter_precio_min(self, queryset, name, value):
        return queryset.filter(variantes__precio__gte=value).distinct()

    def filter_precio_max(self, queryset, name, value):
        return queryset.filter(variantes__precio__lte=value).distinct()

    def filter_stock_min(self, queryset, name, value):
        return queryset.filter(variantes__stock__gte=value).distinct()

    def filter_stock_max(self, queryset, name, value):
        return queryset.filter(variantes__stock__lte=value).distinct()
