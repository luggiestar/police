from django.apps import AppConfig


class PoliceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'POLICE'

    def ready(self):
        import POLICE.signals
