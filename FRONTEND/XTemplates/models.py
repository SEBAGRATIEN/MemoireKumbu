from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Profil(models.Model):
    """
    Informations complémentaires du compte utilisateur.
    """

    utilisateur = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profil"
    )

    post_nom = models.CharField(max_length=100, blank=True)
    prenom = models.CharField(max_length=100, blank=True)

    photo = models.ImageField(
        upload_to="profils/",
        blank=True,
        null=True
    )

    biographie = models.TextField(blank=True)

    etablissement = models.CharField(
        max_length=200,
        blank=True
    )

    filiere = models.CharField(
        max_length=200,
        blank=True
    )

    niveau = models.CharField(
        max_length=100,
        blank=True
    )

    annee_academique = models.CharField(
        max_length=50,
        blank=True
    )

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.utilisateur.get_full_name() or self.utilisateur.username


class Categorie(models.Model):
    """
    Catégories utilisées pour organiser les livres et ressources.
    """

    nom = models.CharField(
        max_length=150,
        unique=True
    )

    description = models.TextField(blank=True)

    slug = models.SlugField(
        max_length=180,
        unique=True
    )

    active = models.BooleanField(default=True)

    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class Livre(models.Model):
    """
    Livre ou document disponible dans KUMBU.
    """

    titre = models.CharField(max_length=255)

    auteur = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="livres"
    )

    couverture = models.ImageField(
        upload_to="livres/couvertures/",
        blank=True,
        null=True
    )

    fichier = models.FileField(
        upload_to="livres/fichiers/",
        blank=True,
        null=True
    )

    isbn = models.CharField(
        max_length=50,
        blank=True
    )

    date_publication = models.DateField(
        blank=True,
        null=True
    )

    nombre_pages = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    langue = models.CharField(
        max_length=50,
        default="Français"
    )

    publie = models.BooleanField(default=False)

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre


class LivreLu(models.Model):
    """
    Livres consultés/lus par un utilisateur.
    """

    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="livres_lus"
    )

    livre = models.ForeignKey(
        Livre,
        on_delete=models.CASCADE,
        related_name="lectures"
    )

    date_debut = models.DateTimeField(
        auto_now_add=True
    )

    derniere_lecture = models.DateTimeField(
        auto_now=True
    )

    progression = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    termine = models.BooleanField(default=False)

    class Meta:
        unique_together = ("utilisateur", "livre")

    def __str__(self):
        return f"{self.utilisateur.username} - {self.livre.titre}"


class LivreSauvegarde(models.Model):
    """
    Livres sauvegardés par les utilisateurs.
    """

    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="livres_sauvegardes"
    )

    livre = models.ForeignKey(
        Livre,
        on_delete=models.CASCADE,
        related_name="sauvegardes"
    )

    date_sauvegarde = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("utilisateur", "livre")

    def __str__(self):
        return f"{self.utilisateur.username} - {self.livre.titre}"


class Question(models.Model):
    """
    Question posée par un utilisateur à l'assistant KUMBU.
    """

    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    livre = models.ForeignKey(
        Livre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="questions"
    )

    texte = models.TextField()

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.texte[:80]


class Reponse(models.Model):
    """
    Réponse de l'assistant à une question.
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="reponses"
    )

    texte = models.TextField()

    est_ia = models.BooleanField(
        default=True
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.texte[:80]


class RessourceApprentissage(models.Model):
    """
    Cours, support ou autre matériel d'apprentissage.
    """

    titre = models.CharField(max_length=255)

    description = models.TextField()

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ressources"
    )

    fichier = models.FileField(
        upload_to="apprentissage/",
        blank=True,
        null=True
    )

    lien = models.URLField(
        blank=True
    )

    auteur = models.CharField(
        max_length=255,
        blank=True
    )

    publie = models.BooleanField(
        default=False
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    date_modification = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.titre


class MessageContact(models.Model):
    """
    Messages envoyés depuis la page Contact.
    """

    nom = models.CharField(max_length=150)

    email = models.EmailField()

    message = models.TextField()

    lu = models.BooleanField(default=False)

    date_envoi = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.nom} - {self.email}"


class Etablissement(models.Model):
    """
    Établissement d'enseignement supérieur.
    """

    nom = models.CharField(
        max_length=255,
        unique=True
    )

    ville = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    actif = models.BooleanField(
        default=True
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nom


class Promotion(models.Model):
    """
    Promotion académique liée à un établissement.
    """

    etablissement = models.ForeignKey(
        Etablissement,
        on_delete=models.CASCADE,
        related_name="promotions"
    )

    nom = models.CharField(
        max_length=150
    )

    annee_academique = models.CharField(
        max_length=50
    )

    description = models.TextField(
        blank=True
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.nom} - {self.etablissement.nom}"


class MembrePromotion(models.Model):
    """
    Liaison entre un étudiant et une promotion.
    """

    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="promotions"
    )

    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name="membres"
    )

    identifiant_annuel = models.CharField(
        max_length=100,
        blank=True
    )

    date_inscription = models.DateTimeField(
        auto_now_add=True
    )

    actif = models.BooleanField(
        default=True
    )

    class Meta:
        unique_together = (
            "utilisateur",
            "promotion"
        )

    def __str__(self):
        return f"{self.utilisateur.username} - {self.promotion}"


class SupportPromotion(models.Model):
    """
    Cours et supports accessibles à une promotion.
    """

    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name="supports"
    )

    titre = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    fichier = models.FileField(
        upload_to="supports_promotions/",
        blank=True,
        null=True
    )

    lien = models.URLField(
        blank=True
    )

    publie = models.BooleanField(
        default=False
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.titre