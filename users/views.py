from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from utils.token import validate_token

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from base.permissions import BlockPostMethod, IsOwnerOrReadOnly
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
    SuperAdminUserSerializer,
    UserSerializer,
    IdentitySerializer,
    ProfileSerializer,
    EducationSerializer,
    ResearchSerializer,
    CertificateSerializer,
    WorkExperienceSerializer,
    SkillSerializer,
    BadgeSerializer
)
from .permissions import IsIdentityOwnerOrReadOnly, IsSuperUserOrReadOnly


class UserViewset(ModelViewSet):
    #queryset = User.objects.all()
    permission_classes = [IsSuperUserOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.superuser_queryset()
        else:
            return self.user_queryset()

    def get_serializer_class(self):
        print(self.request.user.is_superuser)
        if self.request.user.is_superuser:
            return SuperAdminUserSerializer
        else:
            return UserSerializer

    def superuser_queryset(self):
        queryset = User.objects.all()

        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(username__contains=username)

        first_name = self.request.query_params.get('first_name')
        if first_name is not None:
            queryset = queryset.filter(first_name__contains=first_name)

        last_name = self.request.query_params.get('last_name')
        if last_name is not None:
            queryset = queryset.filter(last_name__contains=last_name)

        email = self.request.query_params.get('email')
        if email is not None:
            queryset = queryset.filter(email__contains=email)

        is_staff = self.request.query_params.get('is_staff')
        if is_staff is not None:
            queryset = queryset.filter(is_staff=is_staff)

        is_superuser = self.request.query_params.get('is_superuser')
        if is_superuser is not None:
            queryset = queryset.filter(is_superuser=is_superuser)

        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        date_joined = self.request.query_params.get('date_joined')
        if date_joined is not None:
            queryset = queryset.filter(date_joined=date_joined)

        return queryset

    def user_queryset(self):
        queryset = User.objects.filter(is_active=True)

        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(username__contains=username)

        first_name = self.request.query_params.get('first_name')
        if first_name is not None:
            queryset = queryset.filter(first_name__contains=first_name)

        last_name = self.request.query_params.get('last_name')
        if last_name is not None:
            queryset = queryset.filter(last_name__contains=last_name)

        email = self.request.query_params.get('email')
        if email is not None:
            queryset = queryset.filter(email__contains=email)

        return queryset


class IdentityViewset(ModelViewSet):
    # queryset = Identity.objects.all()
    owner_field = 'identity_user'
    permission_classes = [BlockPostMethod, IsIdentityOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        queryset = Identity.objects.all()
        return queryset

    def get_serializer_class(self):
        return IdentitySerializer


class ProfileViewset(ModelViewSet):
    # queryset = Profile.objects.all()
    owner_field = 'profile_user'
    permission_classes = [BlockPostMethod, IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        queryset = Profile.objects.all()
        return queryset

    def get_serializer_class(self):
        return ProfileSerializer


class EducationViewset(ModelViewSet):
    # queryset = Education.objects.all()
    owner_field = 'education_user'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        queryset = Education.objects.all()
        return queryset

    def get_serializer_class(self):
        return EducationSerializer


class ResearchViewset(ModelViewSet):
    # queryset = Research.objects.all()
    owner_field = 'research_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Research.objects.all()
        return queryset

    def get_serializer_class(self):
        return ResearchSerializer


class CertificateViewset(ModelViewSet):
    # queryset = Certificate.objects.all()
    owner_field = 'certificate_user'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        queryset = Certificate.objects.all()
        return queryset

    def get_serializer_class(self):
        return CertificateSerializer


class WorkExperienceViewset(ModelViewSet):
    # queryset = WorkExperience.objects.all()
    owner_field = 'work_experience_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = WorkExperience.objects.all()
        return queryset

    def get_serializer_class(self):
        return WorkExperienceSerializer


class SkillViewset(ModelViewSet):
    # queryset = Skill.objects.all()
    owner_field = 'skill_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Skill.objects.all()
        return queryset

    def get_serializer_class(self):
        return SkillSerializer


class BadgeViewset(ModelViewSet):
    # queryset = Badge.objects.all()
    owner_field = 'badge_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

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
