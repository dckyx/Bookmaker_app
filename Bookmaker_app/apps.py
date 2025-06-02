from django.apps import AppConfig

class BookmakerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Bookmaker_app'

    def ready(self):
        import Bookmaker_app.signals
