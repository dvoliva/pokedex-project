import requests
from django.core.management.base import BaseCommand
from pokemons.models import Pokemon

class Command(BaseCommand):
    help = 'Descarga los primeros 50 pokémons desde la API y los guarda en la base de datos'

    def handle(self, *args, **kwargs):
        self.stdout.write("descarga iniciada")
        base_url = "https://pokeapi.co/api/v2/pokemon/"

        limit = 50
        for i in range(1, limit + 1):
            try:
                response = requests.get(f"{base_url}{i}/")
                if response.status_code != 200:
                    self.stdout.write(f"error {i}")
                    continue
                data = response.json()

                normal_name = data['name'].capitalize()  # "pikachu" -> "Pikachu"
                inverted_name = normal_name[::-1]  # "Pikachu" -> "uhcakiP"

                type_list = [t['type']['name'] for t in data['types']]

                obj, created = Pokemon.objects.update_or_create(
                    id = data['id'],
                    defaults={
                        'name': normal_name,
                        'name_inverted': inverted_name,
                        'types': type_list,
                        'height': data['height'],
                        'weight': data['weight']
                    }
                )

                action = "Creado" if created else "Actualizado"
                self.stdout.write(self.style.SUCCESS(f"[{i}/50] {normal_name} - {action} correctamente."))

            except Exception as e:
                    self.stdout.write(self.style.ERROR(f"error al procesar el pokémon {i}: {str(e)}"))
        self.stdout.write(self.style.SUCCESS("descarga completada"))
