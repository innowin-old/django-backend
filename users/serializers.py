import requests
import json

from rest_framework.serializers import ModelSerializer, CharField
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
    Badge,
    IdentityUrl,
    UserArticle
)


class SuperAdminUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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
        user_article = UserArticle.objects.create(doi_link=url, doi_meta=article, publisher=article['publisher'], title=article['title'], article_author=article['author'], user_article_related_user=request.user)
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
            user_article = UserArticle.objects.create(doi_link=url, doi_meta=article, publisher=article['publisher'], title=article['title'], article_author=article['author'], user_article_related_user=request.user)
            user_article.save()
        return user_article