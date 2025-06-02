from django.core.management.base import BaseCommand
from Bookmaker_app.models import Event

class Command(BaseCommand):
    help = 'Aktualizuje statusy wszystkich wydarzeń'

    def handle(self, *args, **kwargs):
        events = Event.objects.all()
        updated = 0
        for event in events:
            old_status = event.status
            event.aktualizuj_status()
            if event.status != old_status:
                updated += 1

        self.stdout.write(self.style.SUCCESS(f'Zaktualizowano statusy {updated} wydarzeń.'))
