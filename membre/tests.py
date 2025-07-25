from django.test import TestCase
from django.urls import reverse
from bibliothecaire.models import Media, Membre, Emprunt
from django.utils import timezone

class CatalogueMembreTests(TestCase):
    def setUp(self):
        # Création d'un membre emprunteur
        self.membre = Membre.objects.create(nom="Dupont", prenom="Jean", email="jean@example.com")

        # Médias
        self.media_disponible1 = Media.objects.create(titre="Le Petit Prince", type_media="livre", annee=1943)
        self.media_indisponible = Media.objects.create(titre="Interstellar", type_media="dvd", annee=2014)
        self.media_disponible2 = Media.objects.create(titre="Thriller", type_media="cd", annee=1982)

        # Emprunt en cours sur media_indisponible (donc media non disponible)
        Emprunt.objects.create(membre=self.membre, media=self.media_indisponible, date_emprunt=timezone.now().date())

    def test_catalogue_page_accessible(self):
        response = self.client.get(reverse('membre:liste_medias'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Catalogue des médias")

    def test_recherche_media(self):
        response = self.client.get(reverse('membre:liste_medias') + '?q=prince')
        self.assertContains(response, "Le Petit Prince")
        self.assertNotContains(response, "Interstellar")

    def test_filtre_disponible(self):
        response = self.client.get(reverse('membre:liste_medias') + '?disponible=1')
        self.assertContains(response, "Le Petit Prince")
        self.assertContains(response, "Thriller")
        self.assertNotContains(response, "Interstellar")

