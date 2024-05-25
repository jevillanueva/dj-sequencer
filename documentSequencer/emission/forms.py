from django import forms
from .models import Emission

class EmissionForm(forms.ModelForm):
    class Meta:
        model = Emission
        fields = ['detail', 'destination']