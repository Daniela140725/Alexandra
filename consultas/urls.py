from django.urls import path
from .views import CompraView, CompraViewId, ProveedorView, ProveedorViewId

urlpatterns = [
    path('proveedores/', ProveedorView.as_view(), name='proveedor-list-create'),
    path('proveedores/<int:id>/', ProveedorViewId.as_view(), name='proveedor-detail'),
    path('compras/', CompraView.as_view(), name='compra-list-create'),
    path('compras/<int:id>/', CompraViewId.as_view(), name='compra-detail'),
]
