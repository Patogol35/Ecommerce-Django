from django.contrib import admin
from .models import Producto, Categoria, Carrito, ItemCarrito, Pedido, ItemPedido
from datetime import datetime, timedelta

# ---------------------------
# Filtros personalizados
# ---------------------------
class StockBajoFilter(admin.SimpleListFilter):
    title = 'Stock'
    parameter_name = 'stock'

    def lookups(self, request, model_admin):
        return [
            ('bajo', 'Stock bajo (≤5)'),
            ('sin_stock', 'Sin stock'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'bajo':
            return queryset.filter(stock__lte=5, stock__gt=0)
        if self.value() == 'sin_stock':
            return queryset.filter(stock=0)
        return queryset

class FechaCreacionFilter(admin.SimpleListFilter):
    title = 'Fecha de creación'
    parameter_name = 'fecha_creacion_custom'

    def lookups(self, request, model_admin):
        return [
            ('hoy', 'Hoy'),
            ('semana', 'Esta semana'),
        ]

    def queryset(self, request, queryset):
        hoy = datetime.now().date()
        if self.value() == 'hoy':
            return queryset.filter(fecha_creacion__date=hoy)
        if self.value() == 'semana':
            semana_inicio = hoy - timedelta(days=hoy.weekday())
            return queryset.filter(fecha_creacion__date__gte=semana_inicio)
        return queryset

# ---------------------------
# Admin de Producto
# ---------------------------
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'fecha_creacion', 'mostrar_categorias')
    search_fields = ['nombre']
    list_filter = ['fecha_creacion', StockBajoFilter, FechaCreacionFilter, 'categorias']

    # Muestra las categorías en la lista
    def mostrar_categorias(self, obj):
        return ", ".join([c.nombre for c in obj.categorias.all()])
    mostrar_categorias.short_description = 'Categorías'

# ---------------------------
# Admin de Categoría
# ---------------------------
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ['nombre']

# ---------------------------
# Ítems en línea para Carrito
# ---------------------------
class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0

# ---------------------------
# Admin de Carrito
# ---------------------------
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'creado')
    inlines = [ItemCarritoInline]
    search_fields = ['usuario__username']
    list_filter = ['creado']

# ---------------------------
# Ítems en línea para Pedido
# ---------------------------
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0

# ---------------------------
# Admin de Pedido
# ---------------------------
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha')
    inlines = [ItemPedidoInline]
    search_fields = ['usuario__username']
    list_filter = ['fecha']

# ---------------------------
# Registro en admin
# ---------------------------
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(Pedido, PedidoAdmin)
