from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    
    path('producto/create',views.producto_create,name='producto_create'),
    
    path('producto/buscar/',views.producto_buscar, name='producto_buscar'),
    
    path('producto/buscar/avanzado/',views.producto_buscar_avanzado, name='producto_buscar_avanzado'),
    
    path('producto/editar/<int:producto_id>',views.producto_editar, name='producto_editar'),
    
    path('producto/eliminar/<int:producto_id>',views.producto_eliminar, name='producto_eliminar'),
    
    path('farmacia/create',views.farmacia_create, name='farmacia_create'),
    
    path('farmacia/buscar/',views.farmacia_buscar, name='farmacia_buscar'),
    
    path('farmacia/buscar/avanzado/',views.farmacia_buscar_avanzado, name='farmacia_buscar_avanzado'),
    
    path('farmacia/editar/<int:farmacia_id>',views.farmacia_editar, name='farmacia_editar'),
    
    path('farmacia/eliminar/<int:farmacia_id>',views.farmacia_eliminar, name='farmacia_eliminar'),
    
    path('gerente/create',views.gerente_create, name='gerente_create'),
    
    path('gerente/buscar/',views.gerente_buscar, name='gerente_buscar'),
    
    path('gerente/buscar/avanzado/',views.gerente_buscar_avanzado, name='gerente_buscar_avanzado'),
    
    path('gerente/editar/<int:gerente_id>',views.gerente_editar, name='gerente_editar'),
    
    path('gerente/eliminar/<int:gerente_id>',views.gerente_eliminar, name='gerente_eliminar'),
    
    
    
    
    
    
    
    
    
    
    path('farmacias/lista',views.farmacias_lista, name='lista_farmacias'),
    
    path('gerentes/lista',views.gerentes_lista, name='lista_gerentes'),
    
    
    
    path('productos/lista',views.productos_lista, name='lista_productos'),
    
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
