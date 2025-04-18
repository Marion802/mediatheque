from django.test import TestCase
from datetime import timedelta
from django.utils import timezone
from .models import Media, Emprunteur, Emprunt

class BibliothecaireTests(TestCase):
    def setUp(self):
        # Création d'un emprunteur
        self.emprunteur = Emprunteur.objects.create(nom="Alice")

        # 3 médias différents
        self.media1 = Media.objects.create(titre="Livre 1", type_media="livre", disponible=True)
        self.media2 = Media.objects.create(titre="CD 1", type_media="cd", disponible=True)
        self.media3 = Media.objects.create(titre="DVD 1", type_media="dvd", disponible=True)
        self.media4 = Media.objects.create(titre="Livre 2", type_media="livre", disponible=True)

    def test_emprunt_possible_si_conditions_ok(self):
        peut_emprunter = self.emprunteur.peut_emprunter()
        self.assertTrue(peut_emprunter)

    def test_bloque_si_trop_emprunts(self):
        # Ajouter 3 emprunts actifs
        for media in [self.media1, self.media2, self.media3]:
            Emprunt.objects.create(media=media, emprunteur=self.emprunteur)

        self.assertFalse(self.emprunteur.peut_emprunter())

    def test_bloque_si_retard(self):
        # Créer un emprunt en retard
        emprunt = Emprunt.objects.create(media=self.media1, emprunteur=self.emprunteur)
        emprunt.date_emprunt = timezone.now() - timedelta(days=10)
        emprunt.save()

        self.assertTrue(self.emprunteur.a_un_retard())
        self.assertFalse(self.emprunteur.peut_emprunter())

    def test_retour_emprunt(self):
        emprunt = Emprunt.objects.create(media=self.media1, emprunteur=self.emprunteur)
        emprunt.rendre()

        emprunt.refresh_from_db()
        self.assertIsNotNone(emprunt.date_retour)
        self.media1.refresh_from_db()
        self.assertTrue(self.media1.disponible)
