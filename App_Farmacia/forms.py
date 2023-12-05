from django import forms
from django.forms import ModelForm
from .models import *
from decimal import Decimal

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
    
    textoBusqueda = forms.CharField(required=False)
            
    nombre_prod = forms.CharField (required=False)
    
    descripcion = forms.CharField (required=False)
    
    precio = forms.DecimalField(required=False)
    
    farmacia_prod = forms.CharField (required=False)  
    
    prov_sum_prod = forms.CharField (required=False)
    
    def clean(self):
        
        super().clean()
        
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        nombre_prod = self.cleaned_data.get('nombre_prod')
        descripcion = self.cleaned_data.get('descripcion')
        precio = self.cleaned_data.get('precio')
        farmacia_prod = self.cleaned_data.get('farmacia_prod')
        prov_sum_prod = self.cleaned_data.get('prov_sum_prod')
        
        if(textoBusqueda == ""
           and nombre_prod == ""
           and descripcion == ""
           and farmacia_prod == ""
           and prov_sum_prod == ""
           and precio is None):
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('nombre_prod', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('descripcion', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('farmacia_prod', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('prov_sum_prod', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('precio', 'Debe introducir al menos un valor en un campo del formulario')
                    
        else:
            if(textoBusqueda != "" and len(textoBusqueda) < 3):
                self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres')
                
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
    