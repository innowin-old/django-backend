import requests
import json
import base64

from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    IntegerField,
    ListField,
    URLField,
    Serializer,
    ValidationError
)
from base.serializers import BaseSerializer
from media.serializers import MediaMiniSerializer
from organizations.utils import OrganizationListSerializer
from organizations.models import Confirmation, Organization
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
    Device,
    StrengthStates,
    UserMetaData
)
from .utils import add_user_to_default_exchange


class SuperAdminUserSerializer(ModelSerializer):
    public_email = EmailField(required=False)
    national_code = CharField(required=False, max_length=20, allow_blank=True)
    profile_media = IntegerField(required=False, allow_null=True)
    birth_date = CharField(required=False, max_length=10, allow_blank=True)
    fax = CharField(required=False, allow_blank=True)
    telegram_account = CharField(required=False, max_length=256, allow_blank=True)
    description = CharField(required=False, allow_blank=True)
    web_site = ListField(child=URLField(required=False), required=False)
    phone = ListField(child=CharField(max_length=23, required=False), required=False)
    mobile = ListField(child=CharField(max_length=23, required=False), required=False)
    password = CharField(max_length=255)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'date_joined', 'is_staff',
                  'is_active', 'web_site', 'public_email', 'national_code', 'profile_media', 'birth_date', 'fax',
                  'telegram_account', 'description', 'phone', 'mobile']

    def create(self, validated_data):
        user_validated_data = self.get_user_validated_args(**validated_data)
        user = User.objects.create(**user_validated_data)
        user.set_password(validated_data['password'])
        user.save()
        profile_validated_data = self.get_profile_validated_data(**validated_data)
        profile = Profile.objects.get(profile_user=user)
        for key in profile_validated_data:
            setattr(profile, key, validated_data.get(key))
        user_strength = StrengthStates.objects.get(strength_user=user)
        if validated_data.get('first_name') is not None and validated_data.get('last_name') is not None:
            profile.profile_strength += 5
            profile.save()
            user_strength.first_last_name_obtained = True

        if 'profile_media' in profile_validated_data:
            profile.profile_strength += 10
            profile.save()
            user_strength.profile_media_obtained = True
        user_strength.registration_obtained = True
        user_strength.save()
        # add user to default exchange
        add_user_to_default_exchange(user)
        return user

    def update(self, instance, validated_data):
        user = User.objects.get(pk=instance.id)
        profile = Profile.objects.get(profile_user=user)
        user_validated_data = self.get_user_validated_args(**validated_data)
        try:
            user_strength = StrengthStates.objects.get(user_strength=user)
        except StrengthStates.DoesNotExist:
            user_strength = StrengthStates.objects.create(user_strength=user)
        # check for first name strength rate
        if 'first_name' in user_validated_data and user_validated_data['first_name'] != '':
            user.first_name = user_validated_data['first_name']
            if (user.first_name is None or user.first_name == '') and (
                    user.last_name is not None or user.last_name != ''):
                profile.profile_strength += 5
                user_strength.first_last_name_obtained = True
        # check for last name strength rate
        if 'last_name' in user_validated_data and user_validated_data['last_name'] != '':
            user.last_name = user_validated_data['last_name']
            if (user.last_name is None or user.last_name == '') and (
                    user.first_name is not None or user.first_name != ''):
                profile.profile_strength += 5
                user_strength.first_last_name_obtained = True
        # set validated data to user object
        for key in user_validated_data:
            if key != 'first_name' and key != 'last_name':
                setattr(user, key, user_validated_data.get(key))
        # set password if is in validated data
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
        user.save()

        profile_validated_data = self.get_profile_validated_data(**validated_data)

        if 'profile_media' in profile_validated_data and profile_validated_data['profile_media'] != '' and \
                profile_validated_data['profile_media'] is not None:
            profile.profile_media = profile_validated_data['profile_media']
            if profile.profile_media == '' or profile.profile_media is None:
                profile.profile_strength += 10
                user_strength.profile_media_obtained = True

        # set validated data to profile object
        for key in profile_validated_data:
            if key != 'profile_media':
                setattr(profile, key, validated_data.get(key))

        profile.save()
        user_strength.save()
        return user

    def get_user_validated_args(self, **kwargs):
        user_kwargs = {'username': kwargs['username']}
        if 'first_name' in kwargs:
            user_kwargs['first_name'] = kwargs['first_name']
        if 'last_name' in kwargs:
            user_kwargs['last_name'] = kwargs['last_name']
        if 'email' in kwargs:
            user_kwargs['email'] = kwargs['email']
        if 'is_staff' in kwargs:
            user_kwargs['is_staff'] = kwargs['is_staff']
        if 'is_active' in kwargs:
            user_kwargs['is_active'] = kwargs['is_active']
        if 'date_joined' in kwargs:
            user_kwargs['date_joined'] = kwargs['date_joined']
        return user_kwargs

    def get_profile_validated_data(self, **kwargs):
        profile_kwargs = {}
        if 'public_email' in kwargs:
            profile_kwargs['public_email'] = kwargs['public_email']
        if 'national_code' in kwargs:
            profile_kwargs['national_code'] = kwargs['national_code']
        if 'profile_media' in kwargs:
            profile_kwargs['profile_media'] = kwargs['profile_media']
        if 'birth_date' in kwargs:
            profile_kwargs['birth_date'] = kwargs['birth_date']
        if 'fax' in kwargs:
            profile_kwargs['fax'] = kwargs['fax']
        if 'telegram_account' in kwargs:
            profile_kwargs['telegram_account'] = kwargs['telegram_account']
        if 'description' in kwargs:
            profile_kwargs['description'] = kwargs['description']
        if 'web_site' in kwargs:
            profile_kwargs['web_site'] = kwargs['web_site']
        if 'phone' in kwargs:
            profile_kwargs['phone'] = kwargs['phone']
        if 'mobile' in kwargs:
            profile_kwargs['mobile'] = kwargs['mobile']
        return profile_kwargs


