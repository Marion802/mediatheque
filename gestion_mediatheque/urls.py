from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bibliotheque/', include('bibliothecaire.urls')),
    path('catalogue/', include('membre.urls')),

    # Rediriger la racine vers /catalogue/
    path('', RedirectView.as_view(url='/catalogue/', permanent=False)),
]
