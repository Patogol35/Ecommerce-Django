from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoViewSet, CategoriaViewSet, RegisterView, CarritoView,
    agregar_al_carrito, eliminar_del_carrito, actualizar_cantidad_carrito,
    crear_pedido, ListaPedidosUsuario, user_profile, GoogleLogin
)

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'categorias', CategoriaViewSet, basename='categoria')

urlpatterns = [
    path('api/', include(router.urls)),

    path('api/register/', RegisterView.as_view(), name='register'),

    # 🔥 GOOGLE LOGIN
    path('api/google-login/', GoogleLogin.as_view(), name='google_login'),

    path('api/carrito/', CarritoView.as_view()),
    path('api/carrito/agregar/', agregar_al_carrito),
    path('api/carrito/eliminar/<int:item_id>/', eliminar_del_carrito),
    path('api/carrito/actualizar/<int:item_id>/', actualizar_cantidad_carrito),

    path('api/pedido/crear/', crear_pedido),
    path('api/pedidos/', ListaPedidosUsuario.as_view()),

    path("api/user/profile/", user_profile),
]
