from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from danesh_boom.forms.fields import ArrayField
from organizations.models import Organization, StaffCount, OrganizationPicture


def distinct_list(original_list):
    distinct_array = []
    for i in original_list:
        if i not in distinct_array:
            distinct_array.append(i)
    return distinct_array


class PictureForm(ModelForm):
    class Meta:
        model = OrganizationPicture
        exclude = ['organization', 'picture']


class StaffCountForm(ModelForm):
    class Meta:
        model = StaffCount
        exclude = ['organization']


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        exclude = ['owner', 'admins', 'logo']
        field_classes = {
            'phone': ArrayField,
            'correspondence_language': ArrayField,
            'business_type': ArrayField,
            'social_network': ArrayField,
        }

    def clean_staff_count(self):
        staff_count = self.cleaned_data['staff_count']
        if staff_count and staff_count < 0:
            raise ValidationError(_('Staff Count should be positive number'))
        return staff_count

    def clean_business_type(self):
        business_type = distinct_list(self.cleaned_data['business_type'])
        return business_type
