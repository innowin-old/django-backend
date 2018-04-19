import requests
import json
import base64
from django.core.files.base import ContentFile
from django.conf import settings

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField, FileField, EmailField, IntegerField, ListField, \
    URLField, BooleanField
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from base.serializers import BaseSerializer
from .utils import send_verification_mail
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
        profile.save()
        email = EmailMessage(
            ' تایید حساب کاربری ',
            'https://daneshboom.ir/email/accept?token=123242',
            'amir@localhost',
            [user.email]
        )
        email.send()
        return user

    def update(self, instance, validated_data):
        user = User.objects.get(pk=instance.id)
        user_validated_data = self.get_user_validated_args(**validated_data)
        for key in user_validated_data:
            setattr(user, key, validated_data.get(key))
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
        user.save()

        profile = Profile.objects.get(profile_user=user)
        profile_validated_data = self.get_profile_validated_data(**validated_data)
        for key in profile_validated_data:
            setattr(profile, key, validated_data.get(key))
        profile.save()
        send_verification_mail(user=user)
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
        for key in profile_validated_data:
            setattr(profile, key, validated_data.get(key))
        profile.save()
        email = EmailMessage(
            ' تایید حساب کاربری ',
            'https://daneshboom.ir/email/accept?token=123242',
            'amir@localhost',
            [user.email]
        )
        email.send()
        return user

    def update(self, instance, validated_data):
        user = User.objects.get(pk=instance.id)
        user_validated_data = self.get_user_validated_args(**validated_data)
        for key in user_validated_data:
            setattr(user, key, validated_data.get(key))
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
        user.save()

        profile = Profile.objects.get(profile_user=user)
        profile_validated_data = self.get_profile_validated_data(**validated_data)
        for key in profile_validated_data:
            setattr(profile, key, validated_data.get(key))
        profile.save()
        send_verification_mail(user=user)
        return user

    def get_user_validated_args(self, **kwargs):
        user_kwargs = {'username': kwargs['username']}
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
    class Meta:
        model = Identity
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class IdentityMiniSerializer(BaseSerializer):
    identity_user = UserMiniSerializer()

    class Meta:
        model = Identity
        exclude = ['updated_time']


class ProfileSerializer(BaseSerializer):
    image_url = serializers.RelatedField(source='profile_media', read_only=True)

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

    def create(self, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'education_user' not in validated_data:
            validated_data['education_user'] = request.user
        research = Education.objects.create(**validated_data)
        return research

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'education_user' not in validated_data:
            instance.education_user = request.user
        else:
            instance.education_user = validated_data['education_user']
        instance.grade = validated_data['grade']
        instance.university = validated_data['university']
        instance.field_of_study = validated_data['field_of_study']
        instance.average = validated_data['average']
        instance.description = validated_data['description']
        instance.save()
        return instance


class ResearchSerializer(BaseSerializer):
    class Meta:
        model = Research
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'research_user' not in validated_data:
            validated_data['research_user'] = request.user
        research = Research.objects.create(**validated_data)
        return research

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'research_user' not in validated_data:
            instance.research_user = request.user
        else:
            instance.research_user = validated_data['research_user']
        instance.title = validated_data['title']
        instance.url = validated_data['url']
        instance.author = validated_data['author']
        instance.publication = validated_data['publication']
        instance.year = validated_data['year']
        instance.page_count = validated_data['page_count']
        instance.save()
        return instance


class CertificateSerializer(BaseSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'certificate_user' not in validated_data:
            validated_data['certificate_user'] = request.user
        certificate = Certificate.objects.create(**validated_data)
        return certificate

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'certificate_user' not in validated_data:
            instance.certificate_user = request.user
        else:
            instance.certificate_user = validated_data['certificate_user']
        instance.title = validated_data['title']
        instance.picture_media = validated_data['picture_media']
        instance.save()
        return instance


class WorkExperienceSerializer(BaseSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'work_experience_user' not in validated_data:
            validated_data['work_experience_user'] = request.user
        experience = WorkExperience.objects.create(**validated_data)
        return experience

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'work_experience_user' not in validated_data:
            instance.work_experience_user = request.user
        else:
            instance.work_experience_user = validated_data['work_experience_user']
        instance.name = validated_data['name']
        instance.work_experience_organization = validated_data['work_experience_organization']
        instance.position = validated_data['position']
        instance.status = validated_data['status']
        instance.save()
        return instance


class SkillSerializer(BaseSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'skill_user' not in validated_data:
            validated_data['skill_user'] = request.user
        skill = Skill.objects.create(**validated_data)
        return skill

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'skill_user' not in validated_data:
            instance.skill_user = request.user
        else:
            instance.skill_user = validated_data['skill_user']
        instance.title = validated_data['title']
        instance.tag = validated_data['tag']
        instance.description = validated_data['description']
        instance.save()
        return instance


class BadgeSerializer(BaseSerializer):
    class Meta:
        model = Badge
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'badge_user' not in validated_data:
            validated_data['badge_user'] = request.user
        badge = Badge.objects.create(**validated_data)
        return badge

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'badge_user' not in validated_data:
            instance.badge_user = request.user
        else:
            instance.badge_user = validated_data['badge_user']
        instance.title = validated_data['title']
        instance.save()
        return instance


class IdentityUrlSerilizer(BaseSerializer):
    class Meta:
        model = IdentityUrl
        fields = '__all__'
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
