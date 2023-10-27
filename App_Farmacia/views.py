from django.shortcuts import render

# Create your views here.
from .models import Farmacia, Gerente, Empleado, Producto, Proveedor, SuministroProducto, Cliente, Compra, DetalleCompra, CuentaEmpleado, HistorialCliente, DatosFarmacia, DetalleProducto
from django.db.models import Q
from django.views.defaults import page_not_found


def index(request):
    return render(request, 'index.html')

def listar_farmacias(request):
    farmacias = Farmacia.objects.select_related
    