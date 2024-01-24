from django.urls import path
from .api_views import *

urlpatterns = [
    path('productos', producto_list),
    path('producto/busqueda_simple', producto_buscar),
]
