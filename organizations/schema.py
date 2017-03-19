import django_filters
from django.contrib.auth.models import User
from django_filters import OrderingFilter
from django.contrib.postgres.fields import ArrayField
from graphene import relay, Field, AbstractType, resolve_only_args,\
    List, String, Int, ID
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

from danesh_boom.viewer_fields import ViewerFields
from organizations.models import Organization, StaffCount, Picture,\
    UserAgent
from users.schema import UserNode, WorkExperienceNode, WorkExperienceFilter
from users.models import WorkExperience
from organizations.forms import UserAgentForm, PictureForm, StaffCountForm,\
    OrganizationForm


#################### UserAgent #######################


class UserAgentFilter(django_filters.FilterSet):

    class Meta:
        model = UserAgent
        fields = {
            'id': ['exact'],
            # ---------- Organization ------------
            'organization_id': ['exact'],
            'organization__name': ['exact', 'icontains', 'istartswith'],
            # ---------- User ------------
            'user_id': ['exact'],
            'user__username': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(fields=('id',))


class UserAgentNode(DjangoObjectType):

    user = Field(UserNode)

    class Meta:
        model = UserAgent
        interfaces = (relay.Node, )


class CreateUserAgentMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        organization_id = String(required=True)
        user_id = String(required=True)
        agent_subject = String()

    user_agent = Field(UserAgentNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('organization_id')
        organization_id = from_global_id(organization_id)[1]
        organization = Organization.objects.get(pk=organization_id)

        user_agent_id = input.get('user_id')
        user_agent_id = from_global_id(user_agent_id)[1]
        user_agent = User.objects.get(pk=user_agent_id)

        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        # TODO check business logic
        if organization.user == user_agent:
            raise Exception("Organization Owner cant not be Agent")

        # create user agent
        form = UserAgentForm(input)
        if form.is_valid():
            new_user_agent = form.save(commit=False)
            new_user_agent.organization = organization
            new_user_agent.user = user_agent
            new_user_agent.save()
        else:
            raise Exception(str(form.errors))

        return CreateUserAgentMutation(user_agent=new_user_agent)


class UpdateUserAgentMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        agent_subject = String()

    user_agent = Field(UserAgentNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        user_agent_id = from_global_id(id)[1]
        user_agent = UserAgent.objects.get(pk=user_agent_id)

        if user_agent.organization.user != user:
            raise Exception("Invalid Access to Organization")

        # update agent
        form = UserAgentForm(input, instance=user_agent)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateUserAgentMutation(user_agent=user_agent)


class DeleteUserAgentMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        user_agent_id = from_global_id(id)[1]
        user_agent = UserAgent.objects.get(pk=user_agent_id)

        if user_agent.organization.user != user:
            raise Exception("Invalid Access to Organization")

        # delete user agent
        user_agent.delete()

        return DeleteUserAgentMutation(deleted_id=id)


#################### Picture #######################

class PictureFilter(django_filters.FilterSet):

    class Meta:
        model = Picture
        fields = {
            'id': ['exact'],
        }

    order_by = OrderingFilter(fields=('id', 'order'))


class PictureNode(DjangoObjectType):

    class Meta:
        model = Picture
        interfaces = (relay.Node, )


class CreatePictureMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        organization_id = String(required=True)
        order = Int(required=True)
        description = String()

    picture = Field(PictureNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('organization_id')
        organization_id = from_global_id(organization_id)[1]
        organization = Organization.objects.get(pk=organization_id)

        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        # create picture
        form = PictureForm(input, context.FILES)
        if form.is_valid():
            new_picture = form.save(commit=False)
            new_picture.organization = organization
            new_picture.save()
        else:
            raise Exception(str(form.errors))

        return CreatePictureMutation(picture=new_picture)


class UpdatePictureMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        order = Int(requeired=True)
        description = String()

    picture = Field(PictureNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        picture_id = from_global_id(id)[1]
        picture = Picture.objects.get(pk=picture_id)

        if picture.organization.user != user:
            raise Exception("Invalid Access to Organization")

        # update picture
        form = PictureForm(input, context.FILES, instance=picture)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdatePictureMutation(picture=picture)


class DeletePictureMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        picture_id = from_global_id(id)[1]
        picture = Picture.objects.get(pk=picture_id)

        if picture.organization.user != user:
            raise Exception("Invalid Access to Organization")

        # delete picture
        picture.delete()

        return DeletePictureMutation(deleted_id=id)


#################### StaffCount #######################

class StaffCountFilter(django_filters.FilterSet):

    class Meta:
        model = StaffCount
        fields = {
            'id': ['exact'],
            'count': ['exact', 'gte', 'lte'],
            'create_time': ['exact', 'gte', 'lte'],
        }

    order_by = OrderingFilter(fields=('id', 'count', 'create_time'))


class StaffCountNode(DjangoObjectType):

    class Meta:
        model = StaffCount
        interfaces = (relay.Node, )


class CreateStaffCountMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        organization_id = String(required=True)
        count = Int(requeired=True)

    staff_count = Field(StaffCountNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('organization_id')
        organization_id = from_global_id(organization_id)[1]
        organization = Organization.objects.get(pk=organization_id)

        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        # create staff count
        form = StaffCountForm(input)
        if form.is_valid():
            new_staff_count = form.save(commit=False)
            new_staff_count.organization = organization
            new_staff_count.save()
        else:
            raise Exception(str(form.errors))

        return CreateStaffCountMutation(staff_count=new_staff_count)


class UpdateStaffCountMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        count = Int(requeired=True)

    staff_count = Field(StaffCountNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        staff_count_id = from_global_id(id)[1]
        staff_count = StaffCount.objects.get(pk=staff_count_id)

        if staff_count.organization.user != user:
            raise Exception("Invalid Access to Organization")

        count = input.get('count')

        # update staff count
        form = StaffCountForm(input, instance=staff_count)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateStaffCountMutation(staff_count=staff_count)


class DeleteStaffCountMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        staff_count_id = from_global_id(id)[1]
        staff_count = StaffCount.objects.get(pk=staff_count_id)

        if staff_count.organization.user != user:
            raise Exception("Invalid Access to Organization")

        # delete staff count
        staff_count.delete()

        return DeleteStaffCountMutation(deleted_id=id)


#################### Organization #######################

class OrganizationFilter(django_filters.FilterSet):

    class Meta:
        model = Organization
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
            'national_code': ['exact', 'icontains', 'istartswith'],
            'registrar_organization': ['exact', 'icontains', 'istartswith'],
            'country': ['exact', 'icontains', 'istartswith'],
            'province': ['exact', 'icontains', 'istartswith'],
            'city': ['exact', 'icontains', 'istartswith'],
            'ownership_type': ['exact', 'icontains', 'istartswith'],
            'business_type': ['icontains'],
            # ---------- User ------------
            'user_id': ['exact'],
            'user__username': ['exact', 'icontains', 'istartswith'],
        }
        filter_overrides = {
            ArrayField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }

    order_by = OrderingFilter(fields=('id', 'established_year',))


class OrganizationNode(DjangoObjectType):

    organization_staff_counts = DjangoFilterConnectionField(
        StaffCountNode, filterset_class=StaffCountFilter)
    organization_pictures = DjangoFilterConnectionField(
        PictureNode, filterset_class=PictureFilter)
    organization_user_agents = DjangoFilterConnectionField(
        UserAgentNode, filterset_class=UserAgentFilter)
    organization_work_experiences = DjangoFilterConnectionField(
        WorkExperienceNode, filterset_class=WorkExperienceFilter)

    @resolve_only_args
    def resolve_organization_staff_counts(self, **args):
        staff_counts = StaffCount.objects.filter(organization=self)
        return StaffCountFilter(args, queryset=staff_counts).qs

    @resolve_only_args
    def resolve_organization_pictures(self, **args):
        pictures = Picture.objects.filter(organization=self)
        return PictureFilter(args, queryset=pictures).qs

    @resolve_only_args
    def resolve_organization_user_agents(self, **args):
        user_agents = UserAgent.objects.filter(organization=self)
        return UserAgentFilter(args, queryset=user_agents).qs

    @resolve_only_args
    def resolve_organization_work_experiences(self, **args):
        work_experiences = WorkExperience.objects.filter(
            organization=self)
        return WorkExperienceFilter(args, queryset=work_experiences).qs

    class Meta:
        model = Organization
        interfaces = (relay.Node, )
        only_fields = [
            'id',
            'name',
            'national_code',
            'phone',
            'registration_ads_url',
            'registrar_organization',
            'country',
            'province',
            'city',
            'address',
            'web_site',
            'established_year',
            'ownership_type',
            'business_type',
            'logo',
            'description',
            'advantages',
            'correspondence_language']


class CreateOrganizationMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        name = String(required=True)
        national_code = String(required=True)
        registration_ads_url = String()
        registrar_organization = String()
        country = String(required=True)
        province = String(required=True)
        city = String()
        address = String()
        phone = List(String)
        web_site = String()
        established_year = Int()
        ownership_type = String()
        business_type = List(String, required=True)
        description = String()
        advantages = String()
        correspondence_language = List(String)
        telegram_channel = String()

    organization = Field(OrganizationNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        # create organization
        form = OrganizationForm(input)
        if form.is_valid():
            new_organization = form.save(commit=False)
            new_organization.user = user
            new_organization.save()
        else:
            raise Exception(str(form.errors))

        return CreateOrganizationMutation(organization=new_organization)


class UpdateOrganizationMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        name = String(required=True)
        national_code = String(required=True)
        registration_ads_url = String()
        registrar_organization = String()
        country = String(required=True)
        province = String(required=True)
        city = String()
        address = String()
        phone = List(String)
        web_site = String()
        established_year = Int()
        ownership_type = String()
        business_type = List(String, required=True)
        description = String()
        advantages = String()
        correspondence_language = List(String)
        telegram_channel = String()

    organization = Field(OrganizationNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        organization_id = from_global_id(id)[1]
        organization = Organization.objects.get(pk=organization_id)
        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        # update organization
        form = OrganizationForm(input, instance=organization)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateOrganizationMutation(organization=organization)


class DeleteOrganizationMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        organization_id = from_global_id(id)[1]
        organization = Organization.objects.get(pk=organization_id)
        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        # delete organization
        organization.delete()

        return DeleteOrganizationMutation(deleted_id=id)


#################### Organization Query & Mutation #######################

class OrganizationQuery(AbstractType):

    organization = relay.Node.Field(OrganizationNode)
    organizations = DjangoFilterConnectionField(
        OrganizationNode, filterset_class=OrganizationFilter)


class OrganizationMutation(AbstractType):
    # ---------------- Organization ----------------
    create_organization = CreateOrganizationMutation.Field()
    update_organization = UpdateOrganizationMutation.Field()
    delete_organization = DeleteOrganizationMutation.Field()

    # ---------------- StaffCount ----------------
    create_organization_staff_count = CreateStaffCountMutation.Field()
    update_organization_staff_count = UpdateStaffCountMutation.Field()
    delete_organization_staff_count = DeleteStaffCountMutation.Field()

    # ---------------- Picture ----------------
    create_organization_picture = CreatePictureMutation.Field()
    update_organization_picture = UpdatePictureMutation.Field()
    delete_organization_picture = DeletePictureMutation.Field()

    # ---------------- UserAgent ----------------
    create_organization_user_agent = CreateUserAgentMutation.Field()
    update_organization_user_agent = UpdateUserAgentMutation.Field()
    delete_organization_user_agent = DeleteUserAgentMutation.Field()
