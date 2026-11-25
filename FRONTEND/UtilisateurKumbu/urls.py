from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),

    path('propos/', views.propos, name='propos'),
    path('recherche/', views.recherche, name='recherche'),

    path('assistant/', views.assistant , name='assistant'),
    path('contact/', views.contact, name='contact'),

    # --- Profil ---
    path('mon_profil/', views.mon_profil, name='mon_profil'),
    path('mon_profil/informations/', views.profil_informations, name='profil_informations'),
    path('mon_profil/livres-publies/', views.livres_publies, name='livres_publies'),
    path('mon_profil/livres-lus/', views.livres_lus, name='livres_lus'),
    path('mon_profil/modifier/', views.modifier_profil, name='modifier_profil'),
    path('mon_profil/modifier/supprimer-photo/', views.supprimer_photo, name='supprimer_photo'),
    path('mon_profil/parametres/', views.parametres, name='parametres'),
    path('mon_profil/parametres/supprimer-compte/', views.supprimer_compte, name='supprimer_compte'),
    path('mon_profil/publication/<int:pk>/supprimer/', views.supprimer_publication, name='supprimer_publication'),
    path('mon_profil/publier-livre/', views.publiLivre, name='publiLivre'),

    # --- Livres ---
    path('livre/<int:pk>/', views.livre_detail, name='livre_detail'),
    path('livre/<int:pk>/lire/', views.livre_lire, name='livre_lire'),
    path('livre/<int:pk>/lecture/', views.livre_lu, name='livre_lu'),

    path('centre_aide/', views.centre_aide, name='centre_aide'),
    path('politiques/', views.politiques, name='politiques'),
    path('conditions/', views.conditions, name='conditions'),

    path('connexion/', views.connexion, name='connexion'),
    #path('connexion/google/', views.connexion_google, name='connexion_google'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
]

# Fichiers envoyés (photos de profil, publications…) servis en développement.
# Nécessite MEDIA_URL et MEDIA_ROOT dans settings.py (voir LISEZ-MOI).
if settings.DEBUG and settings.MEDIA_URL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
