"""
models.py - definicion del modelo de datos para pokemon.

este modulo contiene el modelo orm que representa la estructura de datos
de un pokemon, mapeado directamente a la tabla en postgresql.
"""

from django.db import models


class Pokemon(models.Model):
    """
    modelo que representa un pokemon en la base de datos.

    almacena los datos obtenidos de la pokeapi, incluyendo una columna
    calculada (name_inverted) como transformacion de datos requerida.

    attributes:
        id: identificador unico del pokemon en la pokedex (clave primaria).
        name: nombre del pokemon con la primera letra en mayuscula.
        name_inverted: nombre del pokemon invertido (ej: "pikachu" -> "uhcakip").
        types: lista de tipos del pokemon almacenada como json.
        height: altura del pokemon en decimetros.
        weight: peso del pokemon en hectogramos.
    """

    # usamos el id de la pokedex como clave primaria en lugar de autoincrement
    id = models.IntegerField(primary_key=True, verbose_name="ID Pokedex")
    name = models.CharField(max_length=100, verbose_name="Nombre del Pokémon")

    # columna de transformacion: nombre invertido para cumplir requisito 4
    name_inverted = models.CharField(max_length=100, verbose_name="Nombre Invertido")

    # jsonfield permite almacenar multiples tipos sin crear tabla relacional
    types = models.JSONField(default=list, verbose_name="Tipos")

    height = models.IntegerField(verbose_name="Altura")
    weight = models.IntegerField(verbose_name="Peso")

    class Meta:
        """configuracion del modelo."""
        ordering = ['id']
        verbose_name = "Pokemon"
        verbose_name_plural = "Pokemons"

    def __str__(self):
        """representacion en string del pokemon para el admin y debug."""
        return f"{self.id} - {self.name}"
