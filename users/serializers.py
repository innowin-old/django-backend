from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import (
        Identity,
        Profile,
        Education,
        Research,
        Certificate,
        WorkExperience,
        Skill,
        Badge
    )


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class IdentitySerializer(ModelSerializer):
    class Meta:
        model = Identity
        fields = '__all__'


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class EducationSerializer(ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class ResearchSerializer(ModelSerializer):
    class Meta:
        model = Research
        fields = '__all__'


class CertificateSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class WorkExperienceSerializer(ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class BadgeSerializer(ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'
