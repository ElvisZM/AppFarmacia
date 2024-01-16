from rest_framework import serializers
from .models import *

class Farmacia(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
        

