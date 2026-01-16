"""
urls.py - configuracion de rutas principales del proyecto.

define el enrutamiento global de la aplicacion, delegando
las rutas especificas a cada app instalada.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # panel de administracion de django
    path('admin/', admin.site.urls),

    # rutas de la app pokemons (delegacion)
    path('', include('pokemons.urls')),
]
