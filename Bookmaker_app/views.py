import os
from datetime import date, datetime, time
from random import choice

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .forms import CustomUserCreationForm, CustomLogin, KwotaForm, ZakladForm
from django.shortcuts import render, get_object_or_404
from .models import Dyscyplina, Event
from .serializers import *
from .models import *
from .utils import przelicz_i_zapisz_kursy
import logging

logger = logging.getLogger('bookmaker')



def home(request):
    najblizsze_mecze = Event.objects.filter(datetime__gte=timezone.now()).exclude(status='zakonczony').order_by('datetime')[:5]
    return render(request, 'bookmaker_app/home.html', {
        'najblizsze_mecze': najblizsze_mecze,
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f"Zarejestrowano nowego użytkownika: {form.cleaned_data.get('username')}")
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
            logger.info(f"Użytkownik {username} zalogował się.")

            if user is not None:
                login(request, user)
                return redirect(next_url)
            else:
                form.add_error(None, "Niepoprawna nazwa użytkownika lub hasło")
                logger.warning(f"Nieudane logowanie dla użytkownika: {username}")
    else:
        form = CustomLogin()

    return render(request, 'bookmaker_app/login.html', {
        'form': form,
        'next': next_url
    })
@login_required(login_url='login')
def user_panel(request):
    zaklady = ZakladyUzytkownika.objects.filter(user=request.user)
    transakcje = HistoriaTransakcji.objects.filter(user=request.user)
    modal_message = request.session.pop('modal_message', None)
    for z in zaklady:
        z.potencjalna_wygrana = round(z.wartosc * z.kurs, 2)
    return render(request, 'bookmaker_app/user_panel.html', {
        'zaklady': zaklady,
        'transakcje': transakcje,
        'saldo': request.user.saldo,
        'modal_message': modal_message,
    })


def dyscyplina(request, nazwa):
    template_name = 'bookmaker_app/dyscyplina.html'

    # Pobieramy dyscyplinę po nazwie
    dyscyplina_obj = get_object_or_404(Dyscyplina, name=nazwa)

    wydarzenia = Event.objects.filter(
        datetime__gte=date.today(),
        dyscyplina=dyscyplina_obj
    ).exclude(status='zakonczony').order_by('datetime')

    return render(request, template_name, {
        'nazwa': nazwa,
        'wydarzenia': wydarzenia,
    })
# def zaklady_uzytkownika(request, user):
#     template_name = f'Bookmaker_app/{user}_bets.html'
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
        logger.info(f"Użytkownik {request.user.username} wpłacił {kwota} zł.")

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
    })

@login_required
def wyplata(request):
    form = KwotaForm(request.POST or None)
    if form.is_valid():
        kwota = form.cleaned_data['kwota']
        if request.user.saldo >= kwota:
            request.user.saldo -= kwota
            request.user.save()
            logger.info(f"Użytkownik {request.user.username} wypłacił {kwota} zł.")


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
            logger.warning(
                f"Użytkownik {request.user.username} próbował wypłacić {kwota} zł, ale nie miał wystarczających środków.")

    return render(request, 'bookmaker_app/wyplata.html', {
        'form': form,
    })
def spin_react(request):
    return render(request, 'bookmaker_app/spin_react.html', {
    })

class FrontendAppView(TemplateView):
    template_name = "index.html"

def get_template_names(self):
    return [os.path.join(settings.REACT_BUILD_DIR, 'index.html')]

@api_view(['GET'])
def get_dyscypliny(request):
    dyscypliny = Dyscyplina.objects.all().order_by('name')
    serializer = DyscyplinaSerializer(dyscypliny, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_kategorie(request):
    kategorie = Kategoria.objects.all().order_by('name')
    serializer = KategoriaSerializer(kategorie, many=True)
    return Response(serializer.data)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Użytkownik zarejestrowany pomyślnie."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ZakladyUzytkownikaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        zaklady = ZakladyUzytkownika.objects.filter(user=request.user)
        serializer = ZakladUzytkownikaSerializer(zaklady, many=True)
        return Response(serializer.data)


@login_required
def obstaw_mecz(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = ZakladForm(request.POST)
        if form.is_valid():
            wartosc = form.cleaned_data['wartosc']
            kurs = form.cleaned_data['kurs']
            wytypowany = form.cleaned_data['wytypowany']
            from .models import Drużyna
            wytypowany = Drużyna.objects.get(pk=wytypowany)

            if request.user.saldo >= wartosc:
                ZakladyUzytkownika.objects.create(
                    user=request.user,
                    wartosc=wartosc,
                    wynik='w trakcie',
                    kurs=kurs,
                    event1=event,
                    wytypowany=wytypowany
                )
                request.user.saldo -= wartosc
                request.user.save()

                HistoriaTransakcji.objects.create(
                    user=request.user,
                    wartosc=wartosc,
                    typ='Zakład',
                    opis=f'Obstawienie meczu: {event.name}'
                )

                request.session['modal_message'] = 'Zakład został obstawiony.'
                logger.info(
                    f"Użytkownik {request.user.username} obstawił mecz {event.name} na drużynę {wytypowany.name}, kwota: {wartosc} zł, kurs: {kurs}.")
                przelicz_i_zapisz_kursy(event)
                return redirect('user_panel')
            else:
                form.add_error(None, 'Nie masz wystarczającej ilości środków.')
                return render(request, 'bookmaker_app/obstaw.html', {
                    'form': form,
                    'event': event,
                    'saldo_niewystarczajace': True
                })
    else:
        form = ZakladForm()

    return render(request, 'bookmaker_app/obstaw.html', {
        'form': form,
        'event': event
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def spin_api(request):
    user = request.user
    today = timezone.now().date()

    # Sprawdzenie, czy użytkownik już dziś losował
    if HistoriaTransakcji.objects.filter(user=user, typ='Spin', stworzono__date=today).exists():
        logger.info(f"Spin API – użytkownik: {user.username} już dziś kręcił.")
        ostatni_spin = HistoriaTransakcji.objects.filter(user=user, typ='Spin', stworzono__date=today).first()
        return Response({
            'result': float(ostatni_spin.wartosc),
            'message': 'already'
        }, status=200)

    # Losowanie nagrody
    prize_options = [0, 2, 5, 10, 20]
    result = choice(prize_options)

    # Aktualizacja salda użytkownika tylko jeśli wynik > 0
    if result > 0:
        user.saldo += result
        user.save()
        opis = f'Dzienna nagroda: {result} zł'
    else:
        opis = 'Dzienna próba: 0 zł'

    # Zapis do historii transakcji
    HistoriaTransakcji.objects.create(
        user=user,
        wartosc=result,
        typ='Spin',
        opis=opis
    )

    logger.info(f"Spin API – użytkownik: {user.username}, wynik: {result} zł")

    return Response({
        'result': result,
        'message': 'success'
    })

    if result > 0:
        user.saldo += result
        user.save()

    return Response({
        'result': result,
        'message': 'success'
    }, status=200)


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)
