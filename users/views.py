import json

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from utils.token import validate_token

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import list_route
from rest_framework.response import Response
from base.permissions import BlockPostMethod, IsOwnerOrReadOnly
from .models import (
    Identity,
    Profile,
    Education,
    Research,
    Certificate,
    WorkExperience,
    Skill,
    Badge,
    IdentityUrl,
    UserArticle
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
    BadgeSerializer,
    IdentityUrlSerilizer,
    UserArticleListSerializer,
    UserArticleRisSerializer
)
from .permissions import IsIdentityOwnerOrReadOnly, IsSuperUserOrReadOnly, IsUrlOwnerOrReadOnly


class UserViewset(ModelViewSet):
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

    @list_route(methods=['post'])
    def import_users(self, request):
        jsonString = request.data.get('records', None)
        data = json.loads(jsonString)
        errors = []
        for record in data:
            try:
                user = User.objects.create_user(
                    first_name=record.get('first_name', None),
                    last_name=record.get('last_name', None),
                    username=record.get('username', None),
                    password=record.get('password', None),
                    email=record.get('email', None)
                )
            except Exception as e:
                errors.append({
                    'data': record,
                    'status': str(e)
                })
        response = {
            'errors': errors
        }
        return Response(response)


class IdentityViewset(ModelViewSet):
    owner_field = 'identity_user'
    permission_classes = [BlockPostMethod, IsIdentityOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        queryset = Identity.objects.all()

        identity_user = self.request.query_params.get('identity_user')
        if identity_user is not None:
            queryset = queryset.filter(identity_user_id=identity_user)

        return queryset

    def get_serializer_class(self):
        return IdentitySerializer


class ProfileViewset(ModelViewSet):
    owner_field = 'profile_user'
    permission_classes = [IsAuthenticated, BlockPostMethod, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Profile.objects.all()

        profile_user = self.request.query_params.get('profile_user')
        if profile_user is not None:
            queryset = queryset.filter(profile_user_id=profile_user)

        return queryset

    def get_serializer_class(self):
        return ProfileSerializer


class EducationViewset(ModelViewSet):
    owner_field = 'education_user'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        queryset = Education.objects.all()
        return queryset

    def get_serializer_class(self):
        return EducationSerializer


class ResearchViewset(ModelViewSet):
    owner_field = 'research_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Research.objects.all()

        research_user = self.request.query_params.get('research_user')
        if research_user is not None:
            queryset = queryset.filter(research_user_id=research_user)

        return queryset

    def get_serializer_class(self):
        return ResearchSerializer


class CertificateViewset(ModelViewSet):
    owner_field = 'certificate_user'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        queryset = Certificate.objects.all()

        certificate_user = self.request.query_params.get('certificate_user')
        if certificate_user is not None:
            queryset = queryset.filter(certificate_user_id=certificate_user)

        return queryset

    def get_serializer_class(self):
        return CertificateSerializer


class WorkExperienceViewset(ModelViewSet):
    owner_field = 'work_experience_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = WorkExperience.objects.all()

        work_experience_user = self.request.query_params.get('work_experience_user')
        if work_experience_user is not None:
            queryset = queryset.filter(work_experience_user_id=work_experience_user)

        return queryset

    def get_serializer_class(self):
        return WorkExperienceSerializer


class SkillViewset(ModelViewSet):
    owner_field = 'skill_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Skill.objects.all()

        skill_user = self.request.query_params.get('skill_user')
        if skill_user is not None:
            queryset = queryset.filter(skill_user_id=skill_user)

        return queryset

    def get_serializer_class(self):
        return SkillSerializer


class BadgeViewset(ModelViewSet):
    owner_field = 'badge_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Badge.objects.all()

        badge_user = self.request.query_params.get('badge_user')
        if badge_user is not None:
            queryset = queryset.filter(badge_user_id=badge_user)

        return queryset

    def get_serializer_class(self):
        return BadgeSerializer


class IdentityUrlViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsUrlOwnerOrReadOnly]

    def get_queryset(self):
        queryset = IdentityUrl.objects.all()
        return queryset

    def get_serializer_class(self):
        return IdentityUrlSerilizer


class UserArticleViewset(ModelViewSet):
    owner_field = 'user_article_related_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = UserArticle.objects.all()
        return queryset

    def get_serializer_class(self):
        return UserArticleListSerializer


class UserArticleRisViewset(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = UserArticle.objects.all()
        return queryset

    def get_serializer_class(self):
        return UserArticleRisSerializer


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
