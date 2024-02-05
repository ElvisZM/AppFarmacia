from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .forms import *

@api_view(['GET'])
def producto_list(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def producto_list_mejorado(request):
    productos = Producto.objects.all()
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

@api_view(['GET'])    
def producto_busqueda_avanzada(request):
    if (len(request.query_params) > 0):
        formulario = BusquedaAvanzadaProductoFormAPI(request.query_params)
        if formulario.is_valid():
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSproductos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod')
            
            nombre_prod = formulario.cleaned_data.get('nombre_prod')
            descripcion = formulario.cleaned_data.get('descripcion')
            precio = formulario.cleaned_data.get('precio')
            
            if (nombre_prod != ""):
                QSproductos = QSproductos.filter(Q(nombre_prod__contains=nombre_prod) | Q(descripcion__contains=nombre_prod))
                mensaje_busqueda += "Nombre o descripcion que contenga la palabra "+nombre_prod+"\n"
                
            if (descripcion != ""):
                QSproductos = QSproductos.filter(Q(nombre_prod__contains=descripcion) | Q(descripcion__contains=descripcion))
                mensaje_busqueda += "Nombre o descripcion que contenga la palabra "+descripcion+"\n"
            
            if (not precio is None):
                QSproductos = QSproductos.filter(precio__gte= precio)
                mensaje_busqueda += f"Precio que sea igual o mayor a {precio}\n"
            
            productos = QSproductos.all()
            
            serializer = ProductoSerializerMejorado(productos, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def empleado_list(request):
    empleados = Empleado.objects.all()
    serializer = EmpleadoSerializer(empleados, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def empleado_list_mejorado(request):
    empleados = Empleado.objects.all()
    serializer_mejorado = EmpleadoSerializerMejorado(empleados, many=True)
    return Response(serializer_mejorado.data)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def votacion_list_mejorado(request):
    votaciones = Votacion.objects.all()
    serializer_mejorado = VotacionSerializerMejorado(votaciones, many=True)
    return Response(serializer_mejorado.data)

@api_view(['GET'])
def farmacia_list(request):
    farmacias = Farmacia.objects.all()
    serializer = FarmaciaSerializer(farmacias, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    serializer = ProveedorSerializer(proveedores, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def producto_create(request):
    serializers = ProductoSerializerCreate(data=request.data)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Producto CREADO")
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    