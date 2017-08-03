from graphene import relay, Field, String, ID, List, InputObjectType
from danesh_boom.viewer_fields import ViewerFields
from users.models import Identity
from products.schemas.queries.product import ProductNode
from products.models import Category, Product
from products.forms import ProductForm
from utils.relay_helpers import get_node
from utils.Exceptions import ResponseError, FormError
from products.utils import add_attrs, add_custom_attrs


class KeyValueInput(InputObjectType):
    name = String()
    value = String()


class CreateProductMutation(ViewerFields, relay.ClientIDMutation):
    """
    create product mutation: only required fields of product be filled
    possible error codes:
    - invalid_owner
    - invalid_category
    -invalid_category_field
    - form_error
    """

    class Input:
        owner_id = String(required=True)
        category_id = String(required=True)
        name = String(required=True)
        country = String(required=True)
        province = String(required=True)

    product = Field(ProductNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        owner_id = input.get('owner_id')
        owner = get_node(owner_id, context, info, Identity)
        if not owner or not owner.validate_user(user):
            raise ResponseError(
                "Invalid Owner",
                code='invalid_owner')

        category_id = input.get('category_id')
        category = get_node(category_id, context, info, Category)
        if not category or not category.creatable:
            raise ResponseError(
                "Invalid Category",
                code='invalid_category')

        # create product
        form = ProductForm(input)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.owner = owner
            new_product.category = category
            new_product.save()
        else:
            raise FormError(form.errors)
        return CreateProductMutation(product=new_product)


class UpdateProductMutation(ViewerFields, relay.ClientIDMutation):
    """
    update product mutation :whole product fields be updated
    possible error codes:
    - invalid_product
    - invalid_owner
    - invalid_category
    - form_error
    """

    class Input:
        id = String(required=True)
        category_id = String(required=True)
        name = String(required=True)
        country = String(required=True)
        province = String(required=True)
        city = String()
        description = String()
        attrs = List(KeyValueInput)
        custom_attrs = List(KeyValueInput)

    product = Field(ProductNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        product_id = input.get('id')
        product = get_node(product_id, context, info, Product)
        if not product:
            raise ResponseError(
                "Invalid Product",
                code='invalid_product')

        if not product.owner.validate_user(user):
            raise ResponseError(
                "Invalid Owner",
                code='invalid_owner')

        category_id = input.get('category_id')
        category = get_node(category_id, context, info, Category)
        if not category or not category.creatable:
            raise ResponseError(
                "Invalid Category",
                code='invalid_category')

        # update product
        form = ProductForm(input, instance=product)
        form.data['attrs'] = add_attrs(input.get('attrs'), category)
        form.data['custom_attrs'] = add_custom_attrs(input.get('custom_attrs'))
        if form.is_valid():
            product = form.save(commit=False)
            product.category = category
            product.save()
        else:
            raise FormError(form.errors)

        return UpdateProductMutation(product=product)


class DeleteProductMutation(ViewerFields, relay.ClientIDMutation):
    """
    delete product mutation
    possible error codes:
    - invalid_product
    - invalid_owner
    """

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        product_id = input.get('id', None)
        product = get_node(product_id, context, info, Product)
        if not product:
            raise ResponseError(
                "Invalid Product",
                code='invalid_product')

        if not product.owner.validate_user(user):
            raise ResponseError(
                "Invalid Owner",
                code='invalid_owner')

        # delete product
        product.delete()

        return DeleteProductMutation(deleted_id=product_id)
