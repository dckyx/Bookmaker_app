from django.core.management.base import BaseCommand
from Bookmaker_app.models import Event, ZakladyUzytkownika

class Command(BaseCommand):
    help = 'Rozlicza wszystkie zakłady powiązane z zakończonymi wydarzeniami'

    def handle(self, *args, **kwargs):
        zakonczone_eventy = Event.objects.filter(status='zakonczony')

        licznik = 0
        for event in zakonczone_eventy:
            if not event.wynik_druzyna1 or not event.wynik_druzyna2:
                continue  # pomiń jeśli brakuje wyników

            zaklady = ZakladyUzytkownika.objects.filter(event1=event, wynik='w trakcie')
            for zaklad in zaklady:
                zaklad.rozlicz()
                licznik += 1

        self.stdout.write(f"Rozliczono {licznik} zakładów.")
