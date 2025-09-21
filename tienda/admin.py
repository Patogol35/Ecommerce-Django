from django.contrib import admin
from datetime import datetime, timedelta
from .models import Producto, Carrito, ItemCarrito, Pedido, ItemPedido, Categoria  # 👈 nuevo modelo

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ['nombre']

admin.site.register(Categoria, CategoriaAdmin)  # 👈 registro en admin
# Filtro personalizado por stock
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
# Filtro personalizado por fecha de creación
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
# Admin de Producto
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'fecha_creacion')
    search_fields = ['nombre']
    list_filter = ['fecha_creacion', StockBajoFilter, FechaCreacionFilter]
# Ítems en línea para Carrito
class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0
# Admin de Carrito
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'creado')
    inlines = [ItemCarritoInline]
    search_fields = ['usuario__username']
    list_filter = ['creado']
# Ítems en línea para Pedido
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
# Admin de Pedido
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha')
    inlines = [ItemPedidoInline]
    search_fields = ['usuario__username']
    list_filter = ['fecha']
# Registro en admin
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(Pedido, PedidoAdmin)
