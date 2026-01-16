from django.contrib import admin
from .models import Pokemon


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para Pokemon."""

    list_display = ('id', 'name', 'types', 'height', 'weight', 'name_inverted')
    list_filter = ('types',)
    search_fields = ('name',)
