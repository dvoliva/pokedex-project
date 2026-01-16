"""
admin.py - configuracion del panel de administracion de django.

registra el modelo pokemon en el admin para permitir
visualizacion y gestion manual de los datos.
"""

from django.contrib import admin
from .models import Pokemon


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    """
    configuracion del admin para el modelo pokemon.

    personaliza la visualizacion en el panel de administracion
    para facilitar la revision de los datos cargados.
    """

    # columnas visibles en la lista del admin
    list_display = ('id', 'name', 'types', 'height', 'weight', 'name_inverted')

    # filtros laterales disponibles
    list_filter = ('types',)

    # campos en los que se puede buscar
    search_fields = ('name',)
