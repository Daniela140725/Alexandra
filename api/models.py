# Create your models here.
from django.db import models


class Funcionario(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    cargo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Usuario(models.Model):
    TIPOS_USUARIO = [
        ('ADMIN', 'Administrador'),
        ('FUNCIONARIO', 'Funcionario'),
        ('SUPERVISOR', 'Supervisor'),
    ]

    funcionario = models.OneToOneField(
        Funcionario,
        on_delete=models.CASCADE,
        related_name='usuario'
    )

    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPOS_USUARIO
    )
    estado = models.BooleanField(default=True)
    permisos = models.TextField(blank=True)

    def __str__(self):
        return self.username


class Ingreso(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='ingresos'
    )

    fecha_ingreso = models.DateTimeField()
    fecha_salida = models.DateTimeField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Ingreso de {self.usuario.username}"


class Bitacora(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='bitacoras'
    )

    accion = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.accion}"