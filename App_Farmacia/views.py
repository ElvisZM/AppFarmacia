from django.shortcuts import render, redirect

# Create your views here.
from .models import *
from django.db.models import Q, Prefetch
from django.views.defaults import page_not_found
from datetime import datetime, date
from django.db.models import Avg
from .forms import *
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')


# PARA FORMULARIOS 

def producto_create(request):
    
    # Si la petición es GET se creará el formulario Vacio
    # Si la petición es POST se creará el formulario con Datos
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario == request.POST
    
    formulario = ProductoModelForm(datosFormulario)
    
    if (request.method == 'POST'):
        producto_creado = crear_producto_modelo(formulario)
        if (producto_creado):
            messages.success(request, 'Se ha creado el producto'+formulario.cleaned_data.get('nombre_prod')+"correctamente")
            return redirect("productos_con_proveedores")       

    return render(request, 'producto/create.html', {'formulario':formulario})

def crear_producto_modelo(formulario):
        
    producto_creado = False
    #Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            #Guarda el producto en la base de datos
            formulario.save()
            producto_creado = True
        except:
            pass
    return producto_creado                






def farmacia_ordenada_fecha(request):
    farmacias = Farmacia.objects.select_related('datosfarmacia').order_by('datosfarmacia__fecha_creacion')
    return render(request, 'farmacia/farmaciaydatos.html', {'farmacias':farmacias})

def gerente_nombre(request, nombre_introducido):
    gerentes = Gerente.objects.select_related('gerente_farm').filter(nombre_ger__contains=nombre_introducido)
    return render(request, 'gerente/gerentes_filtrado_nombre.html', {'gerentes':gerentes})

def farmacias_con_gerentes(request):
    farmacias = Farmacia.objects.select_related('gerente').all()
    return render(request, 'farmacia/farmaciaygerentes.html', {'farmacias':farmacias, 'gerente':request})

def productos_con_proveedores(request):
    productos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod').all()
    return render(request, 'producto/producto_proveedores.html', {'productos':productos})

def empleado_compras(request):
    empleados = Empleado.objects.select_related('farm_emp').all()
    return render(request, 'empleado/empleado_y_compras.html', {'compras_empleados':empleados})

def detalle_compra(request):
    compra = Compra.objects.select_related('cliente_compra', 'empleado_compra').prefetch_related('producto_compra').all()
    return render(request, 'compra/compra_detalle_empleado.html', {'compras':compra})

def detalle_compra_id(request, id_compra):
    compra = Compra.objects.select_related('cliente_compra', 'empleado_compra').prefetch_related('producto_compra').filter(id=id_compra)
    return render(request, 'compra/compraydetalles_id.html', {'compras_id':compra})

def clientes_productosfavoritos(request):
    clientes = Cliente.objects.prefetch_related('productos_favoritos').all()
    return render(request, 'cliente/cliente_prod_fav.html', {'clientes':clientes})

def empleado_salariosuperior(request, cantidad_salario):
    empleados = Empleado.objects.filter(salario__gte=cantidad_salario).all()   #IMPORTANTE gte = mayor o igual que  y  lte = menor o igual que
    return render(request, 'empleado/empleados_salario_superior.html', {'empleados':empleados})

def productos_disponibles_farmacia_especifica(request, id_farmacia):
    farmacia = Farmacia.objects.get(id=id_farmacia)
    productos = Producto.objects.filter(farmacia_prod = farmacia).order_by('-precio').all()
    return render(request, 'farmacia/farmaciayproductos.html', {'productos':productos, 'farmacia': farmacia})

def compras_entre_fechas(request, fecha_inicio, fecha_fin):
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
    compras = Compra.objects.select_related('cliente_compra', 'empleado_compra').prefetch_related('producto_compra').filter(fecha_compra__gte=fecha_inicio, fecha_compra__lte=fecha_fin)
    return render(request, 'compra/compra_entre_fechas.html', {'compras':compras})

def mi_error_400(request, exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request, exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request, exception=None):
    return render(request, 'errores/500.html',None,None,500)


def ultimo_voto_producto_concreto(request, producto_id):

    ultimo_voto = Votacion.objects.select_related("voto_producto", "voto_cliente").filter(voto_producto__id=producto_id).order_by('-fecha_votacion')[:1].get()
    return render(request, 'votacion/ultimo_voto.html', {'votacion':ultimo_voto})


#def productos_con_puntuacion_3_cliente_concreto(request, cliente_id):
    
    cliente = Cliente.objects.prefetch_related("productos_favoritos", "votacion_prod").get(pk=cliente_id)
    productos_con_votos = Producto.objects.select_related("farmacia_prod").prefetch_related("prov_sum_prod").filter(votacion_prod__puntuacion=3, votacion_prod__voto_cliente=cliente)
    
    return render(request, 'producto/productos_con_3.html', {'productos_con_votos': productos_con_votos})


    from django.db.models import F

def productos_con_puntuacion_3_cliente_concreto(request, cliente_id):
    cliente = Cliente.objects.prefetch_related("productos_favoritos", "votacion_prod").get(pk=cliente_id)

    # Filtrar por votos con puntuación 3 y cliente específico
    productos_con_votos = Producto.objects.filter(votacion_prod__puntuacion=3, votacion_prod__voto_cliente=cliente)

    # Seleccionar campos relacionados
    productos_con_votos = productos_con_votos.select_related("farmacia_prod").prefetch_related("prov_sum_prod")

    return render(request, 'producto/productos_con_3.html', {'productos_con_votos': productos_con_votos})




    
def clientes_nunca_votaron(request):
    clientes_no_votaron = Cliente.objects.prefetch_related("productos_favoritos").filter(votacion__isnull=True).all()
    return render(request, 'cliente/clientesinvoto.html', {'clientes_no_votaron':clientes_no_votaron})    

def cuentas_bancarias_propietario_nombre(request, nombre_propietario):
    cuentas_bancarias = Pago.objects.select_related("cliente_pago", "subscripcion_pago").filter(
        Q(banco='CA') | Q(banco='UN'),Q(cliente_pago__nombre_cli__icontains=nombre_propietario)
    )
    return render(request, 'cuentas/cuentas_bancarias.html', {'cuentas_bancarias': cuentas_bancarias})

def modelos_con_media_superior(request):    
    media_votaciones = Producto.objects.select_related("farmacia_prod").prefetch_related("prov_sum_prod").annotate(media=Avg('votacion__puntuacion'))

    productos_con_media_superior = Producto.objects.select_related("farmacia_prod").prefetch_related("prov_sum_prod").filter(media__gt=2.5)

    return render(request, 'producto.html', {'productos_con_media_superior': productos_con_media_superior})



    