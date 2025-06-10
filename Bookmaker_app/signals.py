from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, ZakladyUzytkownika

import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Event)
def rozlicz_zaklady_po_zakonczeniu_eventu(sender, instance, created, **kwargs):
    if instance.status == 'zakonczony':
        zaklady = ZakladyUzytkownika.objects.filter(event1=instance, wynik='w trakcie')

        if not zaklady.exists():
            logger.info(f'Brak zakładów do rozliczenia dla eventu {instance.id} - {instance.name}')
            return

        logger.info(f'Rozpoczynam rozliczanie {zaklady.count()} zakładów dla eventu {instance.id} - {instance.name}')

        for zaklad in zaklady:
            try:
                zaklad.rozlicz()
                logger.info(f'Zakład {zaklad.id} użytkownika {zaklad.user} rozliczony.')
            except Exception as e:
                logger.error(f'Błąd przy rozliczaniu zakładu {zaklad.id}: {e}')
