from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('productos/lista',views.listar_productos,name='lista_productos'),
]
