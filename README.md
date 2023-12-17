# AppFarmacia
Aplicacion Web - Creacion URLs, Views & QuerySet

EXAMEN CRUD | "PROMOCION"

14/12/2023

URLs:

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
