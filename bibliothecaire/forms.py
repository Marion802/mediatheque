from django import forms
from .models import Membre, Media, Emprunt



class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'prenom', 'email' , 'bloque']

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['titre', 'auteur', 'annee', 'type_media']

class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['membre', 'media']