from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# Create your models here.

class Profil(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil")
    post_nom = models.CharField(max_length=100, blank=True)
    prenom = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to="staticfiles/models/profils/", blank=True, null=True)
    biographie = models.TextField(blank=True)
    etablissement = models.CharField(max_length=200, blank=True)
    filiere = models.CharField(max_length=200, blank=True)
    niveau = models.CharField(max_length=100, blank=True)
    annee_academique = models.CharField(max_length=50, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.utilisateur.get_full_name() or self.utilisateur.username

    @property
    def nom_complet(self):
        """Nom + post-nom + prénom si renseignés, sinon nom complet / identifiant du compte."""
        parties = [self.utilisateur.last_name, self.post_nom, self.prenom]
        nom = " ".join(p for p in parties if p).strip()
        return nom or self.utilisateur.get_full_name() or self.utilisateur.username

    @property
    def initiales(self):
        mots = self.nom_complet.replace(".", " ").split()
        return "".join(m[0] for m in mots[:2]).upper() or "K"

    @property
    def photo_url(self):
        """URL de la photo de profil, ou chaîne vide (le gabarit affiche alors une icône)."""
        if self.photo:
            try:
                return self.photo.url
            except ValueError:
                pass
        return ""

    @property
    def a_une_photo(self):
        return bool(self.photo)

class Categorie(models.Model):
    nom = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=180, unique=True)
    active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nom

class Livre(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    categorie = models.ForeignKey( Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name="livres")
    couverture = models.ImageField(upload_to="staticfiles/models/livres/couvertures/", blank=True,  null=True)
    fichier = models.FileField(upload_to="staticfiles/models/livres/fichiers/", blank=True, null=True)
    isbn = models.CharField(max_length=50, blank=True)
    date_publication = models.DateField(blank=True, null=True)
    nombre_pages = models.PositiveIntegerField(blank=True, null=True)
    langue = models.CharField(max_length=50, default="Français")
    publie = models.BooleanField(default=False)
    ajoute_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="livres_ajoutes")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.titre

    @property
    def variante_couverture(self):
        """1 à 4 : couleur de la couverture par défaut (affichée quand il n'y a pas d'image)."""
        return (self.pk or 0) % 4 + 1

class LivreLu(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="livres_lus")
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name="lectures")
    date_debut = models.DateTimeField(auto_now_add=True)
    derniere_lecture = models.DateTimeField(auto_now=True)
    progression = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    termine = models.BooleanField(default=False)
    class Meta:
        unique_together = ("utilisateur", "livre")
    def __str__(self):
        return f"{self.utilisateur.username} - {self.livre.titre}"

class LivreSauvegarde(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="livres_sauvegardes")
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name="sauvegardes")
    date_sauvegarde = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("utilisateur", "livre")
    def __str__(self):
        return f"{self.utilisateur.username} - {self.livre.titre}"

class Question(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    livre = models.ForeignKey(Livre, on_delete=models.SET_NULL, null=True, blank=True, related_name="questions")
    texte = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.texte[:80]

class Reponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="reponses")
    texte = models.TextField()
    est_ia = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texte[:80]

class RessourceApprentissage(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name="ressources")
    fichier = models.FileField(upload_to="staticfiles/models/apprentissage/", blank=True, null=True)
    lien = models.URLField(blank=True)
    auteur = models.CharField(max_length=255, blank=True)
    publie = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.titre

class MessageContact(models.Model):
    nom = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    lu = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.nom} - {self.email}"

class Etablissement(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    ville = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nom

class Promotion(models.Model):
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE,related_name="promotions")
    nom = models.CharField(max_length=150)
    annee_academique = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.nom} - {self.etablissement.nom}"
 
class MembrePromotion(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="promotions")
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name="membres")
    identifiant_annuel = models.CharField(max_length=100, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)
    class Meta:
        unique_together = ("utilisateur", "promotion")
    def __str__(self):
        return f"{self.utilisateur.username} - {self.promotion}"

class SupportPromotion(models.Model):
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE,related_name="supports")
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    fichier = models.FileField(upload_to="staticfiles/models/supports_promotions/", blank=True, null=True)
    lien = models.URLField(blank=True)
    publie = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titre


class Publication(models.Model):
    """Actualité affichée dans le profil (comme le fil d'un profil Facebook)."""
    TYPE_PUBLICATION = "publication"
    TYPE_PHOTO_PROFIL = "photo_profil"
    TYPES = [
        (TYPE_PUBLICATION, "Publication"),
        (TYPE_PHOTO_PROFIL, "Nouvelle photo de profil"),
    ]
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="publications")
    type = models.CharField(max_length=20, choices=TYPES, default=TYPE_PUBLICATION)
    texte = models.TextField(blank=True)
    image = models.ImageField(upload_to="staticfiles/models/publications/", blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return f"{self.auteur.username} - {self.get_type_display()} - {self.date_creation:%d/%m/%Y}"
