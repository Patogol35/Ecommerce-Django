from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ProductoViewSet, RegisterView, CarritoView,
    agregar_al_carrito, eliminar_del_carrito, actualizar_cantidad_carrito,
    crear_pedido, ListaPedidosUsuario
)
router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')
urlpatterns = [
    path('api/', include(router.urls)),
    # Auth & registro
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Carrito
    path('api/carrito/', CarritoView.as_view(), name='carrito'),
    path('api/carrito/agregar/', agregar_al_carrito, name='agregar-al-carrito'),
    path('api/carrito/eliminar/<int:item_id>/', eliminar_del_carrito, name='eliminar-del-carrito'),
    path('api/carrito/actualizar/<int:item_id>/', actualizar_cantidad_carrito, name='actualizar-cantidad-carrito'),
    # Pedidos
    path('api/pedido/crear/', crear_pedido, name='crear-pedido'),
    path('api/pedidos/', ListaPedidosUsuario.as_view(), name='lista-pedidos'),


    path("user/profile/", user_profile, name="user_profile"),
]
