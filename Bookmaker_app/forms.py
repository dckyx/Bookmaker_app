
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

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

class ZakladForm(forms.Form):
    wartosc = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=1,
        label='Wartość zakładu',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )