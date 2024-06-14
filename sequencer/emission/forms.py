from django import forms
from django.db import transaction
from .models import CustomUser, Department, Emission, EmissionFile, UserDepartment, Sequence


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
        if self.user:
            user_departments = UserDepartment.objects.filter(user=self.user)
            self.fields["sequence"].queryset = Sequence.objects.filter(
                department__in=user_departments.values_list("department", flat=True),
                can_emit=True,
                department=self.department,
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        sequence = Sequence.objects.select_for_update().get(pk=instance.sequence.pk)
        instance.number = sequence.increment()
        instance.user = self.user
        if commit:
            instance.save()
        return instance


class EmissionByDepartmentFormEdit(forms.ModelForm):
    class Meta:
        model = Emission
        fields = ["sequence", "detail", "destination"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.department = kwargs.pop("department", None)
        super().__init__(*args, **kwargs)
        self.fields["sequence"].disabled = True
        if self.user:
            user_departments = UserDepartment.objects.filter(user=self.user)
            self.fields["sequence"].queryset = Sequence.objects.filter(
                department__in=user_departments.values_list("department", flat=True),
                can_emit=True,
                department=self.department,
            )

    def save(self, commit=True):
        # actual emission before update
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

class EmissionByDepartmentBatchForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=2)
    class Meta:
        model = Emission
        fields = ["sequence", "detail", "destination"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.department = kwargs.pop("department", None)
        super().__init__(*args, **kwargs)
        if self.user:
            user_departments = UserDepartment.objects.filter(user=self.user)
            self.fields["sequence"].queryset = Sequence.objects.filter(
                department__in=user_departments.values_list("department", flat=True),
                can_emit=True,
                department=self.department,
            )
class AdminEmissionByDepartmentForm(forms.ModelForm):
    class Meta:
        model = Emission
        fields = ["user", "sequence", "detail", "destination"]

    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop("department", None)
        super().__init__(*args, **kwargs)
        self.fields["sequence"].queryset = Sequence.objects.filter(
            can_emit=True, department=self.department
        )
        users_department = UserDepartment.objects.filter(department=self.department)
        self.fields["user"].queryset = CustomUser.objects.filter(
            pk__in=users_department.values_list("user", flat=True)
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        sequence = Sequence.objects.select_for_update().get(pk=instance.sequence.pk)
        instance.number = sequence.increment()
        if commit:
            instance.save()
        return instance

class AdminEmissionByDepartmentBatchForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=2)
    class Meta:
        model = Emission
        fields = ["user", "sequence", "detail", "destination"]

    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop("department", None)
        super().__init__(*args, **kwargs)
        self.fields["sequence"].queryset = Sequence.objects.filter(
            can_emit=True, department=self.department
        )
        users_department = UserDepartment.objects.filter(department=self.department)
        self.fields["user"].queryset = CustomUser.objects.filter(
            pk__in=users_department.values_list("user", flat=True)
        )

class AdminEmissionByDepartmentFormEdit(forms.ModelForm):
    class Meta:
        model = Emission
        fields = ["user","sequence", "detail", "destination"]

    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop("user", None)
        self.department = kwargs.pop("department", None)
        super().__init__(*args, **kwargs)
        self.fields["sequence"].disabled = True
        user_departments = UserDepartment.objects.filter(department=self.department)
        self.fields["sequence"].queryset = Sequence.objects.filter(
        can_emit=True, department=self.department)
        users_department = UserDepartment.objects.filter(department=self.department)
        self.fields["user"].queryset = CustomUser.objects.filter(
            pk__in=users_department.values_list("user", flat=True)
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

class EmissionFileForm(forms.ModelForm):
    class Meta:
        model = EmissionFile
        fields = ["name","description","file"]

    def __init__(self, *args, **kwargs):
        self.emission = kwargs.pop("emission", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.emission = self.emission
        instance.url = instance.file.url
        if commit:
            instance.save()
        return instance

