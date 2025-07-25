from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import MembreForm, MediaForm, EmpruntForm
from .models import Membre, Media, Emprunt


# Accueil de l'application bibliothécaire
def accueil(request):
    return render(request, 'bibliothecaire/accueil.html')

# --- GESTION DES MEMBRES ---
def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, 'bibliothecaire/liste_membres.html', {'membres': membres})

def bloquer_membre(request, membre_id):
    membre = get_object_or_404(Membre, pk=membre_id)
    membre.est_actif = False
    membre.save()
    return redirect('bibliothecaire:liste_membres')

# --- GESTION DES MÉDIAS ---
def liste_medias(request):
    medias = Media.objects.all()
    return render(request, 'bibliothecaire/liste_medias.html', {'medias': medias})

# --- GESTION DES EMPRUNTS ---
def liste_emprunts(request):
    emprunts = Emprunt.objects.all()
    return render(request, 'bibliothecaire/liste_emprunts.html', {'emprunts': emprunts})

def rendre_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, pk=emprunt_id)
    emprunt.date_retour = timezone.now()
    emprunt.save()
    return redirect('bibliothecaire:liste_emprunts')

def ajouter_emprunt(request):
    if request.method == 'POST':
        form = EmpruntForm(request.POST)
        if form.is_valid():
            emprunt = form.save(commit=False)

            # Vérifier que le média n'est pas un jeu de plateau
            if emprunt.media.type_media == 'jeu':
                messages.error(request, "Les jeux de plateau ne peuvent pas être empruntés.")
                return redirect('bibliothecaire:ajouter_emprunt')

            # Vérifier que le média est disponible
            if not emprunt.media.disponible:
                messages.error(request, "Ce média n'est pas disponible pour un emprunt.")
                return redirect('bibliothecaire:ajouter_emprunt')

            # Vérifier que le membre n’a pas déjà 3 emprunts actifs
            if emprunt.membre.emprunts_actifs().count() >= 3:
                messages.error(request, "Ce membre a déjà 3 emprunts actifs.")
                return redirect('bibliothecaire:ajouter_emprunt')

            # Vérifier que le membre n’a pas de retard
            if emprunt.membre.a_un_retard():
                messages.error(request, "Ce membre a un emprunt en retard et ne peut pas emprunter.")
                return redirect('bibliothecaire:ajouter_emprunt')

            emprunt.save()

            # Marquer le média comme non disponible
            emprunt.media.disponible = False
            emprunt.media.save()

            messages.success(request, "Emprunt enregistré avec succès.")
            return redirect('bibliothecaire:liste_emprunts')
    else:
        form = EmpruntForm()

    return render(request, 'bibliothecaire/ajouter_emprunt.html', {'form': form})


def rendre_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)

    # Si l'emprunt n'est pas déjà retourné, on le marque comme retourné
    if emprunt.date_retour is None:
        emprunt.date_retour = timezone.now().date()
        emprunt.save()

    return redirect('bibliothecaire:liste_emprunts')


def membre_create(request):
    if request.method == "POST":
        form = MembreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bibliothecaire:liste_membres')
    else:
        form = MembreForm()
    return render(request, 'bibliothecaire/membre_create.html', {'form': form})

def modifier_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)

    if request.method == 'POST':
        form = MembreForm(request.POST, instance=membre)
        if form.is_valid():
            form.save()
            return redirect('bibliothecaire:liste_membres')
    else:
        form = MembreForm(instance=membre)

    return render(request, 'bibliothecaire/modifier_membre.html', {'form': form, 'membre': membre})

def supprimer_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)
    membre.delete()
    return redirect('bibliothecaire:liste_membres')

def ajouter_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bibliothecaire:liste_medias')
    else:
        form = MediaForm()
    return render(request, 'bibliothecaire/ajouter_media.html', {'form': form})
