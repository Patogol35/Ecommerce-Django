from decimal import Decimal
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Producto, Carrito, ItemCarrito, Pedido, ItemPedido
from .serializers import (
    ProductoSerializer,
    CarritoSerializer,
    UserSerializer,
    ItemCarritoSerializer,
    PedidoSerializer,
)

# ---------------------------
# AGREGAR PRODUCTO AL CARRITO
# ---------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agregar_al_carrito(request):
    producto_id = request.data.get('producto_id')
    cantidad = int(request.data.get('cantidad', 1))
    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    item, creado = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': max(cantidad, 0)}
    )
    if not creado:
        nueva_cantidad = item.cantidad + cantidad
        if nueva_cantidad <= 0:
            item.delete()
            return Response({'message': 'Producto eliminado del carrito'}, status=status.HTTP_200_OK)
        item.cantidad = nueva_cantidad
        item.save()

    if creado and item.cantidad <= 0:
        item.delete()
        return Response({'message': 'Producto eliminado del carrito'}, status=status.HTTP_200_OK)

    return Response(ItemCarritoSerializer(item).data, status=status.HTTP_201_CREATED)


# ---------------------------
# ELIMINAR ITEM DEL CARRITO
# ---------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_del_carrito(request, item_id):
    try:
        item = ItemCarrito.objects.get(id=item_id, carrito__usuario=request.user)
        item.delete()
        return Response({'message': 'Producto eliminado del carrito'}, status=status.HTTP_200_OK)
    except ItemCarrito.DoesNotExist:
        return Response({'error': 'Producto no encontrado en el carrito'}, status=status.HTTP_404_NOT_FOUND)


# ---------------------------
# ACTUALIZAR CANTIDAD
# ---------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_cantidad_carrito(request, item_id):
    try:
        cantidad = int(request.data.get('cantidad', 1))
    except (TypeError, ValueError):
        return Response({'error': 'Cantidad inválida'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        item = ItemCarrito.objects.get(id=item_id, carrito__usuario=request.user)
    except ItemCarrito.DoesNotExist:
        return Response({'error': 'Producto no encontrado en el carrito'}, status=status.HTTP_404_NOT_FOUND)

    if cantidad <= 0:
        item.delete()
        return Response({'message': 'Producto eliminado del carrito'}, status=status.HTTP_200_OK)

    item.cantidad = cantidad
    item.save()
    return Response(ItemCarritoSerializer(item).data, status=status.HTTP_200_OK)


# ---------------------------
# VER CARRITO
# ---------------------------
class CarritoView(generics.RetrieveAPIView):
    serializer_class = CarritoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        carrito, _ = Carrito.objects.get_or_create(usuario=self.request.user)
        return carrito


# ---------------------------
# REGISTRO USUARIOS
# ---------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ---------------------------
# CRUD PRODUCTOS
# ---------------------------
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


# ---------------------------
# CREAR PEDIDO
# ---------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_pedido(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = list(carrito.items.select_related('producto'))

    if not items:
        return Response({'error': 'El carrito está vacío'}, status=status.HTTP_400_BAD_REQUEST)

    for it in items:
        if it.producto.stock < it.cantidad:
            return Response({'error': f'Stock insuficiente para {it.producto.nombre}'}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        total = sum((Decimal(it.producto.precio) * it.cantidad for it in items), Decimal('0'))
        pedido = Pedido.objects.create(usuario=request.user, total=total)

        for it in items:
            prod = it.producto
            prod.stock -= it.cantidad
            prod.save()
            ItemPedido.objects.create(
                pedido=pedido,
                producto=prod,
                cantidad=it.cantidad,
                precio_unitario=prod.precio
            )

        carrito.items.all().delete()

    return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)


# ---------------------------
# LISTAR PEDIDOS DEL USUARIO (con paginación personalizada)
# ---------------------------
class PedidoPagination(PageNumberPagination):
    page_size = 40  # 🔹 Cambia este número para mostrar menos/más pedidos

class ListaPedidosUsuario(generics.ListAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PedidoPagination

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user).order_by('-fecha')
