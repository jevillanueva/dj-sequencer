import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

# Create your models here.
class GlobalSettings(models.Model):
    name = models.CharField(max_length=255, default="Sequencer")
    logo = models.ImageField(upload_to="logos/")
    primary_color = models.CharField(max_length=7, default="#00d1b2")
    secondary_color = models.CharField(max_length=7, default="#4258ff")
    language = models.CharField(max_length=2, default="es")

    def __str__(self):
        return "Global Settings"

    class Meta:
        verbose_name = "Global Setting"
        verbose_name_plural = "Global Settings"


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class SoftDeleteMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ActiveManager()
    all_objects = models.Manager()  # Manager to include inactive objects

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.deleted_at = timezone.now()

        self.save()

    class Meta:
        abstract = True


class CustomUser(AbstractUser, SoftDeleteMixin):
    pass


class Department(SoftDeleteMixin):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Year(SoftDeleteMixin):
    year = models.IntegerField()

    def __str__(self):
        return str(self.year)


class Document(SoftDeleteMixin):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Sequence(SoftDeleteMixin):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    sequence = models.IntegerField()
    can_emit = models.BooleanField(default=True)

    def increment(self, quantity=1):
        self.sequence += quantity
        self.save()
        return self.sequence

    def __str__(self):
        return f"{self.sequence}: {self.department} - {self.document} - {self.year}"


class Emission(SoftDeleteMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    new = models.BooleanField(default=True)
    received = models.BooleanField(default=False)
    date_received = models.DateField(null=True, blank=True)
    detail = models.TextField(max_length=1500, blank=True)
    destination = models.TextField(max_length=500, default="N/A")
    user_received = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user_received",
        null=True,
        blank=True,
    )
    number = models.IntegerField()
    batch = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return f"{self.number} - {self.detail} - {self.destination} - {self.date}"


class EmissionFile(SoftDeleteMixin):
    emission = models.ForeignKey(Emission, on_delete=models.CASCADE)
    file = models.FileField(upload_to="emission_files/")
    url = models.URLField(null=True, blank=True)
    name = models.TextField(max_length=500, blank=True)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return f"{self.emission} - {self.file}"


class UserDepartment(SoftDeleteMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    can_administrate = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.department} - {self.user} - {'Admin' if self.can_administrate else 'User'}"

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.username = user.email
        return user