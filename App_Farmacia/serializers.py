from rest_framework import serializers
from .models import *

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
        