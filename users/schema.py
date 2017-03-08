import django_filters
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.core.signing import TimestampSigner
from django.template import loader
from django_filters import OrderingFilter
from graphene import relay, Field, AbstractType, resolve_only_args,\
    String, Boolean, Int, Float, List, ID
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

from danesh_boom.viewer_fields import ViewerFields
from users.models import Profile, Education, Research, Certificate,\
    WorkExperience, Skill
from utils.gravatar import get_gravatar_url


#################### Skill #######################

class SkillFilter(django_filters.FilterSet):

    class Meta:
        model = Skill
        fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'tag': ['icontains'],
            'description': ['exact', 'icontains', 'istartswith'],
        }
        filter_overrides = {
             ArrayField: {
                 'filter_class': django_filters.CharFilter,
                 'extra': lambda f: {
                     'lookup_expr': 'icontains',
                 },
             }
        }

    order_by = OrderingFilter(fields=('id', 'title',))


class SkillNode(DjangoObjectType):

    class Meta:
        model = Skill
        interfaces = (relay.Node, )


class CreateSkillMutation(relay.ClientIDMutation):

    class Input:
        title = String(required=True)
        tag = List(String)
        description = String()

    skill = Field(SkillNode)
    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        title = input.get('title')
        tag = input.get('tag', [])
        description = input.get('description', '')

        # create skill
        new_skill = Skill(
            user=user,
            title=title,
            tag=tag,
            description=description
        )
        try:
            new_skill.full_clean()
            new_skill.save()
        except Exception as e:
            return CreateSkillMutation(
                skill=None,
                success=False,
                message=str(e),
            )

        return CreateSkillMutation(skill=new_skill, success=True)


