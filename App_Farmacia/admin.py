from django.contrib import admin
from .models import Farmacia, Gerente, Empleado, Producto, Proveedor, Cliente, Compra, DetalleCompra, CuentaEmpleado, HistorialCliente, DatosFarmacia, DetalleProducto,Usuario
# Register your models here.

admin.site.register(Farmacia)
admin.site.register(Gerente)
admin.site.register(Empleado)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Cliente)
admin.site.register(Compra)
admin.site.register(DetalleCompra)
admin.site.register(CuentaEmpleado)
admin.site.register(HistorialCliente)
admin.site.register(DatosFarmacia)
admin.site.register(DetalleProducto)
admin.site.register(Usuario)
