from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLogin, KwotaForm
from django.shortcuts import render, get_object_or_404
from .models import Dyscyplina, Event


from .models import *

def home(request):
    najblizsze_mecze = Event.objects.filter(datetime__gte=date.today()).order_by('datetime')[:5]
    dyscypliny = Dyscyplina.objects.exclude(name__isnull=True).exclude(name__exact='').order_by('name')
    return render(request, 'Bookmaker_app/home.html', {
        'najblizsze_mecze': najblizsze_mecze,
        'dyscypliny': dyscypliny,
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_panel')
    else:
        form = CustomUserCreationForm()
    return render(request, 'bookmaker_app/register_form.html', {'form': form})


def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'user_panel'
    if request.method == 'POST':
        form = CustomLogin(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(next_url)
            else:
                form.add_error(None, "Niepoprawna nazwa uzytkownika lub haslo")
    else:
        form = CustomLogin()
    return render(request, 'bookmaker_app/login.html', {'form': form, 'next' : next_url})

@login_required(login_url='login')
def user_panel(request):
    zaklady = ZakladyUzytkownika.objects.filter(user=request.user)
    transakcje = HistoriaTransakcji.objects.filter(user=request.user)
    modal_message = request.session.pop('modal_message', None)
    return render(request, 'bookmaker_app/user_panel.html', {
        'zaklady': zaklady,
        'transakcje': transakcje,
        'saldo': request.user.saldo,
        'modal_message': modal_message,
        'dyscypliny': Dyscyplina.objects.exclude(name__isnull=True).exclude(name__exact='').order_by('name'),
    })


def dyscyplina(request, nazwa):
    template_name = 'bookmaker_app/dyscyplina.html'

    # Pobieramy dyscyplinę po nazwie
    dyscyplina_obj = get_object_or_404(Dyscyplina, name=nazwa)

    # Pobieramy wydarzenia powiązane z tą dyscypliną
    wydarzenia = Event.objects.filter(dyscyplina=dyscyplina_obj)

    return render(request, template_name, {
        'nazwa': nazwa,
        'wydarzenia': wydarzenia,
        'dyscypliny': Dyscyplina.objects.exclude(name__isnull=True).exclude(name__exact='').order_by('name')
    })
# def zaklady_uzytkownika(request, user):
#     template_name = f'bookmaker_app/{user}_bets.html'
#     zaklady =


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def wplata(request):
    form = KwotaForm(request.POST or None)
    if form.is_valid():
        kwota = form.cleaned_data['kwota']
        request.user.saldo += kwota
        request.user.save()

        # Dodaj do historii
        HistoriaTransakcji.objects.create(
            user=request.user,
            wartosc=kwota,
            typ='Wpłata',
            opis=f"Wpłata środków: {kwota} zł"

        )

        request.session['modal_message'] = f'Wpłacono {kwota} zł.'
        return redirect('user_panel')
    return render(request, 'bookmaker_app/wplata.html', {
        'form': form,
        'dyscypliny': Dyscyplina.objects.exclude(name__isnull=True).exclude(name__exact='').order_by('name'),
    })

@login_required
def wyplata(request):
    form = KwotaForm(request.POST or None)
    if form.is_valid():
        kwota = form.cleaned_data['kwota']
        if request.user.saldo >= kwota:
            request.user.saldo -= kwota
            request.user.save()

            # Dodaj do historii
            HistoriaTransakcji.objects.create(
                user=request.user,
                wartosc=kwota,
                typ='Wypłata',
                opis=f"Wypłata środków: {kwota} zł"
            )

            request.session['modal_message'] = f'Wypłacono {kwota} zł.'
            return redirect('user_panel')
        else:
            request.session['modal_message'] = 'Nie masz wystarczająco środków.'
    return render(request, 'bookmaker_app/wyplata.html', {
        'form': form,
        'dyscypliny': Dyscyplina.objects.exclude(name__isnull=True).exclude(name__exact='').order_by('name'),
    })