import json
import requests
import random

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from numpy import record
from rest_framework import status

from organizations.models import Follow
from utils.token import validate_token
from utils.number_generator import random_with_N_digits

from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from base.permissions import BlockPostMethod, IsOwnerOrReadOnly, SafeMethodsOnly, OnlyPostMethod, CanReadContent
from base.models import BaseSocialType, BaseSocial, Badge
from .models import (
    Identity,
    Profile,
    Setting,
    Education,
    Research,
    Certificate,
    WorkExperience,
    Skill,
    IdentityUrl,
    UserArticle,
    Device,
    UserMetaData,
    AgentRequest,
    StrengthStates,
    BlockIdentity, UserCode)

from .serializers import (
    SuperAdminUserSerializer,
    UserSerializer,
    IdentitySerializer,
    ProfileSerializer,
    ProfileListSerializer,
    SettingSerializer,
    EducationSerializer,
    ResearchSerializer,
    CertificateSerializer,
    WorkExperienceSerializer,
    SkillSerializer,
    IdentityUrlSerilizer,
    UserArticleListSerializer,
    UserArticleRisSerializer,
    DeviceSerializer,
    UserMetaDataSerializer,
    ForgetPasswordSerializer,
    UserOrganizationSerializer,
    AgentRequestSerializer,
    AgentRequestAdminSerializer,
    StrengthStatesSerializer,
    BlockIdentitySerializer, UserCodeSerializer, UserExploreSerializer)
from .permissions import IsUrlOwnerOrReadOnly, IsAuthenticatedOrCreateOnly, IsDeviceOwnerOrReadOnly


