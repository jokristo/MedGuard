from django.http import HttpResponse

def home_view(request):
    return HttpResponse("<h1>Bienvenue sur MedGuard!</h1><p>Ceci est la page d'accueil.</p>")