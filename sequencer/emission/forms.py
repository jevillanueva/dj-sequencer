from django import forms
from django.db import transaction

from .widgets import (
    BulmaFileWidget,
    BulmaNumberWidget,
    BulmaSelectWidget,
    BulmaSwitchWidget,
    BulmaTextLineWidget,
    BulmaTextWidget,
)
from .models import (
    CustomUser,
    Department,
    Document,
    Emission,
    EmissionFile,
    UserDepartment,
    Sequence,
    Year,
)


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
            self.fields["sequence"].widget = BulmaSelectWidget()

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
            self.fields["detail"].widget = BulmaTextWidget()
            self.fields["sequence"].widget = BulmaSelectWidget()
            self.fields["destination"].widget = BulmaTextLineWidget()
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
        self.fields["detail"].widget = BulmaTextWidget()
        self.fields["sequence"].widget = BulmaSelectWidget()
        self.fields["destination"].widget = BulmaTextLineWidget()
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
    quantity = forms.IntegerField(min_value=2, widget=BulmaNumberWidget)

    class Meta:
        model = Emission
        fields = ["sequence", "detail", "destination"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.department = kwargs.pop("department", None)
        super().__init__(*args, **kwargs)
        self.fields["detail"].widget = BulmaTextWidget()
        self.fields["sequence"].widget = BulmaSelectWidget()
        self.fields["destination"].widget = BulmaTextLineWidget()
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
        self.fields["user"].widget = BulmaSelectWidget()
        self.fields["sequence"].widget = BulmaSelectWidget()
        self.fields["detail"].widget = BulmaTextWidget()
        self.fields["destination"].widget = BulmaTextLineWidget()
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
    quantity = forms.IntegerField(min_value=2, widget=BulmaNumberWidget)

    class Meta:
        model = Emission
        fields = ["user", "sequence", "detail", "destination"]

    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop("department", None)
        super().__init__(*args, **kwargs)
        self.fields["user"].widget = BulmaSelectWidget()
        self.fields["sequence"].widget = BulmaSelectWidget()
        self.fields["detail"].widget = BulmaTextWidget()
        self.fields["destination"].widget = BulmaTextLineWidget()
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
        fields = ["user", "sequence", "detail", "destination"]

    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop("user", None)
        self.department = kwargs.pop("department", None)
        super().__init__(*args, **kwargs)
        self.fields["user"].widget = BulmaSelectWidget()
        self.fields["sequence"].widget = BulmaSelectWidget()
        self.fields["detail"].widget = BulmaTextWidget()
        self.fields["destination"].widget = BulmaTextLineWidget()
        self.fields["sequence"].disabled = True
        user_departments = UserDepartment.objects.filter(department=self.department)
        self.fields["sequence"].queryset = Sequence.objects.filter(
            can_emit=True, department=self.department
        )
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
        fields = ["name", "description", "file"]

    def __init__(self, *args, **kwargs):
        self.emission = kwargs.pop("emission", None)
        super().__init__(*args, **kwargs)
        self.fields["name"].widget = BulmaTextLineWidget()
        self.fields["description"].widget = BulmaTextWidget()
        self.fields["file"].widget = BulmaFileWidget()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.emission = self.emission
        instance.url = instance.file.url
        if commit:
            instance.save()
        return instance


class UserDepartmentForm(forms.ModelForm):
    class Meta:
        model = UserDepartment
        fields = ["user", "can_administrate"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.department = kwargs.pop("department", None)
        super().__init__(*args, **kwargs)
        self.fields["can_administrate"].widget = BulmaSwitchWidget()
        self.fields["can_administrate"].label = ""
        self.fields["user"].widget = BulmaSelectWidget()
        self.fields["user"].queryset = CustomUser.objects.exclude(
            pk=self.user.pk
        ).exclude(
            pk__in=UserDepartment.objects.filter(
                department=self.department
            ).values_list("user", flat=True)
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.department = self.department
        if commit:
            instance.save()
        return instance


class SequenceForm(forms.ModelForm):
    class Meta:
        model = Sequence
        fields = ["document", "year", "sequence", "can_emit"]

    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop("department", None)
        super().__init__(*args, **kwargs)
        self.fields["document"].widget = BulmaSelectWidget()
        self.fields["year"].widget = BulmaSelectWidget()
        self.fields["sequence"].widget = BulmaNumberWidget()
        self.fields["sequence"].initial = 0
        self.fields["can_emit"].widget = BulmaSwitchWidget()
        self.fields["can_emit"].label = ""
        self.fields["document"].queryset = Document.objects.all()
        self.fields["year"].queryset = Year.objects.all()

    def save(self, commit=True):
        if Sequence.objects.filter(
            document=self.cleaned_data["document"],
            year=self.cleaned_data["year"],
            department=self.department,
        ).exists():
            self.add_error(
                None,
                "Already exists a sequence with the same document, year and department",
            )
            return None
        instance = super().save(commit=False)
        instance.department = self.department
        if commit:
            instance.save()
        return instance
