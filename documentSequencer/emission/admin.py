from django.contrib import admin
from .models import Department, Document, Year, Sequence, Emission, EmissionFile, UserDepartment
# Register your models here.
admin.site.register(Department)
admin.site.register(Document)
admin.site.register(Year)
admin.site.register(Sequence)
admin.site.register(Emission)
admin.site.register(EmissionFile)
admin.site.register(UserDepartment)