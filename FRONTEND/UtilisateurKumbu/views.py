from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.conf import settings
import json
import firebase_admin
from firebase_admin import credentials, auth

# Create your views here.
# Initialisation Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate(
        settings.FIREBASE_SERVICE_ACCOUNT
    )
    firebase_admin.initialize_app(cred)


@require_POST
def connexion_google(request):
    try:
        data = json.loads(request.body)
        id_token = data.get("id_token")

        if not id_token:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Token Firebase manquant."
                },
                status=400
            )

        decoded_token = auth.verify_id_token(id_token)

        uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        nom = decoded_token.get("name", "")
        photo = decoded_token.get("picture", "")

        if not email:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Google n'a pas fourni d'adresse e-mail."
                },
                status=400
            )

        # Chercher l'utilisateur Django par e-mail
        utilisateur = User.objects.filter(
            email__iexact=email
        ).first()

        # Créer l'utilisateur s'il n'existe pas
        if utilisateur is None:

            username = email.split("@")[0]

            # Éviter un doublon de username
            base_username = username
            compteur = 1

            while User.objects.filter(
                username=username
            ).exists():

                username = f"{base_username}{compteur}"
                compteur += 1

            utilisateur = User.objects.create_user(
                username=username,
                email=email
            )

        # Mettre à jour le nom si Google en fournit un
        if nom:
            parties = nom.split(" ", 1)

            utilisateur.first_name = parties[0]

            if len(parties) > 1:
                utilisateur.last_name = parties[1]

            utilisateur.save()

        # Créer la session Django
        login(request, utilisateur)

        return JsonResponse({
            "success": True,
            "redirect_url": "/"
        })

    except Exception as e:

        return JsonResponse(
            {
                "success": False,
                "error": "Connexion Google impossible."
            },
            status=401
        )

def base(request):
    return render(request, 'base.html')

def propos(request):
    return render(request, 'propos/info.html') 

def recherche(request):
    return render(request, 'recherche/recherche.html') 

def assistant(request):
    return render(request, 'assistant/discussion.html') 

def contact(request):
    return render(request, 'contact/contact.html') 

def mon_profil(request):
    return render(request, 'mon_profil/profil.html')

def connexion(request):
    return render(request, 'connexion/login.html')

def deconnexion(request):
    # TODO : brancher ici la vraie déconnexion Django, par exemple :
    # from django.contrib.auth import logout
    # logout(request)
    return redirect('connexion')

def centre_aide(request):
    return render(request, 'centre_aide/aide.html')

def politiques(request):
    return render(request, 'politiques/politiques.html')

def conditions(request):
    return render(request, 'conditions/condition.html')
