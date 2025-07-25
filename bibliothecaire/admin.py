from django.contrib import admin
from .models import Membre, Media, Emprunt
from django.utils import timezone

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'bloque', 'nombre_emprunts_actifs', 'a_un_retard')

    def nombre_emprunts_actifs(self, obj):
        return obj.emprunts_actifs().count()

    nombre_emprunts_actifs.admin_order_field = 'nom'
    nombre_emprunts_actifs.short_description = "Emprunts actifs"

    def a_un_retard(self, obj):
        return obj.a_un_retard()

    a_un_retard.boolean = True
    a_un_retard.short_description = "A un retard"

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_media', 'auteur', 'disponible')

@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ('media', 'emprunteur', 'date_emprunt', 'date_retour', 'est_en_retard')
    actions = ['rendre_livre']

    def est_en_retard(self, obj):
        return obj.est_en_retard()
    est_en_retard.boolean = True  # icône ✓/✗ dans l’admin

    def rendre_livre(self, request, queryset):
        nb = queryset.update(date_retour=timezone.now())
        self.message_user(request, f"{nb} emprunt(s) marqué(s) comme retourné(s).")
    rendre_livre.short_description = "Rendre les livres sélectionnés"