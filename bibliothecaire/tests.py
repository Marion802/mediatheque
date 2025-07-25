from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.test import TestCase
from bibliothecaire.models import Membre, Media, Emprunt


class MembreTestCase(TestCase):
    def test_creer_membre(self):
        membre = Membre.objects.create(nom="Doe", prenom="John", email="john@example.com")
        self.assertEqual(str(membre), "John Doe")


class MediaTestCase(TestCase):
    def test_media_disponible_par_defaut(self):
        media = Media.objects.create(titre="1984", auteur="Orwell", annee=1949, type_media="livre")
        self.assertTrue(media.disponible)


class EmpruntTestCase(TestCase):
    def setUp(self):
        self.membre = Membre.objects.create(nom="Test", prenom="Emprunteur", email="test@ex.com")
        self.media = Media.objects.create(titre="Titre", auteur="Auteur", annee=2020, type_media="livre")

    def test_ajout_emprunt(self):
        emprunt = Emprunt(membre=self.membre, media=self.media)
        emprunt.full_clean()  # valider les règles
        emprunt.save()
        self.assertFalse(emprunt.est_en_retard())
        self.assertFalse(self.media.disponible)

    def test_retour_emprunt(self):
        emprunt = Emprunt(membre=self.membre, media=self.media)
        emprunt.full_clean()
        emprunt.save()
        emprunt.date_retour = timezone.now().date()
        emprunt.save()
        self.assertTrue(self.media.disponible)

    def test_emprunt_refuse_si_jeu_de_plateau(self):
        jeu = Media.objects.create(titre="Jeu", auteur="Auteur", annee=2023, type_media="jeu")
        emprunt = Emprunt(membre=self.membre, media=jeu)
        with self.assertRaises(ValidationError):
            emprunt.full_clean()

    def test_membre_ne_peut_pas_avoir_plus_de_3_emprunts(self):
        for i in range(3):
            media = Media.objects.create(titre=f"Media {i}", auteur="Auteur", annee=2020, type_media="livre")
            emprunt = Emprunt(membre=self.membre, media=media)
            emprunt.full_clean()
            emprunt.save()

        media4 = Media.objects.create(titre="Media 4", auteur="Auteur", annee=2020, type_media="livre")
        emprunt4 = Emprunt(membre=self.membre, media=media4)
        with self.assertRaises(ValidationError):
            emprunt4.full_clean()

    def test_emprunt_en_retard_apres_7_jours(self):
        emprunt = Emprunt(membre=self.membre, media=self.media)
        emprunt.full_clean()
        emprunt.save()
        emprunt.date_emprunt = timezone.now().date() - timedelta(days=31)  # > 30 jours pour être en retard
        emprunt.save()
        self.assertTrue(emprunt.est_en_retard())

    def test_membre_avec_retard_ne_peut_plus_emprunter(self):
        media1 = Media.objects.create(titre="Media Retard", auteur="Auteur", annee=2020, type_media="livre")
        emprunt1 = Emprunt(membre=self.membre, media=media1)
        emprunt1.full_clean()
        emprunt1.save()
        emprunt1.date_emprunt = timezone.now().date() - timedelta(days=31)  # plus de 30 jours
        emprunt1.save()

        self.assertTrue(self.membre.a_un_retard())

        media2 = Media.objects.create(titre="Media 2", auteur="Auteur", annee=2020, type_media="livre")
        emprunt2 = Emprunt(membre=self.membre, media=media2)
        with self.assertRaises(ValidationError):
            emprunt2.full_clean()
