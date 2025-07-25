from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Inclure l'app bibliothécaire avec un namespace
    path('bibliothecaire/', include(('bibliothecaire.urls', 'bibliothecaire'), namespace='bibliothecaire')),

    # Inclure l'app membre avec un namespace
    path('membre/', include(('membre.urls', 'membre'), namespace='membre')),

    # Rediriger la racine du site vers la vue membre:liste_medias
    path('', RedirectView.as_view(pattern_name='membre:liste_medias', permanent=False)),
]
