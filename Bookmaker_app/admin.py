from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser
from .models import *




admin.site.register(CustomUser)
admin.site.register(ZakladyUzytkownika)
admin.site.register(HistoriaTransakcji)
admin.site.register(Kategoria)
admin.site.register(Dyscyplina)
admin.site.register(Drużyna)
admin.site.register(Event)
admin.site.register(Stream)

# Register your models here.
