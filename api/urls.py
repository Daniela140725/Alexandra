from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FuncionarioViewSet,
    UsuarioViewSet,
    IngresoViewSet,
    BitacoraViewSet
)


router = DefaultRouter()

router.register(
    r'funcionarios',
    FuncionarioViewSet,
    basename='funcionario'
)

router.register(
    r'usuarios',
    UsuarioViewSet,
    basename='usuario'
)

router.register(
    r'ingresos',
    IngresoViewSet,
    basename='ingreso'
)

router.register(
    r'bitacoras',
    BitacoraViewSet,
    basename='bitacora'
)


urlpatterns = [
    path('', include(router.urls)),
]