from django.shortcuts import render
from .models import Pokemon


def pokemon_list(request):
    """
    Docstring para pokemon_list

    :param request: Descripción
    """
    pokemons = Pokemon.objects.all().order_by('id')

    filter_type = request.GET.get('filter')

    if filter_type == 'heavy':
        pokemons = pokemons.filter(weight__gt=30, weight__lt=80)

    elif filter_type == 'grass':
        # SQLite no soporta __contains en JSONField, usamos icontains como alternativa
        pokemons = pokemons.filter(types__icontains='grass')

    elif filter_type == 'flying':
        pokemons = pokemons.filter(types__icontains='flying', height__gt=10)

    context = {
        'pokemons': pokemons,
        'active_filter': filter_type
    }

    return render(request, 'pokemons/list.html', context)
