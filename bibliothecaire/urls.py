from django.urls import path
from . import views

app_name = 'bibliothecaire'

urlpatterns = [
    path('', views.accueil, name='accueil_biblio'),
    path('medias/', views.liste_medias, name='liste_medias'),
    path('emprunts/', views.liste_emprunts, name='liste_emprunts'),
]

