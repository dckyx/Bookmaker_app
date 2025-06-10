from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('zaklady.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email



class Kategoria(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return f"Kategoria: {self.name}"

class Dyscyplina(models.Model):
    name = models.CharField(max_length=250)
    kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE)

    def __str__(self):
        return f"Dyscyplina: {self.name}"

class Drużyna(models.Model):
    name = models.CharField(max_length=250)
    dyscyplina = models.ForeignKey(Dyscyplina, on_delete=models.CASCADE)

    def __str__(self):
        return f"Drużyna {self.name}"


class Event(models.Model):
    STATUSY = (
        ('nadchodzacy', 'Nadchodzący'),
        ('trwa', 'Trwa'),
        ('zakonczony', 'Zakończony'),
    )

    name = models.CharField(max_length=250)
    datetime = models.DateTimeField()
    dyscyplina = models.ForeignKey(Dyscyplina, on_delete=models.CASCADE)
    druzyna1 = models.ForeignKey(Drużyna, on_delete=models.CASCADE, related_name='druzyna1')
    druzyna2 = models.ForeignKey(Drużyna, on_delete=models.CASCADE, related_name='druzyna2')
    status = models.CharField(max_length=20, choices=STATUSY, default='nadchodzacy')
    wynik_druzyna1 = models.CharField(max_length=50)
    wynik_druzyna2 = models.CharField(max_length=50)
    kurs_druzyna1 = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    kurs_druzyna2 = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    def __str__(self):
        return f"Event {self.id}, wynik {self.druzyna1}: {self.wynik_druzyna1} - {self.wynik_druzyna2}: {self.druzyna2}"

    @property
    def is_future(self):
        return self.datetime > timezone.now()

    @property
    def is_live(self):
        now = timezone.now()
        return self.datetime <= now < self.datetime + timedelta(hours=2)

    @property
    def is_finished(self):
        return timezone.now() > self.datetime + timedelta(hours=2)

    def aktualizuj_status(self):
        teraz = timezone.now()

        if self.is_future:
            self.status = "nadchodzacy"
        elif self.is_live:
            self.status = "trwa"
        else:
            self.status = "zakonczony"

        self.save()

class Stream(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    platforma = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return f"Stream {self.id} możesz obejrzeć na: {self.platforma} --- {self.url}"


class TypZakladu(models.Model):
    nazwa = models.CharField(max_length=100)

    def __str__(self):
        return f"Typ {self.nazwa}"


class OpcjeZakladu(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    typ = models.ForeignKey(TypZakladu, on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=100)
    szanse = models.DecimalField(max_digits=3, decimal_places=2)
    czy_zwyciezca = models.BooleanField(default=False)
    def __str__(self):
        return f"Opcja zakładu {self.id} typu {self.typ.name} o nazwie {self.nazwa} ma {self.szanse} procent szansy na wygranie"



class ZakladyUzytkownika(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #opcja_zakladu = models.ForeignKey(OpcjeZakladu, on_delete=models.CASCADE)
    wartosc = models.DecimalField(max_digits=10, decimal_places=2)
    wynik = models.CharField(max_length=100)
    stworzono = models.DateTimeField(auto_now_add=True)
    kurs = models.DecimalField(max_digits=10, decimal_places=2)
    event1 = models.ForeignKey(Event, on_delete=models.CASCADE)
    wytypowany = models.ForeignKey(Drużyna, on_delete=models.CASCADE)
    # wygrana = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    @property
    def wygrana(self):
        if self.wartosc and self.kurs:
            return self.wartosc * self.kurs
        return Decimal('0.00')

    def rozlicz(self):
        event = self.event1

        # Upewnij się, że wyniki są ustawione
        if event.wynik_druzyna1 is None or event.wynik_druzyna2 is None:
            return  # Nie rozliczaj jeszcze

        try:
            wynik1 = int(event.wynik_druzyna1)
            wynik2 = int(event.wynik_druzyna2)
        except ValueError:
            return  # Wyniki są nieprawidłowe (np. tekstowe)

        if wynik1 > wynik2:
            zwyciezca = event.druzyna1
        elif wynik2 > wynik1:
            zwyciezca = event.druzyna2
        else:
            zwyciezca = None  # Remis

        if zwyciezca == self.wytypowany:
            wygrana = self.wartosc * self.kurs
            self.user.saldo += wygrana
            self.user.save()
            self.wynik = 'wygrany'
            logger.info(f"Zakład {self.id} WYGRANY – użytkownik {self.user.username}, wygrana: {wygrana} zł")
        else:
            self.wynik = 'przegrany'
            logger.info(f"Zakład {self.id} PRZEGRANY – użytkownik {self.user.username}")

        self.save()
    def __str__(self):
        return f"Zakład {self.id} użytkownika {self.user.username}"




class HistoriaTransakcji(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    wartosc = models.DecimalField(max_digits=10, decimal_places=2)
    typ = models.CharField(max_length=50)
    opis = models.CharField(max_length=255)
    stworzono = models.DateTimeField(auto_now_add=True)