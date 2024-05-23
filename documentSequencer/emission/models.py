from django.db import models
from django.utils import timezone

# Create your models here.
class ActiveManager (models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)
    
class SoftDeleteMixin(models.Model):
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = ActiveManager()
    all_objects = models.Manager()  # Manager to include inactive objects

    def delete(self, *args, **kwargs):
        self.active = False
        self.deleted_at = timezone.now()
        
        self.save()

    class Meta:
        abstract = True

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

    class Meta:
        unique_together = ['department', 'document', 'year']

    def __str__(self):
        return f'{self.department} - {self.document} - {self.year} - {self.sequence}'
    
class Emission(SoftDeleteMixin):
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    date = models.DateField()
    received = models.BooleanField(default=False)
    date_received = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.sequence} - {self.date}'
    
class EmissionFile(SoftDeleteMixin):
    emission = models.ForeignKey(Emission, on_delete=models.CASCADE)
    file = models.FileField(upload_to='emission_files/')
    url = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.emission} - {self.file}'