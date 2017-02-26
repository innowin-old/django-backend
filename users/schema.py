from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from graphene import relay, Field, AbstractType,\
    String, Boolean, Int, Float, List
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

from utils.gravatar import get_gravatar_url
from utils.schema_helpers import convert_to_date
from users.models import Profile, Education, Research, Certificate,\
    WorkExperience, Skill


#################### Skill #######################

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

class WorkExperienceNode(DjangoObjectType):

    class Meta:
        model = WorkExperience
        interfaces = (relay.Node, )


class CreateWorkExperienceMutation(relay.ClientIDMutation):

    class Input:
        name = String(required=True)
        position = String(required=True)
        from_date = String()
        to_date = String()

    work_experience = Field(WorkExperienceNode)
    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        name = input.get('name')
        position = input.get('position')
        from_date = convert_to_date(input.get('from_date', ''))
        to_date = convert_to_date(input.get('to_date', ''))

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
            return CreateWorkExperienceMutation(
                work_experience=None,
                success=False,
                message=str(e),
            )

        return CreateWorkExperienceMutation(
            work_experience=new_work_experience,
            success=True
        )


class UpdateWorkExperienceMutation(relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        name = String(required=True)
        position = String(required=True)
        from_date = String()
        to_date = String()

    work_experience = Field(WorkExperienceNode)
    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        work_experience_id = from_global_id(id)[1]
        work_experience = WorkExperience.objects.get(pk=work_experience_id)
        if work_experience.user != user:
            return UpdateWorkExperienceMutation(
                work_experience=None,
                success=False,
                message="Invalid Access to Work Experience",
            )

        name = input.get('name')
        position = input.get('position')
        from_date = convert_to_date(input.get('from_date', ''))
        to_date = convert_to_date(input.get('to_date', ''))

        # update work experience
        work_experience.name = name
        work_experience.position = position
        work_experience.from_date = from_date
        work_experience.to_date = to_date
        try:
            work_experience.full_clean()
            work_experience.save()
        except Exception as e:
            return UpdateWorkExperienceMutation(
                work_experience=None,
                success=False,
                message=str(e),
            )

        return UpdateWorkExperienceMutation(
            work_experience=work_experience,
            success=True
        )


class DeleteWorkExperienceMutation(relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        work_experience_id = from_global_id(id)[1]
        work_experience = WorkExperience.objects.get(pk=work_experience_id)
        if work_experience.user != user:
            return DeleteWorkExperienceMutation(
                success=False,
                message="Invalid Access to Work Experience",
            )

        # delete work experience
        work_experience.delete()

        return DeleteWorkExperienceMutation(success=True)


#################### Certificate #######################

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
        from_date = convert_to_date(input.get('from_date', ''))
        to_date = convert_to_date(input.get('to_date', ''))
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
        from_date = convert_to_date(input.get('from_date', ''))
        to_date = convert_to_date(input.get('to_date', ''))
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


class UpdateProfileMutation(relay.ClientIDMutation):

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
    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        public_email = input.get('public_email', '')
        national_code = input.get('university', '')
        birth_date = convert_to_date(input.get('birth_date', ''))
        web_site = input.get('web_site', [])
        phone = input.get('phone', [])
        mobile = input.get('mobile', [])
        fax = input.get('fax', '')
        telegram_account = input.get('telegram_account', '')
        description = input.get('description', '')

        profile = context.user.profile

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
            return UpdateProfileMutation(
                profile=None,
                success=False,
                message=str(e),
            )

        return UpdateProfileMutation(profile=profile, success=True)


#################### User #######################

class UserNode(DjangoObjectType):
    avatar = String()

    class Meta:
        model = User
        interfaces = (relay.Node, )
        filter_fields = {
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
        only_fields = ['id', 'username', 'first_name', 'last_name',
                       'date_joined', 'profile', 'educations',
                       'researches', 'certificates', 'skills',
                       'work_experiences']

    def resolve_avatar(self, args, context, info):
        return get_gravatar_url(self.email)


class ChangePasswordMutation(relay.ClientIDMutation):

    class Input:
        old_password = String()
        new_password = String()
        confirm_password = String()

    success = Boolean()
    message = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        old_password = input.get('old_password')
        new_password = input.get('new_password')
        confirm_password = input.get('confirm_password')

        if not user.check_password(old_password):
            return ChangePasswordMutation(
                success=False,
                message="Invalid Password",
            )
        if new_password != confirm_password:
            return ChangePasswordMutation(
                success=False,
                message="Password Mismatch",
            )

        # change password
        user.set_password(new_password)
        user.save()

        return ChangePasswordMutation(success=True, message=None)


#################### User Query & Mutation #######################

class UserQuery(AbstractType):
    me = Field(UserNode)

    def resolve_me(self, args, context, info):
        if not context.user.is_authenticated():
            return None
        return context.user
    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)


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
    change_password = ChangePasswordMutation.Field()
