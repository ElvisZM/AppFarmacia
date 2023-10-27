from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    
    path('farmacias/lista',views.listar_farmacias,name='lista_farmacias'),
]
