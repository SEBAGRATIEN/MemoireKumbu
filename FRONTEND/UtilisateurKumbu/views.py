from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from .forms import ConnexionForm, InscriptionForm, LivreForm, ProfilForm, PublicationForm
from .models import Livre, LivreLu, MessageContact, Profil, Publication
#import json
#import firebase_admin
#from firebase_admin import credentials, auth

# Create your views here.
# Initialisation Firebase Admin
""""
if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred)"""

""""
@require_POST
def connexion_google(request):
    try:
        data = json.loads(request.body)
        id_token = data.get("id_token")
        if not id_token:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Token Firebase manquant."},status=400)
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        nom = decoded_token.get("name", "")
        photo = decoded_token.get("picture", "")
        if not email:
            return JsonResponse({"success": False, "error": "Google n'a pas fourni d'adresse e-mail."},status=400)
        utilisateur = User.objects.filter(email__iexact=email).first()
        if utilisateur is None:
            username = email.split("@")[0]
            base_username = username
            compteur = 1
            while User.objects.filter(
                username=username
            ).exists():
                username = f"{base_username}{compteur}"
                compteur += 1
            utilisateur = User.objects.create_user(username=username, email=email)
        if nom:
            parties = nom.split(" ", 1)
            utilisateur.first_name = parties[0]
            if len(parties) > 1:
                utilisateur.last_name = parties[1]
            utilisateur.save()
        login(request, utilisateur)
        return JsonResponse({"success": True, "redirect_url": "/"})
    except Exception as e:
        return JsonResponse(
            {"success": False, "error": "Connexion Google impossible."}, status=401
            )"""

LOGIN_URL_NAME = "connexion"

def base(request):
    profils_recents = []
    livres_recents = []
    if request.user.is_authenticated:
        profils_recents = Profil.objects.select_related("utilisateur").order_by("-date_creation")[:3]
        livres_recents = Livre.objects.filter(publie=True).order_by("-date_creation")[:4]
    User = get_user_model()
    total_users = User.objects.count()

    return render(request, 'base.html', {
        'profils_recents': profils_recents,
        'livres_recents': livres_recents,
        'total_users': total_users,
    })

@login_required(login_url=LOGIN_URL_NAME)
def propos(request):
    return render(request, 'propos/info.html')

@login_required(login_url=LOGIN_URL_NAME)
def recherche(request):
    q = request.GET.get("q", "").strip()
    livre = Livre.objects.filter(Q(publie=True) | Q(ajoute_par=request.user))
    if q:
        livre = livre.filter(Q(titre__icontains=q) | Q(auteur__icontains=q) | Q(description__icontains=q))
    return render(request, 'recherche/recherche.html', {'livre': livre, 'q': q})

@login_required(login_url=LOGIN_URL_NAME)
def assistant(request):
    return render(request, 'assistant/discussion.html')

@login_required(login_url=LOGIN_URL_NAME)
def contact(request):
    if request.method == "POST":
        nom = request.POST.get("nom", "").strip()
        email = request.POST.get("email", "").strip()
        texte = request.POST.get("message", "").strip()
        if nom and email and texte:
            MessageContact.objects.create(nom=nom, email=email, message=texte)
            messages.success(request, "Votre message a bien été envoyé. Nous vous répondrons sous 48 heures.")
            return redirect("contact")
        messages.error(request, "Veuillez remplir tous les champs du formulaire.")
    return render(request, 'contact/contact.html')

@login_required(login_url=LOGIN_URL_NAME)
def centre_aide(request):
    return render(request, 'centre_aide/aide.html')

@login_required(login_url=LOGIN_URL_NAME)
def politiques(request):
    return render(request, 'politiques/politiques.html')

@login_required(login_url=LOGIN_URL_NAME)
def conditions(request):
    return render(request, 'conditions/condition.html')

def _username_unique(email):
    base_username = slugify(email.split("@")[0]) or "utilisateur"
    username, compteur = base_username, 1
    while User.objects.filter(username__iexact=username).exists():
        username = f"{base_username}{compteur}"
        compteur += 1
    return username


