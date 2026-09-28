from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .serializers import CompraSerializer, ProveedorSerializer
from .models import Compra, Proveedor


class ProveedorView(APIView):
    @swagger_auto_schema(operation_description='Registrar proveedor', request_body=ProveedorSerializer)
    def post(self, request):
        serializer = ProveedorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Proveedor guardado correctamente'})
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(operation_description='Listar proveedores')
    def get(self, request):
        proveedores = Proveedor.objects.all()
        serializer = ProveedorSerializer(proveedores, many=True)
        return Response(serializer.data)


class ProveedorViewId(APIView):
    @swagger_auto_schema(operation_description='Buscar proveedor por id')
    def get(self, request, id):
        proveedor = Proveedor.objects.filter(id=id).first()
        if not proveedor:
            return Response({'mensaje': 'Proveedor no encontrado'}, status=404)
        serializer = ProveedorSerializer(proveedor)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description='Eliminar proveedor por id')
    def delete(self, request, id):
        proveedor = Proveedor.objects.filter(id=id).first()
        if not proveedor:
            return Response({'mensaje': 'Proveedor no encontrado'}, status=404)
        proveedor.delete()
        return Response({'mensaje': 'Proveedor eliminado'})

    @swagger_auto_schema(operation_description='Actualizar proveedor', request_body=ProveedorSerializer)
    def put(self, request, id):
        proveedor = Proveedor.objects.filter(id=id).first()
        if not proveedor:
            return Response({'mensaje': 'Proveedor no encontrado'}, status=404)
        serializer = ProveedorSerializer(proveedor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Proveedor actualizado correctamente'})
        return Response(serializer.errors, status=400)
#########################################################################################################################

class CompraView(APIView):
    @swagger_auto_schema(operation_description='Registrar compra', request_body=CompraSerializer)
    def post(self, request):
        serializer = CompraSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Compra guardada correctamente'})
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(operation_description='Listar compras')
    def get(self, request):
        compras = Compra.objects.all()
        serializer = CompraSerializer(compras, many=True)
        return Response(serializer.data)

