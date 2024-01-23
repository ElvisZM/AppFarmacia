"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from App_Farmacia import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('App_Farmacia.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/v1/', include('App_Farmacia.api_urls')),
    path('oauth2/', include('oauth2_provider.urls',namespace='oauth2_provider')),
]

handler400 = 'App_Farmacia.views.mi_error_400'
handler403 = 'App_Farmacia.views.mi_error_403'
handler404 = 'App_Farmacia.views.mi_error_404'
handler500 = 'App_Farmacia.views.mi_error_500'