def connexion(request):
    suivant = request.POST.get("next") or request.GET.get("next") or ""
    if not url_has_allowed_host_and_scheme(suivant, allowed_hosts={request.get_host()}):
        suivant = ""
    if request.user.is_authenticated:
        return redirect(suivant or "mon_profil")

    onglet = "connexion"
    form_connexion = ConnexionForm()
    form_inscription = InscriptionForm()

    if request.method == "POST":
        if request.POST.get("action") == "inscription":
            onglet = "inscription"
            form_inscription = InscriptionForm(request.POST)
            if form_inscription.is_valid():
                d = form_inscription.cleaned_data
                utilisateur = User.objects.create_user(
                    username=_username_unique(d["email"]), email=d["email"],
                    password=d["mot_de_passe"], first_name=d["prenom"], last_name=d["nom"],
                )
                Profil.objects.create(utilisateur=utilisateur, prenom=d["prenom"], post_nom=d["post_nom"])
                login(request, utilisateur)
                messages.success(request, "Bienvenue sur Kumbu ! Complétez votre profil pour commencer.")
                return redirect("modifier_profil")
        else:
            form_connexion = ConnexionForm(request.POST)
            if form_connexion.is_valid():
                identifiant = form_connexion.cleaned_data["identifiant"].strip()
                mot_de_passe = form_connexion.cleaned_data["mot_de_passe"]
                if "@" in identifiant:  # connexion possible avec l'e-mail
                    trouve = User.objects.filter(email__iexact=identifiant).first()
                    identifiant = trouve.username if trouve else identifiant
                utilisateur = authenticate(request, username=identifiant, password=mot_de_passe)
                if utilisateur is not None:
                    login(request, utilisateur)
                    return redirect(suivant or "mon_profil")
                form_connexion.add_error(None, "Identifiant ou mot de passe incorrect.")

    return render(request, 'connexion/login.html', {
        'form_connexion': form_connexion,
        'form_inscription': form_inscription,
        'onglet': onglet,
        'next': suivant,
    })

def deconnexion(request):
    logout(request)
    return redirect('connexion')

def _profil_de(utilisateur):
    profil, _ = Profil.objects.get_or_create(
        utilisateur=utilisateur,
        defaults={"prenom": utilisateur.first_name},
    )
    return profil

def _contexte_profil(request, onglet):
    profil = _profil_de(request.user)
    return {
        'profil': profil,
        'onglet': onglet,
        'nb_publications': request.user.publications.count(),
        'nb_livres_publies': request.user.livres_ajoutes.count(),
        'nb_livres_lus': request.user.livres_lus.count(),
    }


@login_required(login_url=LOGIN_URL_NAME)
def mon_profil(request):
    contexte = _contexte_profil(request, "actus")
    if request.method == "POST":
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            publication = form.save(commit=False)
            publication.auteur = request.user
            publication.save()
            messages.success(request, "Votre publication a été ajoutée.")
            return redirect("mon_profil")
    else:
        form = PublicationForm()
    contexte.update({
        'form': form,
        'publications': request.user.publications.all(),
    })
    return render(request, 'mon_profil/profil.html', contexte)


@login_required(login_url=LOGIN_URL_NAME)
def profil_informations(request):
    return render(request, 'mon_profil/informations.html', _contexte_profil(request, "infos"))


@login_required(login_url=LOGIN_URL_NAME)
def livres_publies(request):
    contexte = _contexte_profil(request, "publies")
    contexte['livres'] = request.user.livres_ajoutes.order_by("-date_creation")
    return render(request, 'mon_profil/livres_publies.html', contexte)


@login_required(login_url=LOGIN_URL_NAME)
def livres_lus(request):
    contexte = _contexte_profil(request, "lus")
    contexte['lectures'] = request.user.livres_lus.select_related("livre").order_by("-derniere_lecture")
    return render(request, 'mon_profil/livres_lus.html', contexte)


@login_required(login_url=LOGIN_URL_NAME)
def modifier_profil(request):
    profil = _profil_de(request.user)
    if request.method == "POST":
        form = ProfilForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            nouvelle_photo = "photo" in form.changed_data and bool(form.cleaned_data.get("photo"))
            profil = form.save()
            if nouvelle_photo:
                # La nouvelle photo apparaît aussi dans le fil d'actualités du profil.
                Publication.objects.create(
                    auteur=request.user,
                    type=Publication.TYPE_PHOTO_PROFIL,
                    image=profil.photo.name,
                )
            messages.success(request, "Votre profil a été mis à jour.")
            return redirect("mon_profil")
    else:
        form = ProfilForm(instance=profil)
    contexte = _contexte_profil(request, "modifier")
    contexte['form'] = form
    return render(request, 'mon_profil/modifier.html', contexte)


@login_required(login_url=LOGIN_URL_NAME)
@require_POST
def supprimer_photo(request):
    profil = _profil_de(request.user)
    if profil.photo:
        profil.photo = None
        profil.save()
        messages.success(request, "Votre photo de profil a été supprimée.")
    return redirect("modifier_profil")


@login_required(login_url=LOGIN_URL_NAME)
@require_POST
def supprimer_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk, auteur=request.user)
    publication.delete()
    messages.success(request, "La publication a été supprimée.")
    return redirect("mon_profil")

