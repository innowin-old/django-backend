from graphene import relay, Field, String, ID, Boolean

from danesh_boom.viewer_fields import ViewerFields
from products.schemas.queries.category import CategoryNode
from products.models import Category
from products.forms import CategoryForm
from utils.relay_helpers import get_node
from products.utils import check_superuser
from utils.Exceptions import ResponseError, FormError


class CreateCategoryMutation(ViewerFields, relay.ClientIDMutation):
    """
    create product category mutation
    possible error codes:
    - form_error
    """

    class Input:
        parent_id = String()
        name = String(required=True)
        title = String(required=True)
        creatable = Boolean()

    category = Field(CategoryNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # check user
        check_superuser(context)

        parent_id = input.get('parent_id')
        parent = get_node(parent_id, context, info, Category)

        # create category
        form = CategoryForm(input)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.parent = parent
            new_category.save()
        else:
            raise FormError(form.errors)

        return CreateCategoryMutation(category=new_category)


class UpdateCategoryMutation(ViewerFields, relay.ClientIDMutation):
    """
    update product category mutation
    possible error codes:
    - invalid_category
    - form_error
    """

    class Input:
        id = String(required=True)
        parent_id = String()
        name = String(required=True)
        title = String(required=True)
        creatable = Boolean()

    category = Field(CategoryNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # check user
        check_superuser(context)

        category_id = input.get('id', None)
        category = get_node(category_id, context, info, Category)
        if not category:
            raise ResponseError(
                "Invalid Category",
                code='invalid_category')

        parent_id = input.get('parent_id')
        parent = get_node(parent_id, context, info, Category)

        # update category
        form = CategoryForm(input, instance=category)
        if form.is_valid():
            form.save()
            category.parent = parent
            category.save()
        else:
            raise FormError(form.errors)

        return UpdateCategoryMutation(category=category)


class DeleteCategoryMutation(ViewerFields, relay.ClientIDMutation):
    """
    delete product category mutation
    possible error codes:
    - invalid_category
    """

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # check user
        check_superuser(context)

        category_id = input.get('id', None)
        category = get_node(category_id, context, info, Category)
        if not category:
            raise ResponseError(
                "Invalid Category",
                code='invalid_category')

        # delete category
        category.delete()

        return DeleteCategoryMutation(deleted_id=category_id)
