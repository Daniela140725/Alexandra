from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    fecha_compra = models.DateField()
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, related_name='compras', on_delete=models.CASCADE)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Compra #{self.pk} - {self.proveedor.nombre}'
