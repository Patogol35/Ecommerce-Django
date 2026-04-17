from decimal import Decimal
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings

from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from rest_framework_simplejwt.tokens import RefreshToken

from google.oauth2 import id_token
from google.auth.transport import requests

from .models import Producto, Categoria, Carrito, ItemCarrito, Pedido, ItemPedido
from .serializers import (
    ProductoSerializer,
    CategoriaSerializer,
    CarritoSerializer,
    UserSerializer,
    ItemCarritoSerializer,
    PedidoSerializer,
)
from .filters import ProductoFilter


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filterset_class = ProductoFilter


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agregar_al_carrito(request):
    producto_id = request.data.get('producto_id')
    cantidad = int(request.data.get('cantidad', 1))

    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)

    if cantidad > producto.stock:
        return Response({'error': f'Solo hay {producto.stock} disponibles'}, status=400)

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    item, creado = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': cantidad}
    )

    if not creado:
        nueva_cantidad = item.cantidad + cantidad
        if nueva_cantidad > producto.stock:
            return Response({'error': 'Stock insuficiente'}, status=400)

        if nueva_cantidad <= 0:
            item.delete()
            return Response({'message': 'Eliminado'}, status=200)

        item.cantidad = nueva_cantidad
        item.save()

    return Response(ItemCarritoSerializer(item).data, status=201)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_del_carrito(request, item_id):
    try:
        item = ItemCarrito.objects.get(id=item_id, carrito__usuario=request.user)
        item.delete()
        return Response({'message': 'Eliminado'}, status=200)
    except ItemCarrito.DoesNotExist:
        return Response({'error': 'No encontrado'}, status=404)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_cantidad_carrito(request, item_id):
    try:
        cantidad = int(request.data.get('cantidad', 1))
        item = ItemCarrito.objects.get(id=item_id, carrito__usuario=request.user)
    except:
        return Response({'error': 'Error'}, status=400)

    if cantidad <= 0:
        item.delete()
        return Response({'message': 'Eliminado'}, status=200)

    item.cantidad = cantidad
    item.save()
    return Response(ItemCarritoSerializer(item).data)


class CarritoView(generics.RetrieveAPIView):
    serializer_class = CarritoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        carrito, _ = Carrito.objects.get_or_create(usuario=self.request.user)
        return carrito


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_pedido(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = list(carrito.items.all())

    if not items:
        return Response({'error': 'Carrito vacío'}, status=400)

    total = sum(Decimal(i.producto.precio) * i.cantidad for i in items)

    pedido = Pedido.objects.create(usuario=request.user, total=total)

    for i in items:
        ItemPedido.objects.create(
            pedido=pedido,
            producto=i.producto,
            cantidad=i.cantidad,
            precio_unitario=i.producto.precio
        )

    carrito.items.all().delete()

    return Response(PedidoSerializer(pedido).data)


class ListaPedidosUsuario(generics.ListAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)


# 🔥 GOOGLE LOGIN
@api_view(['POST'])
def google_login(request):
    token = request.data.get('token')

    if not token:
        return Response({'error': 'Token requerido'}, status=400)

    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        if idinfo['aud'] != settings.GOOGLE_CLIENT_ID:
            return Response({'error': 'Token inválido'}, status=400)

        email = idinfo.get('email')
        name = idinfo.get('name')

        user = User.objects.filter(email=email).first()

        if not user:
            user = User.objects.create(
                username=email,
                email=email,
                first_name=name or ''
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })

    except Exception:
        return Response({'error': 'Token inválido'}, status=400)
