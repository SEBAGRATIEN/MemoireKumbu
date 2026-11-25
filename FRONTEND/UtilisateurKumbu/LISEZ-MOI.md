# KUMBU — mise à jour (icônes, profil, connexion)

Copiez les fichiers dans votre projet en gardant la même arborescence
(`models.py`, `forms.py`, `views.py`, `urls.py`, `templates/`, `static/`).

## 1. Important : vérifier que le NOUVEAU style est chargé
- Remplacez **tout** le dossier `static` (css, js, img) et **tout** le dossier `templates`.
- Supprimez l'ancien dossier `static/img/illustrations`, `static/img/avatars` et `static/img/books` s'ils existent :
  le site n'utilise plus de grandes images, seulement des icônes.
- Ouvrez `http://127.0.0.1:8000/static/css/style.css` : la première ligne doit contenir
  « version icônes ». Sinon, Django sert un autre dossier `static` (voir `STATICFILES_DIRS`).
- Dans le navigateur, faites **Ctrl + F5** pour vider le cache.

## 2. Commandes
```bash
pip install pillow
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## 3. settings.py
```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

## 4. Ce qui change
- **Icônes Bootstrap Icons** (chargées par CDN : connexion Internet nécessaire).
  Plus aucune grande illustration : couvertures de livres = bloc coloré + icône,
  profils sans photo = icône.
- **Photo de profil** : petit cercle ; un clic l'affiche en entier (Échap ou clic pour fermer).
  Une nouvelle photo apparaît aussi dans les actualités du profil.
- **Navigation** : barre flottante espacée ; menu « hamburger » dès 1200 px de large
  (les liens ne se chevauchent plus, même avec le zoom du navigateur).
- **Connexion** : deux volets, bouton Google refait, champs avec icônes, œil pour voir le mot de passe.
- **Contact** : le formulaire enregistre maintenant le message (modèle `MessageContact`, visible dans l'admin).
- **Profil** : Actualités, Informations, Mes livres publiés, Livres lus, Paramètres, Modifier le profil.
