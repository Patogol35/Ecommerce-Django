from django.contrib import admin
from .models import (
    Producto,
    ProductoImagen,
    Categoria,
    Carrito,
    ItemCarrito,
    Pedido,
    ItemPedido,
    VarianteProducto
)
from datetime import datetime, timedelta


# =========================
# 🔴 FILTROS
# =========================

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


# =========================
# 🖼️ INLINE IMÁGENES
# =========================

class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1


# =========================
# 🔥 INLINE VARIANTES
# =========================

class VarianteProductoInline(admin.TabularInline):
    model = VarianteProducto
    extra = 1


# =========================
# 📂 CATEGORÍA
# =========================

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ["nombre"]


# =========================
# 📦 PRODUCTO
# =========================

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'fecha_creacion', 'categoria')
    search_fields = ['nombre']
    list_filter = ['fecha_creacion', 'categoria', FechaCreacionFilter]

    # 🔥 AQUÍ AGREGAMOS VARIANTES
    inlines = [VarianteProductoInline, ProductoImagenInline]


# =========================
# 🔥 VARIANTES (ADMIN DIRECTO)
# =========================

@admin.register(VarianteProducto)
class VarianteProductoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'nombre', 'color', 'talla', 'precio', 'stock')
    list_filter = ('producto', 'color', 'talla', StockBajoFilter)
    search_fields = ('nombre', 'producto__nombre')


# =========================
# 🛒 CARRITO
# =========================

class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0


class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'creado')
    inlines = [ItemCarritoInline]
    search_fields = ['usuario__username']
    list_filter = ['creado']


# =========================
# 📦 PEDIDOS
# =========================

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'total')
    inlines = [ItemPedidoInline]
    search_fields = ['usuario__username']
    list_filter = ['fecha']


# =========================
# 📌 REGISTROS
# =========================

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(Pedido, PedidoAdmin)
