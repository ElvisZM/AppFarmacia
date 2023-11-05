from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    
    path('farmacias/ordenadas',views.farmacia_ordenada_fecha,name='farmacias_ordenadas_fecha'),
    
    path('gerentes/<str:nombre_introducido>',views.gerente_nombre, name='gerentes_nombre'),
    
    path('farmacias',views.farmacias_con_gerentes, name='farmacias_con_gerentes'),
    
    path('productos',views.productos_con_proveedores, name='productos_con_proveedores'),
    
    path('empleados/compras',views.empleado_compras, name='empleados_compras'),
    
    path('detalles/compra/<int:id_compra>',views.detalle_compra, name='detalle_compra'),
    
    path('clientes/productosfavoritos',views.clientes_productosfavoritos, name='clientes_productosfavoritos'),
    
    path('empleados/salariosuperior/<int:cantidad_salario>',views.empleado_salariosuperior, name='empleados_salariosuperior'),
    
    path('productos/disponibles/farmacia/<int:id_farmacia>',views.productos_disponibles_farmacia_especifica, name='productos_disponibles_farmacia_especifica'),
    
    path('compras/entre/<str:fecha_inicio>/<str:fecha_fin>',views.compras_entre_fechas, name="compras_entre_fechas"),
    
]
