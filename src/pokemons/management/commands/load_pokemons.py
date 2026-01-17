"""
load_pokemons.py - comando de django para cargar datos desde pokeapi.

este comando implementa un pipeline etl (extract, transform, load)
que descarga los primeros 50 pokemon desde la api publica y los
persiste en la base de datos.

uso:
    python manage.py load_pokemons
"""

import requests
from django.core.management.base import BaseCommand
from pokemons.models import Pokemon


class Command(BaseCommand):
    """
    comando de django para poblar la base de datos con pokemon.

    realiza las siguientes operaciones:
    1. extract: descarga datos de cada pokemon desde pokeapi
    2. transform: capitaliza nombre, invierte string, extrae tipos
    3. load: guarda o actualiza en la base de datos (upsert)
    """

    help = 'descarga los primeros 50 pokemon desde pokeapi y los guarda en la base de datos'

    # url base de la api publica de pokemon
    BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

    # cantidad de pokemon a descargar segun el enunciado
    POKEMON_LIMIT = 50

    def handle(self, *args, **kwargs):
        """
        punto de entrada del comando.

        verifica si ya existen datos en la base de datos.
        si existen, omite la descarga. si no, itera sobre los ids
        del 1 al 50, descarga cada pokemon y los guarda.
        """
        # verificar si ya hay datos en la base de datos
        existing_count = Pokemon.objects.count()
        if existing_count >= self.POKEMON_LIMIT:
            self.stdout.write(
                self.style.SUCCESS(f"base de datos ya contiene {existing_count} pokemon. omitiendo descarga.")
            )
            return

        self.stdout.write("iniciando descarga de pokemon desde pokeapi...")

        for pokemon_id in range(1, self.POKEMON_LIMIT + 1):
            self._process_pokemon(pokemon_id)

        self.stdout.write(self.style.SUCCESS("descarga completada exitosamente"))

    def _process_pokemon(self, pokemon_id: int) -> None:
        """
        procesa un pokemon individual: descarga, transforma y guarda.

        args:
            pokemon_id: id del pokemon en la pokedex (1-50).
        """
        try:
            # extract: obtener datos de la api
            response = requests.get(f"{self.BASE_URL}{pokemon_id}/")

            if response.status_code != 200:
                self.stdout.write(
                    self.style.WARNING(f"[{pokemon_id}/50] error al descargar, status: {response.status_code}")
                )
                return

            data = response.json()

            # transform: procesar datos para el modelo
            name = data['name'].capitalize()
            name_inverted = name[::-1]  # requisito 4: invertir nombre
            types = [t['type']['name'] for t in data['types']]

            # load: guardar o actualizar en la base de datos (upsert)
            obj, created = Pokemon.objects.update_or_create(
                id=data['id'],
                defaults={
                    'name': name,
                    'name_inverted': name_inverted,
                    'types': types,
                    'height': data['height'],
                    'weight': data['weight']
                }
            )

            action = "creado" if created else "actualizado"
            self.stdout.write(
                self.style.SUCCESS(f"[{pokemon_id}/50] {name} - {action} correctamente")
            )

        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f"[{pokemon_id}/50] error de conexion: {str(e)}")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"[{pokemon_id}/50] error inesperado: {str(e)}")
            )
