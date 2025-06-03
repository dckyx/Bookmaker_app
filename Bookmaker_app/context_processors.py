from .models import Kategoria, Dyscyplina

def global_kategorie_dyscypliny(request):
    kategorie = Kategoria.objects.prefetch_related('dyscyplina_set').all()
    dyscypliny = Dyscyplina.objects.exclude(name__isnull=True).exclude(name__exact='').order_by('name')
    aktywne = []
    if request.user.is_authenticated:
        aktywne = request.user.zakladyuzytkownika_set.filter(wynik='w trakcie').order_by('-stworzono')
    return {
        'kategorie': kategorie,
        'dyscypliny': dyscypliny,
        'active_bets': aktywne
    }