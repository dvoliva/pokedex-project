from django.test import TestCase, Client
from django.urls import reverse
from .models import Pokemon

from django.test import TestCase, Client
from django.urls import reverse
from .models import Pokemon

class PokemonModelTest(TestCase):
    """
    test Unitario: Verifica que el modelo de datos se comporta correctamente
    """
    def setUp(self):
        # setUp se ejecuta ANTES de cada test. Preparamos el terreno.
        self.pokemon = Pokemon.objects.create(
            id=1,
            name="Bulbasaur",
            name_inverted="ruasabluB", # Simulamos que el ETL ya hizo su trabajo
            height=7,
            weight=69,
            types=["grass", "poison"]
        )

    def test_pokemon_creation(self):
        """Verifica que el Pokemon se creó correctamente en la DB temporal"""
        p = Pokemon.objects.get(id=1)
        self.assertEqual(p.name, "Bulbasaur")
        self.assertEqual(p.types[0], "grass")

class PokemonViewTest(TestCase):
    """
    Test de Integración: Verifica que las Vistas (URLs + Lógica) responden 
    correctamente a los filtros de Oak.
    """
    def setUp(self):
        # Creamos datos de prueba variados para probar los filtros
        self.client = Client()

        # Pokemon 1: Ligero y Tipo Fuego
        Pokemon.objects.create(
            id=4, name="Charmander", name_inverted="rednamrahC",
            height=6, weight=85, # Peso > 80 (No pasa filtro heavy)
            types=["fire"]
        )

        # Pokemon 2: Medio y Tipo Planta (Candidato perfecto)
        Pokemon.objects.create(
            id=1, name="Bulbasaur", name_inverted="ruasabluB",
            height=7, weight=69, # Peso entre 30 y 80
            types=["grass", "poison"]
        )

        # Pokemon 3: Volador Alto
        Pokemon.objects.create(
            id=6, name="Charizard", name_inverted="drazirahC",
            height=17, weight=905,
            types=["fire", "flying"]
        )

    def test_view_url_exists_at_desired_location(self):
        """La página principal carga con status 200?"""
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_filter_heavy(self):
        """Filtro 1: Peso entre 30 y 80"""
        # Simulamos que el usuario entra a /?filter=heavy
        response = self.client.get('/?filter=heavy')

        # Bulbasaur (69) debería estar.
        self.assertContains(response, "Bulbasaur")
        # Charmander (85) NO debería estar.
        self.assertNotContains(response, "Charmander")

    def test_filter_grass(self):
        """Filtro 2: Tipo Grass"""
        response = self.client.get('/?filter=grass')
        self.assertContains(response, "Bulbasaur")
        self.assertNotContains(response, "Charizard")

    def test_filter_flying_high(self):
        """Filtro 3: Flying + Altura > 10"""
        response = self.client.get('/?filter=flying')
        self.assertContains(response, "Charizard")
        self.assertNotContains(response, "Bulbasaur")
