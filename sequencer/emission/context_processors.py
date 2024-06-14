from .models import GlobalSettings

def has_permission(request):
    return {
        "can_administrate": request.user.has_perm("emission.can_administrate")
    }

def global_settings(request):
    settings = GlobalSettings.objects.first()
    return {'global_settings': settings}