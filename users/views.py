import json

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import status

from utils.token import validate_token

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import list_route
from rest_framework.response import Response
from base.permissions import BlockPostMethod, IsOwnerOrReadOnly, SafeMethodsOnly
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
    UserArticle,
    Device
)

from .serializers import (
    SuperAdminUserSerializer,
    UserSerializer,
    IdentitySerializer,
    ProfileSerializer,
    ProfileListSerializer,
    EducationSerializer,
    ResearchSerializer,
    CertificateSerializer,
    WorkExperienceSerializer,
    SkillSerializer,
    BadgeSerializer,
    IdentityUrlSerilizer,
    UserArticleListSerializer,
    UserArticleRisSerializer,
    DeviceSerializer
)
from .permissions import IsIdentityOwnerOrReadOnly, IsUrlOwnerOrReadOnly, IsAuthenticatedOrCreateOnly


class UserViewset(ModelViewSet):
    permission_classes = [IsAuthenticatedOrCreateOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.superuser_queryset()
        else:
            return self.user_queryset()

    def get_serializer_class(self):
        #print(self.request.user.is_superuser)
        if self.request and self.request.user and self.request.user.is_superuser:
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
    permission_classes = [IsAuthenticated, SafeMethodsOnly]

    def get_queryset(self):
        queryset = Identity.objects.filter(delete_flag=False)

        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name=name)

        accepted = self.request.query_params.get('accepted')
        if accepted is not None:
            queryset = queryset.filter(accepted=accepted)

        user_id = self.request.query_params.get('identity_user')
        if user_id is not None:
            queryset = queryset.filter(identity_user_id=user_id)

        user_username = self.request.query_params.get('identity_user_username')
        if user_username is not None:
            queryset = queryset.filter(identity_user__username=user_username)

        organization_id = self.request.query_params.get('identity_organization')
        if organization_id is not None:
            queryset = queryset.filter(identity_organization_id=organization_id)

        organization_username = self.request.query_params.get('identity_organization_username')
        if organization_username is not None:
            queryset = queryset.filter(identity_organization__username=organization_username)

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

        public_email = self.request.query_params.get('public_email')
        if public_email is not None:
            queryset = queryset.filter(public_email=public_email)

        national_code = self.request.query_params.get('national_code')
        if national_code is not None:
            queryset = queryset.filter(national_code=national_code)

        birth_date = self.request.query_params.get('birth_date')
        if birth_date is not None:
            queryset = queryset.filter(birth_date=birth_date)

        birth_date = self.request.query_params.get('birth_date')
        if birth_date is not None:
            queryset = queryset.filter(birth_date=birth_date)

        fax = self.request.query_params.get('fax')
        if fax is not None:
            queryset = queryset.filter(fax=fax)

        telegram_account = self.request.query_params.get('telegram_account')
        if telegram_account is not None:
            queryset = queryset.filter(telegram_account=telegram_account)

        gender = self.request.query_params.get('gender')
        if gender is not None:
            queryset = queryset.filter(gender=gender)

        is_plus_user = self.request.query_params.get('is_plus_user')
        if is_plus_user is not None:
            queryset = queryset.filter(is_plus_user=is_plus_user)
            
        return queryset

    def get_serializer_class(self):
        if self.request == 'GET':
            return ProfileListSerializer
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
    owner_field = 'user_article_related_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = UserArticle.objects.all()
        return queryset

    def get_serializer_class(self):
        return UserArticleRisSerializer


class DeviceViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Device.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return DeviceSerializer


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
        try:
            identity = Identity.objects.get(identity_user=user)
        except Identity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        identity.email_verified = True
        try:
            profile = Profile.objects.get(profile_user=user)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not identity.mobile_verified and profile.national_code is not None and user.first_name and user.last_name:
            identity.accepted = True
        identity.save()

    return Response(status=status.HTTP_200_OK)


def jwt_response_payload_handler(token, user=None, request=None):
    profile = Profile.objects.get(profile_user=user)
    identity = Identity.objects.get(identity_user=user)
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data,
        'profile': ProfileSerializer(profile, context={'request': request}).data,
        'identity': IdentitySerializer(identity, context={'request': request}).data
    }


@require_POST
@login_required
@csrf_exempt
def insert_user_data(request):
    users = json.loads(request.POST["users"])
    with transaction.atomic():
        for user in users:

            if user["username"] is None or user["password"] is None:
                return HttpResponse(status=500)

            kwargs = {}

            if hasattr(user, "first_name"):
                kwargs["first_name"] = user["first_name"]

            if hasattr(user, "last_name"):
                kwargs["last_name"] = user["last_name"]

            if hasattr(user, "email"):
                kwargs["email"] = user["email"]

            user_model = User(username=user["username"], **kwargs)
            user_model.set_password(user["password"])
            user_model.save()

    message = " داده مورد نظر با موفقیت ذخیره گردید "
    return HttpResponse(message, status=200)


@require_POST
@csrf_exempt
def get_user_data(request):
    err, user = validate_token(request.POST["token"])
    profile = Profile.objects.get(profile_user=user)
    identity = Identity.objects.get(identity_user=user)
    return {
        'token': request.POST["token"],
        'user': UserSerializer(user, context={'request': request}).data,
        'profile': ProfileSerializer(profile, context={'request': request}).data,
        'identity': IdentitySerializer(identity, context={'request': request}).data
    }
