from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    
    path('farmacias/ordenadas',views.farmacia_ordenada_fecha,name='farmacias_ordenadas_fecha'),
    
    path('gerentes/<str:nombre_introducido>',views.gerente_nombre, name='gerentes_nombre'),
    
    path('farmacias',views.farmacias_con_gerentes, name='farmacias_con_gerentes'),
    
    path('productos',views.productos_con_proveedores, name='productos_con_proveedores'),
    
    path('empleados/compras',views.empleado_compras, name='empleados_compras'),
    
    path('detalles/compra/<int:id_compra>',views.detalle_compra_id, name='detalle_compra'),
    
    path('clientes/productosfavoritos',views.clientes_productosfavoritos, name='clientes_productosfavoritos'),
    
    path('empleados/salariosuperior/<int:cantidad_salario>',views.empleado_salariosuperior, name='empleados_salariosuperior'),
    
    path('productos/disponibles/farmacia/<int:id_farmacia>',views.productos_disponibles_farmacia_especifica, name='productos_disponibles_farmacia_especifica'),
    
    path('compras/entre/<str:fecha_inicio>/<str:fecha_fin>',views.compras_entre_fechas, name="compras_entre_fechas"),

    path('ultimo_voto_producto_concreto/<int:producto_id>',views.ultimo_voto_producto_concreto, name='ultimo_voto_producto_concreto'),
    
    path('productos_puntuacion_3_cliente_concreto/<int:cliente_id>/',views. productos_con_puntuacion_3_cliente_concreto, name='productos_con_puntuacion_3_cliente_concreto'),

    path('clientes_nunca_votaron',views.clientes_nunca_votaron, name='clientes_nunca_votaron'),
    
    path('cuentas_bancarias_propietario_nombre/<str:nombre_propietario>/',views.cuentas_bancarias_propietario_nombre, name='cuentas_bancarias'),
    
    path('signup',views.signup, name='signup'),
    
]
