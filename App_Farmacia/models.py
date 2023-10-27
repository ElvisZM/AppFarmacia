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

class Producto(models.Model):
    nombre_prod = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    farmacia_prod = models.ForeignKey(Farmacia, on_delete=models.CASCADE)

class Proveedor(models.Model):
    nombre_prov = models.CharField(max_length=200)
    direccion_prov = models.CharField(max_length=200)
    producto_prov = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="producto_prov")
    prov_sum_prod = models.ManyToManyField(Producto, through='SuministroProducto', related_name="prov_sum_prod")

class SuministroProducto(models.Model):
    fecha_sum = models.DateField(null=True, blank=True)
    cantidad = models.IntegerField(null=False, blank=False)
    costo_ud = models.DecimalField(max_digits=5, decimal_places=2)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

class Cliente(models.Model):
    nombre_cli = models.CharField(max_length=200)
    telefono_cli = models.IntegerField(null=True, blank=True)
    direccion_cli = models.CharField(max_length=200, null=True, blank=True)
    productos_favoritos = models.ManyToManyField(Producto)

class Compra(models.Model):
    fecha_compra = models.DateField(null=False, blank=False)
    cliente_compra = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto_compra = models.ManyToManyField(Producto, through='DetalleCompra', related_name="producto_compra")
    empleado_compra = models.ForeignKey(Empleado, on_delete=models.CASCADE)

class DetalleCompra(models.Model):
    cantidad_prod_comprado = models.IntegerField(null=False, blank=False)
    precio_ud = models.DecimalField(max_digits=5, decimal_places=2)
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

class DetalleProducto(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    cantidad_stock = models.IntegerField(default=0)
    fecha_vencimiento = models.DateField(null=True, blank=True)