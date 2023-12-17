# AppFarmacia
Aplicacion Web - Creacion URLs, Views & QuerySet


LAS URLS

    * CREATE:
        
        promocion/create

    * BUSCAR:

        promocion/buscar/

    * BUSQUEDA AVANZADA:
        
        promocion/buscar/avanzado/

    * EDITAR:

        promocion/editar/<int:promocion_id>

    * ELIMINAR:

        promocion/eliminar/<int:promocion_id>

    * LISTA:

        promociones/lista


LAS VIEWS:

    Se encuentran en App_Farmacia/views.py y abarcan las lineas 648 y 780

    create: views.promocion_create
    buscar: views.promocion_buscar
    buscar_avanzado: views.promocion_buscar_avanzado
    editar: views.promocion_editar
    eliminar: views.promocion_eliminar
    lista: views.promociones_lista

LAS TEMPLATES:

    Se encuentran en App_Farmacia/templates/promocion y dentro se encuentran cada html que necesito para mi CRUD.

    create: promocion/create_promocion.html
    buscar_avanzado: promocion/promocion_busqueda.html
    editar: promocion/actualizar_promociones.html
    

FORMULARIO:

    Se encuentran en App_Farmacia/forms.py y abarcan las lineas 510 y 633

    class PromocionModelForm(ModelForm)

    class BusquedaPromocionForm(forms.Form)

    class BusquedaAvanzadaPromocionForm(forms.Form)
