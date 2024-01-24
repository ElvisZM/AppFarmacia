from django.urls import path
from .api_views import *

urlpatterns = [
    path('productos', producto_list),
    path('productos/busqueda_simple', producto_buscar),
]
