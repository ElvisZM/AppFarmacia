from rest_framework import serializers
from .models import *

class UsuarioSerializer(serializers.ModelSerializer):
    
    date_joined = serializers.DateTimeField(format=('%d-%m-%Y'))
    
    last_login = serializers.DateTimeField(format=('%d-%m-%Y'))
    
    class Meta:
        model = Usuario
        fields = '__all__'

class FarmaciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
    
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'
        
class ProductoSerializerMejorado(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne o OneToOne
    farmacia_prod = FarmaciaSerializer()
    
    #Para relaciones ManyToMany
    prov_sum_prod = ProveedorSerializer(read_only=True, many=True)
    
    class Meta:
        fields = ('id', 'nombre_prod', 'descripcion', 'precio', 'farmacia_prod', 'prov_sum_prod')
        model = Producto
        
        
class EmpleadoSerializer(serializers.ModelSerializer):
    
    class Meta:        
        model = Empleado
        fields = '__all__'
    
    
class EmpleadoSerializerMejorado(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne u OneToOne
    farm_emp = FarmaciaSerializer()
    usuario = UsuarioSerializer()
    
    #Para formatear fechas si estan heredadas de AbstractUser, se realizan en el campo Usuario
    
    class Meta:
        model = Empleado
        fields = ('id', 'usuario', 'direccion_emp', 'telefono_emp', 'salario', 'farm_emp')
        
class ClienteSerializerMejorado(serializers.ModelSerializer):

    
    #Para relaciones ManyToOne u OneToOne
    usuario = UsuarioSerializer()
    
    #Para relaciones ManyToMany
    productos_favoritos = ProductoSerializerMejorado(read_only=True, many=True)
    votacion_prod = ProductoSerializerMejorado(read_only=True, many=True)
    
    class Meta:
        model = Cliente
        fields = '__all__'
    

class VotacionSerializerMejorado(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne u OneToOne
    voto_producto = ProductoSerializerMejorado()
    voto_cliente = ClienteSerializerMejorado()
    
    #Para obtener el valor de un Choice
    puntuacion = serializers.IntegerField(source='get_puntuacion_display')
    
    #Para formatear fechas
    fecha_votacion = serializers.DateField(format=('%d-%m-%Y'))
    
    class Meta:
        model = Votacion
        fields = '__all__'
    