from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q

from .forms import *

@api_view(['GET'])
def producto_list(request):
    productos = Producto.objects.all()
    #serializer = ProductoSerializer(productos, many=True)
    serializer_mejorado = ProductoSerializerMejorado(productos, many=True)
    return Response(serializer_mejorado.data)

@api_view(['GET'])
def producto_buscar(request):
    if (request.user.has_perm('AppFarmacia.view_producto')):
        formulario = BusquedaProductoForm(request.query_params)
        if (formulario.is_valid()):
            texto = formulario.data.get('textoBusqueda')
            productos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod')
            productos = productos.filter(Q(nombre_prod__contains=texto) | Q(descripcion__contains=texto)).all()
            serializer = ProductoSerializerMejorado(productos, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Sin permisos"}, status=status.HTTP_400_BAD_REQUEST)            