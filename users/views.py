from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from utils.token import validate_token

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
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

from .serializers import (
    IdentitySerializer,
    ProfileSerializer,
    EducationSerializer,
    ResearchSerializer,
    CertificateSerializer,
    WorkExperienceSerializer,
    SkillSerializer,
    BadgeSerializer
)


class IdentityViewset(ModelViewSet):
    # queryset = Identity.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Identity.objects.all()
        return queryset

    def get_serializer_class(self):
        return IdentitySerializer


class ProfileViewset(ModelViewSet):
    # queryset = Profile.objects.all()

    def get_queryset(self):
        queryset = Profile.objects.all()
        return queryset

    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return ProfileSerializer


class EducationViewset(ModelViewSet):
    # queryset = Education.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Education.objects.all()
        return queryset

    def get_serializer_class(self):
        return EducationSerializer


class ResearchViewset(ModelViewSet):
    # queryset = Research.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Research.objects.all()
        return queryset

    def get_serializer_class(self):
        return ResearchSerializer


class CertificateViewset(ModelViewSet):
    # queryset = Certificate.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Certificate.objects.all()
        return queryset

    def get_serializer_class(self):
        return CertificateSerializer


class WorkExperienceViewset(ModelViewSet):
    # queryset = WorkExperience.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = WorkExperience.objects.all()
        return queryset

    def get_serializer_class(self):
        return WorkExperienceSerializer


class SkillViewset(ModelViewSet):
    # queryset = Skill.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Skill.objects.all()
        return queryset

    def get_serializer_class(self):
        return SkillSerializer


class BadgeViewset(ModelViewSet):
    # queryset = Badge.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Badge.objects.all()
        return queryset

    def get_serializer_class(self):
        return BadgeSerializer


def login_page(request):
    logout(request)
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL)
        return redirect(settings.SOCIAL_AUTH_LOGIN_ERROR_URL)
    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('/#/auth/logout/')


def active_user(request, token):
    err, user = validate_token(token)
    if user:
        # active user
        user.is_active = True
        user.save()
        err = 'success-activation'

    return redirect('/#/auth/{}/'.format(err))
