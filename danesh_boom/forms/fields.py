from django.contrib.postgres.forms import SimpleArrayField, ValidationError, prefix_validation_error
from django.core.validators import RegexValidator
from django.forms import CharField, TextInput


class PhoneField(CharField):
    widget = TextInput
    default_validators = [RegexValidator('^\+\d{1,3}-\d{2,3}-\d{3,14}$')]

    def clean(self, value):
        value = self.to_python(value).strip()
        return super(PhoneField, self).clean(value)


class ArrayField(SimpleArrayField):
    def prepare_value(self, value):
        return [self.base_field.prepare_value(v) for v in value]

    def to_python(self, value):
        # see django/contrib/postgres/forms/array.py:37
        if value:
            items = value
        else:
            items = []
        errors = []
        values = []
        for index, item in enumerate(items):
            try:
                values.append(self.base_field.to_python(item))
            except ValidationError as error:
                errors.append(prefix_validation_error(
                    error,
                    prefix=self.error_messages['item_invalid'],
                    code='item_invalid',
                    params={'nth': index},
                ))
        if errors:
            raise ValidationError(errors)
        return values
