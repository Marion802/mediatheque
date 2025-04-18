from django.shortcuts import render
from bibliothecaire.models import Media

def liste_medias(request):
    medias = Media.objects.all()

    # Filtrage par disponibilité
    disponible = request.GET.get('disponible')
    if disponible == '1':
        medias = medias.filter(disponible=True)

    # Filtrage par recherche
    recherche = request.GET.get('q')
    if recherche:
        medias = medias.filter(
            titre__icontains=recherche
        )

    return render(request, 'membre/liste_medias.html', {
        'medias': medias,
        'recherche': recherche,
        'disponible': disponible,
    })
