from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Farmacia(models.Model):
    nombre_farm = models.CharField(max_length=200)
    direccion_farm = models.CharField(max_length=200)
    telefono_farm = models.IntegerField(null=True, blank=True)

class Gerente(models.Model):
    nombre_ger = models.CharField(max_length=200)
    correo = models.EmailField(blank=True)
    fecha_inicio_gestion = models.DateField(null=False, blank=False)
    gerente_farm = models.OneToOneField(Farmacia, on_delete=models.CASCADE)

class Empleado(models.Model):
    nombre_emp = models.CharField(max_length=200)
    cargo = models.CharField(max_length=200)
    salario = models.FloatField(default=1020.40, db_column="salario_empleado")
    farm_emp = models.ForeignKey(Farmacia, on_delete=models.CASCADE) 
    
class Proveedor(models.Model):
    nombre_prov = models.CharField(max_length=200)
    direccion_prov = models.CharField(max_length=200)    

class Producto(models.Model):
    nombre_prod = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    farmacia_prod = models.ForeignKey(Farmacia, on_delete=models.CASCADE)
    prov_sum_prod = models.ManyToManyField(Proveedor, through='SuministroProducto')

class SuministroProducto(models.Model):
    fecha_sum = models.DateField(null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)
    costo_ud = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

class Cliente(models.Model):
    nombre_cli = models.CharField(max_length=200)
    telefono_cli = models.IntegerField(null=True, blank=True, )
    direccion_cli = models.CharField(max_length=200, null=True, blank=True)
    productos_favoritos = models.ManyToManyField(Producto, related_name='productos_favoritos')
    votacion_prod = models.ManyToManyField(Producto, through='Votacion', related_name='votacion_prod')
    
class Subscripcion(models.Model):
    cliente_sub = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    plan_sub = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    
class Votacion(models.Model):
    numeros = [
        (1,"Uno"), 
        (2,"Dos"), 
        (3,"Tres"),
        (4,"Cuatro"),
        (5,"Cinco"),
        ]
    puntuacion = models.CharField(max_length=1, choices=numeros)
    fecha_votacion = models.DateField(null=True, blank=True)
    comenta_votacion = models.TextField()
    voto_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    voto_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

class Pago(models.Model):
    entidades = [
        ("CA","Caixa"),
        ("BB","BBVA"),
        ("UN","UNICAJA"),
        ("IN","ING Direct"),
    ]
    banco = models.CharField(
        max_length=2,
        choices=entidades,
    )
    cuenta_bancaria = models.CharField(max_length=20)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    cliente_pago = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    subscripcion_pago = models.ForeignKey(Subscripcion, on_delete=models.CASCADE)
    

class Compra(models.Model):
    fecha_compra = models.DateField(null=False, blank=False)
    cliente_compra = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto_compra = models.ManyToManyField(Producto, through='DetalleCompra', related_name="producto_compra")
    empleado_compra = models.ForeignKey(Empleado, on_delete=models.CASCADE)

class DetalleCompra(models.Model):
    cantidad_prod_comprado = models.IntegerField(null=True, blank=True)
    precio_ud = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto_detalle = models.ForeignKey(Producto, on_delete=models.CASCADE)

class CuentaEmpleado(models.Model):
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE) 
    nombre_usuario = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=50)

class HistorialCliente(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    total_compras = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class DatosFarmacia(models.Model):
    farmacia_datos = models.OneToOneField(Farmacia, on_delete=models.CASCADE)
    descripcion = models.TextField()
    horario = models.CharField(max_length=100)
    fecha_creacion = models.DateField()

class DetalleProducto(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    cantidad_stock = models.IntegerField(default=0)
    fecha_vencimiento = models.DateField(null=True, blank=True)