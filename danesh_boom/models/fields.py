from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from danesh_boom import forms


class PhoneField(CharField):
    default_validators = [RegexValidator('^\+\d{1,3}\d{2,3}\d{3,14}$')]
    description = _("Phone")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 13
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.PhoneField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
