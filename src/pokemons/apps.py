"""
apps.py - configuracion de la aplicacion pokemons.

define la configuracion de la app django para su registro
en installed_apps del proyecto.
"""

from django.apps import AppConfig


class PokemonsConfig(AppConfig):
    """configuracion de la aplicacion pokemons."""

    name = 'pokemons'
    verbose_name = 'Gestion de Pokemons'
