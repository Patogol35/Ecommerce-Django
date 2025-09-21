from decimal import Decimal
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Producto, Carrito, ItemCarrito, Pedido, ItemPedido, Categoria
from .serializers import (
    ProductoSerializer, CarritoSerializer, ItemCarritoSerializer,
    PedidoSerializer, UserSerializer, CategoriaSerializer
)


# =========================
# CATEGORIAS
# =========================
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]


# =========================
# PRODUCTOS
# =========================
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by("-fecha_creacion")
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]


# =========================
# REGISTRO USUARIO
# =========================
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# =========================
# CARRITO
# =========================
class CarritoView(generics.RetrieveAPIView):
    serializer_class = CarritoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        carrito, created = Carrito.objects.get_or_create(usuario=self.request.user)
        return carrito


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agregar_al_carrito(request):
    producto_id = request.data.get("producto_id")
    cantidad = int(request.data.get("cantidad", 1))

    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)

    if not created:
        item.cantidad += cantidad
    else:
        item.cantidad = cantidad
    item.save()

    return Response(CarritoSerializer(carrito).data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_del_carrito(request, item_id):
    try:
        item = ItemCarrito.objects.get(id=item_id, carrito__usuario=request.user)
        item.delete()
        return Response({"message": "Producto eliminado del carrito"})
    except ItemCarrito.DoesNotExist:
        return Response({"error": "Item no encontrado"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_cantidad_carrito(request, item_id):
    try:
        item = ItemCarrito.objects.get(id=item_id, carrito__usuario=request.user)
        nueva_cantidad = int(request.data.get("cantidad", 1))
        item.cantidad = nueva_cantidad
        item.save()
        return Response(CarritoSerializer(item.carrito).data)
    except ItemCarrito.DoesNotExist:
        return Response({"error": "Item no encontrado"}, status=status.HTTP_404_NOT_FOUND)


# =========================
# PEDIDOS
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def crear_pedido(request):
    carrito = Carrito.objects.get(usuario=request.user)
    if not carrito.items.exists():
        return Response({"error": "El carrito está vacío"}, status=status.HTTP_400_BAD_REQUEST)

    pedido = Pedido.objects.create(usuario=request.user, total=Decimal(0))
    total = Decimal(0)

    for item in carrito.items.all():
        ItemPedido.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )
        total += item.subtotal()

        # Restar stock del producto
        item.producto.stock -= item.cantidad
        item.producto.save()

    pedido.total = total
    pedido.save()

    carrito.items.all().delete()  # vaciar carrito después del pedido

    return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)


class ListaPedidosUsuario(generics.ListAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user).order_by("-fecha")


# =========================
# USER PROFILE
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email
    })
