"""
views.py - vistas de la aplicacion pokemons.

contiene la logica de presentacion y los filtros solicitados
por el profesor oak para analizar los datos de la pokedex.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Pokemon


def pokemon_list(request: HttpRequest) -> HttpResponse:
    """
    vista principal que lista los pokemon con filtros opcionales.

    implementa los 3 filtros requeridos por el profesor oak:
    - heavy: pokemon con peso entre 30 y 80
    - grass: pokemon de tipo planta
    - flying: pokemon voladores con altura mayor a 10

    args:
        request: objeto httprequest de django con posible parametro 'filter'.

    returns:
        httpresponse con el template renderizado y la lista de pokemon.
    """
    # queryset base ordenado por id de pokedex
    pokemons = Pokemon.objects.all().order_by('id')

    # obtener filtro de query params (?filter=xxx)
    filter_type = request.GET.get('filter')

    # filtro 1: peso mayor a 30 y menor a 80
    if filter_type == 'heavy':
        pokemons = pokemons.filter(weight__gt=30, weight__lt=80)

    # filtro 2: tipo grass (planta)
    # nota: usamos icontains para compatibilidad con sqlite en desarrollo
    elif filter_type == 'grass':
        pokemons = pokemons.filter(types__icontains='grass')

    # filtro 3: tipo flying con altura mayor a 10
    elif filter_type == 'flying':
        pokemons = pokemons.filter(types__icontains='flying', height__gt=10)

    context = {
        'pokemons': pokemons,
        'active_filter': filter_type
    }

    return render(request, 'pokemons/list.html', context)
