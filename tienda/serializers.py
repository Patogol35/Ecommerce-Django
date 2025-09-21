
from rest_framework import serializers
from .models import Producto, Carrito, ItemCarrito, Pedido, ItemPedido
from django.contrib.auth.models import User

# =========================
# PRODUCTO
# =========================
class ProductoSerializer(serializers.ModelSerializer):
    # Eliminamos get_imagen_url, usamos directamente el campo imagen
    class Meta:
        model = Producto
        fields = '__all__'  # incluye todos los campos del modelo

# =========================
# ITEM CARRITO
# =========================
class ItemCarritoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = ItemCarrito
        fields = ['id', 'producto', 'cantidad', 'subtotal']

# =========================
# CARRITO
# =========================
class CarritoSerializer(serializers.ModelSerializer):
    items = ItemCarritoSerializer(many=True, read_only=True)

    class Meta:
        model = Carrito
        fields = ['id', 'usuario', 'creado', 'items']

# =========================
# USUARIO
# =========================
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

# =========================
# ITEM PEDIDO
# =========================
class ItemPedidoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemPedido
        fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()

# =========================
# PEDIDO
# =========================
class PedidoSerializer(serializers.ModelSerializer):
    items = ItemPedidoSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'usuario', 'fecha', 'total', 'pendiente', 'items']  # ✅ Incluido
