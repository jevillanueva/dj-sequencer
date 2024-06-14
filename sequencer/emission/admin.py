from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Department,
    Document,
    Year,
    Sequence,
    Emission,
    EmissionFile,
    UserDepartment,
    CustomUser,
    GlobalSettings,
)


# Register your models here.
class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_active=True)


class GlobalSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not GlobalSettings.objects.exists()


admin.site.register(GlobalSettings, GlobalSettingsAdmin)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Document)
admin.site.register(Year)
admin.site.register(Sequence)
admin.site.register(Emission)
admin.site.register(EmissionFile)
admin.site.register(UserDepartment)