class UserSerializer(ModelSerializer):
    public_email = EmailField(required=False)
    national_code = CharField(required=False, max_length=20, allow_blank=True)
    profile_media = IntegerField(required=False, allow_null=True)
    birth_date = CharField(required=False, max_length=10, allow_blank=True)
    fax = CharField(required=False, allow_blank=True)
    telegram_account = CharField(required=False, max_length=256, allow_blank=True)
    description = CharField(required=False, allow_blank=True)
    web_site = ListField(child=URLField(required=False), required=False)
    phone = ListField(child=CharField(max_length=23, required=False), required=False)
    mobile = ListField(child=CharField(max_length=23, required=False), required=False)
    password = CharField(max_length=255)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'password', 'date_joined',
                  'web_site', 'public_email', 'national_code', 'profile_media', 'birth_date', 'fax', 'telegram_account',
                  'description', 'phone', 'mobile']

    def create(self, validated_data):
        user_validated_data = self.get_user_validated_args(**validated_data)
        user = User.objects.create(**user_validated_data)
        user.set_password(validated_data['password'])
        user.save()
        profile_validated_data = self.get_profile_validated_data(**validated_data)
        profile = Profile.objects.get(profile_user=user)
        # set validated data to profile object
        for key in profile_validated_data:
            setattr(profile, key, validated_data.get(key))
        profile.save()
        user_strength = StrengthStates.objects.get(strength_user=user)
        # check for first & last name strength rate
        if validated_data.get('first_name') is not None and validated_data.get('last_name') is not None:
            profile.profile_strength += 5
            profile.save()
            user_strength.first_last_name_obtained = True

        # check for profile media strength rate
        if 'profile_media' in profile_validated_data:
            profile.profile_strength += 10
            profile.save()
            user_strength.profile_media_obtained = True
        user_strength.registration_obtained = True
        user_strength.save()
        # add user to default exchange
        add_user_to_default_exchange(user)
        return user

    def update(self, instance, validated_data):
        user = User.objects.get(pk=instance.id)
        profile = Profile.objects.get(profile_user=user)
        user_validated_data = self.get_user_validated_args(**validated_data)
        try:
            user_strength = StrengthStates.objects.get(user_strength=user)
        except StrengthStates.DoesNotExist:
            user_strength = StrengthStates.objects.create(user_strength=user)
        # check for first name strength rate
        if 'first_name' in user_validated_data and user_validated_data['first_name'] != '':
            user.first_name = user_validated_data['first_name']
            if (user.first_name is None or user.first_name == '') and (
                    user.last_name is not None or user.last_name != ''):
                profile.profile_strength += 5
                user_strength.first_last_name_obtained = True
        # check for last name strength rate
        if 'last_name' in user_validated_data and user_validated_data['last_name'] != '':
            user.last_name = user_validated_data['last_name']
            if (user.last_name is None or user.last_name == '') and (
                    user.first_name is not None or user.first_name != ''):
                profile.profile_strength += 5
                user_strength.first_last_name_obtained = True
        # set validated data to user object
        for key in user_validated_data:
            if key != 'first_name' and key != 'last_name':
                setattr(user, key, user_validated_data.get(key))
        if 'password' in validated_data:
            user.set_password(validated_data['password'])

        user.save()

        profile_validated_data = self.get_profile_validated_data(**validated_data)

        # check for profile media strength rate
        if 'profile_media' in profile_validated_data and profile_validated_data['profile_media'] != '' and \
                profile_validated_data['profile_media'] is not None:
            profile.profile_media = profile_validated_data['profile_media']
            if profile.profile_media == '' or profile.profile_media is None:
                profile.profile_strength += 10
                user_strength.profile_media_obtained = True

        # set validated data to profile object
        for key in profile_validated_data:
            if key != 'profile_media':
                setattr(profile, key, validated_data.get(key))

        profile.save()
        user_strength.save()

        return user

    def validate_first_name(self, value):
        if len(value) > 20:
            error = {'message': "maximum length for first name is 20 character"}
            raise ValidationError(error)
        return value


    def validate_last_name(self, value):
        if len(value) > 20:
            error = {'message': "maximum length for last name is 20 character"}
            raise ValidationError(error)
        return value

    def validate_username(self, value):
        if len(value) < 5:
            error = {'message': "minimum length for last name is 5 character"}
            raise ValidationError(error)
        if len(value) > 32:
            error = {'message': "minimum length for last name is 5 character"}
            raise ValidationError(error)
        return value

    def get_user_validated_args(self, **kwargs):
        user_kwargs = {}
        if 'username' in kwargs:
            user_kwargs['username'] = kwargs['username']
        if 'first_name' in kwargs:
            user_kwargs['first_name'] = kwargs['first_name']
        if 'last_name' in kwargs:
            user_kwargs['last_name'] = kwargs['last_name']
        if 'email' in kwargs:
            user_kwargs['email'] = kwargs['email']
        return user_kwargs

    def get_profile_validated_data(self, **kwargs):
        profile_kwargs = {}
        if 'public_email' in kwargs:
            profile_kwargs['public_email'] = kwargs['public_email']
        if 'national_code' in kwargs:
            profile_kwargs['national_code'] = kwargs['national_code']
        if 'profile_media' in kwargs:
            profile_kwargs['profile_media'] = kwargs['profile_media']
        if 'birth_date' in kwargs:
            profile_kwargs['birth_date'] = kwargs['birth_date']
        if 'fax' in kwargs:
            profile_kwargs['fax'] = kwargs['fax']
        if 'telegram_account' in kwargs:
            profile_kwargs['telegram_account'] = kwargs['telegram_account']
        if 'description' in kwargs:
            profile_kwargs['description'] = kwargs['description']
        if 'web_site' in kwargs:
            profile_kwargs['web_site'] = kwargs['web_site']
        if 'phone' in kwargs:
            profile_kwargs['phone'] = kwargs['phone']
        if 'mobile' in kwargs:
            profile_kwargs['mobile'] = kwargs['mobile']
        return profile_kwargs


class UserListViewSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserMiniSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class IdentitySerializer(BaseSerializer):
    identity_user = UserMiniSerializer()
    identity_organization = OrganizationListSerializer()

    class Meta:
        model = Identity
        exclude = ['updated_time', 'child_name', 'delete_flag']


class IdentityMiniSerializer(BaseSerializer):
    identity_user = UserMiniSerializer()

    class Meta:
        model = Identity
        depth = 1
        exclude = ['updated_time']


class ProfileSerializer(BaseSerializer):
    class Meta:
        model = Profile
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }

    def update(self, instance, validated_data):
        request = self.context.get('request')
        # fill profile_user field for super users
        if not request.user.is_superuser or 'profile_user' not in validated_data:
            instance.profile_user = request.user
        else:
            instance.profile_user = validated_data.get('profile_user', instance.profile_user)

        # check for profile media strength rate
        if 'profile_media' in validated_data and (
                validated_data['profile_media'] != '' or validated_data['profile_media'] is not None):
            if instance.profile_media == '' or instance.profile_media is None:
                try:
                    user_strength = StrengthStates.objects.get(strength_user=instance.profile_user)
                except StrengthStates.DoesNotExist:
                    user_strength = StrengthStates.objects.create(strength_user=instance.profile_user)
                instance.profile_strength += 10
                user_strength.profile_media_obtained = True
            instance.profile_media = validated_data['profile_media']

        # set validated data to profile instance
        for key in validated_data:
            if key != 'profile_user' and key != 'profile_media':
                setattr(instance, key, validated_data.get(key))

        instance.save()
        return instance


