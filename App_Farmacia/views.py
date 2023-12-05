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

def producto_create(request):
    
    # Si la petición es GET se creará el formulario Vacio
    # Si la petición es POST se creará el formulario con Datos
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = ProductoModelForm(datosFormulario)
    if (request.method == 'POST'):
        producto_creado = crear_producto_modelo(formulario)
        if (producto_creado):
            messages.success(request, 'Se ha creado el producto '+formulario.cleaned_data.get('nombre_prod')+" correctamente")
            return redirect("productos_con_proveedores")       

    return render(request, 'producto/create.html', {'formulario':formulario})

def producto_buscar(request):
    
    formulario = BusquedaProductoForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        productos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod')
        productos = productos.filter(Q(nombre_prod__contains=texto) | Q(descripcion__contains=texto)).all()
        return render(request, 'producto/producto_busqueda.html',{"productos_mostrar":productos, "texto_busqueda":texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
def producto_buscar_avanzado(request):
    
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaProductoForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSproductos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod')
            
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            nombre_prod = formulario.cleaned_data.get('nombre_prod')
            descripcion = formulario.cleaned_data.get('descripcion')
            precio = formulario.cleaned_data.get('precio')
            farmacia_prod = formulario.cleaned_data.get('farmacia_prod')
            prov_sum_prod = formulario.cleaned_data.get('prov_sum_prod')
            
            if (textoBusqueda != ""):
                QSproductos = QSproductos.filter(Q(nombre_prod__contains=textoBusqueda) | Q(descripcion__contains=textoBusqueda))
                mensaje_busqueda += "Nombre o descripcion que contenga la palabra "+textoBusqueda+"\n"
                
            if (nombre_prod != ""):
                QSproductos = QSproductos.filter(Q(nombre_prod__contains=nombre_prod) | Q(descripcion__contains=nombre_prod))
                mensaje_busqueda += "Nombre o descripcion que contenga la palabra "+nombre_prod+"\n"
                
            if (descripcion != ""):
                QSproductos = QSproductos.filter(Q(nombre_prod__contains=descripcion) | Q(descripcion__contains=descripcion))
                mensaje_busqueda += "Nombre o descripcion que contenga la palabra "+descripcion+"\n"
            
            if (not precio is None):
                QSproductos = QSproductos.filter(precio = precio)
                mensaje_busqueda += f"Precio que sea igual a {precio}\n"
            
            productos = QSproductos.all()
            
            return render(request, 'producto/producto_busqueda.html', {'productos_mostrar':productos, 'texto_busqueda':mensaje_busqueda})    
                
                
    else:
        formulario = BusquedaAvanzadaProductoForm(None)
        print("No coge nada")
    return render(request, 'producto/busqueda_avanzada.html',{"formulario":formulario})
                

def producto_editar(request, producto_id):
    producto = Producto.objects.get(id=producto_id)

    datosFormulario = None
    
    if request.method == 'POST':
        datosFormulario = request.POST

    formulario = ProductoModelForm(datosFormulario, instance=producto)
    
    if (request.method == "POST"):
        
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                messages.success(request, f"Se ha editado el producto {producto.nombre_prod} correctamente")
                return redirect('productos_con_proveedores')
            except Exception as error:
                print(error)
            
    return render(request, 'producto/actualizar.html',{"formulario":formulario, "producto":producto})

def producto_eliminar(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    try:
        producto.delete()
        messages.success(request, f"Se ha eliminado el producto {producto.nombre_prod} correctamente.")
    except:
        pass
    return redirect('productos_con_proveedores')


def crear_farmacia_modelo(formulario):
    farmacia_creada = False
    
    if formulario.is_valid():
        try:
            formulario.save()
            farmacia_creada = True
        except:
            pass
    return farmacia_creada

def farmacia_create(request):
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
        
    formulario = FarmaciaModelForm(datosFormulario)
    
    if (request.method == 'POST'):
        farmacia_creada = crear_farmacia_modelo(formulario)
        
        if(farmacia_creada):
            messages.success(request, 'Se ha creado la farmacia '+formulario.cleaned_data.get('nombre_farm')+' correctamente.')
            return redirect("farmacias_ordenadas_fecha")
    
    return render(request, 'farmacia/create_farmacia.html',{'formulario':formulario})


def farmacia_buscar(request):
    formulario = BusquedaFarmaciaForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        farmacias = Farmacia.objects.all()
        farmacias = farmacias.filter(nombre_farm__contains=texto).all()
        return render(request, 'farmacia/farmacia_busqueda.html',{'farmacias_mostrar':farmacias, 'texto_busqueda':texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
def farmacia_buscar_avanzado(request):
    
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaFarmaciaForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSfarmacias = Farmacia.objects.all()
            
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            nombre_farm = formulario.cleaned_data.get('nombre_farm')
            direccion_farm = formulario.cleaned_data.get('direccion_farm')
            telefono_farm = formulario.cleaned_data.get('telefono_farm')
            
            if (textoBusqueda != ""):
                QSfarmacias = QSfarmacias.filter(nombre_farm__contains=textoBusqueda)
                mensaje_busqueda += "Nombre o que contenga la palabra "+textoBusqueda+"\n"
                
            if (nombre_farm != ""):
                QSfarmacias = QSfarmacias.filter(nombre_farm__contains=nombre_farm)
                mensaje_busqueda += "Nombre o que contenga la palabra "+nombre_farm+"\n"
                
            if (direccion_farm != ""):
                QSfarmacias = QSfarmacias.filter(direccion_farm__contains=direccion_farm)
                mensaje_busqueda += "Direccion o que contenga la palabra "+direccion_farm+"\n"
            
            if (not telefono_farm is None):
                QSfarmacias = QSfarmacias.filter(telefono_farm = telefono_farm)
                mensaje_busqueda += f"Numero de telefono que sea igual a {telefono_farm}\n"
                
            farmacias = QSfarmacias.all()
            
            return render(request, 'farmacia/farmacia_busqueda.html', {'farmacias_mostrar':farmacias, 'texto_busqueda':mensaje_busqueda})  
                      
    else:
        formulario = BusquedaAvanzadaFarmaciaForm(None)
    return render(request, 'farmacia/busqueda_avanzada_farmacia.html',{'formulario':formulario})    
    
    
def farmacia_editar(request, farmacia_id):
    farmacia = Farmacia.objects.get(id=farmacia_id)
    
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
        
    formulario = FarmaciaModelForm(datosFormulario, instance = farmacia)
    
    if (request.method == "POST"):
        
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                return redirect('farmacias_ordenadas_fecha')
            except Exception as error:
                pass
    return render(request, 'farmacia/actualizar_farmacia.html', {'formulario': formulario, 'farmacia':farmacia})    
    
    
    
def farmacia_eliminar(request, farmacia_id):
    farmacia = Farmacia.objects.get(id=farmacia_id)
    try:
        farmacia.delete()
    except:
        pass
    return redirect('farmacias_ordenadas_fecha')




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





    