class UserViewset(ModelViewSet):
    permission_classes = [IsAuthenticatedOrCreateOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.superuser_queryset()
        else:
            return self.user_queryset()

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return SuperAdminUserSerializer
        else:
            return UserSerializer

    def superuser_queryset(self):
        queryset = User.objects.all()

        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)

        first_name = self.request.query_params.get('first_name', None)
        if first_name is not None:
            queryset = queryset.filter(first_name__contains=first_name)

        last_name = self.request.query_params.get('last_name', None)
        if last_name is not None:
            queryset = queryset.filter(last_name__contains=last_name)

        email = self.request.query_params.get('email', None)
        if email is not None:
            queryset = queryset.filter(email__contains=email)

        is_staff = self.request.query_params.get('is_staff', None)
        if is_staff is not None:
            queryset = queryset.filter(is_staff=is_staff)

        is_superuser = self.request.query_params.get('is_superuser', None)
        if is_superuser is not None:
            queryset = queryset.filter(is_superuser=is_superuser)

        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        date_joined = self.request.query_params.get('date_joined', None)
        if date_joined is not None:
            queryset = queryset.filter(date_joined=date_joined)

        return queryset

    def user_queryset(self):
        queryset = User.objects.filter(is_active=True)

        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)

        first_name = self.request.query_params.get('first_name', None)
        if first_name is not None:
            queryset = queryset.filter(first_name__contains=first_name)

        last_name = self.request.query_params.get('last_name', None)
        if last_name is not None:
            queryset = queryset.filter(last_name__contains=last_name)

        email = self.request.query_params.get('email', None)
        if email is not None:
            queryset = queryset.filter(email__contains=email)

        return queryset

    @list_route(
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def explore(self, request):
        result = []
        users = User.objects.filter(is_active=True)
        self_user_identity = Identity.objects.get(identity_user=request.user)
        username = self.request.query_params.get('username', None)
        if username is not None:
            users = users.filter(username__contains=username)
        for user in users:
            explore_record = {'user': user}
            profile = Profile.objects.select_related(
                'profile_media', 'profile_banner'
            ).only('id', 'profile_media', 'profile_banner', 'description').get(profile_user=user)
            explore_record['profile'] = profile
            user_identity = Identity.objects.filter(identity_user=user)
            explore_record['is_followed'] = False
            follow = Follow.objects.filter(follow_followed=user_identity, follow_follower=self_user_identity, follow_accepted=True)
            if follow.count() != 0:
                explore_record['is_followed'] = True
            badges = Badge.objects.filter(badge_related_parent=user_identity).select_related('badge_related_badge_category')
            explore_record['badges'] = badges
            result.append(explore_record)

        explore_serializer = UserExploreSerializer(result, many=True)

        return Response(explore_serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['post'], permission_classes=[AllowAny])
    def user_exist(self, request):
        username = request.POST.get('username', None)
        if username is not None:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(0, status=status.HTTP_404_NOT_FOUND)
            return Response(1, status=status.HTTP_200_OK)
        return Response('please insert username', status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'], permission_classes=[AllowAny])
    def email_exist(self, request):
        email = request.POST.get('email', None)
        if email is not None:
            email_count = User.objects.filter(email=email).count()
            if email_count == 0:
                return Response(0, status=status.HTTP_404_NOT_FOUND)
            return Response(1, status=status.HTTP_200_OK)
        return Response('please insert email', status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'])
    def import_users(self, request):
        jsonString = request.data.get('records', None)
        data = json.loads(jsonString)
        errors = []
        for record in data:

            # get users with username  if not exist adding it to data baase
            user = User.objects.filter(username=record.get('username', None))
            if user.count() == 0:
                user = User(username=record.get('username', None))
            else:
                user = User.objects.get(username=record.get('username', None))

            # check for user input data and add update fields
            if record.get('password', None) is not None and record.get('password', None) != '':
                user.set_password(record.get('password', None))
            if record.get('email', None) is not None and record.get('email', None) != '':
                user.email = record.get('email', None)
            if record.get('first_name', None) is not None and record.get('first_name', None) != '':
                user.first_name = record.get('first_name', None)
            if record.get('last_name', None) is not None and record.get('last_name', None) != '':
                user.last_name = record.get('last_name', None)
            user.save()

            # get user identity
            user_identity = Identity.objects.get(identity_user=user)

            # adding user phone numbers
            phone_data = record.get('phones', None)
            if phone_data is not None and phone_data != '':
                # get phone numbers with '*' split
                phones = phone_data.split('*')
                if len(phones) < 3:
                    for phone in phones:
                        meta_phone_count = UserMetaData.objects.filter(user_meta_related_user=user, user_meta_type='phone').count()
                        if meta_phone_count < 2:
                            meta_phone_check = UserMetaData.objects.filter(user_meta_value=phone, user_meta_type='phone').count()
                            if meta_phone_check == 0:
                                try:
                                    meta_phone = UserMetaData.objects.create(
                                        user_meta_related_user=user,
                                        user_meta_type='phone',
                                        user_meta_value=phone
                                    )
                                except Exception as e:
                                    errors.append({
                                        'data': record,
                                        'status': str(e)
                                    })
                            else:
                                errors.append({
                                    'data': record,
                                    'status': 'user phone number exist'
                                })
                        else:
                            errors.append({
                                'data': record,
                                'status': 'user can not have more that two phone number'
                            })
                else:
                    errors.append({
                        'data': record,
                        'status': 'user can not have more that two phone number'
                    })
            # adding user mobile numbers
            mobile_data = record.get('mobiles', None)
            if mobile_data is not None and mobile_data != '':
                # get mobile numbers wiht '*' split
                mobiles = mobile_data.split('*')
                if len(mobiles) < 3:
                    for mobile in mobiles:
                        meta_mobile_count = UserMetaData.objects.filter(user_meta_related_user=user, user_meta_type='mobile').count()
                        if meta_mobile_count < 2:
                            meta_mobile_check = UserMetaData.objects.filter(user_meta_value=mobile, user_meta_type='mobile').count()
                            if meta_mobile_check == 0:
                                try:
                                    meta_mobile = UserMetaData.objects.create(
                                        user_meta_related_user=user,
                                        user_meta_type='mobile',
                                        user_meta_value=mobile
                                    )
                                except Exception as e:
                                    errors.append({
                                        'data': record,
                                        'status': str(e)
                                    })
                            else:
                                errors.append({
                                    'data': record,
                                    'status': 'user phone number exist'
                                })
                        else:
                            errors.append({
                                'data': record,
                                'status': 'user can not have more that two mobile number'
                            })
                else:
                    errors.append({
                        'data': record,
                        'status': 'user can not have more that two mobile number'
                    })
            # add user profile data
            profile = Profile.objects.filter(profile_user=user)
            if profile.count() == 0:
                profile = Profile(profile_user=user)
            else:
                profile = Profile.objects.get(profile_user=user)
            # check if data exist update profile instance
            if record.get('profile_national_code', None) is not None and record.get('profile_national_code', None) != '':
                profile.national_code = record.get('profile_national_code', None)
            if record.get('profile_birth_date', None) is not None and record.get('profile_birth_date', None) != '':
                profile.birth_date = record.get('profile_birth_date', None)
            if record.get('profile_description', None) is not None and record.get('profile_description', None) != '':
                profile.description = record.get('description', None)
            if record.get('profile_address', None) is not None and record.get('profile_address', None) != '':
                profile.address = record.get('profile_address', None)
            if record.get('profile_public_email', None) is not None and record.get('profile_public_email', None) != '':
                profile.public_email = record.get('profile_public_email', None)
            if record.get('profile_telegram_account', None) is not None and record.get('profile_telegram_account', None) != '':
                profile.public_email = record.get('profile_telegram_account', None)
            if record.get('profile_instagram_account', None) is not None and record.get('profile_instagram_account', None) != '':
                profile.public_email = record.get('profile_instagram_account', None)
            if record.get('profile_linkedin_account', None) is not None and record.get('profile_linkedin_account', None) != '':
                profile.public_email = record.get('profile_linkedin_account', None)
            # add social data
            if record.get('social_name', None) is not None and record.get('social_name', None) != '':
                try:
                    social_type = BaseSocialType.objects.get(social_name=record.get('social_name', None))
                except Exception as e:
                    social_type = None
                    errors.append({
                        'data': record,
                        'status': str(e)
                    })
                if social_type is not None:
                    social_value = BaseSocial.objects.filter(base_social_related_social_type=social_type,
                                                             base_social_parent=user_identity)
                    if social_value.count() == 0:
                        social_value = BaseSocial(base_social_parent=user_identity)
                    else:
                        social_value = BaseSocial.objects.get(base_social_related_social_type=social_type,
                                                              base_social_parent=user_identity)
                    if record.get('base_social_value', None) is not None and record.get('base_social_value', None) != '':
                        social_value.base_social_parent = user_identity
                    social_value.save()
            # add education data
            if (record.get('education_grade', None) is not None and record.get('education_grade', None) != '') and (record.get('education_university', None) is not None and record.get('education_university', None) != '') and (record.get('education_field_of_study', None) is not None and record.get('education_field_of_study', None) != 0) and (record.get('education_from_date', None) is not None and record.get('education_from_date', None) != '') and (record.get('education_to_date', None) is not None and record.get('education_to_date', None) != ''):
                education = Education.objects.filter(education_user=user,
                                                     grade=record.get('education_grade', None),
                                                     university=record.get('education_university', None),
                                                     field_of_study=record.get('education_field_of_study', None),
                                                     from_date=record.get('education_from_date', None),
                                                     to_date=record.get('education_to_date', None))
                if education.count() == 0:
                    education = Education(education_user=user,
                                          grade=record.get('education_grade', None),
                                          university=record.get('education_university', None),
                                          field_of_study=record.get('education_field_of_study', None),
                                          from_date=record.get('education_from_date', None),
                                          to_date=record.get('education_to_date', None))
                else:
                    education = Education.objects.get(education_user=user,
                                                      grade=record.get('education_grade', None),
                                                      university=record.get('education_university', None),
                                                      field_of_study=record.get('education_field_of_study', None),
                                                      from_date=record.get('education_from_date', None),
                                                      to_date=record.get('education_to_date', None))
                if record.get('education_average', None) is not None and record.get('education_average', None) != '':
                    education.average = record.get('education_average', None)
                if record.get('education_description', None) is not None and record.get('education_description', None) != '':
                    education.description = record.get('education_description', None)
            # add research data
            if record.get('research_title', None) is not None and record.get('research_title', None) != '':
                research = Research.objects.filter(research_user=user, title=record.get('research_title', None))
                if research.count() == 0:
                    research = Research(research_user=user)
                else:
                    research = Research.objects.get(research_user=user, title=record.get('research_title', None))
                if record.get('research_url', None) is not None and record.get('research_url', None) != '':
                    research.url = record.get('research_url', None)
                if record.get('research_author', None) is not None and record.get('research_author', None) != '':
                    research.author = record.get('research_author', None)
                if record.get('research_publication', None) is not None and record.get('research_publication', None):
                    research.publication = record.get('research_publication', None)
                if record.get('research_year', None) is not None and record.get('research_year', None) != '':
                    research.year = record.get('research_year', None)
                if record.get('research_page_count', None) is not None and record.get('research_page_count', None):
                    research.page_count = record.get('research_page_count', None)
                if record.get('research_link', None) is not None and record.get('research_link', None) != '':
                    research.research_link = record.get('research_link', None)
                research.save()
            # add work experience
            if (record.get('work_experience_organization', None) is not None and record.get('work_experience_organization', None) != '') and (record.get('work_experience_from_date', None) is not None and record.get('work_experience_from_date', None) != '') and (record.get('work_experience_to_date', None) is not None and record.get('work_experience_to_date', None) != '') and (record.get('work_experience_position', None) is not None and record.get('work_experience_position', None) != ''):
                work_experience = WorkExperience.objects.filter(work_experience_user=user,
                                                                work_experience_organization=record.get('work_experience_organization', None),
                                                                from_date=record.get('work_experience_from_date', None),
                                                                to_date=record.get('work_experience_to_date', None))
                if work_experience.count() == 0:
                    work_experience = WorkExperience(work_experience_user=user,
                                                     work_experience_organization=record.get('work_experience_organization', None))
                else:
                    work_experience = WorkExperience.objects.get(work_experience_user=user,
                                                                 work_experience_organization=record.get('work_experience_organization', None))
                if record.get('work_experience_name', None) is not None and record.get('work_experience_name', None) != '':
                    work_experience.name = record.get('work_experience_name', None)
                if record.get('work_experience_position', None) is not None and record.get('work_experience_position', None) != '':
                    work_experience.position = record.get('work_experience_position', None)
                if record.get('work_experience_from_date', None) is not None and record.get('work_experience_from_date') != '':
                    work_experience.from_date = record.get('work_experience_from_date', None)
                if record.get('work_experience_to_date', None) is not None and record.get('work_experience_to_date', None) != '':
                    work_experience.to_date = record.get('work_experience_to_date', None)
                work_experience.save()
            # add skills data
            if record.get('skill_title', None) is not None and record.get('skill_title', None) != '':
                skill = Skill.objects.filter(skill_user=user, title=record.get('skill_title', None))
                if skill.count() == 0:
                    skill = Skill.objects.create(skill_user=user, title=record.get('skill_title', None))
                if record.get('skill_tag', None) is not None and record.get('skill_tag', None) != '':
                    skill.tag = record.get('skill_tag', None)
                if record.get('skill_description', None) is not None and record.get('skill_description', None) != '':
                    skill.description = record.get('skill_description', None)

        response = {
            'errors': errors
        }
        return Response(response)

    @list_route(methods=['post', 'get'])
    def password_reset_by_sms(self, request):
        try:
            code_object = UserCode.objects.filter(code=request.POST["code"], active=True, used=False, user_id=request.POST["user_id"], type='sms')
            if code_object.count() > 0:
                code_object = code_object[0]
                user_object = code_object.user
                password = request.POST["password"]
                confirm_password = request.POST["confirm_password"]
                if password == confirm_password:
                    user_object.set_password(password)
                code_object.active = False
                code_object.used = True
                return Response({'status': 'SUCCESS'})
            else:
                return Response({'status': 'FAILED'})
        except Exception as e:
            return Response({'status': 'FAILED', 'message': e})

    @list_route(methods=['post'])
    def password_reset_by_sms_check_code(self, request):
        code_object = UserCode.objects.filter(code=request.POST["code"], active=True, used=False, user_id=request.POST['user_id'], type='sms')
        if code_object.count() > 0:
            return Response({"status": "OK"})
        else:
            return Response({"status": "FAILED"})

    @list_route(methods=['post', 'get'])
    def password_reset_by_sms_request(self, request):
        profile_object = Profile.objects.get(auth_mobile=request.POST["mobile"])
        user_object = profile_object.profile_user
        profile = Profile.objects.get(profile_user=user_object)
        if profile.auth_mobile != '':
            if UserCode.objects.filter(user_id=user_object.id, active=True, used=False, type='sms').count() == 0:
                code = random.randint(10000, 99999)
                code_object = UserCode()
                code_object.code = code
                code_object.user = user_object
                code_object.type = 'sms'
                code_object.save()
            else:
                code_object = UserCode.objects.filter(user=user_object, active=True, used=False, type='sms')[0]
            print(code_object.code)
            data = {
              "UserApiKey": "ead9bf7ba2865979ab2dcc3e",
              "SecretKey": "w9abTCGEEJqPfgWSEv4Dz9NxSqHFxJuj"
            }
            r = requests.post("http://RestfulSms.com/api/Token", data=data)
            tokenData = json.loads(r.text)
            if tokenData["IsSuccessful"] == True:
                sms_body = {
                    "ParameterArray":[
                      { "Parameter": "Name", "ParameterValue": "اینوین" },
                      { "Parameter": "VerificationCode","ParameterValue": code_object.code }
                    ],
                    "Mobile": profile.auth_mobile,
                    "TemplateId":"5253"
                }
                headers = {
                  "Content-Type" : "application/json",
                  "x-sms-ir-secure-token" : tokenData["TokenKey"]
                }
                smsRequest = requests.post("http://RestfulSms.com/api/UltraFastSend", headers=headers, data=json.dumps(sms_body))
                smsRequestData = json.loads(smsRequest.text)
                return Response({'status': 'SUCCESS', 'user_id': user_object.id})
            return Response({'status': 'FAILED'})
        else:
            return Response({'status': 'User not set mobile'})


class IdentityViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, SafeMethodsOnly]

    def get_queryset(self):
        queryset = Identity.objects.filter(delete_flag=False)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        accepted = self.request.query_params.get('accepted', None)
        if accepted is not None:
            queryset = queryset.filter(accepted=accepted)

        user_id = self.request.query_params.get('identity_user', None)
        if user_id is not None:
            queryset = queryset.filter(identity_user_id=user_id)

        user_username = self.request.query_params.get('identity_user_username', None)
        if user_username is not None:
            queryset = queryset.filter(identity_user__username=user_username)

        organization_id = self.request.query_params.get('identity_organization', None)
        if organization_id is not None:
            queryset = queryset.filter(identity_organization_id=organization_id)

        organization_username = self.request.query_params.get('identity_organization_username', None)
        if organization_username is not None:
            queryset = queryset.filter(identity_organization__username=organization_username)

        return queryset

    def get_serializer_class(self):
        return IdentitySerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileViewset(ModelViewSet):
    # this field use for IsOwnerOrReadOnly, CanReadContent permissions
    owner_field = 'profile_user'
    # this field use for CanReadContent permission
    content_target_field = 'who_can_read_base_info'
    permission_classes = [IsAuthenticated, BlockPostMethod, IsOwnerOrReadOnly, CanReadContent]

    def get_queryset(self):
        queryset = Profile.objects.all()

        profile_user = self.request.query_params.get('profile_user', None)
        if profile_user is not None:
            queryset = queryset.filter(profile_user_id=profile_user)

        public_email = self.request.query_params.get('public_email', None)
        if public_email is not None:
            queryset = queryset.filter(public_email=public_email)

        national_code = self.request.query_params.get('national_code', None)
        if national_code is not None:
            queryset = queryset.filter(national_code=national_code)

        birth_date = self.request.query_params.get('birth_date', None)
        if birth_date is not None:
            queryset = queryset.filter(birth_date=birth_date)

        birth_date = self.request.query_params.get('birth_date', None)
        if birth_date is not None:
            queryset = queryset.filter(birth_date=birth_date)

        fax = self.request.query_params.get('fax', None)
        if fax is not None:
            queryset = queryset.filter(fax=fax)

        telegram_account = self.request.query_params.get('telegram_account', None)
        if telegram_account is not None:
            queryset = queryset.filter(telegram_account=telegram_account)

        gender = self.request.query_params.get('gender', None)
        if gender is not None:
            queryset = queryset.filter(gender=gender)

        is_plus_user = self.request.query_params.get('is_plus_user', None)
        if is_plus_user is not None:
            queryset = queryset.filter(is_plus_user=is_plus_user)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProfileListSerializer
        return ProfileSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SettingViewset(ModelViewSet):
    owner_field = 'setting_user'
    permission_classes = [IsAuthenticated, BlockPostMethod, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Setting.objects.filter(delete_flag=False)

        setting_user = self.request.query_params.get('setting_user', None)
        if setting_user is not None:
            queryset = queryset.filter(setting_user_id=setting_user)

        setting_user_username = self.request.query_params.get('setting_user_username', None)
        if setting_user_username is not None:
            queryset = queryset.filter(setting_user__username=setting_user_username)

        account_type = self.request.query_params.get('account_type', None)
        if account_type is not None:
            queryset = queryset.filter(account_type=account_type)

        image_auto_download = self.request.query_params.get('image_auto_download', None)
        if image_auto_download is not None:
            queryset = queryset.filter(image_auto_download=image_auto_download)

        video_auto_download = self.request.query_params.get('video_auto_download', None)
        if video_auto_download is not None:
            queryset = queryset.filter(video_auto_download=video_auto_download)

        who_can_read_base_info = self.request.query_params.get('who_can_read_base_info', None)
        if who_can_read_base_info is not None:
            queryset = queryset.filter(who_can_read_base_info=who_can_read_base_info)

        who_can_read_activity = self.request.query_params.get('who_can_read_activity', None)
        if who_can_read_activity is not None:
            queryset = queryset.filter(who_can_read_activity=who_can_read_activity)

        who_can_read_work_experiences = self.request.query_params.get('who_can_read_work_experiences', None)
        if who_can_read_work_experiences is not None:
            queryset = queryset.filter(who_can_read_work_experiences=who_can_read_work_experiences)

        who_can_read_badges = self.request.query_params.get('who_can_read_badges', None)
        if who_can_read_badges is not None:
            queryset = queryset.filter(who_can_read_badges=who_can_read_badges)

        who_can_read_certificates = self.request.query_params.get('who_can_read_certificates', None)
        if who_can_read_certificates is not None:
            queryset = queryset.filter(who_can_read_certificates=who_can_read_certificates)

        who_can_read_followers = self.request.query_params.get('who_can_read_followers', None)
        if who_can_read_followers is not None:
            queryset = queryset.filter(who_can_read_followers=who_can_read_followers)

        can_search_engins_index_me = self.request.query_params.get('can_search_engins_index_me', None)
        if can_search_engins_index_me is not None:
            queryset = queryset.filter(can_search_engins_index_me=can_search_engins_index_me)

        return queryset

    def get_serializer_class(self):
        return SettingSerializer


class EducationViewset(ModelViewSet):
    owner_field = 'education_user'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        queryset = Education.objects.filter(delete_flag=False)
        education_user = self.request.query_params.get('education_user', None)
        if education_user is not None:
            queryset = queryset.filter(education_user_id=education_user)

        grade = self.request.query_params.get('grade', None)
        if grade is not None:
            queryset = queryset.filter(grade=grade)

        university = self.request.query_params.get('university', None)
        if university is not None:
            queryset = queryset.filter(university=university)

        field_of_study = self.request.query_params.get('field_of_study', None)
        if field_of_study is not None:
            queryset = queryset.filter(field_of_study=field_of_study)

        from_date = self.request.query_params.get('from_date', None)
        if from_date is not None:
            queryset = queryset.filter(from_date=from_date)

        to_date = self.request.query_params.get('to_date', None)
        if to_date is not None:
            queryset = queryset.filter(to_date=to_date)
        return queryset

    @list_route(
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def count(self, request):
        education_count = Education.objects.filter(education_user=request.user, delete_flag=False).count()
        return Response({'count': education_count}, status=status.HTTP_200_OK)

    @list_route(
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def latest(self, request):
        response = {}
        educations_latest = Education.objects.filter(education_user=request.user, delete_flag=False)
        if educations_latest.count() != 0:
            for education_latest in educations_latest:
                if education_latest.grade == 'Phd':
                    response = education_latest
                elif education_latest.grade == 'Master':
                    response = education_latest
                else:
                    response = education_latest
            response = EducationSerializer(response, many=False).data
        return Response(response, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        return EducationSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResearchViewset(ModelViewSet):
    owner_field = 'research_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Research.objects.filter(delete_flag=False)

        research_user = self.request.query_params.get('research_user')
        if research_user is not None:
            queryset = queryset.filter(research_user_id=research_user)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

    def get_serializer_class(self):
        return ResearchSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CertificateViewset(ModelViewSet):
    # this field use for IsOwnerOrReadOnly, CanReadContent permissions
    owner_field = 'certificate_user'
    # this field use for CanReadContent permission
    content_target_field = 'who_can_read_certificates'

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, CanReadContent]

    def get_queryset(self):
        queryset = Certificate.objects.filter(delete_flag=False)

        certificate_user = self.request.query_params.get('certificate_user')
        if certificate_user is not None:
            queryset = queryset.filter(certificate_user_id=certificate_user)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

    def get_serializer_class(self):
        return CertificateSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkExperienceViewset(ModelViewSet):
    # this field use for IsOwnerOrReadOnly, CanReadContent permissions
    owner_field = 'work_experience_user'
    # this field use for CanReadContent permission
    content_target_field = 'who_can_read_work_experiences'

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, CanReadContent]

    def get_queryset(self):
        queryset = WorkExperience.objects.filter(delete_flag=False)

        work_experience_user = self.request.query_params.get('work_experience_user', None)
        if work_experience_user is not None:
            queryset = queryset.filter(work_experience_user_id=work_experience_user)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__contains=name)

        work_experience_organization = self.request.query_params.get('work_experience_organization', None)
        if work_experience_organization is not None:
            queryset = queryset.filter(work_experience_organization=work_experience_organization)

        position = self.request.query_params.get('position', None)
        if position is not None:
            queryset = queryset.filter(position=position)

        from_date = self.request.query_params.get('from_date', None)
        if from_date is not None:
            queryset = queryset.filter(from_date=from_date)

        to_date = self.request.query_params.get('to_date', None)
        if to_date is not None:
            queryset = queryset.filter(to_date=to_date)

        experience_status = self.request.query_params.get('status', None)
        if experience_status is not None:
            queryset = queryset.filter(status=experience_status)

        return queryset

    def get_serializer_class(self):
        return WorkExperienceSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SkillViewset(ModelViewSet):
    owner_field = 'skill_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Skill.objects.filter(delete_flag=False)

        skill_user = self.request.query_params.get('skill_user', None)
        if skill_user is not None:
            queryset = queryset.filter(skill_user_id=skill_user)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

    def get_serializer_class(self):
        return SkillSerializer

    @list_route(
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def count(self, request):
        skills_count = Skill.objects.filter(skill_user=request.user, delete_flag=False).count()
        return Response({'count': skills_count}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IdentityUrlViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsUrlOwnerOrReadOnly]

    def get_queryset(self):
        queryset = IdentityUrl.objects.filter(delet_flag=False)

        url = self.request.query_params.get('url', None)
        if url is not None:
            queryset = queryset.filter(url=url)

        identity_url_related_identity = self.request.query_params.get('identity_url_related_identity', None)
        if identity_url_related_identity is not None:
            queryset = queryset.filter(identity_url_related_identity=identity_url_related_identity)

        return queryset

    def get_serializer_class(self):
        return IdentityUrlSerilizer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserArticleViewset(ModelViewSet):
    owner_field = 'user_article_related_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = UserArticle.objects.filter(delete_flag=False)

        publisher = self.request.query_params.get('publisher', None)
        if publisher is not None:
            queryset = queryset.filter(publisher=publisher)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

    def get_serializer_class(self):
        return UserArticleListSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserArticleRisViewset(ModelViewSet):
    owner_field = 'user_article_related_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = UserArticle.objects.all()
        return queryset

    def get_serializer_class(self):
        return UserArticleRisSerializer


class DeviceViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsDeviceOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Device.objects.filter(delete_flag=False)

        device_user = self.request.query_params.get('device_user', None)
        if device_user is not None:
            queryset = queryset.filter(device_user=device_user)

        fingerprint = self.request.query_params.get('fingerprint', None)
        if fingerprint is not None:
            queryset = queryset.filter(fingerprint=fingerprint)

        browser_name = self.request.query_params.get('browser_name', None)
        if browser_name is not None:
            queryset = queryset.filter(browser_name=browser_name)

        return queryset

    def get_serializer_class(self):
        return DeviceSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserMetaDataViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = UserMetaData.objects.filter(delete_flag=False)

        user_meta_related_user = self.request.query_params.get('user_meta_related_user', None)
        if user_meta_related_user is not None:
            queryset = queryset.filter(user_meta_related_user=user_meta_related_user)

        user_meta_type = self.request.query_params.get('user_meta_related_user', None)
        if user_meta_type is not None:
            queryset = queryset.filter(user_meta_type=user_meta_type)

        user_meta_value = self.request.query_params.get('user_meta_value', None)
        if user_meta_value is not None:
            queryset = queryset.filter(user_meta_value=user_meta_value)

        return queryset

    def get_serializer_class(self):
        return UserMetaDataSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserOrganizationViewset(ModelViewSet):
    permission_classes = [OnlyPostMethod]

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def get_serializer_class(self):
        return UserOrganizationSerializer


class AgentReuqestViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = AgentRequest.objects.filter(delete_flag=False)

        agent_request_title = self.request.query_params.get('agent_request_title', None)
        if agent_request_title is not None:
            queryset = queryset.filter(agent_request_title=agent_request_title)

        agent_request_identity = self.request.query_params.get('agent_request_identity', None)
        if agent_request_identity is not None:
            queryset = queryset.filter(agent_request_identity_id=agent_request_identity)

        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return AgentRequestAdminSerializer
        return AgentRequestSerializer


class StrengthStatesViewset(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = StrengthStates.objects.all()
        return queryset

    def get_serializer_class(self):
        return StrengthStatesSerializer


class BlockIdentityViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = BlockIdentity.objects.filter(delete_flag=False)
        blocked_identity = self.request.query_params.get('blocked_identity', None)
        if blocked_identity is not None:
            queryset = queryset.filter(blocked_identity_id=blocked_identity)
        blocked_identity_name = self.request.query_params.get('blocked_identity_name', None)
        if blocked_identity_name is not None:
            queryset = queryset.filter(blocked_identity__name=blocked_identity_name)
        blocker_identity = self.request.query_params.get('blocker_identity', None)
        if blocker_identity is not None:
            queryset = queryset.filter(blocker_identity_id=blocker_identity)
        blocker_identity_name = self.request.query_params.get('blocker_identity_name', None)
        if blocker_identity_name is not None:
            queryset = queryset.filter(blocker_identity__name=blocker_identity_name)
        return queryset

    def get_serializer_class(self):
        print('in get serializer')
        return BlockIdentitySerializer


class ForgetPasswordViewset(ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        forget_password_serializer = ForgetPasswordSerializer(data=request.POST)
        if forget_password_serializer.is_valid():
            send_sms = False
            if 'email' in forget_password_serializer.validated_data:
                try:
                    user = User.objects.get(email=forget_password_serializer.validated_data['email'])
                except User.DoesNotExist:
                    return Response({'detail': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
            elif 'mobile' in forget_password_serializer.validated_data:
                send_sms = True
                try:
                    profile = Profile.objects.get(mobile__in=forget_password_serializer.validated_data['mobile'])
                except Profile.DoesNotExist:
                    return Response({'detail': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
                user = User.objects.get(pk=profile.profile_user)
            else:
                return Response({'detail': 'please insert email or mobile'}, status=status.HTTP_400_BAD_REQUEST)
            random_number = random_with_N_digits(5)
            # code = '‫‪WiniO-‬‬' + str(random_number)
            user_code = UserCode.objects.create(code=random_number, user=user)
            user_code.save()
            if send_sms is True:
                print('sms')
                # send random number via sms
            else:
                print('email')
                # send random number via email
                subject = ' بازیابی رمز عبور '
                message = settings.EMAIL_TEXT + '\n' + ' کد : ' + str(user_code.code)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                send_mail(subject, message, email_from, recipient_list)
            return Response({'detail': 'code sended'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class UserCodeViewset(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = UserCode.objects.all()
        return queryset

    def get_serializer_class(self):
        return UserCodeSerializer

    @list_route(methods=['post'], permission_classes=[AllowAny])
    def change_password(self, request):
        code = request.data.get('code', None)
        password = request.data.get('password')
        if code is not None:
            try:
                user_code = UserCode.objects.get(code=code, used=False)
            except UserCode.DoesNotExist:
                return Response({'detail': 'code not found or used before'}, status=status.HTTP_404_NOT_FOUND)
            user = User.objects.get(pk=user_code.user_id)
            user.set_password(password)
            user_code.used = True
            user_code.save()
        return Response({'detail': 'password changed'}, status=status.HTTP_200_OK)


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
