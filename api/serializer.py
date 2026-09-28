from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Funcionario, Usuario, Ingreso, Bitacora


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    funcionario_detalle = FuncionarioSerializer(
        source='funcionario',
        read_only=True
    )

    class Meta:
        model = Usuario
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            validated_data['password'] = make_password(password)
        return super().update(instance, validated_data)


class IngresoSerializer(serializers.ModelSerializer):
    usuario_detalle = UsuarioSerializer(
        source='usuario',
        read_only=True
    )

    class Meta:
        model = Ingreso
        fields = '__all__'


class BitacoraSerializer(serializers.ModelSerializer):
    usuario_detalle = UsuarioSerializer(
        source='usuario',
        read_only=True
    )

    class Meta:
        model = Bitacora
        fields = '__all__'