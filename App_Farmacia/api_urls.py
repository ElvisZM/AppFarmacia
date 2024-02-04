from django.urls import path
from .api_views import *

urlpatterns = [
    path('productos', producto_list),
    path('productos/mejorado', producto_list_mejorado),
    path('producto/busqueda_simple', producto_buscar),
    path('producto/busqueda_avanzada', producto_busqueda_avanzada),
    path('producto/crear', producto_create),
    
    path('empleados', empleado_list),
    path('empleados/mejorado', empleado_list_mejorado),
    path('votaciones/mejorado', votacion_list_mejorado),
    
    path('farmacias', farmacia_list),
    
    path('proveedores', proveedor_list),
]
