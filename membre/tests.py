from django.test import TestCase
from django.urls import reverse
from bibliothecaire.models import Media

class CatalogueMembreTests(TestCase):
    def setUp(self):
        # On crée quelques médias de test
        Media.objects.create(titre="Le Petit Prince", type_media="livre", disponible=True)
        Media.objects.create(titre="Interstellar", type_media="dvd", disponible=False)
        Media.objects.create(titre="Thriller", type_media="cd", disponible=True)

    def test_catalogue_page_accessible(self):
        response = self.client.get(reverse('liste_medias'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Catalogue des médias")

    def test_recherche_media(self):
        response = self.client.get(reverse('liste_medias') + '?q=prince')
        self.assertContains(response, "Le Petit Prince")
        self.assertNotContains(response, "Interstellar")

    def test_filtre_disponible(self):
        response = self.client.get(reverse('liste_medias') + '?disponible=1')
        self.assertContains(response, "Le Petit Prince")
        self.assertContains(response, "Thriller")
        self.assertNotContains(response, "Interstellar")
