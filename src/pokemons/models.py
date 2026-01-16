from django.db import models


class Pokemon(models.Model):
    """
    modelo para representar los datos de un pokémon.
    """

    id = models.IntegerField(primary_key=True, verbose_name="ID Pokedex")
    name = models.CharField(max_length=100, verbose_name="Nombre del Pokémon")
    name_inverted = models.CharField(max_length=100, verbose_name="Nombre Invertido")
    types = models.JSONField(default=list, verbose_name="Tipos")
    height = models.IntegerField(verbose_name="Altura")
    weight = models.IntegerField(verbose_name="Peso")

    def __str__(self):
        return f"{self.id} - {self.name}"
