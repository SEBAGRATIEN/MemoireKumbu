from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Categorie, Livre, Profil, Publication

TAILLE_MAX_IMAGE = 5 * 1024 * 1024  # 5 Mo


def _verifier_image(fichier):
    """Refuse les images trop lourdes (le format est déjà contrôlé par ImageField / Pillow)."""
    if fichier and hasattr(fichier, "size") and fichier.size > TAILLE_MAX_IMAGE:
        raise ValidationError("L'image est trop lourde (5 Mo maximum).")
    return fichier


# ---------------------------------------------------------------- Connexion
class ConnexionForm(forms.Form):
    identifiant = forms.CharField(max_length=150)
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)


class InscriptionForm(forms.Form):
    nom = forms.CharField(max_length=150)
    post_nom = forms.CharField(max_length=100, required=False)
    prenom = forms.CharField(max_length=100)
    email = forms.EmailField()
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)
    mot_de_passe2 = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Cette adresse e-mail est déjà utilisée.")
        return email

    def clean(self):
        data = super().clean()
        mdp1, mdp2 = data.get("mot_de_passe"), data.get("mot_de_passe2")
        if mdp1 and mdp2 and mdp1 != mdp2:
            self.add_error("mot_de_passe2", "Les deux mots de passe ne correspondent pas.")
        elif mdp1:
            try:
                validate_password(mdp1)
            except ValidationError as erreur:
                self.add_error("mot_de_passe", erreur)
        return data


# ------------------------------------------------------------------- Profil
class ProfilForm(forms.ModelForm):
    """Modification du profil : identité, informations académiques et photo."""
    nom = forms.CharField(max_length=150, required=False, label="Nom")
    email = forms.EmailField(required=False, label="Adresse e-mail")

    class Meta:
        model = Profil
        fields = ["prenom", "post_nom", "biographie", "etablissement",
                  "filiere", "niveau", "annee_academique", "photo"]
        widgets = {
            "photo": forms.FileInput(attrs={"accept": "image/*", "id": "id_photo",
                                            "data-preview-img": "photoPreview", "data-preview-hide": "photoVide"}),
            "biographie": forms.Textarea(attrs={"rows": 4, "maxlength": 400,
                                                "placeholder": "Parlez un peu de vous…"}),
            "annee_academique": forms.TextInput(attrs={"placeholder": "ex. 2025-2026"}),
            "niveau": forms.TextInput(attrs={"placeholder": "ex. L2"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        utilisateur = self.instance.utilisateur
        self.fields["nom"].initial = utilisateur.last_name
        self.fields["email"].initial = utilisateur.email

    def clean_photo(self):
        return _verifier_image(self.cleaned_data.get("photo"))

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if email and User.objects.filter(email__iexact=email).exclude(pk=self.instance.utilisateur_id).exists():
            raise ValidationError("Cette adresse e-mail est déjà utilisée par un autre compte.")
        return email

    def save(self, commit=True):
        profil = super().save(commit=commit)
        utilisateur = profil.utilisateur
        utilisateur.last_name = self.cleaned_data.get("nom", "")
        utilisateur.first_name = self.cleaned_data.get("prenom", "")
        if self.cleaned_data.get("email"):
            utilisateur.email = self.cleaned_data["email"]
        if commit:
            utilisateur.save()
        return profil


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ["texte", "image"]
        widgets = {
            "texte": forms.Textarea(attrs={"rows": 2, "maxlength": 1000,
                                           "placeholder": "Partagez une actualité, une lecture, une idée…"}),
            "image": forms.FileInput(attrs={"accept": "image/*", "id": "id_pub_image",
                                            "data-preview-img": "pubPreview", "data-preview-box": "pubBox"}),
        }

    def clean_image(self):
        return _verifier_image(self.cleaned_data.get("image"))

    def clean(self):
        data = super().clean()
        if not (data.get("texte") or "").strip() and not data.get("image"):
            raise ValidationError("Écrivez un texte ou ajoutez une image pour publier.")
        return data


# -------------------------------------------------------------------- Livres
EXTENSIONS_LIVRE = (".pdf", ".epub", ".doc", ".docx", ".txt")
TAILLE_MAX_LIVRE = 50 * 1024 * 1024  # 50 Mo


class LivreForm(forms.ModelForm):
    """Formulaire de publication d'un livre depuis le profil."""

    class Meta:
        model = Livre
        fields = ["titre", "auteur", "description", "categorie", "couverture", "fichier",
                  "isbn", "date_publication", "nombre_pages", "langue"]
        labels = {
            "titre": "Titre du livre",
            "auteur": "Auteur",
            "description": "Description",
            "categorie": "Catégorie",
            "couverture": "Couverture",
            "fichier": "Fichier du livre (PDF, EPUB, DOC, DOCX, TXT)",
            "isbn": "ISBN (facultatif)",
            "date_publication": "Date de publication (facultatif)",
            "nombre_pages": "Nombre de pages (facultatif)",
            "langue": "Langue",
        }
        widgets = {
            "titre": forms.TextInput(attrs={"placeholder": "ex. Réseaux et télécommunications"}),
            "auteur": forms.TextInput(attrs={"placeholder": "Nom de l'auteur"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "De quoi parle ce livre ?"}),
            "couverture": forms.FileInput(attrs={"accept": "image/*", "id": "id_couverture",
                                                 "data-preview-img": "couvPreview", "data-preview-hide": "couvVide"}),
            "fichier": forms.FileInput(attrs={"accept": ",".join(EXTENSIONS_LIVRE)}),
            "date_publication": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "nombre_pages": forms.NumberInput(attrs={"min": 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categorie"].queryset = Categorie.objects.filter(active=True).order_by("nom")
        self.fields["categorie"].empty_label = "Choisir une catégorie"
        self.fields["fichier"].required = True      # un livre doit pouvoir être ouvert
        self.fields["description"].required = False

    def clean_couverture(self):
        return _verifier_image(self.cleaned_data.get("couverture"))

    def clean_fichier(self):
        fichier = self.cleaned_data.get("fichier")
        if fichier:
            nom = fichier.name.lower()
            if not nom.endswith(EXTENSIONS_LIVRE):
                raise ValidationError("Format non pris en charge (PDF, EPUB, DOC, DOCX ou TXT).")
            if getattr(fichier, "size", 0) > TAILLE_MAX_LIVRE:
                raise ValidationError("Le fichier est trop lourd (50 Mo maximum).")
        return fichier
