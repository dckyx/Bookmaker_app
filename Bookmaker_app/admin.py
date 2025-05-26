from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission






# Register your models here.

@admin.register(Drużyna)
class DruzynaAdmin(admin.ModelAdmin):
    list_display = ('name', 'dyscyplina')  # <-- dodana kolumna
    list_filter = ('dyscyplina',)           # <-- filtr z boku
    search_fields = ('name',)              # <-- wyszukiwarka
    ordering = ('dyscyplina', 'name')      # <-- sortowanie

@admin.register(Dyscyplina)
class DyscyplinaAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'saldo')
    list_filter = ('is_staff', 'is_active', 'saldo')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username', 'email', 'first_name', 'last_name')
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Dane osobowe', {'fields': ('first_name', 'last_name', 'saldo')}),
        ('Uprawnienia', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions')}
         ),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'datetime', 'dyscyplina','druzyna1','druzyna2','status','wynik_druzyna1','wynik_druzyna2')
    list_filter = ('name','datetime','status')
    search_fields = ('name','datetime','dyscyplina','druzyna1','druzyna2','status')
    ordering = ('datetime','status')

@admin.register(Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('name',)

@admin.register(ZakladyUzytkownika)
class ZakladyUzytkownikaAdmin(admin.ModelAdmin):
    list_display = ('user','wartosc','wynik')
    search_fields = ('user','wartosc','wynik')
    ordering = ('user','wartosc','wynik')
    list_filter = ('user','wartosc','wynik')

# admin.site.register(HistoriaTransakcji)

@admin.register(HistoriaTransakcji)
class HistoriaTransakcjiAdmin(admin.ModelAdmin):
    list_display = ('user','wartosc','typ','opis')
    search_fields = ('user','wartosc','typ','opis')
    ordering = ('user','wartosc','typ','opis')
    list_filter = ('user','wartosc','typ','opis')



# admin.site.register(Stream)
@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('event','platforma','url')
    search_fields = ('event','platforma','url')
    ordering = ('event','platforma','url')
    list_filter = ('event','platforma')