class UpdateSkillMutation(relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        title = String(required=True)
        tag = List(String)
        description = String()

    skill = Field(SkillNode)
    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        skill_id = from_global_id(id)[1]
        skill = Skill.objects.get(pk=skill_id)
        if skill.user != user:
            return UpdateSkillMutation(
                skill=None,
                success=False,
                message="Invalid Access to Skill",
            )

        title = input.get('title')
        tag = input.get('tag', [])
        description = input.get('description', '')

        # update skill
        skill.title = title
        skill.tag = tag
        skill.description = description
        try:
            skill.full_clean()
            skill.save()
        except Exception as e:
            return UpdateSkillMutation(
                skill=None,
                success=False,
                message=str(e),
            )

        return UpdateSkillMutation(skill=skill, success=True)


class DeleteSkillMutation(relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        skill_id = from_global_id(id)[1]
        skill = Skill.objects.get(pk=skill_id)
        if skill.user != user:
            return DeleteSkillMutation(
                success=False,
                message="Invalid Access to Skill",
            )

        # delete skill
        skill.delete()

        return DeleteSkillMutation(success=True)


#################### Work Experience #######################

class WorkExperienceFilter(django_filters.FilterSet):

    class Meta:
        model = WorkExperience
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'position': ['exact', 'icontains', 'istartswith'],
            'from_date': ['exact', 'gte', 'lte'],
            'to_date': ['exact', 'gte', 'lte'],
        }

    order_by = OrderingFilter(
        fields=(
            'id',
            'name',
            'position',
            'from_date',
            'to_date'))


class WorkExperienceNode(DjangoObjectType):

    class Meta:
        model = WorkExperience
        interfaces = (relay.Node, )


class CreateWorkExperienceMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        name = String(required=True)
        position = String(required=True)
        from_date = String()
        to_date = String()

    work_experience = Field(WorkExperienceNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        name = input.get('name')
        position = input.get('position')
        from_date = input.get('from_date', '')
        to_date = input.get('to_date', '')

        # create work experience
        new_work_experience = WorkExperience(
            user=user,
            name=name,
            position=position,
            from_date=from_date,
            to_date=to_date,
        )
        try:
            new_work_experience.full_clean()
            new_work_experience.save()
        except Exception as e:
            raise Exception(str(e))

        return CreateWorkExperienceMutation(
            work_experience=new_work_experience,
        )


class UpdateWorkExperienceMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        name = String(required=True)
        position = String(required=True)
        from_date = String()
        to_date = String()

    work_experience = Field(WorkExperienceNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        work_experience_id = from_global_id(id)[1]
        work_experience = WorkExperience.objects.get(pk=work_experience_id)
        if work_experience.user != user:
            raise Exception("Invalid Access to Work Experience")

        name = input.get('name')
        position = input.get('position')
        from_date = input.get('from_date', '')
        to_date = input.get('to_date', '')

        # update work experience
        work_experience.name = name
        work_experience.position = position
        work_experience.from_date = from_date
        work_experience.to_date = to_date
        try:
            work_experience.full_clean()
            work_experience.save()
        except Exception as e:
            raise Exception(str(e))

        return UpdateWorkExperienceMutation(
            work_experience=work_experience
        )


class DeleteWorkExperienceMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        work_experience_id = from_global_id(id)[1]
        work_experience = WorkExperience.objects.get(pk=work_experience_id)
        if work_experience.user != user:
            raise Exception("Invalid Access to Work Experience")

        # delete work experience
        work_experience.delete()

        return DeleteWorkExperienceMutation(deleted_id=id)


#################### Certificate #######################

class CertificateFilter(django_filters.FilterSet):

    class Meta:
        model = Certificate
        fields = {
            'title': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(
        fields=('id', 'title'))


class CertificateNode(DjangoObjectType):

    class Meta:
        model = Certificate
        interfaces = (relay.Node, )


class CreateCertificateMutation(relay.ClientIDMutation):

    class Input:
        title = String(required=True)

    certificate = Field(CertificateNode)
    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        title = input.get('title')
        files = context.FILES
        picture = files.get('picture', None)

        # create certificate
        new_certificate = Certificate(
            user=user,
            title=title,
            picture=picture,
        )
        try:
            new_certificate.full_clean()
            new_certificate.save()
        except Exception as e:
            return CreateCertificateMutation(
                certificate=None,
                success=False,
                message=str(e),
            )

        return CreateCertificateMutation(
            certificate=new_certificate,
            success=True
        )


class UpdateCertificateMutation(relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        title = String(required=True)

    certificate = Field(CertificateNode)
    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        certificate_id = from_global_id(id)[1]
        certificate = Certificate.objects.get(pk=certificate_id)
        if certificate.user != user:
            return UpdateCertificateMutation(
                certificate=None,
                success=False,
                message="Invalid Access to Work Certificate",
            )

        title = input.get('title')
        files = context.FILES
        picture = files.get('picture', None)

        # update certificate
        certificate.title = title
        if picture:
            certificate.picture = picture
        try:
            certificate.full_clean()
            certificate.save()
        except Exception as e:
            return UpdateCertificateMutation(
                certificate=None,
                success=False,
                message=str(e),
            )

        return UpdateCertificateMutation(
            certificate=certificate,
            success=True
        )


class DeleteCertificateMutation(relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        certificate_id = from_global_id(id)[1]
        certificate = Certificate.objects.get(pk=certificate_id)
        if certificate.user != user:
            return DeleteCertificateMutation(
                success=False,
                message="Invalid Access to Work Certificate",
            )

        # delete certificate
        certificate.delete()

        return DeleteCertificateMutation(success=True)


#################### Research #######################

class ResearchFilter(django_filters.FilterSet):

    class Meta:
        model = Research
        fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'publication': ['exact', 'icontains', 'istartswith'],
            'author': ['icontains'],
            'year': ['exact', 'gte', 'lte'],
            'page_count': ['exact', 'gte', 'lte'],
        }
        filter_overrides = {
             ArrayField: {
                 'filter_class': django_filters.CharFilter,
                 'extra': lambda f: {
                     'lookup_expr': 'icontains',
                 },
             }
        }

    order_by = OrderingFilter(
        fields=(
            'id',
            'title',
            'publication',
            'year',
            'page_count'))


class ResearchNode(DjangoObjectType):

    class Meta:
        model = Research
        interfaces = (relay.Node, )


class CreateResearchMutation(relay.ClientIDMutation):

    class Input:
        title = String(required=True)
        url = String()
        author = List(String)
        publication = String()
        year = Int()
        page_count = Int()

    research = Field(ResearchNode)
    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        title = input.get('title')
        url = input.get('url', '')
        author = input.get('author', [])
        publication = input.get('publication', '')
        year = input.get('year', None)
        page_count = input.get('page_count', None)

        # create research
        new_research = Research(
            user=user,
            title=title,
            url=url,
            author=author,
            publication=publication,
            year=year,
            page_count=page_count,
        )
        try:
            new_research.full_clean()
            new_research.save()
        except Exception as e:
            return CreateResearchMutation(
                success=False,
                message=str(e)
            )

        return CreateResearchMutation(
            research=new_research,
            success=True
        )


class UpdateResearchMutation(relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        title = String(required=True)
        url = String()
        author = List(String)
        publication = String()
        year = Int()
        page_count = Int()

    research = Field(ResearchNode)
    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        research_id = from_global_id(id)[1]
        research = Research.objects.get(pk=research_id)
        if research.user != user:
            return UpdateResearchMutation(
                research=None,
                success=False,
                message="Invalid Access to Work Research",
            )

        title = input.get('title')
        url = input.get('url', '')
        author = input.get('author', [])
        publication = input.get('publication', '')
        year = input.get('year', None)
        page_count = input.get('page_count', None)

        # update research
        research.title = title
        research.url = url
        research.author = author
        research.publication = publication
        research.year = year
        research.page_count = page_count
        try:
            research.full_clean()
            research.save()
        except Exception as e:
            return UpdateResearchMutation(
                success=False,
                message=str(e)
            )

        return UpdateResearchMutation(
            research=research,
            success=True
        )


class DeleteResearchMutation(relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        research_id = from_global_id(id)[1]
        research = Research.objects.get(pk=research_id)
        if research.user != user:
            return DeleteResearchMutation(
                success=False,
                message="Invalid Access to Work Research",
            )

        # delete research
        research.delete()

        return DeleteResearchMutation(success=True)


#################### Education #######################

class EducationFilter(django_filters.FilterSet):

    class Meta:
        model = Education
        fields = {
            'grade': ['exact', 'icontains', 'istartswith'],
            'university': ['exact', 'icontains', 'istartswith'],
            'field_of_study': ['exact', 'icontains', 'istartswith'],
            'from_date': ['exact', 'gte', 'lte'],
            'to_date': ['exact', 'gte', 'lte'],
            'average': ['exact', 'gte', 'lte'],
            'description': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(
        fields=(
            'id',
            'grade',
            'university',
            'field_of_study',
            'from_date',
            'to_date',
            'average'))


class EducationNode(DjangoObjectType):

    class Meta:
        model = Education
        interfaces = (relay.Node, )


class CreateEducationMutation(relay.ClientIDMutation):

    class Input:
        grade = String(required=True)
        university = String(required=True)
        field_of_study = String(required=True)
        from_date = String()
        to_date = String()
        average = Float()
        description = String()

    education = Field(EducationNode)
    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        grade = input.get('grade')
        university = input.get('university')
        field_of_study = input.get('field_of_study')
        from_date = input.get('from_date', '')
        to_date = input.get('to_date', '')
        average = input.get('tag', None)
        description = input.get('description', '')

        # create research
        try:
            new_education = Education(
                user=user,
                grade=grade,
                university=university,
                field_of_study=field_of_study,
                from_date=from_date,
                to_date=to_date,
                average=average,
                description=description
            )
            new_education.full_clean()
            new_education.save()
        except Exception as e:
            return CreateEducationMutation(
                education=None,
                success=False,
                message=str(e)
            )

        return CreateEducationMutation(
            education=new_education,
            success=True
        )


class UpdateEducationMutation(relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        grade = String(required=True)
        university = String(required=True)
        field_of_study = String(required=True)
        from_date = String()
        to_date = String()
        average = Float()
        description = String()

    education = Field(EducationNode)
    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        education_id = from_global_id(id)[1]
        education = Education.objects.get(pk=education_id)
        if education.user != user:
            return UpdateEducationMutation(
                education=None,
                success=False,
                message="Invalid Access to Education",
            )

        grade = input.get('grade')
        university = input.get('university')
        field_of_study = input.get('field_of_study')
        from_date = input.get('from_date', '')
        to_date = input.get('to_date', '')
        average = input.get('tag', None)
        description = input.get('description', '')

        # update education
        education.grade = grade
        education.university = university
        education.field_of_study = field_of_study
        education.from_date = from_date
        education.to_date = to_date
        education.average = average
        education.description = description
        try:
            education.full_clean()
            education.save()
        except Exception as e:
            return UpdateEducationMutation(
                education=None,
                success=False,
                message=str(e)
            )

        return UpdateEducationMutation(
            education=education,
            success=True
        )


class DeleteEducationMutation(relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        education_id = from_global_id(id)[1]
        education = Education.objects.get(pk=education_id)
        if education.user != user:
            return DeleteEducationMutation(
                success=False,
                message="Invalid Access to Education",
            )

        # delete education
        education.delete()

        return DeleteEducationMutation(success=True)


#################### Profile #######################

class ProfileNode(DjangoObjectType):

    class Meta:
        model = Profile
        interfaces = (relay.Node, )


class UpdateProfileMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        public_email = String()
        national_code = String()
        birth_date = String()
        web_site = List(String)
        phone = List(String)
        mobile = List(String)
        fax = String()
        telegram_account = String()
        description = String()

    profile = Field(ProfileNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        public_email = input.get('public_email', '')
        national_code = input.get('national_code', '')
        birth_date = input.get('birth_date', '')
        web_site = input.get('web_site', [])
        phone = input.get('phone', [])
        mobile = input.get('mobile', [])
        fax = input.get('fax', '')
        telegram_account = input.get('telegram_account', '')
        description = input.get('description', '')

        if hasattr(context.user, 'profile'):
            profile = context.user.profile
        else:
            profile = Profile()
            profile.user = context.user

        # update profile
        profile.public_email = public_email
        profile.national_code = national_code
        profile.birth_date = birth_date
        profile.web_site = web_site
        profile.phone = phone
        profile.mobile = mobile
        profile.fax = fax
        profile.telegram_account = telegram_account
        profile.description = description
        try:
            profile.full_clean()
            profile.save()
        except Exception as e:
            raise Exception(str(e))

        return UpdateProfileMutation(profile=profile)


#################### User #######################

class UserFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = {
            'id': ['exact'],
            'username': ['exact', 'icontains', 'istartswith'],
            'first_name': ['exact', 'icontains', 'istartswith'],
            'last_name': ['exact', 'icontains', 'istartswith'],
            'date_joined': ['exact', 'gte', 'lte'],
            # ---------- Profile ------------
            'profile__public_email': ['exact', 'icontains',
                                      'istartswith'],
            'profile__national_code': ['exact', 'icontains',
                                       'istartswith'],
        }

    order_by = OrderingFilter(fields=('id', 'date_joined', 'username',))


class UserNode(DjangoObjectType):
    avatar = String()
    user_skills = DjangoFilterConnectionField(
        SkillNode, filterset_class=SkillFilter)
    user_work_experiences = DjangoFilterConnectionField(
        WorkExperienceNode, filterset_class=WorkExperienceFilter)
    user_certificates = DjangoFilterConnectionField(
        CertificateNode, filterset_class=CertificateFilter)
    user_researches = DjangoFilterConnectionField(
        ResearchNode, filterset_class=ResearchFilter)
    user_educations = DjangoFilterConnectionField(
        EducationNode, filterset_class=EducationFilter)

    @resolve_only_args
    def resolve_user_skills(self, **args):
        skills = Skill.objects.filter(user=self)
        return SkillFilter(args, queryset=skills).qs

    @resolve_only_args
    def resolve_user_work_experiences(self, **args):
        work_experiences = WorkExperience.objects.filter(user=self)
        return WorkExperienceFilter(args, queryset=work_experiences).qs

    @resolve_only_args
    def resolve_user_certificates(self, **args):
        certificates = Certificate.objects.filter(user=self)
        return CertificateFilter(args, queryset=certificates).qs

    @resolve_only_args
    def resolve_user_researches(self, **args):
        researches = Research.objects.filter(user=self)
        return ResearchFilter(args, queryset=researches).qs

    @resolve_only_args
    def resolve_user_educations(self, **args):
        educations = Education.objects.filter(user=self)
        return EducationFilter(args, queryset=educations).qs

    class Meta:
        model = User
        interfaces = (relay.Node, )
        only_fields = ['id', 'username', 'first_name', 'last_name',
                       'date_joined', 'profile', 'educations']

    def resolve_avatar(self, args, context, info):
        return get_gravatar_url(self.email)


class CreateUserMutation(relay.ClientIDMutation):

    class Input:
        username = String()
        email = String()
        password = String()

    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        username = input.get('username')
        email = input.get('email')
        password = input.get('password')

        # check username
        if User.objects.filter(username=username).exists():
            return CreateUserMutation(
                success=False,
                message="Username Already exists",
            )

        # check email
        if User.objects.filter(email=email).exists():
            return CreateUserMutation(
                success=False,
                message="Email Already exists",
            )

        # create user
        user = User.objects.create(
            username=username,
            email=email,
            is_active=False,
        )

        # set password
        user.set_password(password)
        user.save()

        # create user Profile
        Profile.objects.create(user=user)

        # send activation email
        from_email = 'info@daneshboom.com'
        to_email = user.email
        signer = TimestampSigner()
        token = signer.sign(user.pk)
        subject = "Activation Email"
        current_site = get_current_site(context)
        domain = current_site.domain
        context = {
            'email': user.email,
            'domain': domain,
            'user': user,
            'token': token,
            'protocol': 'http',
        }
        email_template = html_email_template = "activation_email.html"
        body = loader.render_to_string(email_template, context)

        email_message = EmailMultiAlternatives(
            subject, body, from_email, [to_email])
        html_email = loader.render_to_string(html_email_template, context)
        email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

        return CreateUserMutation(success=True, message=None)


class ChangePasswordMutation(relay.ClientIDMutation):

    class Input:
        old_password = String()
        new_password = String()

    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        old_password = input.get('old_password')
        new_password = input.get('new_password')

        if user.has_usable_password():
            if not user.check_password(old_password):
                return ChangePasswordMutation(
                    success=False,
                    message="Invalid Password",
                )
        # change password
        user.set_password(new_password)
        user.save()

        return ChangePasswordMutation(success=True, message=None)


class PasswordResetMutation(relay.ClientIDMutation):

    class Input:
        email = String()

    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        email = input.get('email')

        form = PasswordResetForm(input)
        form.email = email
        if form.is_valid():
            opts = {
                'use_https': context.is_secure(),
                'from_email': 'info@daneshboom.com',
                'email_template_name': 'password_reset_email.html',
                'request': context,
                #'subject_template_name': subject_template_name,
                #'html_email_template_name': html_email_template_name,
            }
            form.save(**opts)

        return PasswordResetMutation(success=True, message=None)


#################### User Query & Mutation #######################


class UserQuery(AbstractType):
    me = Field(UserNode)

    def resolve_me(self, args, context, info):
        if not context.user.is_authenticated():
            return None
        return context.user
    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode, filterset_class=UserFilter)


class UserMutation(AbstractType):
    # ---------------- Skill ----------------
    create_skill = CreateSkillMutation.Field()
    update_skill = UpdateSkillMutation.Field()
    delete_skill = DeleteSkillMutation.Field()

    # ---------------- Work Experience ----------------
    create_work_experience = CreateWorkExperienceMutation.Field()
    update_work_experience = UpdateWorkExperienceMutation.Field()
    delete_work_experience = DeleteWorkExperienceMutation.Field()

    # ---------------- Certificate ----------------
    create_certificate = CreateCertificateMutation.Field()
    update_certificate = UpdateCertificateMutation.Field()
    delete_certificate = DeleteCertificateMutation.Field()

    # ---------------- Research ----------------
    create_research = CreateResearchMutation.Field()
    update_research = UpdateResearchMutation.Field()
    delete_research = DeleteResearchMutation.Field()

    # ---------------- Education ----------------
    create_education = CreateEducationMutation.Field()
    update_education = UpdateEducationMutation.Field()
    delete_education = DeleteEducationMutation.Field()

    # ---------------- Profile ----------------
    update_profile = UpdateProfileMutation.Field()

    # ---------------- User ----------------
    create_user = CreateUserMutation.Field()
    change_password = ChangePasswordMutation.Field()
    password_reset = PasswordResetMutation.Field()
