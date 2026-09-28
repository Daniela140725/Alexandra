from rest_framework import serializers
from .models import Compra, Proveedor

class ProveedorSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=150)
    telefono = serializers.CharField(max_length=20)
    correo = serializers.EmailField()

class CompraSerializer(serializers.Serializer):
    fecha_compra = serializers.DateField()
    valor_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    proveedor = serializers.PrimaryKeyRelatedField(queryset=Proveedor.objects.all())
    observacion = serializers.CharField(required=False, allow_blank=True)