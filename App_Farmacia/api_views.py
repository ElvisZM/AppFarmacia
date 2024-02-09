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
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaProductoForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSproductos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod')
            
            nombre_prod = formulario.cleaned_data.get('nombre_prod')
            descripcion = formulario.cleaned_data.get('descripcion')
            precio = formulario.cleaned_data.get('precio')
            farmacia_prod = formulario.cleaned_data.get('farmacia_prod')
            prov_sum_prod = formulario.cleaned_data.get('prov_sum_prod')
                            
            if (nombre_prod != ""):
                QSproductos = QSproductos.filter(Q(nombre_prod__contains=nombre_prod) | Q(descripcion__contains=nombre_prod))
                mensaje_busqueda += "Nombre o descripcion que contenga la palabra "+nombre_prod+"\n"
                
            if (descripcion != ""):
                QSproductos = QSproductos.filter(Q(nombre_prod__contains=descripcion) | Q(descripcion__contains=descripcion))
                mensaje_busqueda += "Nombre o descripcion que contenga la palabra "+descripcion+"\n"
            
            if (not precio is None):
                QSproductos = QSproductos.filter(precio__gte= precio)
                mensaje_busqueda += f"Precio que sea igual o mayor a {precio}\n"
            
            if (not farmacia_prod is None):
                QSproductos = QSproductos.filter(farmacia_prod=farmacia_prod)
                mensaje_busqueda += "Que la farmacia a la que pertence sea "+farmacia_prod.nombre_farm+"\n"
                
            if (not prov_sum_prod is None):
                QSproductos = QSproductos.filter(prov_sum_prod=prov_sum_prod)
                mensaje_busqueda += "Que el proveedor sea "+prov_sum_prod.nombre_prov+"\n"
        
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
    producto_serializers = ProductoSerializerCreate(data=request.data)
    if producto_serializers.is_valid():
        try:
            producto_serializers.save()
            return Response("Producto CREADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(error)
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(producto_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['GET'])  
def producto_obtener(request, producto_id):
    producto = Producto.objects.select_related("farmacia_prod").prefetch_related("prov_sum_prod")
    producto = producto.get(id=producto_id)
    serializer = ProductoSerializerMejorado(producto)
    return Response(serializer.data)  
  
    
@api_view(['PUT'])
def producto_editar(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    productoCreateSerializer = ProductoSerializerCreate(instance=producto, data=request.data)
    if productoCreateSerializer.is_valid():
        try:
            productoCreateSerializer.save()
            return Response("Producto EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    else:
        return Response(productoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def producto_actualizar_nombre(request, producto_id):
    serializers = ProductoSerializerCreate(data=request.data)
    producto = Producto.objects.get(id=producto_id)
    serializers = ProductoSerializerActualizarNombre(data=request.data, instance=producto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Producto EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['DELETE'])
def producto_eliminar(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    try:
        producto.delete()
        return Response("Producto DELETEADO")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
 

 
 
 
    

@api_view(['GET'])    
def empleado_busqueda_avanzada(request):
    if (len(request.query_params) > 0):
        formulario = BusquedaAvanzadaEmpleadoForm(request.query_params)
        if formulario.is_valid():
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSempleados = Empleado.objects.all()
            
            first_name = formulario.cleaned_data.get('first_name')
            email = formulario.cleaned_data.get('email')
            direccion_emp = formulario.cleaned_data.get('direccion_emp')
            date_joined = formulario.cleaned_data.get('date_joined')
            telefono_emp = formulario.cleaned_data.get('telefono_emp')
            salario = formulario.cleaned_data.get('salario')
            farm_emp = formulario.cleaned_data.get('farm_emp')
            
            if (first_name != ""):
                QSempleados = QSempleados.filter(usuario__first_name__contains=first_name)
                mensaje_busqueda += "Nombre o que contenga la palabra "+first_name+"\n"
                
            if (email != ""):
                QSempleados = QSempleados.filter(usuario__email=email)
                mensaje_busqueda += "Email sea igual a "+email+"\n"
            
            if (direccion_emp != ""):
                mensaje_busqueda += f"Direccion o que contenga la palabra "+direccion_emp+"\n"
                QSempleados = QSempleados.filter(direccion_emp__contains = direccion_emp)
            
            if (not date_joined is None):
                mensaje_busqueda += f"Fecha de registro que sea igual o mayor a "+str(date_joined)+"\n"
                QSempleados = QSempleados.filter(usuario__date_joined__gte = date_joined)
            
            if (not telefono_emp is None):
                mensaje_busqueda += f"Telefono que sea igual a "+str(telefono_emp)+"\n"
                QSempleados = QSempleados.filter(telefono_emp = telefono_emp)
            
            if (not salario is None):
                mensaje_busqueda += f"Salario que sea igual o mayor a "+str(salario)+"\n"
                QSempleados = QSempleados.filter(salario__gte = salario)
                
            if (not farm_emp is None):
                QSempleados = QSempleados.filter(farm_emp=farm_emp)
                mensaje_busqueda += "Que este asignado/a a la Farmacia "+farm_emp.nombre_farm+"\n"
            
            empleados = QSempleados.all()
            
            serializer = EmpleadoSerializerMejorado(empleados, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET']) 
def clientes_list(request):
    clientes = Cliente.objects.all()
    serializer = ClienteSerializerMejorado(clientes, many=True)
    return Response(serializer.data)



@api_view(['GET'])    
def votacion_busqueda_avanzada(request):
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaVotacionForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSvotaciones = Votacion.objects.all()
            
            puntuacion = formulario.cleaned_data.get('puntuacion')
            fechaDesde = formulario.cleaned_data.get('fecha_desde')
            fechaHasta = formulario.cleaned_data.get('fecha_hasta')
            comenta_votacion = formulario.cleaned_data.get('comenta_votacion')
            voto_producto = formulario.cleaned_data.get('voto_producto')
            voto_cliente = formulario.cleaned_data.get('voto_cliente')
            
            if (not puntuacion is None):
                QSvotaciones = QSvotaciones.filter(puntuacion=puntuacion)
                mensaje_busqueda += "Puntuacion sea "+str(puntuacion)+"\n"
                
            if(not fechaDesde is None):
                mensaje_busqueda +=" La fecha sea mayor a "+date.strftime(fechaDesde,'%d-%m-%Y')+"\n"
                QSvotaciones = QSvotaciones.filter(fecha_votacion__gte=fechaDesde)
            
            if(not fechaHasta is None):
                mensaje_busqueda +=" La fecha sea menor a "+date.strftime(fechaHasta,'%d-%m-%Y')+"\n"
                QSvotaciones = QSvotaciones.filter(fecha_votacion__lte=fechaHasta)
            
            if (comenta_votacion != ""):
                QSvotaciones = QSvotaciones.filter(comenta_votacion__contains=comenta_votacion)
                mensaje_busqueda += "Comentario o que contenga la palabra "+comenta_votacion+"\n"
            
            if (not voto_producto is None):
                QSvotaciones = QSvotaciones.filter(voto_producto=voto_producto)
                mensaje_busqueda += "Que el producto sea "+voto_producto.nombre_prod+"\n"
                
            if (not voto_cliente is None):
                QSvotaciones = QSvotaciones.filter(voto_cliente=voto_cliente)
                mensaje_busqueda += "Que el cliente sea "+voto_cliente.usuario.first_name+"\n"
        
            
            votaciones = QSvotaciones.all()
            
            serializer = VotacionSerializerMejorado(votaciones, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    