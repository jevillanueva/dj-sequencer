from django import forms
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
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance