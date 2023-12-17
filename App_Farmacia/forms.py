from django import forms
from django.forms import ModelForm
from .models import *
from decimal import Decimal
from datetime import date
import datetime
from django.forms.widgets import DateInput
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.contrib.auth.forms import UserCreationForm


class RegistroForm(UserCreationForm):
    roles = (
                (Usuario.CLIENTE, 'cliente'),
                (Usuario.EMPLEADO, 'empleado'),
                (Usuario.GERENTE, 'gerente'),
    )
    rol = forms.ChoiceField(choices=roles)
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'rol')


class ProductoModelForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_prod','descripcion','precio','farmacia_prod','prov_sum_prod']
        labels = {
            "nombre_prod": "Nombre del Producto",
            "descripcion": "Descripcion del Producto",
            "precio": "Precio",
            "farmacia_prod":"Farmacia",
            "prov_sum_prod": "Proveedor del Producto",
        }
        help_texts = {
            "nombre_prod": "200 carácteres como máximo",
            "descripcion": "Al menos 10 carácteres como mínimo",
            "precio": "Indique un precio para el Producto",
            "farmacia_prod": "Indique la Farmacia del Producto",
            "prov_sum_prod": "Indique quien es el Proveedor",
        }
        
        widgets = {   
            
        }
        
    def clean(self):
        
        super().clean()
        
        #Obtenemos los campos
        nombre_prod = self.cleaned_data.get('nombre_prod')
        descripcion = self.cleaned_data.get('descripcion')
        precio = self.cleaned_data.get('precio')
        farmacia_prod = self.cleaned_data.get('farmacia_prod')
        prov_sum_prod = self.cleaned_data.get('prov_sum_prod')
        
        #Comprobamos que no existe un producto con ese nombre
        productoNombre = Producto.objects.filter(nombre_prod=nombre_prod).first()
        if (not productoNombre is None):
            if(not self.instance is None and productoNombre.id == self.instance.id):
                pass
            else:
                self.add_error('nombre_prod','Ya existe un producto con ese nombre')
            
        #Comprobamos que la descripción tiene al menos 10 carácteres.            
        if len(descripcion) < 10:
            self.add_error('descripcion','Al menos debes indicar 10 carácteres')
            
        #Comprobamos que el precio está puesto en su formato con decimales (float)
        if type(precio) != Decimal:
            self.add_error('precio','El precio introducido no es válido')
                        
        #Comprobamos que al menos seleccione un Proveedor
        if len(prov_sum_prod) < 1:
            self.add_error('prov_sum_prod','Debe seleccionar al menos un proveedor')
        
        #Siempre devolver los datos    
        return self.cleaned_data
    
class BusquedaProductoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
            
class BusquedaAvanzadaProductoForm(forms.Form):
    
    nombre_prod = forms.CharField (required=False, label="Nombre del Producto")
    
    descripcion = forms.CharField (required=False)
    
    precio = forms.DecimalField(required=False)
    
    farmacia_prod = forms.ModelChoiceField (queryset=Farmacia.objects.all(), required=False, label="Farmacia", widget=forms.Select())  
    
    prov_sum_prod = forms.ModelChoiceField (queryset=Proveedor.objects.all(), required=False, label="Proveedor", widget=forms.Select())
    
    def clean(self):
        
        super().clean()
        
        nombre_prod = self.cleaned_data.get('nombre_prod')
        descripcion = self.cleaned_data.get('descripcion')
        precio = self.cleaned_data.get('precio')
        farmacia_prod = self.cleaned_data.get('farmacia_prod')
        prov_sum_prod = self.cleaned_data.get('prov_sum_prod')
        
        if(nombre_prod == ""
           and descripcion == ""
           and farmacia_prod is None
           and prov_sum_prod is None
           and precio is None):
            self.add_error('nombre_prod', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('descripcion', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('farmacia_prod', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('prov_sum_prod', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('precio', 'Debe introducir al menos un valor en un campo del formulario')
                    
        else:
            if(nombre_prod != "" and len(nombre_prod) < 3):
                self.add_error('nombre_prod', 'Debe introducir al menos 3 caracteres')
                
            if(descripcion != "" and len(descripcion) < 10):
                self.add_error('nombre_prod', 'Debe introducir al menos 10 caracteres')
                
        return self.cleaned_data
    
    
class FarmaciaModelForm(ModelForm):
    class Meta:
        model = Farmacia
        fields = ['nombre_farm','direccion_farm','telefono_farm']
        labels = {
            'nombre_farm': "Nombre de la Farmacia",
            'direccion_farm': "Dirección",
            'telefono_farm': "Telefono",
        }
        help_texts = {
            "nombre_farm": "200 carácteres como máximo",
            "direccion_farm": "Al menos 10 carácteres como mínimo",
            "telefono_farm": "Indique un número de contacto",
        }
        widgets ={
            
        }
        
    def clean(self):
        
        super().clean()
        
        nombre_farm = self.cleaned_data.get('nombre_farm')
        direccion_farm = self.cleaned_data.get('direccion_farm')
        telefono_farm = self.cleaned_data.get('telefono_farm')
        
        #Comprobamos que no exista una farmacia con ese nombre
        farmaciaNombre = Farmacia.objects.filter(nombre_farm=nombre_farm).first()
        if(not (farmaciaNombre is None or (not self.instance is None and farmaciaNombre.id == self.instance.id))):
            self.add_error('nombre_farm','Ya existe una farmacia con ese nombre')
            
        #Comprobamos que se inserte una dirección
        if (direccion_farm is None):
            self.add_error('direccion_farm','Debe especificar una dirección para la farmacia')
            
        #Comprobamos que el numero tenga 9 digitos, sea español y no exista ya.
        if (str(telefono_farm)[0] not in ('6','7','9') or len(str(telefono_farm)) != 9):
            self.add_error('telefono_farm','Debe especificar un número español de 9 dígitos.')
        
        #Comprobamos que el numero no exista en otra farmacia.
        farmaciaTelefono = Farmacia.objects.filter(telefono_farm=telefono_farm).first()    
        if (not farmaciaTelefono is None):
            self.add_error('telefono_farm','Ya existe una farmacia con ese teléfono.')
            
        return self.cleaned_data

class BusquedaFarmaciaForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaFarmaciaForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)
            
    nombre_farm = forms.CharField (required=False)
    
    direccion_farm = forms.CharField (required=False)
    
    telefono_farm = forms.IntegerField(required=False)
    
    def clean(self):
        
        super().clean()
        
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        nombre_farm = self.cleaned_data.get('nombre_farm')
        direccion_farm = self.cleaned_data.get('direccion_farm')
        telefono_farm = self.cleaned_data.get('telefono_farm')
        
        if(textoBusqueda == ""
           and nombre_farm == ""
           and direccion_farm == ""
           and telefono_farm is None):
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('nombre_farm', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('direccion_farm', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('telefono_farm', 'Debe introducir al menos un valor en un campo del formulario')
                    
        else:
            if(textoBusqueda != "" and len(textoBusqueda) < 3):
                self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres')
                
        return self.cleaned_data
    
    
class GerenteModelForm(ModelForm):
    class Meta:
        model = Gerente
        fields = ['nombre_ger', 'correo', 'fecha_inicio_gestion', 'gerente_farm']
        labels = {
            "nombre_ger": 'Nombre del Gerente', 
            "correo": 'Correo Electrónico',
            "fecha_inicio_gestion" : 'Fecha de Inicio',
            "gerente_farm" : 'Farmacia Asignada',
        }
        help_texts = {
            "nombre_ger": '100 caracteres como máximo',
            "correo" : 'Por favor, introduce tu dirección de correo electrónico en el formato nombre@ejemplo.com.',
            "fecha_inicio_gestion" : 'Introduzca la fecha que inicia la gestion',
            "gerente_farm": 'Asigne una farmacia',
        }
        widgets = {
            "correo":forms.EmailInput(),
            "fecha_inicio_gestion":forms.SelectDateWidget(years=range(2000,2040)),
        }
        localized_fields = ["fecha_inicio_gestion"]
        
        
    def clean(self):
    
        super().clean()

        nombre_ger = self.cleaned_data.get('nombre_ger')
        correo = self.cleaned_data.get('correo')
        fecha_inicio_gestion = self.cleaned_data.get('fecha_inicio_gestion')
        gerente_farm = self.cleaned_data.get('gerente_farm')

        #Comprobamos que no exista un gerente con ese nombre
        gerenteNombre = Gerente.objects.filter(nombre_ger=nombre_ger).first()
        if(not (gerenteNombre is None or (not self.instance is None and gerenteNombre.id == self.instance.id))):
            self.add_error('nombre_ger','Ya existe un gerente con ese nombre')

        #Comprobamos que se inserte un correo
        if (correo is None):
            self.add_error('correo','Debe especificar un correo electrónico para la farmacia')

        #Comprobamos que la fecha de inicio de gestion no sea mayor a la de hoy.
        fechaHoy = date.today()
        if fechaHoy < fecha_inicio_gestion:
            self.add_error('fecha_inicio_gestion','La fecha de inicio de gestión no puede ser mayor a la fecha actual.')
               
        #Comprobamos que inserte una farmacia a gestionar    
        if (gerente_farm is None):
            self.add_error('gerente_farm','Debe introducir una farmacia a gestionar.')
            
        #Comprobamos que la farmacia no tenga ya a un gerente que la gestione
        farmaciaGestionada = Gerente.objects.filter(gerente_farm=gerente_farm).first()
        if (farmaciaGestionada):
            self.add_error('gerente_farm','La farmacia ya tiene a un gerente asignado.')

        return self.cleaned_data
               

class BusquedaGerenteForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaGerenteForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)
            
    nombre_ger = forms.CharField (required=False, label="Nombre del Gerente")
    
    correo = forms.CharField (required=False, label="Correo Electronico")
    
    fecha_inicio_gestion = forms.DateField(required=False, widget= forms.SelectDateWidget())
    
    gerente_farm = forms.ModelChoiceField (queryset=Farmacia.objects.all(), required=False, label="Farmacia Asignada", widget=forms.Select())
    
    def clean(self):
        
        super().clean()
        
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        nombre_ger = self.cleaned_data.get('nombre_ger')
        fecha_inicio_gestion = self.cleaned_data.get('fecha_inicio_gestion')
        correo = self.cleaned_data.get('correo')
        gerente_farm = self.cleaned_data.get('gerente_farm')
        fecha_hoy = date.today()
        if(textoBusqueda == ""
           and nombre_ger == ""
           and fecha_inicio_gestion is None
           and correo == ""
           and gerente_farm is None):
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('nombre_ger', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_inicio_gestion', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('correo', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('gerente_farm', 'Debe introducir al menos un valor en un campo del formulario')
                    
        else:
            if(textoBusqueda != "" and len(textoBusqueda) < 3):
                self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres')
                
            if(fecha_inicio_gestion and fecha_inicio_gestion > fecha_hoy):
                self.add_error('fecha_inicio_gestion','La busqueda por una fecha mayor a la de hoy no es válida, introduzca una fecha anterior.')
                
        return self.cleaned_data
    
    
    
    
    
    
    
    
class EmpleadoModelForm(ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre_emp', 'cargo', 'salario', 'farm_emp']
        labels = {
            "nombre_emp": 'Nombre del Empleado', 
            "cargo": 'Cargo del Empleado',
            "salario" : 'Salario',
            "farm_emp" : 'Farmacia Asignada',
        }
        help_texts = {
            "nombre_emp": '100 caracteres como máximo',
            "cargo" : 'Por favor, introduzca el cargo otorgado al empleado.',
            "salario" : 'Introduzca el salario del empleado.',
            "farm_emp": 'Asigne una farmacia',
        }
        widgets = {
        }
        
        
    def clean(self):
    
        super().clean()

        nombre_emp = self.cleaned_data.get('nombre_emp')
        cargo = self.cleaned_data.get('cargo')
        salario = self.cleaned_data.get('salario')
        farm_emp = self.cleaned_data.get('farm_emp')

        #Comprobamos que no exista un empleado con ese nombre
        empleadoNombre = Empleado.objects.filter(nombre_emp=nombre_emp).first()
        if(not (empleadoNombre is None or (not self.instance is None and empleadoNombre.id == self.instance.id))):
            self.add_error('nombre_emp','Ya existe un empleado con ese nombre.')

        #Comprobamos que se inserte un cargo para el empleado.
        if (cargo is None):
            self.add_error('cargo','Debe especificar un cargo para el empleado.')

        #Comprobamos que se inserte un salario para el empleado.
        if (salario is None):
            self.add_error('salario','Debe especificar un salario para el empleado.')
    
            
        #Comprobamos que se le asigne una farmacia al empleado.    
        if (farm_emp is None):
            self.add_error('farm_emp','Debe asignar una farmacia al empleado.')

        return self.cleaned_data
               

class BusquedaEmpleadoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaEmpleadoForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)
            
    nombre_emp = forms.CharField (required=False, label="Nombre del Empleado")
    
    cargo = forms.CharField (required=False, label="Cargo del Empleado")
    
    salario = forms.FloatField(required=False, label="Salario del Empleado")
    
    farm_emp = forms.ModelChoiceField (queryset=Farmacia.objects.all(), required=False, label="Farmacia Asignada", widget=forms.Select())
    
    def clean(self):
        
        super().clean()
        
        nombre_emp = self.cleaned_data.get('nombre_emp')
        cargo = self.cleaned_data.get('cargo')
        salario = self.cleaned_data.get('salario')
        farm_emp = self.cleaned_data.get('farm_emp')

        if(nombre_emp == ""
           and cargo == ""
           and salario is None
           and farm_emp is None):
            self.add_error('nombre_emp', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('cargo', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('salario', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('farm_emp', 'Debe introducir al menos un valor en un campo del formulario')
                    
        else:
            if(nombre_emp != "" and len(nombre_emp) < 3):
                self.add_error('nombre_emp', 'Debe introducir al menos 3 caracteres')
                
        return self.cleaned_data
    
    
    
    
    
class VotacionModelForm(ModelForm):
    class Meta:
        model = Votacion
        fields = ['puntuacion', 'comenta_votacion','voto_producto','voto_cliente']
        labels = {
            "puntuacion": "Puntuacion del Producto",
            "comenta_votacion": "Comentario sobre la Votacion",
            "voto_producto": "Nombre del Producto",
            "voto_cliente": "Nombre del Cliente",
            
        }
        help_texts = {
            "puntuacion": "Indique una puntuacion",
            "comenta_votacion": "Indiquenos por qué ha dado esta puntuación",
            "voto_producto": "Indique el nombre del producto",
            "voto_cliente": "Indique su nombre",
        }
        widgets = {
        }
        
    def clean(self):
        
        super().clean()
        
        #Obtenemos los campos
        puntuacion = self.cleaned_data.get('puntuacion')
        comenta_votacion = self.cleaned_data.get('comenta_votacion')
        voto_producto = self.cleaned_data.get('voto_producto')
        voto_cliente = self.cleaned_data.get('voto_cliente')
        
        
        #Comprobamos que el comentario tiene al menos 10 carácteres.            
        if len(comenta_votacion) < 10:
            self.add_error('comenta_votacion','Al menos debes indicar 10 carácteres')
                            
        #Comprobamos que seleccione un Producto
        if (voto_producto is None):
            self.add_error('voto_producto','Debe seleccionar un producto')
        
        #Comprobamos que seleccione un cliente
        if (voto_cliente is None):
            self.add_error('voto_cliente','Debe seleccionar quien realizo la votación')
        
        #Siempre devolver los datos    
        return self.cleaned_data
    
class BusquedaVotacionForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
            
class BusquedaAvanzadaVotacionForm(forms.Form):
    
    puntuacion = forms.IntegerField (required=False, label="Puntuacion")
    
    fecha_desde = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2030))
                                )
    
    fecha_hasta = forms.DateField(label="Fecha Hasta",
                                  required=False,
                                  widget= forms.SelectDateWidget(years=range(1990,2030))
                                )       
    
    comenta_votacion = forms.CharField(required=False)
    
    voto_producto = forms.ModelChoiceField (queryset=Producto.objects.all(), required=False, label="Producto", widget=forms.Select())  
    
    voto_cliente = forms.ModelChoiceField (queryset=Cliente.objects.all(), required=False, label="Cliente", widget=forms.Select())
    
    def clean(self):
        
        super().clean()
        
        puntuacion = self.cleaned_data.get('puntuaciom')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')
        comenta_votacion = self.cleaned_data.get('comenta_votacion')
        voto_producto = self.cleaned_data.get('voto_producto')
        voto_cliente = self.cleaned_data.get('voto_cliente')
        
        if(puntuacion is None
           and fecha_desde is None
           and fecha_hasta is None
           and comenta_votacion == ""
           and voto_producto is None
           and voto_cliente is None):
            self.add_error('puntuacion', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_desde', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_hasta', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('comenta_votacion', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('voto_producto', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('voto_cliente', 'Debe introducir al menos un valor en un campo del formulario')
                    
        else:
            if(comenta_votacion != "" and len(comenta_votacion) < 3):
                self.add_error('comenta_votacion', 'Debe introducir al menos 3 caracteres')
                
        return self.cleaned_data
    
  
    
    
class ClienteModelForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_cli', 'telefono_cli', 'direccion_cli', 'productos_favoritos']
        labels = {
            "nombre_cli": 'Nombre del Cliente', 
            "telefono_cli": 'Telefono del Cliente',
            "direccion_cli" : 'Direccion del Cliente',
            "productos_favoritos" : 'Productos Favoritos del Cliente',
        }
        help_texts = {
            "nombre_cli": '100 caracteres como máximo',
            "telefono_cli" : 'Número de teléfono del cliente.',
            "direccion_cli" : 'Introduzca la dirección del cliente.',
            "productos_favoritos" : 'Indique producto favorito del cliente.',
        }
        widgets = {
            
        }
        
        
    def clean(self):
    
        super().clean()

        nombre_cli = self.cleaned_data.get('nombre_cli')
        telefono_cli = self.cleaned_data.get('telefono_cli')
        direccion_cli = self.cleaned_data.get('direccion_cli')
        productos_favoritos = self.cleaned_data.get('productos_favoritos')

        #Comprobamos que no exista un cliente con ese nombre
        clienteNombre = Cliente.objects.filter(nombre_cli=nombre_cli).first()
        if(not (clienteNombre is None or (not self.instance is None and clienteNombre.id == self.instance.id))):
            self.add_error('nombre_cli','Ya existe un cliente con ese nombre.')

        #Comprobamos que se inserte una dirección para el cliente.
        if (direccion_cli is None):
            self.add_error('direccion_cli', 'Debe especificar una direccioón para el cliente.')
            
        #Comprobamos que el numero tenga 9 digitos, sea español y no exista ya.
        if (str(telefono_cli)[0] not in ('6','7','9') or len(str(telefono_cli)) != 9):
            self.add_error('telefono_cli','Debe especificar un número español de 9 dígitos.')
        
        #Comprobamos que el numero no exista en otro cliente.
        clienteTelefono = Cliente.objects.filter(telefono_cli=telefono_cli).first()    
        if (not clienteTelefono is None):
            self.add_error('telefono_cli','Ya existe un cliente con ese teléfono.')
                
        return self.cleaned_data
               

class BusquedaClienteForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaClienteForm(forms.Form):
    
    nombre_cli = forms.CharField (required=False, label="Nombre del Cliente")
    
    telefono_cli = forms.IntegerField (required=False, label="Teléfono del Cliente")
    
    direccion_cli = forms.CharField (required=False, label="Direccion del Cliente")
    
    productos_favoritos = forms.ModelChoiceField(queryset=Producto.objects.all(), required=False, label="Producto Favorito del Cliente", widget=forms.Select())
    
    votacion_prod = forms.ModelChoiceField (queryset=Producto.objects.all(), required=False, label="Productos Votados por el Cliente", widget=forms.Select())
    
    def clean(self):
        
        super().clean()
        
        nombre_cli = self.cleaned_data.get('nombre_cli')
        telefono_cli = self.cleaned_data.get('telefono_cli')
        direccion_cli = self.cleaned_data.get('direccion_cli')
        productos_favoritos = self.cleaned_data.get('productos_favoritos')
        votacion_prod = self.cleaned_data.get('votacion_prod')

        if(nombre_cli == ""
           and telefono_cli is None
           and direccion_cli == ""
           and productos_favoritos is None
           and votacion_prod is None):
            self.add_error('nombre_cli', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('telefono_cli', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('direccion_cli', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('productos_favoritos', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('votacion_prod', 'Debe introducir al menos un valor en un campo del formulario')
                    
        else:
            if(nombre_cli != "" and len(nombre_cli) < 3):
                self.add_error('nombre_cli', 'Debe introducir al menos 3 caracteres')
                
            if(direccion_cli != "" and len(direccion_cli) < 10):
                self.add_error('direccion_cli', 'Debe introducir al menos 10 caracteres')
                
        return self.cleaned_data
        
    
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    
    
    
    
    
    
    
class PromocionModelForm(ModelForm):
    class Meta:
        model = Promocion
        fields = ['nombre_promo', 'descripcion_promo','valor_promo','fecha_fin_promo','cliente_promo']
        labels = {
            "nombre_promo": "Nombre de la Promocion",
            "descripcion_promo": "Describe la Promocion",
            "valor_promo": "Valor de la Promocion",
            "fecha_fin_promo": "Indique fin de la promocion",
            "cliente_promo": "Seleccione al cliente beneficiado",
            
        }
        help_texts = {
            "nombre_promo": "Nombre la promocion",
            "descripcion_promo": "Describa la promocion",
            "valor_promo": "Indique de cuanto es la promoción",
            "fecha_fin_promo": "Fecha de expiración de la promoción",
            "cliente_promo": "Seleccione al cliente beneficiado",
        }
        widgets = {
            "fecha_fin_promo":forms.SelectDateWidget(),
        }
        
    def clean(self):
        
        super().clean()
        
        #Obtenemos los campos
        nombre_promo = self.cleaned_data.get('nombre_promo')
        descripcion_promo = self.cleaned_data.get('descripcion_promo')
        valor_promo = self.cleaned_data.get('valor_promo')
        fecha_fin_promo = self.cleaned_data.get('fecha_fin_promo')
        cliente_promo = self.cleaned_data.get('cliente_promo')
        
        
        #Nombre de la Promoción es único
        promocionNombre = Promocion.objects.filter(nombre_promo=nombre_promo).first()
        if(not (promocionNombre is None or (not self.instance is None and promocionNombre.id == self.instance.id))):
            self.add_error('nombre_promo','Ya existe una promocion con ese nombre')
        
        #Comprobamos que la descripción tiene al menos 100 carácteres.            
        if len(descripcion_promo) < 100:
            self.add_error('descripcion_promo','Al menos debes indicar 100 carácteres')
            
        #Comprobamos que el cliente no tenga ya la misma promoción aplicada
        mismaPromocionFalse = Promocion.objects.filter(cliente_promo=cliente_promo, nombre_promo=nombre_promo).exists()
        
        if (mismaPromocionFalse):
            self.add_error('nombre_promo','El cliente ya tiene esta promoción aplicada.')    
        
        #Comprobamos que el valor del descuento sea un entero entre 0 y 100
        if (valor_promo is None or valor_promo not in range(0,101)):
            self.add_error('valor_promo','Debe introducir un valor entero entre 0 y 100')
        
        #Comprobamos la fecha de expiración no sea inferior a la actual.
        fechaHoy = date.today()
        if (fechaHoy > fecha_fin_promo):
            self.add_error('fecha_fin_promo','Debe seleccionar una fecha de expiración mayor a la de hoy.')
        
        #Siempre devolver los datos    
        return self.cleaned_data
    
class BusquedaPromocionForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
            
class BusquedaAvanzadaPromocionForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)
            
    nombre_promo = forms.CharField (required=False, label="Nombre de la Promocion")
    
    descripcion_promo = forms.CharField(required=False)
    
    valor_promo = forms.IntegerField (required=False)
    
    fecha_desde = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2030))
                                )
    
    fecha_hasta = forms.DateField(label="Fecha Hasta",
                                  required=False,
                                  widget= forms.SelectDateWidget(years=range(1990,2030))
                                )       
                                  
    cliente_promo = forms.ModelChoiceField(queryset=Cliente.objects.all() ,required=False, label="Cliente con promoción", widget=forms.Select())
    
    def clean(self):
        
        super().clean()
        
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        nombre_promo = self.cleaned_data.get('nombre_promo')
        descripcion_promo = self.cleaned_data.get('descripcion_promo')
        valor_promo = self.cleaned_data.get('valor_promo')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')
        cliente_promo = self.cleaned_data.get('cliente_promo')
        
        if(textoBusqueda == ""
           and nombre_promo == ""
           and descripcion_promo == ""
           and valor_promo is None
           and fecha_desde is None
           and fecha_hasta is None
           and cliente_promo is None):
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('nombre_promo', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('descripcion_promo', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('valor_promo', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_desde', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_hasta', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('cliente_promo', 'Debe introducir al menos un valor en un campo del formulario')
            
                    
        else:
            if(textoBusqueda != "" and len(textoBusqueda) < 3):
                self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres')
            
            if(not fecha_desde is None  and not fecha_hasta is None and fecha_hasta < fecha_desde):
                self.add_error('fecha_desde','La fecha hasta no puede ser menor que la fecha desde')
                self.add_error('fecha_hasta','La fecha hasta no puede ser menor que la fecha desde')
                
        return self.cleaned_data