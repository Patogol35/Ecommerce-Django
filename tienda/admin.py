from django.contrib import admin
from .models import Producto, Carrito, ItemCarrito, Pedido, ItemPedido, Categoria


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ['nombre']


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'fecha_creacion', 'mostrar_categoria')
    search_fields = ['nombre']

    def mostrar_categoria(self, obj):
        return obj.categoria.nombre if obj.categoria else "Sin categoría"
    mostrar_categoria.short_description = "Categoría"


class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0


class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'creado')
    inlines = [ItemCarritoInline]


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha')
    inlines = [ItemPedidoInline]


# ==== Registro ====
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(Pedido, PedidoAdmin)
