from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser
from .models import *




admin.site.register(ZakladyUzytkownika)
admin.site.register(HistoriaTransakcji)
admin.site.register(Kategoria)
admin.site.register(Stream)

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
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'saldo')
    list_filter = ('is_staff', 'is_active', 'saldo')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username', 'email', 'first_name', 'last_name')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'datetime', 'dyscyplina','druzyna1','druzyna2','status','wynik_druzyna1','wynik_druzyna2')
    list_filter = ('name','datetime','status')
    search_fields = ('name','datetime','dyscyplina','druzyna1','druzyna2','status')
    ordering = ('datetime','status')