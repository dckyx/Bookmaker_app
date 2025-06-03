from decimal import Decimal

from django.db.models import Sum

from Bookmaker_app.models import ZakladyUzytkownika


def przelicz_i_zapisz_kursy(event):
    zaklady = ZakladyUzytkownika.objects.filter(event1=event)
    suma1 = zaklady.filter(wytypowany=event.druzyna1).aggregate(Sum('wartosc'))['wartosc__sum'] or Decimal('0.00')
    suma2 = zaklady.filter(wytypowany=event.druzyna2).aggregate(Sum('wartosc'))['wartosc__sum'] or Decimal('0.00')

    if suma1 > suma2:
        event.kurs_druzyna1 += Decimal('0.10')
        event.kurs_druzyna2 = max(event.kurs_druzyna2 - Decimal('0.10'), Decimal('1.01'))
    elif suma2 > suma1:
        event.kurs_druzyna2 += Decimal('0.10')
        event.kurs_druzyna1 = max(event.kurs_druzyna1 - Decimal('0.10'), Decimal('1.01'))

    event.save()