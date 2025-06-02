from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, ZakladyUzytkownika

@receiver(post_save, sender=Event)
def rozlicz_zaklady_po_zakonczeniu_eventu(sender, instance, **kwargs):
    if instance.status == 'zakonczony':
        zaklady = ZakladyUzytkownika.objects.filter(event1=instance, wynik='w trakcie')
        for zaklad in zaklady:
            zaklad.rozlicz()
