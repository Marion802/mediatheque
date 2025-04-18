from django.db import models
from django.utils import timezone
from datetime import timedelta

class Emprunteur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bloque = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

    def emprunts_actifs(self):
        return self.emprunt_set.filter(date_retour__isnull=True)

    def a_un_retard(self):
        for emprunt in self.emprunts_actifs():
            if emprunt.est_en_retard():
                return True
        return False

    def peut_emprunter(self):
        if self.bloque:
            return False
        if self.a_un_retard():
            return False
        if self.emprunts_actifs().count() >= 3:
            return False
        return True

class Media(models.Model):
    TYPE_CHOICES = [
        ('livre', 'Livre'),
        ('cd', 'CD'),
        ('dvd', 'DVD'),
        ('jeu', 'Jeu de Plateau'),
    ]

    titre = models.CharField(max_length=255)
    type_media = models.CharField(max_length=10, choices=TYPE_CHOICES)
    auteur = models.CharField(max_length=255, blank=True, null=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titre} ({self.get_type_media_display()})"

    def est_empruntable(self):
        return self.disponible and self.type_media != 'jeu'

class Emprunt(models.Model):
    emprunteur = models.ForeignKey(Emprunteur, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    date_emprunt = models.DateField(default=timezone.now)
    date_retour = models.DateField(blank=True, null=True)

    def est_en_retard(self):
        if not self.date_retour:
            return timezone.now().date() > self.date_emprunt + timedelta(days=7)
        return False

    def __str__(self):
        return f"{self.media.titre} emprunté par {self.emprunteur.nom}"

    def rendre(self):
        self.date_retour = timezone.now()
        self.media.disponible = True
        self.media.save()
        self.save()