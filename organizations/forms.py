from django.forms import ModelForm

from danesh_boom.forms.fields import ArrayField
from organizations.models import Organization, StaffCount, Picture,\
    UserAgent


class UserAgentForm(ModelForm):

    class Meta:
        model = UserAgent
        exclude = ['organization', 'user']


class PictureForm(ModelForm):

    class Meta:
        model = Picture
        exclude = ['organization']


class StaffCountForm(ModelForm):

    class Meta:
        model = StaffCount
        exclude = ['organization']


class OrganizationForm(ModelForm):

    class Meta:
        model = Organization
        exclude = ['user']
        field_classes = {
            'phone': ArrayField,
        }
