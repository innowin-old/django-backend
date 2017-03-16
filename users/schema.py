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
    List, String, Boolean, Int, Float, ID
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

from danesh_boom.viewer_fields import ViewerFields
from users.models import Profile, Education, Research, Certificate,\
    WorkExperience, Skill
from users.forms import SkillForm, WorkExperienceForm, CertificateForm,\
    ResearchForm, EducationForm, ProfileForm, RegisterUserForm
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


class CreateSkillMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        title = String(required=True)
        tag = List(String)
        description = String()

    skill = Field(SkillNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        # create skill
        form = SkillForm(input)
        if form.is_valid():
            new_skill = form.save(commit=False)
            new_skill.user = user
            new_skill.save()
        else:
            raise Exception(str(form.errors))

        return CreateSkillMutation(skill=new_skill)


class UpdateSkillMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        title = String(required=True)
        tag = List(String)
        description = String()

    skill = Field(SkillNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        skill_id = from_global_id(id)[1]
        skill = Skill.objects.get(pk=skill_id)
        if skill.user != user:
            raise Exception("Invalid Access to Skill")

        # update skill
        form = SkillForm(input, instance=skill)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateSkillMutation(skill=skill)


class DeleteSkillMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        skill_id = from_global_id(id)[1]
        skill = Skill.objects.get(pk=skill_id)
        if skill.user != user:
            raise Exception("Invalid Access to Skill")

        # delete skill
        skill.delete()

        return DeleteSkillMutation(deleted_id=id)


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

        # create work experience
        form = WorkExperienceForm(input)
        if form.is_valid():
            new_work_experience = form.save(commit=False)
            new_work_experience.user = user
            new_work_experience.save()
        else:
            raise Exception(str(form.errors))

        return CreateWorkExperienceMutation(
            work_experience=new_work_experience
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

        # update work experience
        form = WorkExperienceForm(input, instance=work_experience)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateWorkExperienceMutation(work_experience=work_experience)


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


class CreateCertificateMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        title = String(required=True)

    certificate = Field(CertificateNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        # create certificate
        form = CertificateForm(input, context.FILES)
        if form.is_valid():
            new_certificate = form.save(commit=False)
            new_certificate.user = user
            new_certificate.save()
        else:
            raise Exception(str(form.errors))

        return CreateCertificateMutation(certificate=new_certificate)


class UpdateCertificateMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        title = String(required=True)

    certificate = Field(CertificateNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        certificate_id = from_global_id(id)[1]
        certificate = Certificate.objects.get(pk=certificate_id)
        if certificate.user != user:
            raise Exception("Invalid Access to Certificate")

        # update certificate
        form = CertificateForm(input, context.FILES, instance=certificate)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateCertificateMutation(certificate=certificate)


class DeleteCertificateMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        certificate_id = from_global_id(id)[1]
        certificate = Certificate.objects.get(pk=certificate_id)
        if certificate.user != user:
            raise Exception("Invalid Access to Work Certificate")

        # delete certificate
        certificate.delete()

        return DeleteCertificateMutation(deleted_id=id)


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


class CreateResearchMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        title = String(required=True)
        url = String()
        author = List(String)
        publication = String()
        year = Int()
        page_count = Int()

    research = Field(ResearchNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        # create research
        form = ResearchForm(input)
        if form.is_valid():
            new_research = form.save(commit=False)
            new_research.user = user
            new_research.save()
        else:
            raise Exception(str(form.errors))

        return CreateResearchMutation(research=new_research)


class UpdateResearchMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        title = String(required=True)
        url = String()
        author = List(String)
        publication = String()
        year = Int()
        page_count = Int()

    research = Field(ResearchNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        research_id = from_global_id(id)[1]
        research = Research.objects.get(pk=research_id)
        if research.user != user:
            raise Exception("Invalid Access to Work Research")

        # update research
        form = ResearchForm(input, instance=research)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateResearchMutation(research=research)


class DeleteResearchMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        research_id = from_global_id(id)[1]
        research = Research.objects.get(pk=research_id)
        if research.user != user:
            raise Exception("Invalid Access to Work Research")

        # delete research
        research.delete()

        return DeleteResearchMutation(deleted_id=id)


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


class CreateEducationMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        grade = String(required=True)
        university = String(required=True)
        field_of_study = String(required=True)
        from_date = String()
        to_date = String()
        average = Float()
        description = String()

    education = Field(EducationNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        # create research
        form = EducationForm(input)
        if form.is_valid():
            new_education = form.save(commit=False)
            new_education.user = user
            new_education.save()
        else:
            raise Exception(str(form.errors))

        return CreateEducationMutation(education=new_education)


class UpdateEducationMutation(ViewerFields, relay.ClientIDMutation):

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

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        education_id = from_global_id(id)[1]
        education = Education.objects.get(pk=education_id)
        if education.user != user:
            raise Exception("Invalid Access to Education")

        # update education
        form = EducationForm(input, instance=education)
        if form.is_valid():
            education.save()
        else:
            raise Exception(str(form.errors))

        return UpdateEducationMutation(education=education)


class DeleteEducationMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        education_id = from_global_id(id)[1]
        education = Education.objects.get(pk=education_id)
        if education.user != user:
            raise Exception("Invalid Access to Education")

        # delete education
        education.delete()

        return DeleteEducationMutation(deleted_id=id)


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

        if hasattr(context.user, 'profile'):
            profile = context.user.profile
        else:
            profile = Profile()
            profile.user = context.user

        # update profile
        form = ProfileForm(input, instance=profile)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

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


class RegisterUserMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        username = String()
        email = String()
        password = String()

    user = Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # create user
        form = RegisterUserForm(input, initial={'is_active': False})
        if form.is_valid():
            user = form.save()
        else:
            raise Exception(str(form.errors))

        # set password
        password = form.cleaned_data['password']
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

        return RegisterUserMutation(user=user)


class ChangePasswordMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        old_password = String()
        new_password = String()

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        old_password = input.get('old_password')
        new_password = input.get('new_password')

        if user.has_usable_password():
            if not user.check_password(old_password):
                raise Exception("Invalid Password")

        # change password
        user.set_password(new_password)
        user.save()

        return ChangePasswordMutation(success=True)


class PasswordResetMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        email = String()

    success = Boolean()

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

        return PasswordResetMutation(success=True)


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
    register_user = RegisterUserMutation.Field()
    change_password = ChangePasswordMutation.Field()
    password_reset = PasswordResetMutation.Field()
