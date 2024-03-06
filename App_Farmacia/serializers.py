from rest_framework import serializers
from .models import *
from .forms import *



class UsuarioSerializerRegistro(serializers.Serializer):
    
    username = serializers.CharField()
    first_name = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.IntegerField()
    
    def validate_username(self, username):
        usuario = Usuario.objects.filter(username=username).first()
        
        if(not usuario is None):
            raise serializers.ValidationError('Ya existe un usuario con ese nombre.')
        return username



class UsuarioSerializer(serializers.ModelSerializer):
    
    date_joined = serializers.DateTimeField(format=('%d-%m-%Y'))
    
    last_login = serializers.DateTimeField(format=('%d-%m-%Y'))
    
    class Meta:
        model = Usuario
        fields = '__all__'

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('file', 'uploaded_on',)

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
        fields = ('id', 'imagen_prod', 'nombre_prod', 'descripcion', 'precio', 'farmacia_prod', 'prov_sum_prod')
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
    
    
class SuministroProductoSerializer(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne u OneToOne
    producto = ProductoSerializerMejorado()
    proveedor = ProveedorSerializer()
    
    class Meta:
        model = SuministroProducto
        fields = '__all__'
    
    
class ProductoSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Producto
        fields = ['imagen_prod', 'nombre_prod','descripcion','precio','farmacia_prod','prov_sum_prod']
            
    def validate_nombre_prod(self,nombre):
        productoNombre = Producto.objects.filter(nombre_prod=nombre, farmacia_prod=self.initial_data['farmacia_prod']).first()
        if(not productoNombre is None):
            if(not self.instance is None and productoNombre.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe un producto con ese nombre en esta farmacia.')        
        return nombre
    
    def validate_imagen_prod(self, imagen):
        if (imagen is None):
            raise serializers.ValidationError('Necesita insertar una imagen del producto.')
        return imagen
    
    def validate_descripcion(self,descripcion):
        if len(descripcion) < 10:
            raise serializers.ValidationError('Al menos debes indicar 10 caracteres')
        return descripcion
    
    def validate_precio(self,precio):
        if type(precio) != Decimal:
            raise serializers.ValidationError('El precio introducido no es válido')
        return precio
    
    def create(self, validated_data):
        if('prov_sum_prod' not  in self.initial_data):
            raise serializers.ValidationError(
                {'prov_sum_prod':
                ['No ha enviado proveedores']
                })
        proveedores = self.initial_data['prov_sum_prod']
        if len(proveedores) < 2:
            raise serializers.ValidationError(
                {'prov_sum_prod':
                ['Debe seleccionar al menos dos proveedores.']
                })
        
        producto = Producto.objects.create(
            imagen_prod = validated_data['imagen_prod'],
            nombre_prod = validated_data['nombre_prod'],
            descripcion = validated_data['descripcion'],
            precio = validated_data['precio'],
            farmacia_prod = validated_data['farmacia_prod'],
            )
        for proveedor in proveedores:
            modeloProveedor = Proveedor.objects.get(id=proveedor)
            SuministroProducto.objects.create(proveedor=modeloProveedor, producto=producto)
        
        return producto
    
    def update(self, instance, validated_data):
        proveedores = self.initial_data['prov_sum_prod']
        if len(proveedores) < 1:
            raise serializers.ValidationError(
                {'prov_sum_prod':
                ['Debe seleccionar al menos un proveedor']
                })
        
        instance.nombre_prod = validated_data["nombre_prod"]
        instance.descripcion = validated_data["descripcion"]
        instance.precio = validated_data["precio"]
        instance.farmacia_prod = validated_data["farmacia_prod"]
        instance.save()
        
        instance.prov_sum_prod.clear()
        for proveedor in proveedores:
            modeloProveedor = Proveedor.objects.get(id=proveedor)
            SuministroProducto.objects.create(proveedor=modeloProveedor, producto=instance)
        return instance
 
   
class ProductoSerializerActualizarNombre(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre_prod']
        
    def validate_nombre_prod(self, nombre_prod):
        productoNombre = Producto.objects.filter(nombre_prod=nombre_prod).first()
        if(not productoNombre is None and productoNombre.id != self.instance.id):
            raise serializers.ValidationError('Ya existe un producto con ese nombre')
        return nombre_prod
    
    
    

    
    
class FarmaciaSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Farmacia
        fields = ['nombre_farm','direccion_farm','telefono_farm']
        
    def validate_nombre_farm(self,nombre):
        farmaciaNombre = Farmacia.objects.filter(nombre_farm=nombre).first()
        if(not (farmaciaNombre is None or (not self.instance is None and farmaciaNombre.id == self.instance.id))):
            raise serializers.ValidationError('Ya existe una farmacia con ese nombre.')        
        return nombre
    
    def validate_direccion_farm(self,direccion):
        if len(direccion) < 10:
            raise serializers.ValidationError('Al menos debes indicar 10 caracteres')
        return direccion
    
    def validate_telefono_farm(self,telefono):
        if (str(telefono)[0] not in ('6','7','9') or len(str(telefono)) != 9):
            raise serializers.ValidationError('Debe especificar un número español de 9 dígitos.')
        return telefono
    
    def update(self, instance, validated_data):
        
        instance.nombre_farm = validated_data["nombre_farm"]
        instance.direccion_farm = validated_data["direccion_farm"]
        instance.telefono_farm = validated_data["telefono_farm"]
        instance.save()
        
        return instance
   
class FarmaciaSerializerActualizarNombre(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = ['nombre_farm']
        
    def validate_nombre_farm(self, nombre):
        farmaciaNombre = Farmacia.objects.filter(nombre_farm=nombre).first()
        if(not farmaciaNombre is None and farmaciaNombre.id != self.instance.id):
            raise serializers.ValidationError('Ya existe una farmacia con ese nombre')
        return nombre
        
    
    



   
class VotacionSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Votacion
        fields = ['numeros','puntuacion','fecha_votacion','comenta_votacion','voto_producto','voto_cliente']
        
    def validate_comenta_votacion(self,comentario):
        if len(comentario) < 10:
            raise serializers.ValidationError('Al menos debes indicar 10 caracteres')
        return comentario
    
    def validate_voto_producto(self,productoSeleccionado):
        if (productoSeleccionado is None):
            raise serializers.ValidationError('Debe seleccionar un producto a votar.')
        return productoSeleccionado
    
    def validate_voto_cliente(self,clienteVota):
        if (clienteVota is None):
            raise serializers.ValidationError('Debe seleccionar quien realizo la votación.')
        return clienteVota
    
    
    def update(self, instance, validated_data):
        
        instance.puntuacion = validated_data["puntuacion"]
        instance.comenta_votacion = validated_data["comenta_votacion"]
        instance.voto_producto = validated_data["voto_producto"]
        instance.voto_cliente = validated_data["voto_cliente"]
        instance.save()
        
        return instance
   
class VotacionSerializerActualizarPuntuacion(serializers.ModelSerializer):
    class Meta:
        model = Votacion
        fields = ['puntuacion']
    