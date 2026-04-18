from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen = models.URLField(max_length=500)  # imagen principal
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos"
    )

    def __str__(self):
        return self.nombre


# 🔥 NUEVO: Variantes del producto
class VarianteProducto(models.Model):
    producto = models.ForeignKey(
        Producto,
        related_name='variantes',
        on_delete=models.CASCADE
    )
    talla = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    sku = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.talla or ''} - {self.color or ''}"


class ProductoImagen(models.Model):
    producto = models.ForeignKey(
        Producto,
        related_name='imagenes',
        on_delete=models.CASCADE
    )
    imagen = models.URLField(max_length=500)

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"


class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carrito de {self.usuario.username}'


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)

    # 🔥 CAMBIO CLAVE: ahora se guarda la variante
    variante = models.ForeignKey(VarianteProducto, on_delete=models.CASCADE)

    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cantidad} x {self.variante.producto.nombre} ({self.variante.talla} - {self.variante.color})'

    def subtotal(self):
        return self.cantidad * self.variante.precio


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Pedido #{self.id} - {self.usuario.username}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)

    # 🔥 también aquí usamos variante
    variante = models.ForeignKey(VarianteProducto, on_delete=models.CASCADE)

    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f'{self.cantidad} x {self.variante.producto.nombre} ({self.variante.talla} - {self.variante.color})'
