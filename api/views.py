from rest_framework import viewsets

from .models import Funcionario, Usuario, Ingreso, Bitacora
from .serializer import (
    FuncionarioSerializer,
    UsuarioSerializer,
    IngresoSerializer,
    BitacoraSerializer
)


class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.select_related('funcionario').all()
    serializer_class = UsuarioSerializer


class IngresoViewSet(viewsets.ModelViewSet):
    queryset = Ingreso.objects.select_related(
        'usuario', 'usuario__funcionario'
    ).all()
    serializer_class = IngresoSerializer


class BitacoraViewSet(viewsets.ModelViewSet):
    queryset = Bitacora.objects.select_related(
        'usuario', 'usuario__funcionario'
    ).all()
    serializer_class = BitacoraSerializer