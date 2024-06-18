from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe


class BulmaSelectWidget(forms.Select):
    def __init__(self, attrs=None):
        final_attrs = {}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        # Llamar al método render del padre para obtener el HTML del select
        select_html = super().render(name, value, attrs, renderer)
        # Crear el HTML del contenedor con la clase "input-group"
        input_group_html = f'<div class="select is-primary is-rounded is-fullwidth">{select_html}</div>'
        return mark_safe(input_group_html)


class BulmaTextWidget(forms.Textarea):
    def __init__(self, attrs=None):
        final_attrs = {"class": "textarea is-primary"}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)


class BulmaTextLineWidget(forms.TextInput):
    def __init__(self, attrs=None):
        final_attrs = {"class": "input is-primary"}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)


class BulmaNumberWidget(forms.NumberInput):
    def __init__(self, attrs=None):
        final_attrs = {"class": "input is-primary"}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)


class BulmaFileWidget(forms.ClearableFileInput):
    def __init__(self, attrs=None):
        final_attrs = {"class": "file-input"}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        # Llamar al método render del padre para obtener el HTML del select
        file_html = super().render(name, value, attrs, renderer)
        # Crear el HTML del contenedor con la clase "input-group"
        input_group_html = f"""
        <div class="file has-name is-boxed is-fullwidth is-primary">
            <label class="file-label">
                {file_html}
                <span class="file-cta">
                    <span class="file-icon">
                        <i class="fa fa-upload"></i>
                    </span>
                    <span class="file-label"></span>
                </span>
                <span class="file-name"></span>
            </label>
        </div>
        """
        return mark_safe(input_group_html)


class BulmaSwitchWidget(forms.CheckboxInput):
    def __init__(self, attrs=None):
        final_attrs = {"class": "styled"}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        # Llamar al método render del padre para obtener el HTML del select
        switch_html = super().render(name, value, attrs, renderer)
        checkbox_id = attrs.get("id", "") if attrs else ""
        # Crear el HTML del contenedor con la clase "input-group"
        input_group_html = f"""
        <br>
        <div class="field">
            <p class="control">
                <div class="b-checkbox is-primary is-circular">
                    {switch_html}
                    <label for="{checkbox_id}">
                        {name.replace('_', ' ').capitalize()}
                    </label>
                </div>
            </p>
        </div>
        """
        return mark_safe(input_group_html)
