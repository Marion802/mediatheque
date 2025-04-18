from django.urls import path
from .views import liste_medias

urlpatterns = [
    path('', liste_medias, name='liste_medias'),
]
