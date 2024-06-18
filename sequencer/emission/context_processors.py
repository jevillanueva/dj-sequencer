from .models import GlobalSettings, UserDepartment


def has_permission(request):
    can_administrate = False
    if request.user.is_authenticated:
        user_department = UserDepartment.objects.filter(
            user=request.user, can_administrate=True
        )
        if user_department:
            can_administrate = True
    return {"can_administrate": can_administrate}


def global_settings(request):
    settings = GlobalSettings.objects.first()
    return {"global_settings": settings}
