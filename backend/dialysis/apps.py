from django.apps import AppConfig

class DialysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dialysis'

    def ready(self):
        import dialysis.signals
