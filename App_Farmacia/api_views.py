from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *

@api_view(['GET'])
def producto_list(request):
    productos = Producto.objects.all()
    #serializer = ProductoSerializer(productos, many=True)
    serializer_mejorado = ProductoSerializerMejorado(productos, many=True)
    return Response(serializer_mejorado.data)

def producto_buscar(request):
    if (request.user.has_perm('AppFarmacia.view_producto')):
        formulario = BusquedaProductoForm(request.query_params)
        if (formulario.is_valid()):
            texto = formulario.cleaned_data.get('textoBusqueda')