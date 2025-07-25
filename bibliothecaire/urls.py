from django.urls import path
from . import views

app_name = 'bibliothecaire'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('medias/', views.liste_medias, name='liste_medias'),
    path('emprunts/', views.liste_emprunts, name='liste_emprunts'),
    path('membres/', views.liste_membres, name='liste_membres'),
    path('membres/create/', views.membre_create, name='membre_create'),
    path('membre/<int:membre_id>/bloquer/', views.bloquer_membre, name='bloquer_membre'),
    path('membre/<int:membre_id>/modifier/', views.modifier_membre, name='modifier_membre'),
    path('medias/ajouter/', views.ajouter_media, name='ajouter_media'),
    path('membres/<int:membre_id>/supprimer/', views.supprimer_membre, name='supprimer_membre'),
    path('emprunts/ajouter/', views.ajouter_emprunt, name='ajouter_emprunt'),
    path('emprunts/<int:emprunt_id>/rendre/', views.rendre_emprunt, name='rendre_emprunt'),

]

