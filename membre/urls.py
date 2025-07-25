from django.urls import path
from . import views

app_name = 'membre'

urlpatterns = [
    path('medias/', views.liste_medias, name='liste_medias'),
]
