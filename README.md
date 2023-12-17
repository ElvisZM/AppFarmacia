# AppFarmacia

# APLICACION WEB | PROYECTO DE FIN DE GRADO - 2ºDAW


# CRUD | "PRODUCTOS"



URLs y VIEWS:

    * CREATE:
        
        path('producto/create',views.producto_create,name='producto_create')

    * BUSCAR:

        path('producto/buscar/',views.producto_buscar, name='producto_buscar')

    * BUSQUEDA AVANZADA:
        
        path('producto/buscar/avanzado/',views.producto_buscar_avanzado, name='producto_buscar_avanzado'),

    * EDITAR:

        path('producto/editar/<int:producto_id>',views.producto_editar, name='producto_editar')

    * ELIMINAR:

        path('producto/eliminar/<int:producto_id>',views.producto_eliminar, name='producto_eliminar')

    * LISTA:

        path('productos/lista',views.productos_lista, name='lista_productos')


TEMPLATES:


    * CREATE:

        'producto/create_producto.html'

    * BUSQUEDA RÁPIDA:

        'producto/producto_busqueda.html'

    * BUSQUEDA AVANZADA:

        'producto/producto_busqueda.html'

    * EDITAR:

        'producto/actualizar_promocion.html'

    * ELIMINAR Y LISTA:

        'producto/lista_productos.html'


FORMULARIOS:


    * CREATE:
    
        class ProductoModelForm(ModelForm)

    * BÚSQUEDA RÁPIDA:

        class BusquedaProductoForm(forms.Form)

    * BÚSQUEDA AVANZADA:
    
        class BusquedaAvanzadaProductoForm(forms.Form)


VALIDACIONES:


    * Comprobamos que no existe un producto con ese nombre

    * Comprobamos que la descripción tiene al menos 10 carácteres.

    * Comprobamos que el precio está puesto en su formato con decimales (float)

    * Comprobamos que al menos seleccione un Proveedor



# CRUD | "GERENTES"



URLs y VIEWS:

    * CREATE:
        
        path('gerente/create',views.gerente_create, name='gerente_create')

    * BUSCAR:

        path('gerente/buscar/',views.gerente_buscar, name='gerente_buscar')

    * BUSQUEDA AVANZADA:
        
        path('gerente/buscar/avanzado/',views.gerente_buscar_avanzado, name='gerente_buscar_avanzado')

    * EDITAR:

        path('gerente/editar/<int:gerente_id>',views.gerente_editar, name='gerente_editar')

    * ELIMINAR:

        path('gerente/eliminar/<int:gerente_id>',views.gerente_eliminar, name='gerente_eliminar')

    * LISTA:

       path('gerentes/lista',views.gerentes_lista, name='lista_gerentes')


TEMPLATES:


    * CREATE:

        'gerente/create_gerente.html'

    * BUSQUEDA RÁPIDA:

        'gerente/gerente_busqueda.html'

    * BUSQUEDA AVANZADA:

        'gerente/busqueda_avanzada_gerente.html'

    * EDITAR:

        'gerente/actualizar_gerente.html'

    * ELIMINAR Y LISTA:

        'gerente/lista_gerentes.html'


FORMULARIOS:


    * CREATE:
    
        class GerenteModelForm(ModelForm)

    * BÚSQUEDA RÁPIDA:

        class BusquedaGerenteForm(forms.Form)

    * BÚSQUEDA AVANZADA:
    
        class BusquedaAvanzadaGerenteForm(forms.Form)


VALIDACIONES:


    * Comprobamos que no exista un gerente con ese nombre

    * Comprobamos que se inserte un correo

    * Comprobamos que la fecha de inicio de gestion no sea mayor a la de hoy.

    * Comprobamos que inserte una farmacia a gestionar 

    * Comprobamos que la farmacia no tenga ya a un gerente que la gestione






# EXAMEN CRUD | "PROMOCION"

14/12/2023

