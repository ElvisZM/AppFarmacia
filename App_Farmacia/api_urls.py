from django.urls import path
from .api_views import *

urlpatterns = [
    path('productos', producto_list),
    path('productos/mejorado', producto_list_mejorado),
    path('producto/busqueda_simple', producto_buscar),
    path('producto/busqueda_avanzada', producto_busqueda_avanzada),
    path('producto/crear', producto_create),
    path('producto/editar/<int:producto_id>', producto_editar),
    
    path('empleados', empleado_list),
    path('empleados/mejorado', empleado_list_mejorado),
    path('empleado/busqueda_avanzada', empleado_busqueda_avanzada),
    
    path('votaciones/mejorado', votacion_list_mejorado),
    path('votacion/busqueda_avanzada', votacion_busqueda_avanzada),
    
    path('farmacias', farmacia_list),
    
    path('proveedores', proveedor_list),
    
    path('clientes', clientes_list),
]
