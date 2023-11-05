from django.shortcuts import render

# Create your views here.
from .models import Farmacia, Gerente, Empleado, Producto, Proveedor, SuministroProducto, Cliente, Compra, DetalleCompra, CuentaEmpleado, HistorialCliente, DatosFarmacia, DetalleProducto
from django.db.models import Q
from django.views.defaults import page_not_found
from datetime import datetime, date


def index(request):
    return render(request, 'index.html')

def farmacia_ordenada_fecha(request):
    farmacias = Farmacia.objects.select_related('datosfarmacia').order_by('datosfarmacia__fecha_creacion')
    return render(request, 'farmacia/farmaciaydatos.html', {'farmacias':farmacias})

def gerente_nombre(request, nombre_introducido):
    gerentes = Gerente.objects.select_related('gerente_farm').filter(nombre_ger__contains=nombre_introducido)
    return render(request, 'gerente/gerente.html', {'gerentes':gerentes})

def farmacias_con_gerentes(request):
    farmacias = Farmacia.objects.select_related('gerente').all()
    return render(request, 'farmacia/farmaciaygerentes.html', {'farmacias':farmacias})

def productos_con_proveedores(request):
    productos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod').all()
    return render(request, 'producto/producto.html', {'productos':productos})

def empleado_compras(request):
    empleados = Empleado.objects.select_related('farm_emp').all()
    return render(request, 'empleado/empleado_y_compras.html', {'empleados':empleados})

def detalle_compra(request, id_compra):
    compra = Compra.objects.select_related('cliente_compra', 'empleado_compra').prefetch_related('producto_compra').filter(id=id_compra)
    return render(request, 'compra/compra.html', {'compras':compra})

def clientes_productosfavoritos(request):
    clientes = Cliente.objects.prefetch_related('productos_favoritos').all()
    return render(request, 'cliente/cliente.html', {'clientes':clientes})

def empleado_salariosuperior(request, cantidad_salario):
    empleados = Empleado.objects.filter(salario__gte=cantidad_salario).all()   #IMPORTANTE gte = mayor o igual que  y  lte = menor o igual que
    return render(request, 'empleado/empleado.html', {'empleados':empleados})

def productos_disponibles_farmacia_especifica(request, id_farmacia):
    farmacia = Farmacia.objects.get(id=id_farmacia)
    productos = Producto.objects.filter(farmacia_prod = farmacia).order_by('-precio').all()
    return render(request, 'farmacia/farmaciayproductos.html', {'productos':productos, 'farmacia': farmacia})

def compras_entre_fechas(request, fecha_inicio, fecha_fin):
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
    compras = Compra.objects.select_related('cliente_compra', 'empleado_compra').prefetch_related('producto_compra').filter(fecha_compra__gte=fecha_inicio, fecha_compra__lte=fecha_fin)
    return render(request, 'compra/compra.html', {'compras':compras})

def mi_error_400(request, exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request, exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request, exception=None):
    return render(request, 'errores/500.html',None,None,500)

    