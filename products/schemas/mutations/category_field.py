from graphene import relay, Field, String, Int, ID

from danesh_boom.viewer_fields import ViewerFields
from products.schemas.queries.category_field import CategoryFieldNode
from products.models import Category, CategoryField
from products.forms import CategoryFieldForm
from utils.relay_helpers import get_node
from products.utils import check_superuser
from utils.Exceptions import ResponseError, FormError


class CreateCategoryFieldMutation(ViewerFields, relay.ClientIDMutation):
    """
    create product category field mutation
    possible error codes:
    - invalid_category
    - form_error
    """

    class Input:
        category_id = String(required=True)
        name = String(required=True)
        title = String(required=True)
        type = String(required=True)
        order = Int(required=True)
        option = String()

    category_field = Field(CategoryFieldNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # check user
        check_superuser(context)

        category_id = input.get('category_id')
        category = get_node(category_id, context, info, Category)
        if not category:
            raise ResponseError(
                "Invalid Category",
                code='invalid_category')

        # create category field
        form = CategoryFieldForm(input)
        if form.is_valid():
            new_category_field = form.save(commit=False)
            new_category_field.category = category
            new_category_field.save()
        else:
            raise FormError(form.errors)

        return CreateCategoryFieldMutation(category_field=new_category_field)


class UpdateCategoryFieldMutation(ViewerFields, relay.ClientIDMutation):
    """
    update product category field mutation
    possible error codes:
    - invalid_category_field
    - invalid_category
    - form_error
    """

    class Input:
        id = String(required=True)
        category_id = String(required=True)
        name = String(required=True)
        title = String(required=True)
        type = String(required=True)
        order = Int(required=True)
        option = String()

    category_field = Field(CategoryFieldNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # check user
        check_superuser(context)

        category_field_id = input.get('id')
        category_field = get_node(
            category_field_id, context, info, CategoryField)
        if not category_field:
            raise ResponseError(
                "Invalid Category Field",
                code='invalid_category_field')

        category_id = input.get('category_id')
        category = get_node(category_id, context, info, Category)
        if not category:
            raise ResponseError(
                "Invalid Category",
                code='invalid_category')

        # update category field
        form = CategoryFieldForm(input, instance=category_field)
        if form.is_valid():
            form.save()
            category_field.category = category
            category_field.save()
        else:
            raise FormError(form.errors)

        return UpdateCategoryFieldMutation(category_field=category_field)


class DeleteCategoryFieldMutation(ViewerFields, relay.ClientIDMutation):
    """
    delete product category field mutation
    possible error codes:
    - invalid_category_field
    """

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # check user
        check_superuser(context)

        category_field_id = input.get('id', None)
        category_field = get_node(
            category_field_id, context, info, CategoryField)
        if not category_field:
            raise ResponseError(
                "Invalid Category Field",
                code='invalid_category_field')

        # delete category field
        category_field.delete()

        return DeleteCategoryFieldMutation(deleted_id=category_field_id)
