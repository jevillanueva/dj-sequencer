from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import GlobalSettings

@receiver(post_migrate)
def create_default_global_settings(sender, **kwargs):
    if not GlobalSettings.objects.exists():
        GlobalSettings.objects.create()