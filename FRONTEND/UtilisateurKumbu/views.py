from django.shortcuts import render, redirect

# Create your views here.
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
