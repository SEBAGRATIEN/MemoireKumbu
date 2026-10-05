from django.contrib import admin

# Register your models here.
admin.site_header = "ADMINISTRATION KUMBU"
admin.site_title = "KUMBU"
admin.site.index_title = "MemoireKumbu"

from django.contrib import admin
from .models import (
    Profil,
    Categorie,
    Livre,
    LivreLu,
    LivreSauvegarde,
    Question,
    Reponse,
    RessourceApprentissage,
    MessageContact,
    Etablissement,
    Promotion,
    MembrePromotion,
    SupportPromotion,
)


admin.site.site_header = "ADMINISTRATION KUMBU"
admin.site.site_title = "KUMBU"
admin.site.index_title = "Gestion de la plateforme KUMBU"


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = (
        "utilisateur",
        "post_nom",
        "prenom",
        "etablissement",
        "filiere",
        "niveau",
        "date_creation",
    )

    search_fields = (
        "utilisateur__username",
        "utilisateur__first_name",
        "utilisateur__last_name",
        "post_nom",
        "prenom",
        "etablissement",
        "filiere",
    )

    list_filter = (
        "etablissement",
        "filiere",
        "niveau",
    )


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "slug",
        "active",
        "date_creation",
    )

    search_fields = (
        "nom",
        "description",
    )

    list_filter = (
        "active",
    )

    prepopulated_fields = {
        "slug": ("nom",)
    }


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = (
        "titre",
        "auteur",
        "categorie",
        "langue",
        "publie",
        "date_creation",
    )

    search_fields = (
        "titre",
        "auteur",
        "description",
        "isbn",
    )

    list_filter = (
        "categorie",
        "langue",
        "publie",
        "date_creation",
    )

    list_editable = (
        "publie",
    )


@admin.register(LivreLu)
class LivreLuAdmin(admin.ModelAdmin):
    list_display = (
        "utilisateur",
        "livre",
        "progression",
        "termine",
        "derniere_lecture",
    )

    search_fields = (
        "utilisateur__username",
        "livre__titre",
    )

    list_filter = (
        "termine",
        "derniere_lecture",
    )


@admin.register(LivreSauvegarde)
class LivreSauvegardeAdmin(admin.ModelAdmin):
    list_display = (
        "utilisateur",
        "livre",
        "date_sauvegarde",
    )

    search_fields = (
        "utilisateur__username",
        "livre__titre",
    )

    list_filter = (
        "date_sauvegarde",
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "utilisateur",
        "livre",
        "question_courte",
        "date_creation",
    )

    search_fields = (
        "utilisateur__username",
        "livre__titre",
        "texte",
    )

    list_filter = (
        "date_creation",
    )

    def question_courte(self, obj):
        return obj.texte[:80]

    question_courte.short_description = "Question"


@admin.register(Reponse)
class ReponseAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "reponse_courte",
        "est_ia",
        "date_creation",
    )

    search_fields = (
        "question__texte",
        "texte",
    )

    list_filter = (
        "est_ia",
        "date_creation",
    )

    def reponse_courte(self, obj):
        return obj.texte[:80]

    reponse_courte.short_description = "Réponse"


@admin.register(RessourceApprentissage)
class RessourceApprentissageAdmin(admin.ModelAdmin):
    list_display = (
        "titre",
        "categorie",
        "auteur",
        "publie",
        "date_creation",
    )

    search_fields = (
        "titre",
        "description",
        "auteur",
    )

    list_filter = (
        "categorie",
        "publie",
        "date_creation",
    )

    list_editable = (
        "publie",
    )


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "email",
        "message_court",
        "lu",
        "date_envoi",
    )

    search_fields = (
        "nom",
        "email",
        "message",
    )

    list_filter = (
        "lu",
        "date_envoi",
    )

    list_editable = (
        "lu",
    )

    readonly_fields = (
        "date_envoi",
    )

    def message_court(self, obj):
        return obj.message[:80]

    message_court.short_description = "Message"


@admin.register(Etablissement)
class EtablissementAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "ville",
        "actif",
        "date_creation",
    )

    search_fields = (
        "nom",
        "ville",
        "description",
    )

    list_filter = (
        "ville",
        "actif",
    )


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "etablissement",
        "annee_academique",
        "active",
    )

    search_fields = (
        "nom",
        "etablissement__nom",
        "annee_academique",
    )

    list_filter = (
        "etablissement",
        "annee_academique",
        "active",
    )


@admin.register(MembrePromotion)
class MembrePromotionAdmin(admin.ModelAdmin):
    list_display = (
        "utilisateur",
        "promotion",
        "identifiant_annuel",
        "actif",
        "date_inscription",
    )

    search_fields = (
        "utilisateur__username",
        "utilisateur__first_name",
        "utilisateur__last_name",
        "identifiant_annuel",
        "promotion__nom",
    )

    list_filter = (
        "promotion",
        "actif",
        "date_inscription",
    )


@admin.register(SupportPromotion)
class SupportPromotionAdmin(admin.ModelAdmin):
    list_display = (
        "titre",
        "promotion",
        "publie",
        "date_creation",
    )

    search_fields = (
        "titre",
        "description",
        "promotion__nom",
    )

    list_filter = (
        "promotion",
        "publie",
        "date_creation",
    )

    list_editable = (
        "publie",
    )