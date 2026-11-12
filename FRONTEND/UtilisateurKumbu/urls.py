from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),

    path('propos/', views.propos, name='propos'),
    path('recherche/', views.recherche, name='recherche'),

    path('assistant/', views.assistant , name='assistant'),
    path('contact/', views.contact, name='contact'),

    path('mon_profil/', views.mon_profil, name='mon_profil'),

    path('centre_aide/', views.centre_aide, name='centre_aide'),
    path('politiques/', views.politiques, name='politiques'),
    path('conditions/', views.conditions, name='conditions'),

    path('connexion/', views.connexion, name='connexion'),
    path('connexion/google/', views.connexion_google, name='connexion_google'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
]    