@login_required(login_url=LOGIN_URL_NAME)
def publiLivre(request):
    """Formulaire de publication d'un livre (depuis le profil)."""
    if request.method == "POST":
        form = LivreForm(request.POST, request.FILES)
        if form.is_valid():
            livre = form.save(commit=False)
            livre.ajoute_par = request.user
            livre.publie = False          # visible de tous après validation par un administrateur
            livre.save()
            messages.success(request, "Votre livre a été envoyé. Il sera visible de tous après approbation.")
            return redirect("livres_publies")
    else:
        form = LivreForm()
    contexte = _contexte_profil(request, "publier")
    contexte['form'] = form
    return render(request, 'mon_profil/livreForm.html', contexte)


# ----------------------------------------------------------------------
#  Un livre : fiche, lecture, enregistrement dans « Livres lus »
# ----------------------------------------------------------------------
def _livre_accessible(request, pk):
    """Un livre non approuvé n'est visible que par son auteur (et le personnel)."""
    livre = get_object_or_404(Livre, pk=pk)
    if not livre.publie and livre.ajoute_par_id != request.user.id and not request.user.is_staff:
        raise Http404("Livre introuvable")
    return livre


@login_required(login_url=LOGIN_URL_NAME)
def livre_detail(request, pk):
    livre = _livre_accessible(request, pk)
    lecture = LivreLu.objects.filter(utilisateur=request.user, livre=livre).first()
    return render(request, 'livres/detail.html', {
        'livre': livre,
        'lecture': lecture,
        'est_auteur': livre.ajoute_par_id == request.user.id,
    })


@login_required(login_url=LOGIN_URL_NAME)
def livre_lire(request, pk):
    """Ouvre le fichier du livre (le PDF s'affiche directement dans le navigateur)."""
    livre = _livre_accessible(request, pk)
    if not livre.fichier:
        messages.error(request, "Ce livre n'a pas de fichier à lire pour le moment.")
        return redirect("livre_detail", pk=livre.pk)
    lecture = LivreLu.objects.filter(utilisateur=request.user, livre=livre).first()
    if lecture:
        lecture.save()                    # met à jour « dernière lecture »
    return redirect(livre.fichier.url)


@login_required(login_url=LOGIN_URL_NAME)
@require_POST
def livre_lu(request, pk):
    """Enregistrer / mettre à jour / retirer un livre dans « Livres lus »."""
    livre = _livre_accessible(request, pk)
    action = request.POST.get("action", "ajouter")
    lecture = LivreLu.objects.filter(utilisateur=request.user, livre=livre).first()

    if action == "retirer":
        if lecture:
            lecture.delete()
            messages.success(request, "Le livre a été retiré de vos livres lus.")
    else:
        if lecture is None:
            lecture = LivreLu(utilisateur=request.user, livre=livre)
        if action == "terminer":
            lecture.termine, lecture.progression = True, 100
            messages.success(request, "Livre marqué comme terminé.")
        elif action == "progression":
            try:
                valeur = int(request.POST.get("progression", 0))
            except ValueError:
                valeur = 0
            lecture.progression = max(0, min(100, valeur))
            lecture.termine = lecture.progression == 100
            messages.success(request, "Votre progression a été enregistrée.")
        else:
            messages.success(request, "Le livre a été enregistré dans vos livres lus.")
        lecture.save()

    suivant = request.POST.get("next", "")
    if suivant and url_has_allowed_host_and_scheme(suivant, allowed_hosts={request.get_host()}):
        return redirect(suivant)
    return redirect("livre_detail", pk=livre.pk)


@login_required(login_url=LOGIN_URL_NAME)
def parametres(request):
    """Paramètres : mot de passe, thème (géré côté navigateur) et suppression du compte."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            utilisateur = form.save()
            update_session_auth_hash(request, utilisateur)  # reste connecté
            messages.success(request, "Votre mot de passe a été modifié.")
            return redirect("parametres")
    else:
        form = PasswordChangeForm(request.user)
    contexte = _contexte_profil(request, "parametres")
    contexte['form'] = form
    return render(request, 'mon_profil/parametres.html', contexte)


@login_required(login_url=LOGIN_URL_NAME)
@require_POST
def supprimer_compte(request):
    if not request.user.check_password(request.POST.get("mot_de_passe", "")):
        messages.error(request, "Mot de passe incorrect : le compte n'a pas été supprimé.")
        return redirect("parametres")
    utilisateur = request.user
    logout(request)
    utilisateur.delete()
    return redirect("connexion")
