from django.core.validators import RegexValidator
from django.forms import CharField, TextInput


class PhoneField(CharField):
    widget = TextInput
    default_validators = [RegexValidator('^\+\d{1,3}-\d{2,3}-\d{3,14}$')]

    def clean(self, value):
        value = self.to_python(value).strip()
        return super(PhoneField, self).clean(value)
