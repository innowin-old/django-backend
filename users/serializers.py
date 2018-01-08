from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from base.serializers import BaseSerializer
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


class SuperAdminUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined']


class IdentitySerializer(BaseSerializer):
    class Meta:
        model = Identity
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class ProfileSerializer(BaseSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class EducationSerializer(BaseSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class ResearchSerializer(BaseSerializer):
    class Meta:
        model = Research
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class CertificateSerializer(BaseSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class WorkExperienceSerializer(BaseSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class SkillSerializer(BaseSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class BadgeSerializer(BaseSerializer):
    class Meta:
        model = Badge
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }
