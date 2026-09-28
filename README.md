# Kumbu

**Kumbu** est une plateforme numérique conçue pour les étudiants, les apprenants et les chercheurs. Elle permet de sauvegarder et de partager des livres, de les retrouver facilement, et de poser des questions à un assistant d'intelligence artificielle pour approfondir sa lecture.

Kumbu s'ouvre aussi aux établissements d'enseignement supérieur : chaque université ou institut dispose d'un espace dédié où chaque promotion accède à ses propres cours, notes et supports.

Le projet est développé avec **Python** et **Django**.

---

## Sommaire

1. [Fonctionnalités](#fonctionnalités)
2. [Types d'utilisateurs](#types-dutilisateurs)
3. [Technologies](#technologies)
4. [Installation](#installation)
5. [Structure du projet](#structure-du-projet)
6. [Template front-end](#template-front-end)
7. [Feuille de route](#feuille-de-route)
8. [Auteur](#auteur)

---

## Fonctionnalités

### Pour tout le monde (utilisateur simple)

- Inscription et connexion (nom, post-nom, prénom, mot de passe confirmé)
- Recherche et consultation de livres
- Assistant IA pour poser des questions sur un livre ou un sujet
- Espace d'apprentissage : faire connaissance avec d'autres utilisateurs et échanger des messages
- Publication de livres (soumise à l'approbation du super-administrateur)
- Profil : photo, informations personnelles, changement de mot de passe, changement de thème, liste des livres lus
- Page d'accueil : À propos, Contact, Assistant IA, moteur de recherche, nouveaux inscrits, actualités (derniers livres publiés)

### Espace étudiant (établissement)

- Connexion via le lien « Se connecter en tant qu'étudiant »
- Parcours d'inscription : choix de l'établissement, choix de la faculté, saisie de l'ID étudiant, création du compte
- Espace réservé à la promotion : chaque promotion voit uniquement ses propres cours, notes, PDF et supports (un étudiant de L1 n'accède pas aux données de L3)
- Accès à toutes les fonctionnalités de l'utilisateur simple
- L'ID étudiant apparaît sur le profil

### Administration

- Le super-administrateur génère les ID étudiants (valables une année académique)
- Le super-administrateur approuve ou refuse les livres publiés avant leur mise en ligne
- Gestion des établissements, facultés et promotions

---

## Types d'utilisateurs

| Type | Accès |
|------|-------|
| Utilisateur simple | Livres, recherche, assistant IA, espace d'apprentissage, profil |
| Étudiant | Tout ce qui précède + espace de sa promotion (cours, notes, supports) |
| Super-administrateur | Génération des ID, approbation des livres, gestion des établissements |

---

## Technologies

- **Backend** : Python 3, Django
- **Base de données** : SQLite en développement (PostgreSQL recommandé en production)
- **Front-end** : HTML, CSS, JavaScript (template statique fourni, à intégrer dans les templates Django)
- **Assistant IA** : appel à une API d'IA côté serveur (à connecter)

---

## Installation

### 1. Cloner le projet

```bash
git clone <url-du-depot>
cd kumbu
```

### 2. Créer et activer un environnement virtuel

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Si le fichier `requirements.txt` n'existe pas encore :

```bash
pip install django pillow
pip freeze > requirements.txt
```

`pillow` est nécessaire pour les photos de profil et les couvertures de livres.

### 4. Appliquer les migrations

```bash
python manage.py migrate
```

### 5. Créer le super-administrateur

```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur

```bash
python manage.py runserver
```

Le site est accessible sur `http://127.0.0.1:8000/` et l'administration sur `http://127.0.0.1:8000/admin/`.

---

## Structure du projet

Structure proposée (à adapter à l'organisation réelle du dépôt) :

```
kumbu/
├── manage.py
├── requirements.txt
├── README.md
├── kumbu/                  # Configuration du projet (settings, urls, wsgi)
├── comptes/                # Inscription, connexion, profil, ID étudiants
├── livres/                 # Livres, recherche, publication et approbation
├── etablissements/         # Établissements, facultés, promotions, cours
├── assistant/              # Assistant IA (questions / réponses)
├── templates/              # Templates HTML (base.html, accueil, connexion…)
│   ├── base.html
│   ├── accueil.html
│   ├── apropos.html
│   ├── contact.html
│   ├── connexion.html
│   └── profil.html
├── static/
│   ├── css/style.css
│   └── js/script.js
└── media/                  # Fichiers envoyés (photos, PDF, couvertures)
```

---

## Template front-end

Le template statique fournit toutes les pages grand public dans un seul fichier `index.html`, avec `style.css` et `script.js`.

Pour l'intégrer dans Django :

1. Placer `style.css` et `script.js` dans `static/css/` et `static/js/`.
2. Découper chaque `<section id="page-...">` de `index.html` dans son propre template.
3. Créer un `base.html` avec l'en-tête, le pied de page et les balises suivantes :

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/script.js' %}"></script>
```

4. Remplacer la navigation par page (`data-page`) par de vrais liens `{% url '...' %}`.
5. Ajouter `{% csrf_token %}` dans chaque formulaire.

Le template inclut un bouton de changement de thème (clair / sombre) et un menu hamburger pour les petits écrans.

---

## Feuille de route

- [ ] Modèles Django : utilisateur, établissement, faculté, promotion, cours, livre
- [ ] Génération sécurisée des ID étudiants par le super-administrateur
- [ ] Espace étudiant : cours, notes, supports PDF par promotion
- [ ] Publication de livres avec validation par le super-administrateur
- [ ] Moteur de recherche de livres
- [ ] Connexion de l'assistant IA
- [ ] Messagerie entre amis
- [ ] Ouverture à l'ensemble des établissements universitaires de la RDC

---

## Auteur

**Nzayituriki Habyarimana Gracieux**
Étudiant en L1 — Réseaux et Télécommunications

© 2026 Kumbu — Tous droits réservés
