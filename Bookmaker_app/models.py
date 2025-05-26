from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from decimal import Decimal

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
    name = models.CharField(max_length=250)
    datetime = models.DateField()
    dyscyplina = models.ForeignKey(Dyscyplina, on_delete=models.CASCADE)
    druzyna1 = models.ForeignKey(Drużyna, on_delete=models.CASCADE,related_name='druzyna1')
    druzyna2 = models.ForeignKey(Drużyna, on_delete=models.CASCADE,related_name="druzyna2")
    status = models.CharField(max_length=50)
    wynik_druzyna1 = models.CharField(max_length=50)
    wynik_druzyna2 = models.CharField(max_length=50)
    kurs_druzyna1 = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    kurs_druzyna2 = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    def __str__(self):
        return f"Event {self.id}, wynik {self.druzyna1}: {self.wynik_druzyna1} - {self.wynik_druzyna2}: {self.druzyna2}"


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
    wytypowany = models.CharField(max_length=100)
    #wygrana = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    @property
    def wygrana(self):
        if self.wartosc and self.kurs:
            return self.wartosc * self.kurs
        return Decimal('0.00')


    def __str__(self):
        return f"Zakład {self.id} użytkownika {self.user.username}"




class HistoriaTransakcji(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    wartosc = models.DecimalField(max_digits=10, decimal_places=2)
    typ = models.CharField(max_length=50)
    opis = models.CharField(max_length=255)
    stworzono = models.DateTimeField(auto_now_add=True)