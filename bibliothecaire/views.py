from django.shortcuts import render
from .models import Media, Emprunt, Emprunteur  # ou Membre si tu l’as renommé

def accueil(request):
    return render(request, 'bibliothecaire/accueil.html')

def liste_medias(request):
    medias = Media.objects.all()
    return render(request, 'bibliothecaire/liste_medias.html', {'medias': medias})

def liste_emprunts(request):
    emprunts = Emprunt.objects.all()
    return render(request, 'bibliothecaire/liste_emprunts.html', {'emprunts': emprunts})
