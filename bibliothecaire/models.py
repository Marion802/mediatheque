from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Membre(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bloque = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def emprunts_actifs(self):
        return self.emprunt_set.filter(date_retour__isnull=True)

    def a_un_retard(self):
        today = timezone.now().date()
        il_y_a_30_jours = today - timedelta(days=30)
        return self.emprunts_actifs().filter(date_emprunt__lt=il_y_a_30_jours).exists()

class Media(models.Model):
    TYPE_CHOICES = [
        ('livre', 'Livre'),
        ('dvd', 'DVD'),
        ('cd', 'CD'),
        ('jeu', 'Jeu de plateau'),
    ]
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=100)
    annee = models.PositiveIntegerField()
    type_media = models.CharField(max_length=10, choices=TYPE_CHOICES, default='livre')

    def __str__(self):
        return self.titre

    @property
    def disponible(self):
        return not self.emprunt_set.filter(date_retour__isnull=True).exists()

class Emprunt(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Emprunt de {self.media} par {self.membre}"

    def est_en_retard(self):
        if self.date_retour:
            return False
        return self.date_emprunt < timezone.now().date() - timedelta(days=30)

    def clean(self):
        if self.membre.emprunts_actifs().count() >= 3:
            raise ValidationError("Ce membre a déjà 3 emprunts en cours.")
        if self.membre.a_un_retard():
            raise ValidationError("Ce membre a un emprunt en retard.")
        if self.media.type_media == "jeu":
            raise ValidationError("Les jeux de plateau ne peuvent pas être empruntés.")

    @property
    def emprunteur(self):
        return self.membre

