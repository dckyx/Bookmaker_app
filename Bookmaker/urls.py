"""
URL configuration for Bookmaker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView

from Bookmaker_app import views
from Bookmaker_app.views import get_dyscypliny, get_kategorie, RegisterView, ZakladyUzytkownikaView, spin_react, home, \
      spin_api

urlpatterns = [
      path('', home, name='home'),
      path('admin/', admin.site.urls),
      path('logout/', views.logout_view, name='logout'),
      path('register/', views.register, name='register'),
      path('login/', views.login_view, name='login'),
      path('user_panel/', views.user_panel, name='user_panel'),
      path('wplata/', views.wplata, name='wplata'),
      path('wyplata/', views.wyplata, name='wyplata'),
      path('api/spin/', spin_api, name='spin_api'),
      path('spin/', TemplateView.as_view(template_name='bookmaker_app/spin_react.html'), name='spin'),
      path('api/dyscypliny/', get_dyscypliny),
      path('api/kategorie/', get_kategorie),
      path('api/register/', views.register, name='register'),
      path('api/zaklady/', ZakladyUzytkownikaView.as_view(), name='zaklady-uzytkownika'),
      path('obstaw/<int:event_id>/', views.obstaw_mecz, name='obstaw_mecz'),
      path('dyscyplina/<str:nazwa>/', views.dyscyplina, name='dyscyplina'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)