from django.shortcuts import render, redirect

# Create your views here.
from .models import *
from django.db.models import Q, Prefetch
from django.views.defaults import page_not_found
from datetime import datetime as dt, date
from django.db.models import Avg
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required



def index(request):
    if(not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = dt.now().strftime("%d/%m/%Y %H:%M")
    
    return render(request, 'index.html')

def borrar_sesion(request):
    del request.session["fecha_inicio"]
    
    return render(request, 'index.html')

def registrar_usuario(request):
    
    if request.method == "POST":
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            if (rol == Usuario.CLIENTE):
                cliente = Cliente.objects.create(usuario = user)
                cliente.save()
            if (rol == Usuario.EMPLEADO):
                empleado = Empleado.objects.create(usuario = user)
                empleado.save()
            if (rol == Usuario.GERENTE):
                gerente = Gerente.objects.create(usuario = user)
                gerente.save()
                
            login(request, user)
            return redirect('index')
        
    else:
        formulario = RegistroForm()
    
    return render(request, 'registration/signup.html', {'formulario': formulario})

def login_menu (request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Credenciales incorrectas. Por favor, inténtalo de nuevo.')

            return redirect('index')
        
    return render(request, 'registration/login_menu.html')


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

@permission_required('App_Farmacia.add_producto')
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
            return redirect("lista_productos")       

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
            
            return render(request, 'producto/producto_busqueda.html', {'productos_mostrar':productos, 'texto_busqueda':mensaje_busqueda})    
                
                
    else:
        formulario = BusquedaAvanzadaProductoForm(None)
    return render(request, 'producto/busqueda_avanzada.html',{"formulario":formulario})
                
@permission_required('App_Farmacia.change_producto')
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
                return redirect('lista_productos')
            except Exception as error:
                print(error)
            
    return render(request, 'producto/actualizar.html',{"formulario":formulario, "producto":producto})

@permission_required('App_Farmacia.delete_producto')
def producto_eliminar(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    try:
        producto.delete()
        messages.success(request, f"Se ha eliminado el producto {producto.nombre_prod} correctamente.")
    except:
        pass
    return redirect('lista_productos')

def crear_farmacia_modelo(formulario):
    farmacia_creada = False
    
    if formulario.is_valid():
        try:
            formulario.save()
            farmacia_creada = True
        except:
            pass
    return farmacia_creada

@permission_required('App_Farmacia.add_farmacia')
def farmacia_create(request):
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
        
    formulario = FarmaciaModelForm(datosFormulario)
    
    if (request.method == 'POST'):
        farmacia_creada = crear_farmacia_modelo(formulario)
        
        if(farmacia_creada):
            messages.success(request, 'Se ha creado la farmacia '+formulario.cleaned_data.get('nombre_farm')+' correctamente.')
            return redirect("lista_farmacias")
    
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
    
    
@permission_required('App_Farmacia.change_farmacia')
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
                messages.success(request, f"Se ha editado la farmacia {farmacia.nombre_farm} correctamente")
                return redirect('lista_farmacias')
            except Exception as error:
                pass
    return render(request, 'farmacia/actualizar_farmacia.html', {'formulario': formulario, 'farmacia':farmacia})    
    
    

@permission_required('App_Farmacia.delete_farmacia')
def farmacia_eliminar(request, farmacia_id):
    farmacia = Farmacia.objects.get(id=farmacia_id)
    try:
        farmacia.delete()
        messages.success(request, f"Se ha eliminado la farmacia {farmacia.nombre_farm} correctamente.")
    except:
        pass
    return redirect('lista_farmacias')


def crear_gerente_modelo(formulario):
        
    gerente_creado = False
    #Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            #Guarda el producto en la base de datos
            formulario.save()
            gerente_creado = True
        except:
            pass
    return gerente_creado                

@permission_required('App_Farmacia.add_gerente')
def gerente_create(request):
    
    # Si la petición es GET se creará el formulario Vacio
    # Si la petición es POST se creará el formulario con Datos
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = GerenteModelForm(datosFormulario)
    if (request.method == 'POST'):
        gerente_creado = crear_gerente_modelo(formulario)
        if (gerente_creado):
            messages.success(request, 'Se ha añadido el gerente '+formulario.cleaned_data.get('nombre_ger')+" correctamente")
            return redirect("lista_gerentes")       

    return render(request, 'gerente/create_gerente.html', {'formulario':formulario})

@permission_required('App_Farmacia.view_gerente')
def gerente_buscar(request):
    formulario = BusquedaGerenteForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        gerentes = Gerente.objects.all()
        gerentes = gerentes.filter(nombre_ger__contains=texto).all()
        return render(request, 'gerente/gerente_busqueda.html',{'gerentes_mostrar':gerentes, 'texto_busqueda':texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
@permission_required('App_Farmacia.view_gerente')
def gerente_buscar_avanzado(request):
    
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaGerenteForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSgerentes = Gerente.objects.all()
            
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            nombre_ger = formulario.cleaned_data.get('nombre_ger')
            correo = formulario.cleaned_data.get('correo')
            fecha_inicio_gestion = formulario.cleaned_data.get('fecha_inicio_gestion')
            gerente_farm = formulario.cleaned_data.get('gerente_farm')
            
            if (textoBusqueda != ""):
                QSgerentes = QSgerentes.filter(nombre_ger__contains=textoBusqueda)
                mensaje_busqueda += "Nombre o que contenga la palabra "+textoBusqueda+"\n"
                
            if (nombre_ger != ""):
                QSgerentes = QSgerentes.filter(nombre_ger__contains=nombre_ger)
                mensaje_busqueda += "Nombre o que contenga la palabra "+nombre_ger+"\n"
                
            if (correo != ""):
                QSgerentes = QSgerentes.filter(correo__contains=correo)
                mensaje_busqueda += "Direccion o que contenga la palabra "+correo+"\n"
            
            if (not fecha_inicio_gestion is None):
                mensaje_busqueda += f"Fecha de inicio de gestion que sea igual o mayor a "+datetime.strftime(fecha_inicio_gestion, '%d-%m-%Y')+"\n"
                QSgerentes = QSgerentes.filter(fecha_inicio_gestion__gte = fecha_inicio_gestion)
                
            if (not gerente_farm is None):
                mensaje_busqueda += "Gerente que tenga asignado la farmacia "+gerente_farm.nombre_farm+"\n"
                QSgerentes = QSgerentes.filter(gerente_farm=gerente_farm)
                
            gerentes = QSgerentes.all()
            
            return render(request, 'gerente/gerente_busqueda.html', {'gerentes_mostrar':gerentes, 'texto_busqueda':mensaje_busqueda})  
                      
    else:
        formulario = BusquedaAvanzadaGerenteForm(None)
        
    return render(request, 'gerente/busqueda_avanzada_gerente.html',{'formulario':formulario})    
    
    
@permission_required('App_Farmacia.change_gerente')
def gerente_editar(request, gerente_id):
    gerente = Gerente.objects.get(id=gerente_id)
    
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
        
    formulario = GerenteModelForm(datosFormulario, instance = gerente)
    
    if (request.method == "POST"):
        
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                messages.success(request, f"Se ha editado el gerente {gerente.nombre_ger} correctamente")
                return redirect('lista_gerentes')
            except Exception as error:
                pass
    return render(request, 'gerente/actualizar_gerente.html', {'formulario': formulario, 'gerente':gerente})    
    
    
    
@permission_required('App_Farmacia.delete_gerente')
def gerente_eliminar(request, gerente_id):
    gerente = Gerente.objects.get(id=gerente_id)
    try:
        gerente.delete()
        messages.success(request, f"Se ha eliminado el gerente {gerente.nombre_ger} correctamente.")
    except:
        pass
    return redirect('lista_gerentes')



def crear_empleado_modelo(formulario):
        
    empleado_creado = False
    #Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            #Guarda el producto en la base de datos
            usuario = Usuario.objects.create(
                 username=formulario.cleaned_data.get('username'),
                first_name=formulario.cleaned_data.get('first_name'),
                email=formulario.cleaned_data.get('email'),
                date_joined=formulario.cleaned_data.get('date_joined'),
                rol=Usuario.EMPLEADO
            )
            usuario.set_password(formulario.cleaned_data.get("password"))
            usuario.save()
            empleado = Empleado.objects.create(
                usuario= usuario,
                salario= formulario.cleaned_data.get("salario"),
                farm_emp= formulario.cleaned_data.get("farm_emp"),
            )
            empleado.save() 
            empleado_creado = True
        except Exception as e: 
            print(e)
    return empleado_creado                

@permission_required('App_Farmacia.add_empleado')
def empleado_create(request):
    
    # Si la petición es GET se creará el formulario Vacio
    # Si la petición es POST se creará el formulario con Datos
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = EmpleadoModelForm(datosFormulario)
    if (request.method == 'POST'):
        empleado_creado = crear_empleado_modelo(formulario)
        if (empleado_creado):
            messages.success(request, 'Se ha añadido el '+formulario.cleaned_data.get('first_name')+" correctamente")
            return redirect("lista_empleados")       

    return render(request, 'empleado/create_empleado.html', {'formulario':formulario})

@permission_required('App_Farmacia.view_empleado')
def empleado_buscar(request):
    formulario = BusquedaEmpleadoForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        empleados = Empleado.objects.all()
        empleados = empleados.filter(nombre_emp__contains=texto).all()
        return render(request, 'empleado/empleado_busqueda.html',{'empleados_mostrar':empleados, 'texto_busqueda':texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
@permission_required('App_Farmacia.view_empleado')
def empleado_buscar_avanzado(request):
    
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaEmpleadoForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSempleados = Empleado.objects.all()
            
            nombre_emp = formulario.cleaned_data.get('nombre_emp')
            cargo = formulario.cleaned_data.get('cargo')
            salario = formulario.cleaned_data.get('salario')
            farm_emp = formulario.cleaned_data.get('farm_emp')
            
            if (nombre_emp != ""):
                QSempleados = QSempleados.filter(nombre_emp__contains=nombre_emp)
                mensaje_busqueda += "Nombre o que contenga la palabra "+nombre_emp+"\n"
                
            if (cargo != ""):
                QSempleados = QSempleados.filter(cargo__contains=cargo)
                mensaje_busqueda += "Cargo o que contenga la palabra "+cargo+"\n"
            
            if (not salario is None):
                mensaje_busqueda += f"Salario que sea igual o mayor a "+str(salario)+"\n"
                QSempleados = QSempleados.filter(salario__gte = salario)
                
            if (not farm_emp is None):
                QSempleados = QSempleados.filter(farm_emp=farm_emp)
                mensaje_busqueda += "Que este asignado/a a la Farmacia "+farm_emp.nombre_farm+"\n"
            
            empleados = QSempleados.all()
            
            return render(request, 'empleado/empleado_busqueda.html', {'empleados_mostrar':empleados, 'texto_busqueda':mensaje_busqueda})  
                      
    else:
        formulario = BusquedaAvanzadaEmpleadoForm(None)
        
    return render(request, 'empleado/busqueda_avanzada_empleado.html',{'formulario':formulario})    
  
    
@permission_required('App_Farmacia.change_empleado')
def empleado_editar(request, empleado_id):
    empleado = Empleado.objects.get(id=empleado_id)
    
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
        
    formulario = EmpleadoModelForm(datosFormulario, instance = empleado)
    
    if (request.method == "POST"):
        
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                messages.success(request, f"Se ha editado el empleado {empleado.nombre_emp} correctamente")
                return redirect('lista_empleados')
            except Exception as error:
                pass
    return render(request, 'empleado/actualizar_empleado.html', {'formulario': formulario, 'empleado':empleado})    
        
@permission_required('App_Farmacia.delete_empleado')
def empleado_eliminar(request, empleado_id):
    empleado = Empleado.objects.get(id=empleado_id)
    try:
        empleado.delete()
        messages.success(request, f"Se ha eliminado el empleado {empleado.nombre_emp} correctamente.")
    except:
        pass
    return redirect('lista_empleados')


def crear_votacion_modelo(formulario):
        
    votacion_creada = False
    #Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            #Guarda el producto en la base de datos
            formulario.save()
            votacion_creada = True
        except:
            pass
    return votacion_creada                

@permission_required('App_Farmacia.add_votacion')
def votacion_create(request):
    
    # Si la petición es GET se creará el formulario Vacio
    # Si la petición es POST se creará el formulario con Datos
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = VotacionModelForm(datosFormulario)
    if (request.method == 'POST'):
        votacion_creada = crear_votacion_modelo(formulario)
        if (votacion_creada):
            messages.success(request, 'Se ha añadido la votación al producto '+formulario.cleaned_data.get('voto_producto').nombre_prod+" correctamente")
            return redirect("lista_votaciones")       

    return render(request, 'votacion/create_votacion.html', {'formulario':formulario})

def votacion_buscar(request):
    formulario = BusquedaVotacionForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        votaciones = Votacion.objects.all()
        votaciones = votaciones.filter(Q(comenta_votacion__contains=texto) | Q(voto_producto__nombre_prod__contains=texto)).all()
        return render(request, 'votacion/votacion_busqueda.html',{'votaciones_mostrar':votaciones, 'texto_busqueda':texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
def votacion_buscar_avanzado(request):
    
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
                mensaje_busqueda += "Puntuacion sea o que contenga la palabra "+puntuacion+"\n"
                
            if(not fechaDesde is None):
                mensaje_busqueda +=" La fecha sea mayor a "+date.strftime(fechaDesde,'%d-%m-%Y')+"\n"
                QSpromociones = QSpromociones.filter(fecha_fin_promo__gte=fechaDesde)
            
            if(not fechaHasta is None):
                mensaje_busqueda +=" La fecha sea menor a "+date.strftime(fechaHasta,'%d-%m-%Y')+"\n"
                QSpromociones = QSpromociones.filter(fecha_fin_promo__lte=fechaHasta)
            
            if (comenta_votacion != ""):
                QSvotaciones = QSvotaciones.filter(comenta_votacion__contains=comenta_votacion)
                mensaje_busqueda += "Comentario o que contenga la palabra "+comenta_votacion+"\n"
            
            if (not voto_producto is None):
                QSvotaciones = QSvotaciones.filter(voto_producto=voto_producto)
                mensaje_busqueda += "Que el producto sea "+voto_producto.nombre_prod+"\n"
                
            if (not voto_cliente is None):
                QSvotaciones = QSvotaciones.filter(voto_cliente=voto_cliente)
                mensaje_busqueda += "Que el cliente sea "+voto_cliente.nombre_cli+"\n"
        
            
            votaciones = QSvotaciones.all()
            
            return render(request, 'votacion/votacion_busqueda.html', {'votaciones_mostrar':votaciones, 'texto_busqueda':mensaje_busqueda})  
                      
    else:
        formulario = BusquedaAvanzadaVotacionForm(None)
        
    return render(request, 'votacion/busqueda_avanzada_votacion.html',{'formulario':formulario})    
    
    
@permission_required('App_Farmacia.change_votacion')
def votacion_editar(request, votacion_id):
    votacion = Votacion.objects.get(id=votacion_id)
    
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
        
    formulario = VotacionModelForm(datosFormulario, instance = votacion)
    
    if (request.method == "POST"):
        
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                messages.success(request, f"Se ha editado la votación al producto {votacion.voto_producto.nombre_prod} correctamente")
                return redirect('lista_votaciones')
            except Exception as error:
                pass
    return render(request, 'votacion/actualizar_votacion.html', {'formulario': formulario, 'votacion':votacion})    
        
    
@permission_required('App_Farmacia.delete_votacion')
def votacion_eliminar(request, votacion_id):
    votacion = Votacion.objects.get(id=votacion_id)
    try:
        votacion.delete()
        messages.success(request, f"Se ha eliminado la votación al producto {votacion.voto_producto.nombre_prod} correctamente.")
    except:
        pass
    return redirect('lista_votaciones')




def crear_cliente_modelo(formulario):
        
    cliente_creado = False
    #Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            #Guarda el producto en la base de datos
            formulario.save()
            cliente_creado = True
        except:
            pass
    return cliente_creado                

@permission_required('App_Farmacia.add_cliente')
def cliente_create(request):
    
    # Si la petición es GET se creará el formulario Vacio
    # Si la petición es POST se creará el formulario con Datos
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = ClienteModelForm(datosFormulario)
    if (request.method == 'POST'):
        cliente_creado = crear_cliente_modelo(formulario)
        
        if (cliente_creado):
            messages.success(request, 'Se ha añadido el cliente '+formulario.cleaned_data.get('nombre_cli')+" correctamente")
            return redirect("lista_clientes")       

    return render(request, 'cliente/create_cliente.html', {'formulario':formulario})

@permission_required('App_Farmacia.view_cliente')
def cliente_buscar(request):
    formulario = BusquedaClienteForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        clientes = Cliente.objects.all()
        clientes = clientes.filter(nombre_cli__contains=texto).all()
        return render(request, 'cliente/cliente_busqueda.html',{'clientes_mostrar':clientes, 'texto_busqueda':texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
@permission_required('App_Farmacia.view_cliente')
def cliente_buscar_avanzado(request):
    
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaClienteForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSclientes = Cliente.objects.all()
            
            nombre_cli = formulario.cleaned_data.get('nombre_cli')
            telefono_cli = formulario.cleaned_data.get('telefono_cli')
            direccion_cli = formulario.cleaned_data.get('direccion_cli')
            productos_favoritos = formulario.cleaned_data.get('productos_favoritos')
            votacion_prod = formulario.cleaned_data.get('votacion_prod')
                
            if (nombre_cli != ""):
                QSclientes = QSclientes.filter(nombre_cli__contains=nombre_cli)
                mensaje_busqueda += "Nombre o que contenga la palabra "+nombre_cli+"\n"
                
            if (not telefono_cli is None):
                QSclientes = QSclientes.filter(telefono_cli=telefono_cli)
                mensaje_busqueda += "Que el teléfono sea "+telefono_cli+"\n"
            
            if (direccion_cli != ""):
                mensaje_busqueda += f"Que la direccion sea o contenga la palabra "+direccion_cli+"\n"
                QSclientes = QSclientes.filter(direccion_cli__contains = direccion_cli)
                
            if (not productos_favoritos is None):
                QSclientes = QSclientes.filter(productos_favoritos=productos_favoritos)
                mensaje_busqueda += "Que el producto favorito sea "+productos_favoritos.nombre_prod+"\n"
            
            if (not votacion_prod is None):
                QSclientes = QSclientes.filter(votacion_prod=votacion_prod)
                mensaje_busqueda += "Que el producto que ha votado sea  "+votacion_prod.nombre_prod+"\n"
            
            clientes = QSclientes.all()
            
            return render(request, 'cliente/cliente_busqueda.html', {'clientes_mostrar':clientes, 'texto_busqueda':mensaje_busqueda})  
                      
    else:
        formulario = BusquedaAvanzadaClienteForm(None)
        
    return render(request, 'cliente/busqueda_avanzada_cliente.html',{'formulario':formulario})    
    
@permission_required('App_Farmacia.change_cliente')    
def cliente_editar(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
        
    formulario = ClienteModelForm(datosFormulario, instance = cliente)
    
    if (request.method == "POST"):
        
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                messages.success(request, f"Se ha editado el cliente {cliente.nombre_cli} correctamente")
                return redirect('lista_clientes')
            except Exception as error:
                pass
    return render(request, 'cliente/actualizar_cliente.html', {'formulario': formulario, 'cliente':cliente})    
        
@permission_required('App_Farmacia.delete_cliente')      
def cliente_eliminar(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    try:
        cliente.delete()
        messages.success(request, f"Se ha eliminado el cliente {cliente.nombre_cli} correctamente.")
    except:
        pass
    return redirect('lista_clientes')

















def crear_promocion_modelo(formulario):
        
    promocion_creada = False
    #Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            #Guarda el producto en la base de datos
            formulario.save()
            promocion_creada = True
        except:
            pass
    return promocion_creada                

@permission_required('App_Farmacia.add_promocion')
def promocion_create(request):
    
    # Si la petición es GET se creará el formulario Vacio
    # Si la petición es POST se creará el formulario con Datos
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = PromocionModelForm(datosFormulario)
    if (request.method == 'POST'):
        promocion_creada = crear_promocion_modelo(formulario)
        if (promocion_creada):
            messages.success(request, 'Se ha añadido la promocion '+formulario.cleaned_data.get('nombre_promo')+" correctamente")
            return redirect("lista_promociones")       

    return render(request, 'promocion/create_promocion.html', {'formulario':formulario})

def promocion_buscar(request):
    formulario = BusquedaPromocionForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        promociones = Promocion.objects.all()
        promociones = promociones.filter(Q(nombre_promo__contains=texto) | Q(descripcion_promo__contains=texto)).all()
        return render(request, 'promocion/promocion_busqueda.html',{'promociones_mostrar':promociones, 'texto_busqueda':texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
def promocion_buscar_avanzado(request):
    
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaPromocionForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSpromociones = Promocion.objects.all()
            
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            nombre_promo = formulario.cleaned_data.get('nombre_promo')
            descripcion_promo = formulario.cleaned_data.get('descripcion_promo')
            valor_promo = formulario.cleaned_data.get('valor_promo')
            fechaDesde = formulario.cleaned_data.get('fecha_desde')
            fechaHasta = formulario.cleaned_data.get('fecha_hasta')
            cliente_promo = formulario.cleaned_data.get('cliente_promo')
            
            if (textoBusqueda != ""):
                QSvotaciones = QSvotaciones.filter(Q(nombre_promo__contains=textoBusqueda) | Q(descripcion_promo__contains=textoBusqueda))
                mensaje_busqueda += "Que su comentario sea o contenga la palabra "+textoBusqueda+"\n"
                
            if (nombre_promo != ""):
                QSpromociones = QSpromociones.filter(nombre_promo__contains=nombre_promo)
                mensaje_busqueda += "Nombre sea o que contenga la palabra "+nombre_promo+"\n"
                
            if(not fechaDesde is None):
                mensaje_busqueda +=" La fecha sea mayor a "+date.strftime(fechaDesde,'%d-%m-%Y')+"\n"
                QSpromociones = QSpromociones.filter(fecha_fin_promo__gte=fechaDesde)
            
            if(not fechaHasta is None):
                mensaje_busqueda +=" La fecha sea menor a "+date.strftime(fechaHasta,'%d-%m-%Y')+"\n"
                QSpromociones = QSpromociones.filter(fecha_fin_promo__lte=fechaHasta)
            
                
            if (descripcion_promo != ""):
                QSpromociones = QSpromociones.filter(descripcion_promo__contains=descripcion_promo)
                mensaje_busqueda += "Descripcion sea o que contenga la palabra "+descripcion_promo+"\n"
            
            if (not valor_promo is None):
                QSpromociones = QSpromociones.filter(valor_promo__gte=valor_promo)
                mensaje_busqueda += "Promociones que sean mayor a "+valor_promo+"\n"
                
            if (not cliente_promo is None):
                QSpromociones = QSpromociones.filter(cliente_promo=cliente_promo)
                mensaje_busqueda += "Cliente/s que tienen promociones "+cliente_promo.nombre_cli+"\n"
        
            
            promociones = QSpromociones.all()
            
            return render(request, 'promocion/promocion_busqueda.html', {'promociones_mostrar':promociones, 'texto_busqueda':mensaje_busqueda})  
                      
    else:
        formulario = BusquedaAvanzadaPromocionForm(None)
        
    return render(request, 'promocion/busqueda_avanzada_promocion.html',{'formulario':formulario})    
    
    
@permission_required('App_Farmacia.change_promocion')
def promocion_editar(request, promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
        
    formulario = PromocionModelForm(datosFormulario, instance = promocion)
    
    if (request.method == "POST"):
        
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                messages.success(request, f"Se ha editado la promocion {promocion.nombre_promo} correctamente")
                return redirect('lista_promociones')
            except Exception as error:
                pass
    return render(request, 'promocion/actualizar_promocion.html', {'formulario': formulario, 'promocion':promocion})    
        
    
@permission_required('App_Farmacia.delete_promocion')
def promocion_eliminar(request, promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    try:
        promocion.delete()
        messages.success(request, f"Se ha eliminado la promocion {promocion.nombre_promo} correctamente.")
    except:
        pass
    return redirect('lista_promociones')









@permission_required('App_Farmacia.view_cliente')
def clientes_lista(request):
    clientes = Cliente.objects.select_related('usuario').prefetch_related('productos_favoritos', 'votacion_prod').all()
    
    return render(request, 'cliente/lista_clientes.html', {'clientes': clientes})


def promociones_lista(request):
    promociones = Promocion.objects.select_related('cliente_promo').all()
    
    return render(request, 'promocion/lista_promociones.html', {'promociones': promociones})


def votaciones_lista(request):
    votaciones = Votacion.objects.select_related('voto_producto', 'voto_cliente').all()
    
    return render(request, 'votacion/lista_votaciones.html', {'votaciones': votaciones})

@permission_required('App_Farmacia.view_empleado')
def empleados_lista(request):
    empleados = Empleado.objects.select_related('farm_emp', 'usuario').all()
    
    return render(request, 'empleado/lista_empleados.html', {'empleados':empleados})

def farmacias_lista(request):
    farmacias = Farmacia.objects.all()
    
    return render(request, 'farmacia/lista_farmacias.html', {'farmacias':farmacias})

@permission_required('App_Farmacia.view_gerente')
def gerentes_lista(request):
    gerentes = Gerente.objects.select_related('gerente_farm','usuario').all()
    
    return render(request, 'gerente/lista_gerentes.html', {'gerentes':gerentes})

def productos_lista(request):
    productos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod').all()

    return render(request, 'producto/lista_productos.html', {'productos':productos})



def farmacia_ordenada_fecha(request):
    datos = DatosFarmacia.objects.select_related("farmacia_datos").order_by("fecha_creacion").all()
    return render(request, 'farmacia/farmaciaydatos.html', {'farmacias_fecha':datos})

def gerente_nombre(request, nombre_introducido):
    gerentes = Gerente.objects.select_related('gerente_farm', 'usuario').filter(nombre_ger__contains=nombre_introducido)
    return render(request, 'gerente/gerentes_filtrado_nombre.html', {'gerentes':gerentes})

def farmacias_con_gerentes(request):
    farmacias = Farmacia.objects.select_related('gerente').all()
    return render(request, 'farmacia/farmaciaygerentes.html', {'farmacias':farmacias, 'gerente':request})

def productos_con_proveedores(request):
    productos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod').all()
    return render(request, 'producto/producto_proveedores.html', {'productos':productos})

def empleado_compras(request):
    compras = Compra.objects.select_related("empleado_compra").prefetch_related("producto_compra").all()
    return render(request, 'empleado/empleado_y_compras.html', {'compras_empleados':compras})

def detalle_compra(request):
    compra = Compra.objects.select_related('cliente_compra', 'empleado_compra').prefetch_related('producto_compra').all()
    return render(request, 'compra/compra_detalle_empleado.html', {'compras':compra})

def detalle_compra_id(request, id_compra):
    compra = Compra.objects.select_related('cliente_compra', 'empleado_compra').prefetch_related('producto_compra').filter(id=id_compra)
    return render(request, 'compra/compraydetalles_id.html', {'compras_id':compra})

def clientes_productosfavoritos(request):
    clientes = Cliente.objects.select_related('usuario').prefetch_related('productos_favoritos').all()
    return render(request, 'cliente/cliente_prod_fav.html', {'clientes':clientes})

def empleado_salariosuperior(request, cantidad_salario):
    empleados = Empleado.objects.select_related('usuario', 'farm_emp').filter(salario__gte=cantidad_salario).all()   #IMPORTANTE gte = mayor o igual que  y  lte = menor o igual que
    return render(request, 'empleado/empleados_salario_superior.html', {'empleados':empleados})

def productos_disponibles_farmacia_especifica(request, id_farmacia):
    farmacia = Farmacia.objects.get(id=id_farmacia)
    productos = Producto.objects.filter(farmacia_prod = farmacia).order_by('-precio').all()
    return render(request, 'farmacia/farmaciayproductos.html', {'productos':productos, 'farmacia': farmacia})

def compras_entre_fechas(request, fecha_inicio, fecha_fin):
    fecha_inicio = dt.strptime(fecha_inicio, '%Y-%m-%d').date()
    fecha_fin = dt.strptime(fecha_fin, '%Y-%m-%d').date()
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




def productos_con_puntuacion_3_cliente_concreto(request, cliente_id):
    cliente = Cliente.objects.select_related('usuario').prefetch_related("productos_favoritos", "votacion_prod").get(pk=cliente_id)
    
    votaciones_cliente = Votacion.objects.filter(voto_cliente=cliente, puntuacion=3).values_list('id', flat=True)
    
    productos_con_votos = Producto.objects.filter(votacion_prod__in=votaciones_cliente).all()
    
    return render(request, 'producto/productos_con_3.html', {'productos_con_votos': productos_con_votos})

    
def clientes_nunca_votaron(request):
    clientes_no_votaron = Cliente.objects.select_related('usuario').prefetch_related("productos_favoritos", "votacion_prod").filter(votacion__isnull=True).all()
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





    