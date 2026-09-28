from django.contrib import admin
from .models import Funcionario, Usuario, Ingreso, Bitacora

admin.site.register(Funcionario)
admin.site.register(Usuario)
admin.site.register(Ingreso)
admin.site.register(Bitacora)
