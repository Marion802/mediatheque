from django.shortcuts import render
from bibliothecaire.models import Media, Emprunt
from django.utils import timezone
from datetime import timedelta

def liste_medias(request):
    medias = Media.objects.all()

    disponible = request.GET.get('disponible')
    if disponible == '1':
        aujourd_hui = timezone.now().date()
        duree_emprunt = timedelta(days=7)

        emprunts_actifs = Emprunt.objects.filter(date_emprunt__gte=aujourd_hui - duree_emprunt)
        ids_indisponibles = emprunts_actifs.values_list('media_id', flat=True)

        medias = medias.exclude(id__in=ids_indisponibles)

    recherche = request.GET.get('q')
    if recherche:
        medias = medias.filter(titre__icontains=recherche)

    return render(request, 'membre/liste_medias.html', {
        'medias': medias,
        'recherche': recherche,
        'disponible': disponible,
    })
