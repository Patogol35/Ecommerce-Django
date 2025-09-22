from django.db import models
from django.contrib.auth.models import User


class Producto(models.Model):
    CATEGORIAS = [
        ('DEPORTES', 'Deportes'),
        ('TECNOLOGIA', 'Tecnologías'),
        ('VIDEOJUEGOS', 'Videojuegos'),
        ('ZAPATOS', 'Zapatos'),
        ('LIBROS', 'Libros'),
    ]

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.URLField(max_length=500)  # usamos URLField en lugar de ImageField
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='VIDEOJUEGOS')

    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carrito de {self.usuario.username}'


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

    def subtotal(self):
        return self.cantidad * self.producto.precio


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Pedido #{self.id} - {self.usuario.username}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'
