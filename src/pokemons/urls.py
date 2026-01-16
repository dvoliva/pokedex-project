"""
urls.py - configuracion de rutas de la aplicacion pokemons.

define los endpoints disponibles para acceder a las vistas
de pokemon desde el navegador.
"""

from django.urls import path
from . import views

# namespace de la app para referencia en templates: {% url 'pokemon_list' %}
app_name = 'pokemons'

urlpatterns = [
    # ruta principal: lista todos los pokemon con filtros opcionales
    path('', views.pokemon_list, name='pokemon_list'),
]
