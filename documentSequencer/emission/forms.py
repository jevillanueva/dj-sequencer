from django import forms
from django.db import transaction
from .models import Emission, UserDepartment, Sequence


class EmissionForm(forms.ModelForm):
    class Meta:
        model = Emission
        fields = ["sequence", "detail", "destination"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            user_departments = UserDepartment.objects.filter(user=self.user)
            self.fields["sequence"].queryset = Sequence.objects.filter(
                department__in=user_departments.values_list("department", flat=True),
                can_emit=True,
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        sequence = Sequence.objects.select_for_update().get(id=instance.sequence.id)
        sequence.increment()
        instance.number = sequence.sequence
        instance.user = self.user
        if commit:
            instance.save()
        return instance
    
class EmissionByDepartmentForm(forms.ModelForm):
    class Meta:
        model = Emission
        fields = ["sequence", "detail", "destination"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.department = kwargs.pop("department", None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["sequence"].disabled = True

        if self.user:
            user_departments = UserDepartment.objects.filter(user=self.user)
            self.fields["sequence"].queryset = Sequence.objects.filter(
                department__in=user_departments.values_list("department", flat=True),
                can_emit=True, department=self.department
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk:
            sequence = Sequence.objects.select_for_update().get(id=instance.sequence.id)
            sequence.increment()
            instance.number = sequence.sequence
            instance.user = self.user
        if commit:
            instance.save()
        return instance