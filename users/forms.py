from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from danesh_boom.forms.fields import ArrayField
from users.models import Profile, Education, Research, Certificate, \
    WorkExperience, Skill


class SkillForm(ModelForm):

    class Meta:
        model = Skill
        exclude = ['user']
        field_classes = {
            'tag': ArrayField,
        }


class WorkExperienceForm(ModelForm):

    class Meta:
        model = WorkExperience
        exclude = ['user']


class CertificateForm(ModelForm):

    class Meta:
        model = Certificate
        exclude = ['user', 'picture']


class ResearchForm(ModelForm):

    class Meta:
        model = Research
        exclude = ['user']
        field_classes = {
            'author': ArrayField,
        }


class EducationForm(ModelForm):

    class Meta:
        model = Education
        exclude = ['user']


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        exclude = ['user']
        field_classes = {
            'web_site': ArrayField,
            'phone': ArrayField,
            'mobile': ArrayField,
        }


class RegisterUserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_active']
        # TODO password validator

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "Username Already Exists",
                code='username_exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Email Address Already Exists",
                code='email_exists')
        return email