class ProfileListSerializer(BaseSerializer):
    profile_user = UserMiniSerializer()
    profile_media = MediaMiniSerializer()

    class Meta:
        model = Profile
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class EducationSerializer(BaseSerializer):
    class Meta:
        model = Education
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'education_user': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        # fill education user for super users
        if not request.user.is_superuser or 'education_user' not in validated_data:
            validated_data['education_user'] = request.user
        education = Education.objects.create(**validated_data)
        education.save()
        # check for education user strength rate
        self.check_education_profile_strength(validated_data['education_user'])
        return education

    def update(self, instance, validated_data):
        request = self.context.get("request")
        # fill education user for super users
        if not request.user.is_superuser or 'education_user' not in validated_data:
            instance.education_user = request.user
        else:
            instance.education_user = validated_data['education_user']

        for key in validated_data:
            if key != 'education_user':
                setattr(instance, key, validated_data.get(key))

        instance.save()
        return instance

    def check_education_profile_strength(self, user):
        educations = Education.objects.filter(education_user=user)
        try:
            user_strength = StrengthStates.objects.get(strength_user=user)
        except StrengthStates.DoesNotExist:
            user_strength = StrengthStates.objects.create(strength_user=user)
        if educations.count() == 1 and user_strength.education_obtained is False:
            try:
                profile = Profile.objects.get(profile_user=user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(profile_user=user)
            profile.profile_strength += 5
            profile.save()
            user_strength.education_obtained = True
            user_strength.save()


class ResearchSerializer(BaseSerializer):
    class Meta:
        model = Research
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'research_user': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        # fill research_user for super users
        if not request.user.is_superuser or 'research_user' not in validated_data:
            validated_data['research_user'] = request.user
        research = Research.objects.create(**validated_data)
        return research

    def update(self, instance, validated_data):
        request = self.context.get("request")
        # fill research_user for super users
        if not request.user.is_superuser or 'research_user' not in validated_data:
            instance.research_user = request.user
        else:
            instance.research_user = validated_data['research_user']

        # set validated data to instance object
        for key in validated_data:
            if key != 'research_user':
                setattr(instance, key, validated_data.get(key))

        instance.save()
        return instance


class CertificateSerializer(BaseSerializer):
    class Meta:
        model = Certificate
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'certificate_user': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        # fill certificate_user for super users
        if not request.user.is_superuser or 'certificate_user' not in validated_data:
            validated_data['certificate_user'] = request.user
        certificate = Certificate.objects.create(**validated_data)
        return certificate

    def update(self, instance, validated_data):
        request = self.context.get("request")
        # fill certificate_user for super users
        if not request.user.is_superuser or 'certificate_user' not in validated_data:
            instance.certificate_user = request.user
        else:
            instance.certificate_user = validated_data.get('certificate_user')

        # set validated data to certificate instance
        for key in validated_data:
            if key != 'certificate_user':
                setattr(instance, key, validated_data.get(key))

        instance.save()
        return instance


class WorkExperienceSerializer(BaseSerializer):
    class Meta:
        model = WorkExperience
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'status': {'read_only': True},
            'work_experience_user': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        # fill work_experience_user for super users
        if not request.user.is_superuser or 'work_experience_user' not in validated_data:
            validated_data['work_experience_user'] = request.user
        experience = WorkExperience.objects.create(**validated_data)
        experience.save()

        # create confirmation object
        organization_identity = Identity.objects.get(identity_organization=experience.work_experience_organization)
        user_identity = Identity.objects.get(identity_user=experience.work_experience_user)
        description = experience.work_experience_user.username + ' - ' + experience.work_experience_organization.official_name
        confirmation = Confirmation.objects.create(
            confirmation_corroborant=organization_identity,
            confirmation_confirmed=user_identity,
            title=organization_identity.name,
            description=description,
            link='https://daneshboom.ir/',
            confirmation_parent=experience
        )
        confirmation.save()
        # check for experience profile points
        self.check_experience_profile_strength(validated_data.get('work_experience_user'))
        return experience

    def update(self, instance, validated_data):
        request = self.context.get("request")
        # fill work_experience_user for super users
        if not request.user.is_superuser or 'work_experience_user' not in validated_data:
            instance.work_experience_user = request.user
        else:
            instance.work_experience_user = validated_data['work_experience_user']

        # set validated data to work experience instance
        for key in validated_data:
            if key != 'work_experience_user':
                setattr(instance, key, validated_data.get(key))

        instance.save()
        return instance

    def check_experience_profile_strength(self, user):
        works = WorkExperience.objects.filter(work_experience_user=user)
        try:
            user_strength = StrengthStates.objects.get(strength_user=user)
        except StrengthStates.DoesNotExist:
            user_strength = StrengthStates.objects.create(strength_user=user)
        if user_strength.work_obtained is False and works.count() == 1:
            try:
                profile = Profile.objects.get(profile_user=user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(profile_user=user)
            profile.profile_strength += 5
            profile.save()
            user_strength.work_obtained = True
            user_strength.save()


class SkillSerializer(BaseSerializer):
    class Meta:
        model = Skill
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'skill_user': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        # fill skill_user for super users
        if not request.user.is_superuser or 'skill_user' not in validated_data:
            validated_data['skill_user'] = request.user
        skill = Skill.objects.create(**validated_data)
        return skill

    def update(self, instance, validated_data):
        request = self.context.get("request")
        # fill skill_user for super users
        if not request.user.is_superuser or 'skill_user' not in validated_data:
            instance.skill_user = request.user
        else:
            instance.skill_user = validated_data['skill_user']

        # set validated data to skill instance
        for key in validated_data:
            if key != 'skill_user':
                setattr(instance, key, validated_data.get(key))

        instance.save()
        return instance


class BadgeSerializer(BaseSerializer):
    class Meta:
        model = Badge
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'badge_user': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'badge_user' not in validated_data:
            validated_data['badge_user'] = request.user
        badge = Badge.objects.create(**validated_data)
        badge.save()
        self.check_badge_profile_strength(badge.badge_user)
        return badge

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'badge_user' not in validated_data:
            instance.badge_user = request.user
        else:
            instance.badge_user = validated_data['badge_user']

        for key in validated_data:
            if key != 'badge_user':
                setattr(instance, key, validated_data.get(key))

        instance.save()
        return instance

    def check_badge_profile_strength(self, user):
        badges = Badge.objects.filter(badge_user=user)
        try:
            user_strength = StrengthStates.objects.get(strength_user=user)
        except StrengthStates.DoesNotExist:
            user_strength = StrengthStates.objects.create(strength_user=user)
        if user_strength.badge_obtained is False and badges.count() == 1:
            try:
                profile = Profile.objects.get(profile_user=user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(profile_user=user)
            profile.profile_strength += 5
            profile.save()
            user_strength.badge_obtained = True
            user_strength.save()


class IdentityUrlSerilizer(BaseSerializer):
    class Meta:
        model = IdentityUrl
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class UserArticleSerializer(BaseSerializer):
    class Meta:
        model = UserArticle
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'user_article_related_user': {'read_only': True},
            'doi_meta': {'read_only': True},
            'publisher': {'read_only': True},
            'title': {'read_only': True},
            'article_author': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        url = validated_data['doi_link']
        req = requests.get(url, headers={'Accept': 'application/vnd.citationstyles.csl+json', })
        article = req.json()
        user_article = UserArticle.objects.create(doi_link=url, doi_meta=article, publisher=article['publisher'],
                                                  title=article['title'], article_author=article['author'],
                                                  user_article_related_user=request.user)
        return user_article


class UserArticleListSerializer(BaseSerializer):
    doi_list = CharField(required=False)

    class Meta:
        model = UserArticle
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'user_article_related_user': {'read_only': True},
            'doi_meta': {'read_only': True},
            'publisher': {'read_only': True},
            'title': {'read_only': True},
            'article_author': {'read_only': True},
            'doi_link': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        doi_list = json.loads(validated_data['doi_list'])
        for item in doi_list['doi_link_list']:
            url = item['doi_link']
            req = requests.get(url, headers={'Accept': 'application/vnd.citationstyles.csl+json', })
            article = req.json()
            user_article = UserArticle.objects.create(doi_link=url, doi_meta=article, publisher=article['publisher'],
                                                      title=article['title'], article_author=article['author'],
                                                      user_article_related_user=request.user)
            user_article.save()
        return user_article


class UserArticleRisSerializer(BaseSerializer):
    ris_file = CharField(required=False)

    class Meta:
        model = UserArticle
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'user_article_related_user': {'read_only': True},
            'doi_meta': {'read_only': True},
            'publisher': {'read_only': True},
            'title': {'read_only': True},
            'article_author': {'read_only': True},
            'doi_link': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user_article_related_user'] = request.user
        ris_file = validated_data.pop('ris_file')
        format, imgstr = ris_file.split(';base64,')
        ext = format.split('/')[-1]
        filelines = ContentFile(base64.b64decode(imgstr), name='temp.' + ext).readlines()
        filelines_decoded = []
        for fileline in filelines:
            fileline_decoded = fileline.decode()
            filelines_decoded.append(fileline_decoded)
        map_array = settings.TAG_KEY_MAPPING
        doi_media = {}
        authors_array = []
        publishers_array = []
        for item in filelines_decoded:
            item_split = item.split('-')
            first_item = item_split[0].strip()
            if map_array[first_item] == 'first_authors':
                authors_array.append(item_split[1].strip())
            if map_array[first_item] == 'publisher':
                publishers_array.append(item_split[1].strip())
            if map_array[first_item] == 'primary_title':
                validated_data['title'] = item_split[1].strip()
                doi_media['title'] = item_split[1].strip()
            if map_array[first_item] == 'abstract':
                doi_media['abstract'] = item_split[1].strip()
            if map_array[first_item] == 'date':
                doi_media['date'] = item_split[1].strip()
            if map_array[first_item] == 'doi':
                doi_media['doi'] = item_split[1].strip()
            if map_array[first_item] == 'edition':
                doi_media['edition'] = item_split[1].strip()
        validated_data['article_author'] = authors_array
        doi_media['authors'] = authors_array
        doi_media['publishers'] = publishers_array
        article = UserArticle.objects.create(**validated_data, doi_meta=doi_media, doi_link='http://doi.org/')
        return article


class DeviceSerializer(BaseSerializer):
    class Meta:
        model = Device
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class UserMetaDataSerializer(BaseSerializer):
    class Meta:
        model = UserMetaData
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'user_meta_related_user': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'user_meta_related_user' not in validated_data:
            validated_data['user_meta_related_user'] = request.user
        if validated_data['user_meta_type'] == 'phone' or validated_data['user_meta_type'] == 'mobile':
            print('phone or mobile')
            user_related_meta_data = UserMetaData.objects.filter(
                user_meta_related_user=validated_data['user_meta_related_user'],
                user_meta_type=validated_data['user_meta_type'])
            if user_related_meta_data.count() >= 2:
                error = {'message': "user have more than 2 " + validated_data['user_meta_type'] + ' !'}
                raise ValidationError(error)
        user_meta_data = UserMetaData.objects.create(**validated_data)
        user_meta_data.save()
        return user_meta_data


class ForgetPasswordSerializer(Serializer):
    mobile = CharField(required=False, max_length=20)
    email = EmailField(required=False)


class OrganizationMiniSerializer(BaseSerializer):
    class Meta:
        model = Organization
        fields = ['username', 'official_name', 'national_code', 'country', 'province', 'city', 'ownership_type', 'business_type', 'owner']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class UserOrganizationSerializer(BaseSerializer):
    organization = OrganizationMiniSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'organization']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        organization_data = validated_data.pop('organization')
        user = User.objects.create_user(**validated_data)
        # add user to default exchange
        add_user_to_default_exchange(user)
        organization = Organization.objects.create(owner=user, **organization_data)
        response = {
            'id': user.id,
            'username': user.username,
            'password': user.password,
            'first_name': user.last_name,
            'email': user.email,
            'organization': organization
        }
        return response