URLs y VIEWS:

    * CREATE:
        
        path('promocion/create',views.promocion_create, name='promocion_create')

    * BUSCAR:

        path('promocion/buscar/',views.promocion_buscar, name='promocion_buscar')

    * BUSQUEDA AVANZADA:
        
        path('promocion/buscar/avanzado/',views.promocion_buscar_avanzado, name='promocion_buscar_avanzado')

    * EDITAR:

        path('promocion/editar/<int:promocion_id>',views.promocion_editar, name='promocion_editar')

    * ELIMINAR:

        path('promocion/eliminar/<int:promocion_id>',views.promocion_eliminar, name='promocion_eliminar')

    * LISTA:

        path('promociones/lista',views.promociones_lista, name='lista_promociones')


TEMPLATES:


    * CREATE:

        'promocion/create_promocion.html'

    * BUSQUEDA RÁPIDA:

        'promocion/promocion_busqueda.html'

    * BUSQUEDA AVANZADA:

        'promocion/busqueda_avanzada_promocion.html'

    * EDITAR:

        'promocion/actualizar_promocion.html'

    * ELIMINAR Y LISTA:

        'promocion/lista_promociones.html'


FORMULARIOS:


    * CREATE:
    
        class PromocionModelForm(ModelForm)

    * BÚSQUEDA RÁPIDA:

        class BusquedaPromocionForm(forms.Form)

    * BÚSQUEDA AVANZADA:
    
        class BusquedaAvanzadaPromocionForm(forms.Form)


VALIDACIONES:


    * Nombre de la Promoción es única

    * Comprobamos que la descripción tiene al menos 100 carácteres.

    * Comprobamos que el cliente no tenga ya la misma promoción aplicada

    * Comprobamos que el valor del descuento sea un entero entre 0 y 100

    * Comprobamos la fecha de expiración no sea inferior a la actual.










## PEQUEÑA ANOTACIÓN, NO OLVIDAR!!!:

    En las templates, se puede acceder a los datos de cualquier campo siempre y cuando tengan relacion entre ellos.

    En el siguiente caso, observamos que compra tiene dos relaciones ForeignKey(ManyToOne) con Cliente y Empleado. 
    
    También tiene una relacion ManyToMany con Producto a través de DetalleCompra. 
    
    Luego DetalleCompra tiene dos relaciones ForeignKey(ManyToOne) con Compra y Producto.

    Como podemos observar existe una relacion inversa entre Compra y DetalleCompra.

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


    Si quisieramos acceder desde compra a un dato que no esta en nuestro modelo, si es una ForeignKey, podemos acceder 
    facilmente recorriendo el nombre de la variable que recoge esta relacion con:
    
    "compra.empleado_compra"

    Esto nos situa en el campo que la relaciona, en este caso Empleado. Una vez estamos situados en ese campo, es tan 
    fácil como seleccionar que información queremos mostrar (en mi caso nombre del empleado) y la agregamos.

    "compra.empleado_compra.nombre_emp"

    Si quisieramos acceder desde compra a un dato de DetalleCompra, al ser esta una relación inversa, lo que se me 
    ocurrio fue recoger todos los datos Producto mediante producto_compra y dentro de producto hacer una relacion inversa para coger los datos de DetalleCompra usando 
    
    "for det in producto.detallecompra_set.all".
    
    De este modo puedo mostrar fácilmente los datos que necesite.


    <div>
        <h2> Fecha Compra: {{ compra.fecha_compra|date:"d-m-Y" }}</h2>
        <h2> Cliente: {{ compra.cliente_compra.nombre_cli|truncatewords:1 }} </h2>
        {% for producto in compra.producto_compra.all %}
            <h2>Producto comprado: {{ producto.nombre_prod|truncatewords:2 }} </h2>
            {%for det in producto.detallecompra_set.all %}
                <h2>Cantidad: {{ det.cantidad_prod_comprado }}
                <h2>Precio Unidad: {{ det.precio_ud }} </h2>
            {% endfor %}
        {% endfor %}
        <h2> Empleado: {{ compra.empleado_compra.nombre_emp|truncatewords:2 }} </h2>
    </div> 


