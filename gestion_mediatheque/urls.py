from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bibliotheque/', include('bibliothecaire.urls')),  # ✅ c’est cette ligne qui importe les URLs
    path('catalogue/', include('membre.urls')),
    path('', RedirectView.as_view(url='/catalogue/', permanent=False)),
]
