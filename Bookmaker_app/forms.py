from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
import logging
logger = logging.getLogger(__name__)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class CustomLogin(AuthenticationForm):
    username = forms.CharField(label='Nazwa uzytkownik',max_length=50)
    password = forms.CharField(label='Haslo',widget=forms.PasswordInput)

from django import forms

class KwotaForm(forms.Form):
    kwota = forms.DecimalField(label="Kwota (zł)", min_value=0.01, max_digits=10, decimal_places=2)

    def clean_kwota(self):
        kwota = self.cleaned_data['kwota']
        if kwota > 100000:
            logger.warning(f"Bardzo duża wpłata {kwota}")
        return kwota

class ZakladForm(forms.Form):
    wartosc = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=1,
        label='Wartość zakładu',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    wytypowany = forms.IntegerField(widget=forms.HiddenInput())
    kurs = forms.DecimalField(widget=forms.HiddenInput())