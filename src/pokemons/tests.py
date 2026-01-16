"""
tests.py - suite de pruebas para la aplicacion pokemons.

contiene tests unitarios para el modelo y tests de integracion
para verificar que los filtros del profesor oak funcionan correctamente.

uso:
    python manage.py test pokemons
"""

from django.test import TestCase, Client
from .models import Pokemon


class PokemonModelTest(TestCase):
    """
    tests unitarios para el modelo pokemon.

    verifican que el modelo se crea correctamente y que
    los campos almacenan los datos esperados.
    """

    def setUp(self):
        """prepara datos de prueba antes de cada test."""
        self.pokemon = Pokemon.objects.create(
            id=1,
            name="Bulbasaur",
            name_inverted="ruasabluB",
            height=7,
            weight=69,
            types=["grass", "poison"]
        )

    def test_pokemon_creation(self):
        """verifica que el pokemon se crea correctamente en la base de datos."""
        pokemon = Pokemon.objects.get(id=1)
        self.assertEqual(pokemon.name, "Bulbasaur")
        self.assertEqual(pokemon.types[0], "grass")


class PokemonViewTest(TestCase):
    """
    tests de integracion para las vistas.

    verifican que los filtros del profesor oak funcionan correctamente
    a traves de peticiones http simuladas.
    """

    def setUp(self):
        """prepara datos de prueba variados para probar cada filtro."""
        self.client = Client()

        # pokemon tipo fuego con peso > 80 (no pasa filtro heavy)
        Pokemon.objects.create(
            id=4, name="Charmander", name_inverted="rednamrahC",
            height=6, weight=85,
            types=["fire"]
        )

        # pokemon tipo planta con peso entre 30 y 80 (pasa filtro heavy y grass)
        Pokemon.objects.create(
            id=1, name="Bulbasaur", name_inverted="ruasabluB",
            height=7, weight=69,
            types=["grass", "poison"]
        )

        # pokemon volador con altura > 10 (pasa filtro flying)
        Pokemon.objects.create(
            id=6, name="Charizard", name_inverted="drazirahC",
            height=17, weight=905,
            types=["fire", "flying"]
        )

    def test_view_returns_200(self):
        """verifica que la pagina principal responde con status 200."""
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_filter_heavy(self):
        """
        filtro 1: pokemon con peso entre 30 y 80.

        bulbasaur (peso 69) debe aparecer.
        charmander (peso 85) no debe aparecer.
        """
        response = self.client.get('/?filter=heavy')
        self.assertContains(response, "Bulbasaur")
        self.assertNotContains(response, "Charmander")

    def test_filter_grass(self):
        """
        filtro 2: pokemon tipo grass.

        bulbasaur (tipo grass) debe aparecer.
        charizard (tipo fire/flying) no debe aparecer.
        """
        response = self.client.get('/?filter=grass')
        self.assertContains(response, "Bulbasaur")
        self.assertNotContains(response, "Charizard")

    def test_filter_flying_high(self):
        """
        filtro 3: pokemon tipo flying con altura > 10.

        charizard (tipo flying, altura 17) debe aparecer.
        bulbasaur (tipo grass) no debe aparecer.
        """
        response = self.client.get('/?filter=flying')
        self.assertContains(response, "Charizard")
        self.assertNotContains(response, "Bulbasaur")
